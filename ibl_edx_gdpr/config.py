import copy
from django.conf import settings
IBL_RETIREMENT_STATES = [
    'PENDING',

    # 'LOCKING_ACCOUNT',
    # 'LOCKING_COMPLETE',
    #
    # 'RETIRING_EMAIL_LISTS',
    # 'EMAIL_LISTS_COMPLETE',

    'RETIRING_ENROLLMENTS',
    'ENROLLMENTS_COMPLETE',
]

if getattr(settings, 'ENABLE_STUDENT_NOTES', None):
    IBL_RETIREMENT_STATES += (
        'RETIRING_NOTES',
        'NOTES_COMPLETE',
    )

if getattr(settings, 'ENABLE_DISCUSSION_SERVICE', None):
    IBL_RETIREMENT_STATES += (
        'RETIRING_FORUMS',
        'FORUMS_COMPLETE',
    )
# This should always come last else errors would happen
IBL_RETIREMENT_STATES+=['RETIRING_LMS','LMS_COMPLETE',]

START_STATE = 'PENDING'
END_STATES = ['ERRORED', 'ABORTED', 'COMPLETE']


# We attach final states here at the end
IBL_RETIREMENT_STATES += END_STATES

REQUIRED_STATES = copy.deepcopy(END_STATES)
REQ_STR = ','.join(REQUIRED_STATES)
COOL_OFF_DAYS = 0 # Users that requested for deletion instantly can be completely retired, increase to give gap
ERROR_STATE = 'ERRORED'
COMPLETE_STATE = 'COMPLETE'
ABORTED_STATE = 'ABORTED'

IBL_RETIREMENT_PIPELINE = [
    # [start_state, end_state, method to call]
    ['RETIRING_ENROLLMENTS', 'ENROLLMENTS_COMPLETE', 'retirement_unenroll'],
]

if getattr(settings.FEATURES, 'ENABLE_STUDENT_NOTES', None):
    IBL_RETIREMENT_PIPELINE += ['RETIRING_NOTES', 'NOTES_COMPLETE', 'retirement_retire_notes']

if getattr(settings.FEATURES, 'ENABLE_DISCUSSION_SERVICE', None):
    IBL_RETIREMENT_PIPELINE += ['RETIRING_FORUMS', 'FORUMS_COMPLETE', 'retirement_retire_forum']

# LMS should always be last
IBL_RETIREMENT_PIPELINE+= ['RETIRING_LMS', 'LMS_COMPLETE', 'retirement_lms_retire'],
IBL_RETIREMENT_APPNAME = 'IBL Retirement App'
IBL_RETIREMENT_SERVICE_WORKER = 'ibl.retirement.user'
IBL_RETIREMENT_EMAIL = '{}@ibleducation.com'.format(IBL_RETIREMENT_SERVICE_WORKER)

# Event handlers
EDX_USER_PROFILE_CHANGED = 'edx.user.settings.changed'
EMIT_EVENTS = bool(getattr(settings, 'IBL_GDPR_EMIT_EVENTS', True))