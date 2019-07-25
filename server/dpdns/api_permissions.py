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

from rest_framework import permissions

from dpdns.models import APIKey


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        return APIKey.objects.filter(key=api_key).exists()

    def has_object_permission(self, request, view, obj):
        api_key = request.META.get('HTTP_API_KEY', '')
        key = APIKey.objects.get(key=api_key)
        domain = key.domain
        return domain == obj