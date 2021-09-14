# Patch to update all existing entries that have the old usernames and names saved
import logging
logging.getLogger(__name__)


def remove_original_values():
    from ibl_edx_gdpr.config import COMPLETE_STATE
    from openedx.core.djangoapps.user_api.models import RetirementState,UserRetirementStatus
    complete_state = RetirementState.objects.get(state_name=COMPLETE_STATE)
    # Get completed states and remove the names
    UserRetirementStatus.objects.filter(
        current_state=complete_state, original_username__isnull=False,
    ).update(
        original_username='', original_name='', original_email=''
    )
    logging.info('Patched IBL-GDPR: Removed original values')

