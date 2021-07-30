
from rest_framework.viewsets import ViewSet

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser

class AccountRetirementView(ViewSet):
    """
    Provides API endpoint for retiring a user.
    """
    authentication_classes = (JwtAuthentication,)
    permission_classes = (permissions.IsAuthenticated, CanRetireUser,)
    parser_classes = (JSONParser,)

    @request_requires_username
    def post(self, request):
        pass