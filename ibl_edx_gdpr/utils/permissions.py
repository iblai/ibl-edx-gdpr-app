from rest_framework import permissions
from django.conf import settings

class CanRetireUser(permissions.BasePermission):
    """
    Grants access to the various retirement API endpoints if the requesting user is
    a superuser, the RETIREMENT_SERVICE_USERNAME, or has the explicit permission to
    retire a User account.
    """
    def has_permission(self, request, view):
        return request.user.username == getattr(settings, 'RETIREMENT_SERVICE_WORKER_USERNAME', False)

