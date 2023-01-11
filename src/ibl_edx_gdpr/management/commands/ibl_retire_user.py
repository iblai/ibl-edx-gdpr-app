import logging
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Manually move a user into the retirement queue, so that they can be
    picked up by the user retirement pipeline. This should only be done in
    the case that a user has tried and is unable to delete their account
    via the UI.

    Most of this code has been lifted from openedx/core/djangoapps/user_api/accounts/views

    As this is a fairly sensitive operation, we want to make sure that human
    error is accounted for. In order to make sure that something like a typo
    during command invocation does not result in the retirement of a
    different user, you must supply both the username and email address linked
    to the user account.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            required=True,
            type=str,
            help='Username to be retired'
        )
        parser.add_argument(
            '--user_email',
            required=True,
            type=str,
            help='User email address.'
        )

    def handle(self, *args, **options):
        """
        Execute the command.
        """

        username = options['username']
        user_email = options['user_email']
        try:
            user = User.objects.get(username=username, email=user_email)
        except:
            error_message = (
                'Could not find a user with specified username and email '
                'address. Make sure you have everything correct before '
                'trying again'
            )
            logger.error(error_message)
            raise CommandError(error_message)

        user_model = get_user_model()

        try:
            from ibl_edx_gdpr.client import RetirementClient
            RetirementClient().place_in_retirement_pipeline(user)

        except KeyError:
            error_message = 'Username not specified {}'.format(user)
            logger.error(error_message)
            raise CommandError(error_message)
        except user_model.DoesNotExist:
            error_message = 'The user "{}" does not exist.'.format(user.username)
            logger.error(error_message)
            raise CommandError(error_message)
        except ImproperlyConfigured as e:
            raise e
        except Exception as exc:  # pylint: disable=broad-except
            error_message = '500 error deactivating account {}'.format(exc)
            logger.error(error_message)
            raise CommandError(error_message)
        msg = "User ({}) successfully moved to the retirement pipeline".format(username)
        print(msg)

