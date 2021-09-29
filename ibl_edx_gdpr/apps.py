import logging

from django.apps import AppConfig

from edx_django_utils.plugins.constants import (
    PluginURLs, PluginSettings, PluginContexts
)
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType


class EdxGDPRConfig(AppConfig):
    name = 'ibl_edx_gdpr'
    verbose_name = "IBL edX GDPR"

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: 'ibl_edx_gdpr',
                PluginURLs.REGEX: r'^api/ibl/retirements/',
                PluginURLs.RELATIVE_PATH: 'urls'
            },
        },
        
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common'
                },
            }
        }
    }

    def ready(self):
        # Attach signals to emit retired user events in tracking.log
        from .signals import enable_retirement_signal
        enable_retirement_signal()

        from openedx.core.djangoapps.user_api.models import RetirementState

        if not RetirementState.objects.all().count():
            message = 'ImproperlyConfigured: Retirement states not populated, run manage.py lms ibl_retirement_states to populate'
            logging.error(message)
