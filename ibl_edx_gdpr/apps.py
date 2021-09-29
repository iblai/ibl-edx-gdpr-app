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
        from .management.commands.ibl_retirement_states import Command
        command = Command()
        command.handle()

        # Attach signals to emit retired user events in tracking.log
        from .signals import enable_retirement_signal
        enable_retirement_signal()
