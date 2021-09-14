from ibl_edx_gdpr.config import EDX_USER_PROFILE_CHANGED, EMIT_EVENTS
from eventtracking import tracker
from django.db.models.signals import post_save

try:
    from common.djangoapps.student.models import UserProfile
except:
    from student.models import UserProfile


def retirement_handler(sender, instance, **kwargs):
    """Emits 'edx.user.settings.changed' event when a user is placed in retirement """
    context = {
        'extra': 'ibl.edx.gdpr.retire_learner',
        'is_retired': 'retired__user' in instance.email,
        'user_id': instance.user.id,
        'username': instance.user.username,
        'email': instance.user.email,
    }
    tracker.emit(EDX_USER_PROFILE_CHANGED, context)


def enable_retirement_signal():
    if EMIT_EVENTS:
        post_save.connect(
            retirement_handler,
            sender=UserProfile,
            dispatch_uid='retirement_handler')
