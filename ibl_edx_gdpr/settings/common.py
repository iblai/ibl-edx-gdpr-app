"""
Settings for the ibl_edx_gdpr app.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


USE_TZ = True

INSTALLED_APPS = (
    'ibl_edx_gdpr',
)


def plugin_settings(settings):
    pass