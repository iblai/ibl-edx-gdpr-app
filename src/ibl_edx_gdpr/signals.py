from ibl_edx_gdpr.config import EDX_USER_PROFILE_CHANGED, EMIT_EVENTS
from eventtracking import tracker
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import logging

logging.getLogger(__name__)
try:
    from common.djangoapps.student.models import UserProfile
except:
    from student.models import UserProfile


def retirement_handler(sender, instance, **kwargs):
    """Emits 'edx.user.settings.changed' event when a user is placed in retirement """
    is_retirement = 'retired__user' in instance.email
    logging.info('Event triggered: is_gdpr:{}'.format(is_retirement))
    if is_retirement:
        context = {
            'extra': 'ibl.edx.gdpr.retire_learner',
            'is_gdpr': is_retirement,
            'user_id': instance.id,
            'username': instance.username,
            'email': instance.email,
        }
        tracker.emit(EDX_USER_PROFILE_CHANGED, context)


def enable_retirement_signal():

    if EMIT_EVENTS:
        logging.info('Retirement signals enabled')
        post_save.connect(
            retirement_handler,
            sender=User,
            dispatch_uid='retirement_handler')
