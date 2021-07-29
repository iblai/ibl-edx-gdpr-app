"""
Defines URL routes for the API.
"""
from django.conf import settings
from django.conf.urls import url

from ibl_edx_gdpr.views.populate_states import populate_retirement_states


urlpatterns = [
    url(
        r'^status/certificate/{}?$'.format(settings.COURSE_ID_PATTERN),
        certificate_status,
        name="ibl_edx_gdpr_certificate_status"
    ),
    url(
        r'^status/course/{}?$'.format(settings.COURSE_ID_PATTERN),
        course_completion,
        name="ibl_edx_gdpr_course_status"
    ),
    url(
        r'^course_outline/{}?$'.format(settings.COURSE_ID_PATTERN),
        course_block_tree,
        name="ibl_edx_gdpr_course_outline"
    )
]
