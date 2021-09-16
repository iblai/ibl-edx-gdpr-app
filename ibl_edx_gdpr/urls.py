"""
Defines URL routes for the API.
"""
from django.conf import settings
from django.conf.urls import url

from ibl_edx_gdpr.views import retirement


urlpatterns = [
    url(
        r'^place_in_retirements/',
        retirement.place_learner_in_retirement_pipeline,
        name="ibl_edx_gdpr_place_in_retirements"
    ),
    url(
        r'^retire_user/',
        retirement.retire_learner,
        name="ibl_edx_gdpr_retire_learner"
    ),
    url(
        r'',
        retirement.get_learners_in_retirement_pipeline,
        name="ibl_edx_gdpr_get_retirements"
    ),
]

# Activate task to clean their userdata from tracking logs
# This way it runs just once.
from .patch import remove_original_values
remove_original_values()