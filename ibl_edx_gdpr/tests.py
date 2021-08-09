import datetime

from django.test import TestCase
from django.utils import timezone

from ibl_edx_gdpr.client import RetirementClient


def generate_user():
    from django.contrib.auth.models import User
    user =  User.create_user(first_name='IBL Test', last_name='Last Name', email='test.ibl@mail.com', username='test.ibl.user')
    user.set_password('password123')
    return user

#WIP
class IBLRetirementTest(TestCase):

    def setUp(self):
        self.valid_user = generate_user()
        self.invalid_user = 'random.invalid.user'
        self.client = RetirementClient()

    def test_client_invalid_user_cannot_be_retired(self):
        self.client.retire_learner(self.invalid_user)


    def test_client_valid_user_can_be_retired(self):
        pass

    def test_client_invalid_user_cannot_be_placed_in_pipeline(self):
        pass

    def test_client_valid_user_can_be_placed_in_pipeline(self):
        pass


