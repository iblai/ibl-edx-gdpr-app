import logging
try:
    from urlparse import urlparse
except ImportError:
    # Python 3
    from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory


log = logging.getLogger(__name__)


def get_edx_domain():
    lms_url = getattr(settings, 'LMS_ROOT_URL', '')
    lms_domain = ''
    if lms_url:
        lms_domain = urlparse(lms_url).netloc
    return lms_domain


def get_mock_edx_request(user=None):
    factory = RequestFactory()
    request = factory.get('')
    if user is not None:
        request.user = user
        request.META['SERVER_NAME'] = get_edx_domain()
    return request


def get_user_from_request(request):
    username = request.query_params.get('username')
    if username:
        # most be admin/staff to request completion status of other users
        if request.user.is_superuser or request.user.is_staff:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                return None
    return request.user
