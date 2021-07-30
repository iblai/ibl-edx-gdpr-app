from django.apps import AppConfig
from django.conf import settings


class EdxGDPRConfig(AppConfig):
    name = 'ibl_edx_gdpr'
    verbose_name = "IBL edX GDPR"

    def ready(self):
        from .management.commands.ibl_retirement_states import Command
        # # Set Retirement User to IBLs
        # from django.conf import settings
        # from ibl_edx_gdpr.config import IBL_RETIREMENT_SERVICE_WORKER
        # setattr(settings, 'RETIREMENT_SERVICE_WORKER_USERNAME', IBL_RETIREMENT_SERVICE_WORKER)
        command = Command()
        command.handle()
