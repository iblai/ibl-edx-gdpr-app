from oauth2_provider.models import get_application_model
from django.contrib.auth.models import User

from ibl_edx_gdpr.config import IBL_RETIREMENT_APPNAME, IBL_RETIREMENT_SERVICE_WORKER, IBL_RETIREMENT_EMAIL

Application = get_application_model()


def create_oauth_app():
    user, user_created = User.objects.get_or_create(username=IBL_RETIREMENT_SERVICE_WORKER,
                                                    email=IBL_RETIREMENT_EMAIL)
    application_kwargs = dict(
        redirect_uris='',
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        skip_authorization=False
    )
    application, created = Application.objects.get_or_create(
        user=user, name=IBL_RETIREMENT_APPNAME, **application_kwargs
    )
    status = 'Created' if created else 'Found'
    print('{} {} application with id: {}, client_id: {}, and client_secret: {}'.format(
        status,
        IBL_RETIREMENT_APPNAME,
        application.id,
        application.client_id,
        application.client_secret,
    ))


def get_oauth_app():
    """
    This would return the Oauth app
    :return:
    """
    user, user_created = User.objects.get_or_create(username=IBL_RETIREMENT_SERVICE_WORKER,
                                                    email=IBL_RETIREMENT_EMAIL)
    application, created = Application.objects.get_or_create(
        user=user
    )
    return application



