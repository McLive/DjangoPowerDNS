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

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime

import binascii

import os
import rest_framework
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

from DjangoPowerDNS import settings


class Comments(models.Model):
    domain_id = models.IntegerField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    modified_at = models.IntegerField()
    account = models.CharField(max_length=40)
    comment = models.CharField(max_length=64000)

    class Meta:
        managed = False
        db_table = 'comments'


class Cryptokeys(models.Model):
    domain_id = models.IntegerField()
    flags = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cryptokeys'


class Domainmetadata(models.Model):
    domain_id = models.IntegerField()
    kind = models.CharField(max_length=32, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domainmetadata'


class Domains(models.Model):
    name = models.CharField(unique=True, max_length=255)
    master = models.CharField(max_length=128, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6)
    notified_serial = models.IntegerField(blank=True, null=True)
    account = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domains'

    def get_records(self):
        return Records.objects.filter(domain=self)

    def get_record(self, id):
        try:
            return Records.objects.get(domain=self, pk=id)
        except Records.DoesNotExist:
            return False

    def generate_soa(self):
        content = "{0} {1} {2} 3600 900 604800 86400".format(
            settings.PDNS_DEFAULT_SOA['PRIMARY_NS'],
            settings.PDNS_DEFAULT_SOA['EMAIL'].replace("@", "."),
            int(self.get_current_timestamp() + str("00"))
        )
        Records(domain=self, name=self.name, type="SOA", content=content, prio=0, ttl=86400).save()

    def get_soa(self):
        return Records.objects.filter(domain=self).get(type__exact="SOA")

    def update_soa_serial(self):
        if not self.get_soa():
            return False

        soa = self.get_soa()
        parts = soa.content.split(" ")

        serial = parts[2]
        incr = int(serial[-2:])

        new_serial = self.get_current_timestamp() + str(incr + 1).zfill(2)

        new_soa = soa.content.replace(serial, new_serial)

        soa.content = new_soa
        soa.save()

    def get_current_timestamp(self):
        return datetime.datetime.today().strftime('%Y%m%d')

    def check_user_access(self, user):
        try:
            return DomainAccess.objects.get(domain=self, user=user)
        except DomainAccess.DoesNotExist:
            return False

    def check_key_access(self, key):
        try:
            api_key = APIKey.objects.get(key=key)
            return self == api_key.domain
        except APIKey.DoesNotExist:
            return False

    def get_users(self):
        return DomainAccess.objects.filter(domain=self).all()

    def get_api_keys(self):
        try:
            api_keys = self.api_keys.all()
            #api_keys = APIKey.objects.filter(domain=self).all()
            return api_keys
        except APIKey.DoesNotExist:
            return None

    def __str__(self):
        return self.name


class Options(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    value = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'options'


class Records(models.Model):
    RECORD_TYPE_CHOICES = []
    for enabled_rr_type in settings.PDNS_ENABLED_RR_TYPES:
        RECORD_TYPE_CHOICES.append((enabled_rr_type, enabled_rr_type))

    id = models.BigAutoField(primary_key=True)
    domain = models.ForeignKey(Domains, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True, choices=RECORD_TYPE_CHOICES)
    content = models.CharField(max_length=64000, blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True)
    prio = models.IntegerField(blank=True, null=True)
    change_date = models.IntegerField(blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True, default=0)
    ordername = models.CharField(max_length=255, blank=True, null=True)
    auth = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records'


class Remote(models.Model):
    record = models.IntegerField()
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    security = models.CharField(max_length=2000)
    nonce = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'remote'


class Supermasters(models.Model):
    ip = models.CharField(primary_key=True, max_length=64)
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'supermasters'
        unique_together = (('ip', 'nameserver'),)


class Tsigkeys(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tsigkeys'
        unique_together = (('name', 'algorithm'),)


class Users(models.Model):
    name = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=200)
    type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'


# djdns models

class DomainAccess(models.Model):
    PERMISSIONS = (
        (0, 'User'),
        (10, 'Owner')
    )
    domain = models.ForeignKey(Domains, related_name="domain_accesses")
    user = models.ForeignKey(User)
    permission = models.SmallIntegerField(choices=PERMISSIONS, default=0)

    def get_permission_description(self):
        for (id, description) in self.PERMISSIONS:
            if id == self.permission:
                return description

    """def clean(self):
        is_insert = self.pk is None

        print self.domain
        print self.user

        if DomainAccess.objects.filter(domain=self.domain, user=self.user).exists() and is_insert:
            raise ValidationError('Domain access already exists with this user')"""

    class Meta:
        unique_together = (('domain', 'user'),)


"""class DomainApiAccess(models.Model):
    domain = models.ForeignKey(Domains, related_name="domain_accesses", unique=True)
    token = models.CharField(max_length=256)"""

import rest_framework.authtoken.models


@python_2_unicode_compatible
# class Token(rest_framework.authtoken.models.Token):
class Token(models.Model):
    # key is no longer primary key, but still indexed and unique
    key = models.CharField(max_length=40, db_index=True, unique=True)
    # relation to user is a ForeignKey, so each user can have more than one token
    # user = models.ForeignKey(User, related_name='auth_tokens', on_delete=models.CASCADE, verbose_name=_("User"))
    domain = models.ForeignKey(Domains, related_name="api_tokens")

    # class Meta:
    #    unique_together = (('user', 'name'),)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class APIKey(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    domain = models.ForeignKey(Domains, related_name="api_keys")
    key = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = "API Keys"
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(APIKey, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.domain.name


@receiver(post_save, sender=Domains)
def domain_saved(sender, created, instance, **kwargs):
    # if domain is new object, we generate the default SOA
    if created:
        instance.generate_soa()
        APIKey(domain=instance).save()

    else:
        instance.update_soa_serial()


#@receiver(post_save, sender=Records)
#def record_saved(sender, created, instance, **kwargs):
    # creates infinitive loop
    # instance.domain.update_soa_serial()

