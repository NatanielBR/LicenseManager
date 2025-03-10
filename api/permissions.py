from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsRight(BasePermission):
    def has_permission(self, request: Request, view):
        if request.path == '/api/docs/swagger/':
            return True

        return request.headers.get('Authorization') == settings.API_TOKEN