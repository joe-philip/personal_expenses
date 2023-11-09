from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from main.models import APIKeyManager


class HasAPIKey(BasePermission):
    message = 'Invalid API Key'

    def has_permission(self, request: Request, view) -> bool:
        if 'HTTP_X_API_KEY' in request.META:
            key = request.META['HTTP_X_API_KEY']
            if APIKeyManager().validate_key(key):
                return True
        return False
