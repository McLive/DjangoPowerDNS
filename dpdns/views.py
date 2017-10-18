# -*- coding: utf-8 -*-
# --
# DjangoPowerDNS - A PowerDNS web interface
# Copyright (C) 2017 McLive
# --
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU AFFERO General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# --

from __future__ import unicode_literals

import json
import socket
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logut
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from DjangoPowerDNS import settings
from dpdns.api import TokenAuthentication
from dpdns.forms import LoginForm, DomainAddForm, DomainUserAddForm, DomainClaimForm
from dpdns.serializers import RecordSerializer
from models import Domains, DomainAccess, Records


# Create your views here.

# Todo: decorator to check if domain exists
# Todo: decorator to check if user has access to domain

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def login(req):
    if req.user.is_authenticated():
        return redirect('/')

    if req.method == 'POST':
        f = LoginForm(req.POST)
        if f.is_valid():
            username = req.POST['username']
            password = req.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(req, user)
                    if 'next' in req.POST:
                        if len(req.POST['next']) > 2 and req.POST['next'][0] == '/':
                            return redirect(req.POST['next'])
                    # else:
                    return redirect('/')
            else:
                time.sleep(1)
                f._errors['password'] = ["Logindaten falsch."]
    else:
        f = LoginForm()

    # Bestimme "$next"
    next = ''
    if 'next' in req.GET:
        next = req.GET['next']
    elif 'next' in req.POST:
        next = req.POST['next']

    return render(req, 'login.html', {
        'form': f,
        'next': next,
    })


def logout(req):
    if req.user.is_authenticated():
        auth_logut(req)
        return redirect('/')

    return redirect('/login/')


@login_required
def domains(req):
    # get all domains the current user has access to = DomainAccess entry
    domains = Domains.objects.filter(domain_accesses__user=req.user)

    # get all domains without any user owning them
    free_domains = Domains.objects.filter(domain_accesses__isnull=True)

    return render(req, 'domains.html', {
        'domains': domains,
        'free_domains': free_domains
    })


@login_required
def domain_claim(req):
    if not req.user.is_superuser:
        return redirect('domains')

    # get all domains without any user owning them
    free_domains = Domains.objects.filter(domain_accesses__isnull=True)
    if not free_domains:
        return redirect('domains')

    if req.method == 'POST':
        form = DomainClaimForm(req.POST)

        if form.is_valid():
            for item in form.cleaned_data['domain']:
                DomainAccess(domain=item, user=req.user, permission=10).save()
                messages.add_message(req, messages.SUCCESS, u"Successfully claimed Domain %s." % item.name)
            return redirect('domains')
    else:
        form = DomainClaimForm()
    return render(req, 'domain-claim.html', {
        'form': form,
    })


@login_required
def domain_add(req):
    if req.method == 'POST':
        form = DomainAddForm(req.POST)

        if form.is_valid():
            f = form.save()
            DomainAccess(domain=f, user=req.user, permission=10).save()
            messages.add_message(req, messages.SUCCESS, u"Successfully added Domain %s." % f.name)
            return redirect('domains')
    else:
        form = DomainAddForm()
    return render(req, 'domain-add.html', {
        'form': form,
    })


@login_required
def domain_delete(req, id):
    try:
        domain = Domains.objects.get(pk=id)

        domain_access = domain.check_user_access(req.user)

        if not domain_access:
            messages.add_message(req, messages.ERROR, u"You don't have access to that domain")
            return redirect('domains')

        if domain_access.permission != 10:
            messages.add_message(req, messages.ERROR, u"You don't have permission to delete this domain.")
            return redirect('domains')

        domain.delete()
        messages.add_message(req, messages.SUCCESS, u"Successfully deleted Domain %s." % domain.name)

        return redirect('domains')

    except Domains.DoesNotExist:
        messages.add_message(req, messages.ERROR, u"That domain doesn't exist.")
        return redirect('domains')


@login_required()
def domain(req, id):
    try:
        domain = Domains.objects.get(pk=id)

        domain_access = domain.check_user_access(req.user)

        if not domain_access:
            messages.add_message(req, messages.ERROR, u"You don't have access to that domain")
            return redirect('domains')

        return render(req, 'domain.html', {
            'domain': domain,
            'domain_access': domain_access
        })

    except Domains.DoesNotExist:
        messages.add_message(req, messages.ERROR, u"Error viewing domain.")
        return redirect('domains')


