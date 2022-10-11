import json

from common.djangoapps.student.tests.factories import UserFactory
from django.core.management import call_command
from django.shortcuts import reverse as django_reverse
from rest_framework.test import APIClient

LMS_HOST = "lms.lenovo.com"


def get_authenticated_client_and_user(*args, **kwargs):
    client = APIClient()
    kwargs_user = kwargs.pop("user", None)
    if not kwargs_user:
        user = UserFactory(*args, **kwargs)
    else:
        user = kwargs_user
    client.force_authenticate(user=user)
    return client, user


def reverse(name, args=None, kwargs=None):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = []
    return django_reverse(f"ibl_edx_gdpr:{name}", args=args, kwargs=kwargs)


def setup():
    call_command("ibl_retirement_states")
    SetupStatus.value = True


class SetupStatus:
    value = False


def requests_mock_token(requests_mock):
    requests_mock.post(
        f"https://{LMS_HOST}/oauth2/access_token",
        text=json.dumps(
            {
                "access_token": "23ba8d53c1094c41a8ebb42752cd283b",
                "expires_in": 3600,
                "token_type": "bearer",
                "scope": "read write",
            }
        ),
    )


def get_place_in_retirement_resp(client, data, token):
    return client.post(
        reverse("ibl_edx_gdpr_place_in_retirements"),
        data,
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )
