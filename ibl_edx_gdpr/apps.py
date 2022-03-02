import logging

from django.apps import AppConfig
from django.conf import settings


class EdxGDPRConfig(AppConfig):
    name = 'ibl_edx_gdpr'
    verbose_name = "IBL edX GDPR"

    def ready(self):
        # Attach signals to emit retired user events in tracking.log
        from .signals import enable_retirement_signal
        enable_retirement_signal()

        from openedx.core.djangoapps.user_api.models import RetirementState

        if not RetirementState.objects.all().count():
            message = 'ImproperlyConfigured: Retirement states not populated, run manage.py lms ibl_retirement_states to populate'
            logging.error(message)
            print(message)

