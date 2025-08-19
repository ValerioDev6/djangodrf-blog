from django.conf import settings
from rest_framework import permissions


class HasValidApiKey(permissions.BasePermission):
    """
    Custom permission to check if a valid API key is provided in the request headers.
    """

    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-KEY")

        return api_key in getattr(settings, "VALID_API_KEYS", [])
