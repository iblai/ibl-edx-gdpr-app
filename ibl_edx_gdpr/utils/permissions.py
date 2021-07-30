from rest_framework import permissions


class CanRetireUser(permissions.BasePermission):
    """
    Grants access to the various retirement API endpoints if the requesting user is
    a superuser, the RETIREMENT_SERVICE_USERNAME, or has the explicit permission to
    retire a User account.
    """
    def has_permission(self, request, view):
        return request.user.has_perm('accounts.can_retire_user')