@login_required()
def domain_users(req, id):
    try:
        domain = Domains.objects.get(pk=id)

        domain_access = domain.check_user_access(req.user)

        if not domain_access:
            messages.add_message(req, messages.ERROR, u"You don't have access to that domain")
            return redirect('domains')

        if domain_access.permission != 10:
            messages.add_message(req, messages.ERROR, u"You don't have permission to edit users.")
            return redirect('domain', domain.id)

        users = domain.get_users()

        return render(req, 'domain-users.html', {
            'domain': domain,
            'domain_access': domain_access,
            'users': users
        })

    except Domains.DoesNotExist:
        messages.add_message(req, messages.ERROR, u"That domain doesn't exist.")
        return redirect('domains')


@login_required
def domain_user_add(req, id):
    try:
        domain = Domains.objects.get(pk=id)

        domain_access = domain.check_user_access(req.user)

        if not domain_access:
            messages.add_message(req, messages.ERROR, u"You don't have access to that domain")
            return redirect('domains')

        if domain_access.permission != 10:
            messages.add_message(req, messages.ERROR, u"You don't have permission to add users.")
            return redirect('domain', domain.id)

        if req.method == 'POST':
            form = DomainUserAddForm(req.POST)

            if form.is_valid():
                user = req.POST['user']
                if DomainAccess.objects.filter(domain=domain, user=user).exists():
                    form._errors['user'] = [u"Domain access already exists with this user"]
                else:
                    f = form.save(commit=False)
                    f.domain = domain
                    f.save()
                    messages.add_message(req, messages.SUCCESS, u"Successfully added User %s." % f.user)
                    return redirect('domain-users', domain.id)
        else:
            form = DomainUserAddForm()
        return render(req, 'domain-user-add.html', {
            'domain': domain,
            'form': form,
        })

    except Domains.DoesNotExist:
        messages.add_message(req, messages.ERROR, u"That domain doesn't exist.")
        return redirect('domains')


@login_required()
def domain_api(req, id):
    try:
        domain = Domains.objects.get(pk=id)

        domain_access = domain.check_user_access(req.user)

        if not domain_access:
            messages.add_message(req, messages.ERROR, u"You don't have access to that domain")
            return redirect('domains')

        return render(req, 'domain-api.html', {
            'domain': domain,
        })

    except Domains.DoesNotExist:
        messages.add_message(req, messages.ERROR, u"That domain doesn't exist.")
        return redirect('domains')


@login_required()
def domain_json_get_records(req, id):
    try:
        domain = Domains.objects.get(pk=id)

        if not domain.check_user_access(req.user):
            return JsonResponse({'error': "You don't have access to that domain."})

        record_response = []
        records = domain.get_records()

        exclude = settings.PDNS_EXCLUDE_RECORDS

        if exclude:
            for ex in exclude:
                if domain.id == ex['domain']:
                    if "regex" in ex:
                        records = records.exclude(name__regex=ex['regex'])

        for record in records:
            record_response.append({
                "id": record.id,
                "name": record.name,
                "strippedName": record.name[:-(len(domain.name) + 1)],  # cut off ".<domain>.tld"
                "type": record.type,
                "content": record.content,
                "prio": record.prio,
                "ttl": record.ttl,
            })

        return JsonResponse({
            "domain": domain.name,
            "records": record_response,
            "update-url": reverse(domain_json_update_record, args=[domain.id]),
            "delete-url": reverse(domain_json_delete_record, args=[domain.id]),
        })

    except Domains.DoesNotExist:
        return JsonResponse({'error': "Error viewing domain."})


def isBlank(myString):
    return not (myString and myString.strip())


