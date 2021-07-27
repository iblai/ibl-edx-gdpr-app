from oauth2_provider.models import get_application_model
from django.contrib.auth.models import User

Application = get_application_model()
app_name = 'IBL Retirement App'
user_name = 'ibl.retirement.user'
email = '{}@ibleducation.com'.format(user_name)


def create_ouath_app():
    user, user_created = User.objects.get_or_create(username=user_name,
                                                    email=email)
    application_kwargs = dict(
        redirect_uris='',
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        skip_authorization=False
    )
    application, created = Application.objects.get_or_create(
        user=user, name=app_name, **application_kwargs
    )
    status = 'Created' if created else 'Found'
    print('{} {} application with id: {}, client_id: {}, and client_secret: {}'.format(
        status,
        app_name,
        application.id,
        application.client_id,
        application.client_secret,
    ))


def get_oauth_app():
    """
    This would return the Oauth app
    :return:
    """
    user, user_created = User.objects.get_or_create(username=user_name,
                                                    email=email)
    application, created = Application.objects.get_or_create(
        user=user
    )
    return application
