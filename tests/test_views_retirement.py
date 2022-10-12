import json

import pytest
from common.djangoapps.student.tests.factories import UserFactory
from openedx.core.djangoapps.oauth_dispatch.tests.factories import (
    AccessTokenFactory,
    ApplicationFactory,
)

from .utils import get_authenticated_client_and_user, reverse, setup

LMS_HOST = "lms.lenovo.com"


@pytest.mark.django_db
class TestViewsRetirement:
    @property
    def staff(self):
        if hasattr(self, "_staff") is False:
            self._staff = UserFactory(is_staff=True)
        return self._staff

    @property
    def application(self):
        if hasattr(self, "_application") is False:
            self._application = ApplicationFactory.create(user=self.staff)
        return self._application

    @property
    def token(self):
        return AccessTokenFactory.create(
            user=self.staff, application=self.application
        ).token

    def test_place_learner_in_retirement_pipeline_returns_200(self, requests_mock):
        setup()
        requests_mock.post(
            f"https://{LMS_HOST}/oauth2/access_token",
            text=json.dumps(
                {
                    "access_token": "23ba8d53c1094c41a8ebb42752cd283b",
                    "expires_in": 3600,
                    "token_type": "bearer",
                    "scope": "read write",
                }
            ),
        )
        user = UserFactory()
        client, _ = get_authenticated_client_and_user(user=self.staff)
        data = {
            "username": user.username,
        }

        resp = client.post(
            reverse("ibl_edx_gdpr_place_in_retirements"),
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        assert resp.status_code == 200
        assert resp.data["message"] == "{} added to retirements successfully".format(
            user.username
        )

    def test_get_learners_in_retirement_pipeline_returns_200(self, requests_mock):
        setup()
        requests_mock.post(
            f"https://{LMS_HOST}/oauth2/access_token",
            text=json.dumps(
                {
                    "access_token": "23ba8d53c1094c41a8ebb42752cd283b",
                    "expires_in": 3600,
                    "token_type": "bearer",
                    "scope": "read write",
                }
            ),
        )
        client, _ = get_authenticated_client_and_user(user=self.staff)
        data = {
            "username": UserFactory().username,
        }
        client.post(
            reverse("ibl_edx_gdpr_place_in_retirements"),
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        resp = client.get(
            reverse("ibl_edx_gdpr_get_retirements"),
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )

        assert resp.status_code == 200
        assert resp.data["message"] == 1
