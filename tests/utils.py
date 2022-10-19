import pytest
from common.djangoapps.student.tests.factories import UserFactory
from django.core.management import call_command
from django.shortcuts import reverse as django_reverse
from rest_framework.test import APIClient


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


@pytest.mark.django_db
def setup():
    call_command("ibl_retirement_states")
