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

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Implementation of the populate command
    """
    help = 'Produces a list of users who have requested retirement'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry_run',
            action='store_true',
            help='Run checks without making any changes'
        )

    def handle(self, *args, **options):
        """
        Execute the command.
        """
        from ibl_edx_gdpr.client import RetirementClient
        client = RetirementClient()
        learners = client.get_learners_to_retire_usernames()
        print('Retirements Available: ')
        print(learners)
