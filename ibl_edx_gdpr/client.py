import os
from ibl_edx_gdpr.config import IBL_RETIREMENT_STATES, COOL_OFF_DAYS
from ibl_edx_gdpr.utils.edx_api import LmsApi
from ibl_edx_gdpr.utils.oauth import get_oauth_app


class RetirementClient:

    def get_learners_to_retire(self, lms_base_url=None, cool_off_days=COOL_OFF_DAYS):
        """
        Retrieves a JWT token as the retirement service user, then calls the LMS
        endpoint to retrieve the list of learners awaiting retirement.
        :param cool_off_days: Filters users to continue retirement pipeline that have requested for deletion from X days
        :param self:
        """
        if not lms_base_url:
            lms_base_url = getattr(os.environ, 'HOST', 'lms.lenovo.com')


        # set lms url properly
        lms_base_url = "http://{}".format(lms_base_url.strip('http://').strip('http://').strip('/'))
        application = get_oauth_app()
        end_states = [state for state in IBL_RETIREMENT_STATES if 'COMPLETE' not in state]
        states_to_request = ['PENDING'] + end_states

        api = LmsApi(lms_base_url, lms_base_url, application.client_id, application.client_secret)

        # Retrieve the learners to retire and export them to separate Jenkins property files.
        learners_to_retire = api.learners_to_retire(states_to_request, cool_off_days)

        return learners_to_retire
