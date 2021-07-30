import os
from functools import partial
from time import time
from slumber.exceptions import HttpNotFoundError
from six import text_type

from ibl_edx_gdpr.config import IBL_RETIREMENT_STATES, COOL_OFF_DAYS, END_STATES, ERROR_STATE, COMPLETE_STATE, \
    IBL_RETIREMENT_PIPELINE, START_STATE
from ibl_edx_gdpr.utils.edx_api import LmsApi
from ibl_edx_gdpr.utils.oauth import get_oauth_app

from ibl_edx_gdpr.utils.helpers import (
    _fail,
    _fail_exception,
    _get_error_str_from_exception,
    _log,
)

# Return codes for various fail cases
ERR_SETUP_FAILED = -1
ERR_USER_AT_END_STATE = -2
ERR_USER_IN_WORKING_STATE = -3
ERR_WHILE_RETIRING = -4
ERR_BAD_LEARNER = -5
ERR_UNKNOWN_STATE = -6
ERR_BAD_CONFIG = -7

SCRIPT_SHORTNAME = 'Learner Retirement'
LOG = partial(_log, SCRIPT_SHORTNAME)
FAIL = partial(_fail, SCRIPT_SHORTNAME)
FAIL_EXCEPTION = partial(_fail_exception, SCRIPT_SHORTNAME)

AUTH_HEADER = {}
WORKING_STATES = list(set(IBL_RETIREMENT_STATES) - set(END_STATES + [START_STATE]))


class RetirementClient:
    lms_base_url = getattr(os.environ, 'HOST', 'lms.lenovo.com')
    lms_api = None

    def __init__(self):
        self.lms_base_url = "http://{}".format(self.lms_base_url.strip('http://').strip('http://').strip('/'))

    def setup_api(self):
        """
        Refreshes API
        :return:
        """
        application = get_oauth_app()
        self.lms_base_url = "http://{}".format(self.lms_base_url.strip('https://').strip('http://').strip('/'))
        self.lms_api = LmsApi(self.lms_base_url, self.lms_base_url, application.client_id, application.client_secret)

    def get_learners_to_retire(self, cool_off_days=COOL_OFF_DAYS):
        """
        Retrieves a JWT token as the retirement service user, then calls the LMS
        endpoint to retrieve the list of learners awaiting retirement.
        :param cool_off_days: Filters users to continue retirement pipeline that have requested for deletion from X days
        :param
        """
        # set lms url properly
        if not self.lms_api:
            self.setup_api()

        end_states = [state for state in IBL_RETIREMENT_STATES if 'COMPLETE' in state]
        states_to_request = ['PENDING'] + end_states

        # Retrieve the learners to retire and export them to separate Jenkins property files.
        learners_to_retire = self.lms_api.learners_to_retire(states_to_request, cool_off_days)

        return learners_to_retire

    def get_learners_to_retire_usernames(self, lms_base_url=None, cool_off_days=COOL_OFF_DAYS):
        learner_list = []
        learners = self.get_learners_to_retire(cool_off_days=COOL_OFF_DAYS)
        if learners:
            learner_list = [user['user']['username'] for user in learners if 'retired' not in user['user']['username'] ]
        return learner_list

    def _get_learner_state_index_or_exit(self, learner):
        """
        Returns the index in the ALL_STATES retirement state list, validating that it is in
        an appropriate state to work on.
        """
        try:
            learner_state = learner['current_state']['state_name']
            original_username = learner['original_username']
            learner_state_index = IBL_RETIREMENT_STATES.index(learner_state)

            if learner_state in END_STATES:
                FAIL(ERR_USER_AT_END_STATE, 'User {} already in end state: {}'.format(original_username ,learner_state))

            if learner_state in WORKING_STATES:
                FAIL(ERR_USER_IN_WORKING_STATE, 'User is already in a working state! {}'.format(learner_state))

            return learner_state_index
        except KeyError:
            FAIL(ERR_BAD_LEARNER, 'Bad learner response missing current_state or state_name: {}'.format(learner))
        except ValueError:
            FAIL(ERR_UNKNOWN_STATE, 'Unknown learner retirement state for learner: {}'.format(learner))

    def _get_learner_and_state_index_or_exit(self, username):
        """
        Double-checks the current learner state, contacting LMS, and maps that state to its
        index in the pipeline. Exits out if the learner is in an invalid state or not found
        in LMS.
        """
        try:
            learner = self.lms_api.get_learner_retirement_state(username)
            learner_state_index = self._get_learner_state_index_or_exit(learner)
            return learner, learner_state_index
        except HttpNotFoundError:
            FAIL(ERR_BAD_LEARNER, 'Learner {} not found. Please check that the learner is present in '
                                  'UserRetirementStatus, is not already retired, '
                                  'and is in an appropriate state to be acted upon.'.format(username))
        except Exception as exc:  # pylint: disable=broad-except
            FAIL_EXCEPTION(ERR_SETUP_FAILED, 'Unexpected error fetching user state!', text_type(exc))

    def retire_learner(self, username):
        """
        Retrieves a JWT token as the retirement service learner, then performs the retirement process as
        defined in WORKING_STATE_ORDER
        """
        learner, learner_state_index = self._get_learner_and_state_index_or_exit(username)
        user_prefix = "({})".format(username)
        start_state = None
        try:
            for start_state, end_state, method in IBL_RETIREMENT_PIPELINE:
                # Skip anything that has already been done
                if IBL_RETIREMENT_STATES.index(start_state) < learner_state_index:
                    LOG('{} State {} completed in previous run, skipping'.format(user_prefix,start_state))
                    continue

                LOG('{} Starting state {}'.format(user_prefix, start_state))

                self.lms_api.update_learner_retirement_state(username, start_state, 'Starting: {}'.format(start_state))

                # This does the actual API call
                start_time = time()
                response = getattr(self.lms_api, method)(learner)
                end_time = time()

                LOG('{} State {} completed in {} seconds'.format(user_prefix,start_state, end_time - start_time))

                self.lms_api.update_learner_retirement_state(
                    username,
                    end_state,
                    'Ending: {} with response:\n{}'.format(end_state, response)
                )
                learner_state_index += 1
                LOG('{} Progressing to state {}'.format(user_prefix, end_state))

            self.lms_api.update_learner_retirement_state(username, COMPLETE_STATE, 'Learner retirement complete.')
            LOG('{} Retirement complete for learner {}'.format(user_prefix,username))
        except Exception as exc:  # pylint: disable=broad-except
            exc_msg = _get_error_str_from_exception(exc)

            try:
                LOG('{} Error in retirement state {}: {}'.format(user_prefix,start_state, exc_msg))
                self.lms_api.update_learner_retirement_state(username, ERROR_STATE, exc_msg)
            except Exception as update_exc:  # pylint: disable=broad-except
                LOG('{} Critical error attempting to change learner state to ERRORED: {}'.format(user_prefix,update_exc))

            FAIL_EXCEPTION(ERR_WHILE_RETIRING, '{} Error encountered in state "{}"'.format(user_prefix,start_state), exc)
