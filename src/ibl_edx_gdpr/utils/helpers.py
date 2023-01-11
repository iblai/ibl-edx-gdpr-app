"""
Common helper methods to use in tubular scripts.
"""
# NOTE: Make sure that all non-ascii text written to standard output (including
# print statements and logging) is manually encoded to bytes using a utf-8 or
# other encoding.  We currently make use of this library within a context that
# does NOT tolerate unicode text on sys.stdout, namely python 2 on Build
# Jenkins.  PLAT-2287 tracks this Tech Debt.


import io
import json
import sys
import traceback
import unicodedata
from os import path

from six import text_type

# Add top-level module path to sys.path before importing tubular code.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def _log(kind, message):
    """
    Convenience method to log text. Prepended "kind" text makes finding log entries easier.
    """
    print(u'{}: {}'.format(kind, message).encode('utf-8'))  # See note at the top of this file.


def _fail(kind, code, message):
    """
    Convenience method to fail out of the command with a message and traceback.
    """
    _log(kind, message)

    # Try to get a traceback, if there is one. On Python 3.4 this raises an AttributeError
    # if there is no current exception, so we eat that here.
    try:
        _log(kind, traceback.format_exc())
    except AttributeError:
        pass

    sys.exit(code)


def _fail_exception(kind, code, message, exc):
    """
    A version of fail that takes an exception to be utf-8 decoded
    """
    exc_msg = _get_error_str_from_exception(exc)
    message += '\n' + exc_msg
    _fail(kind, code, message)


def _get_error_str_from_exception(exc):
    """
    Return a string from an exception that may or may not have a .content (Slumber)
    """
    exc_msg = text_type(exc)

    if hasattr(exc, 'content'):
        # Slumber inconveniently discards the decoded .text attribute from the Response object,
        # and instead gives us the raw encoded .content attribute, so we need to decode it first.
        # Python 2 needs the decode, Py3 does not have it.
        try:
            exc_msg += '\n' + str(exc.content).decode('utf-8')
        except AttributeError:
            exc_msg += '\n' + str(exc.content)

    return exc_msg

