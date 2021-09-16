from functools import wraps
import logging
from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from ibl_edx_gdpr.utils.permissions import CanRetireUser
from ibl_edx_gdpr.client import RetirementClient


try:
    # Ironwood
    from openedx.core.lib.api.authentication import OAuth2AuthenticationAllowInactiveUser as OAuth2Authentication
except:
    # KOA
    from openedx.core.lib.api.authentication import BearerAuthentication as OAuth2Authentication

logger = logging.getLogger(__name__)


def request_requires_valid_username(function):
    """
    Requires that a ``username`` key containing a truthy value exists in
    the ``request.data`` attribute of the decorated function.
    """

    @wraps(function)
    def wrapper(request):  # pylint: disable=missing-docstring
        username = request.data.get('username', None)

        if not username:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': 'The user was not specified.'}
            )
        if not User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': 'The username does not match a known valid username'}
            )

        return function(request)

    return wrapper


@api_view(['GET'])
@authentication_classes((OAuth2Authentication,))
@permission_classes([permissions.IsAuthenticated, CanRetireUser, ])
def get_learners_in_retirement_pipeline(request):
    """
    :parameter cool_off_days: int In the past X days, defines how many days has the learner been deactivated
    :param request:
    :return:
    """
    try:
        client = RetirementClient()
        usernames = client.get_learners_to_retire_usernames()
    except Exception as e:
        logger.error("Error processing task {}".format(e.args))
        return Response({'error': 'Failed to fetch retirements'}, status=400)
    return Response({'message': usernames})


@api_view(['POST'])
@authentication_classes((OAuth2Authentication,))
@permission_classes([permissions.IsAuthenticated, CanRetireUser, ])
@request_requires_valid_username
def place_learner_in_retirement_pipeline(request):
    """
    Rather than have the learner click deactivate, this would as well act like deactivate my account
    :param request:
    :return:
    """
    try:
        username = str(request.data.get('username'))
        client = RetirementClient()
        client.place_in_retirement_pipeline(username)

    except Exception as e:
        if 'has a retirement' in e.args[0]:
            return Response({'message': '{} already in retirement'.format(username)})

        logger.error("Error processing task ({}): {}".format(username, e.args))
        return Response({'error': 'Failed to place in retirements'}, status=400)

    return Response({'message': '{} added to retirements successfully'.format(username)})


@api_view(['POST'])
@authentication_classes((OAuth2Authentication,))
@permission_classes([permissions.IsAuthenticated, CanRetireUser, ])
@request_requires_valid_username
def retire_learner(request):
    """
    Performs extra retirement steps as defined in IBL_RETIREMENT_PIPELINE
    :param request:
    :return:
    """
    username = str(request.data.get('username'))
    try:
        client = RetirementClient()
        client.retire_learner(username)
    except Exception as e:
        logger.error("Error processing task ({}): {}".format(username, e.args))
        return Response({'error': 'Failed to retire learner'}, status=400)

    return Response({'message': '{} retired successfully'.format(username)})