@login_required()
def domain_json_update_record(req, id):
    if req.method != 'POST':
        return JsonResponse(data={'error': "Invalid request method."}, status=500)

    try:
        domain = Domains.objects.get(pk=id)

        if not domain.check_user_access(req.user):
            return JsonResponse(data={'error': "You don't have access to that domain."}, status=500)

        json_record = json.loads(req.body)

        if isBlank(json_record['content']):
            return JsonResponse(data={'error': "Content is required"}, status=500)

        name = domain.name
        if not isBlank(json_record['name']):
            # return JsonResponse(data={'error': "Name is required"}, status=500)
            name = json_record['name'] + "." + domain.name

        print "name: " + name

        if json_record['type'] not in settings.PDNS_ENABLED_RR_TYPES:
            return JsonResponse(data={'error': "Invalid Type"}, status=500)

        # Validate A record
        if json_record['type'] == "A" and not is_valid_ipv4_address(json_record['content']):
            return JsonResponse(data={'error': "{0} is not a valid IPv4 address.".format(json_record['content'])}, status=500)

        # Validate AAAA record
        if json_record['type'] == "AAAA" and not is_valid_ipv6_address(json_record['content']):
            return JsonResponse(data={'error': "{0} is not a valid IPv6 address.".format(json_record['content'])}, status=500)


        try:
            # try to update existing record
            record = Records.objects.get(pk=json_record['id'])
            record.name = name
            record.type = json_record['type']
            record.content = json_record['content']
            record.prio = json_record['prio']
            record.ttl = json_record['ttl']
            record.save()
            domain.update_soa_serial()
            return JsonResponse({'success': "Updated record.", 'id': record.id})
        except Records.DoesNotExist:
            # create new record
            new_record = Records(domain=domain, name=name, type=json_record['type'], content=json_record['content'], prio=json_record['prio'], ttl=json_record['ttl'])
            new_record.save()
            domain.update_soa_serial()
            return JsonResponse({'success': "Created new record.", 'id': new_record.id})
        except ValueError:
            return JsonResponse(data={'error': "Internal Servererror."}, status=500)

    except Domains.DoesNotExist:
        return JsonResponse(data={'error': "Error viewing domain."}, status=500)


@login_required()
def domain_json_delete_record(req, id):
    if req.method != 'POST':
        return JsonResponse(data={'error': "Invalid request method."}, status=500)

    try:
        domain = Domains.objects.get(pk=id)

        if not domain.check_user_access(req.user):
            return JsonResponse(data={'error': "You don't have access to that domain."}, status=500)

        json_record = json.loads(req.body)

        try:
            record = Records.objects.get(pk=json_record['id'])
            record.delete()
            domain.update_soa_serial()
            return JsonResponse({'success': "Deleted record.", 'id': record.id})

        except Records.DoesNotExist:
            return JsonResponse(data={'error': "Error deleting record."}, status=500)

    except Domains.DoesNotExist:
        return JsonResponse(data={'error': "Error viewing domain."}, status=500)


def index(req):
    return render(req, 'index.html', {
    })


def check_api_key(req):
    api_key = req.META.get('HTTP_API_KEY', '')
    if not api_key:
        api_key = req.GET.get('apiKey', '')

    if not api_key:
        return Response({'error': "No Api-Key provided."})


@api_view(['GET', 'POST'])
def api_get_records(req, pk):
    api_key = req.META.get('HTTP_API_KEY', '')
    if not api_key:
        api_key = req.GET.get('apiKey', '')

    if not api_key:
        return Response({'error': "No Api-Key provided."})

    try:
        domain = Domains.objects.get(pk=pk)

        if not domain.check_key_access(api_key):
            return Response({'error': "You don't have access to that domain."})

        # list all existing records
        if req.method == 'GET':
            records = domain.get_records()
            serializer = RecordSerializer(records, many=True)

            return Response(serializer.data)

        # create a new record
        elif req.method == 'POST':
            serializer = RecordSerializer(data=req.data)
            if serializer.is_valid():
                serializer.validated_data['domain'] = domain
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Domains.DoesNotExist:
        return Response(data={'error': "Error viewing domain."}, status=500)


@api_view(['GET', 'PUT', 'DELETE'])
def api_record(req, pk, id):
    api_key = req.META.get('HTTP_API_KEY', '')
    if not api_key:
        api_key = req.GET.get('apiKey', '')

    if not api_key:
        return Response({'error': "No Api-Key provided."})

    try:
        domain = Domains.objects.get(pk=pk)

        if not domain.check_key_access(api_key):
            return Response({'error': "You don't have access to that domain."})

        record = domain.get_record(id)
        if not record:
            return Response({'error': "That record doesn't exist."})

        if req.method == 'GET':
            serializer = RecordSerializer(record)
            return Response(serializer.data)

        elif req.method == 'PUT':
            serializer = RecordSerializer(record, data=req.data)
            if serializer.is_valid():
                serializer.save()
                domain.update_soa_serial()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif req.method == 'DELETE':
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Domains.DoesNotExist:
        return Response(data={'error': "Error viewing domain."}, status=500)