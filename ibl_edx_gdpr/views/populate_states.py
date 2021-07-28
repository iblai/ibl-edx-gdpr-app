from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from openedx.core.lib.api.view_utils import view_auth_classes
from ibl_edx_gdpr.utils.request import get_user_from_request


@api_view(['POST', ])
@view_auth_classes(is_authenticated=True)
def populate_retirement_states(request):
    return Response()
