from django.apps import AppConfig
from django.conf import settings

IBL_APP_LEGACY_STARTUP = getattr(settings, 'IBL_APP_LEGACY_STARTUP', False)


class EdxGDPRConfig(AppConfig):
    name = 'ibl_edx_gdpr'
    verbose_name = "IBL edX GDPR"

    def ready(self):
        from .management.commands.ibl_retirement_states import Command
        command = Command()
        command.handle()
