from django.apps import AppConfig
from django.conf import settings


class EdxGDPRConfig(AppConfig):
    name = 'ibl_edx_gdpr'
    verbose_name = "IBL edX GDPR"

    def ready(self):
        from .management.commands.ibl_retirement_states import Command

        command = Command()
        command.handle()

        from .patch import remove_original_values
        remove_original_values()