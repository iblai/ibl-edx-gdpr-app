from django.apps import AppConfig
from django.conf import settings


class EdxGDPRConfig(AppConfig):
    name = 'ibl_edx_gdpr'
    verbose_name = "IBL edX GDPR"

    def ready(self):
        from .management.commands.ibl_retirement_states import Command
        command = Command()
        command.handle()

        # Attach signals to emit retired user events in tracking.log
        from .signals import enable_retirement_signal
        enable_retirement_signal()

