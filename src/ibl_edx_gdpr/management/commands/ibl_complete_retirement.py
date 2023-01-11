"""
Take the list of states from settings.RETIREMENT_STATES and forces the
RetirementState table to mirror it.

We use a foreign keyed table for this instead of just using the settings
directly to generate a `choices` tuple for the model because the states
need to be configurable by open source partners and modifying the
`choices` for a model field causes new migrations to be generated,
with a variety of unpleasant follow-on effects for the partner when
upgrading the model at a later date.
"""

import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Implementation of the populate command
    """
    help = 'Produces a list of users who have requested retirement'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            required=True,
            type=str,
            help='Username to retire <Must be a username found after running ibl_get_retirements command>'
        )

    def handle(self, *args, **options):
        """
        Execute the command.
        """
        username = options.get('username', None)
        try:
            User.objects.get(username=username)
        except:
            msg = 'Could not find a user with the specified username'
            logger.error(msg)
            raise CommandError(msg)
        from ibl_edx_gdpr.client import RetirementClient
        client = RetirementClient()
        client.retire_learner(username)
        logger.info('User retired successfully.')
