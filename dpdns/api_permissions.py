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