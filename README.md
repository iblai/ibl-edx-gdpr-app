## IBL EDX GDPR API

## Setup
### edX Server Setup
See 
1. Enable retirement in LMS, ensure 
```
FEATURES = {
    ...
    "ACCOUNT_DELETION": True,
    ...
}
```
2. Set RETIREMENT_STATES using the ``./manage.py lms ibl_retirement_states`` or via the API 'api/user_api/populate_retirement'
```
RETIREMENT_STATES = [
    'PENDING',

    'LOCKING_ACCOUNT',
    'LOCKING_COMPLETE',

    # Use these states only when ENABLE_DISCUSSION_SERVICE is True.
    'RETIRING_FORUMS',
    'FORUMS_COMPLETE',

    'RETIRING_EMAIL_LISTS',
    'EMAIL_LISTS_COMPLETE',

    'RETIRING_ENROLLMENTS',
    'ENROLLMENTS_COMPLETE',

    # Use these states only when ENABLE_STUDENT_NOTES is True.
    'RETIRING_NOTES',
    'NOTES_COMPLETE',

    'RETIRING_LMS',
    'LMS_COMPLETE',

    'ERRORED',
    'ABORTED',
    'COMPLETE',
]
```

3. Important, configure SALT and username that would be used for email and username hashing
```
RETIRED_USER_SALTS = ['some-Complicated-something', 'some-Complicated-something']
RETIREMENT_SERVICE_WORKER_USERNAME = ibl.retirement.user
```

### Install command
#### Install
```shell
sudo -Hu edxapp /edx/app/edxapp/venvs/edxapp/bin/pip install \
    git+https://gitlab.com/iblstudios/ibl-edx-gdpr.git
```

#### Reinstall
```shell
sudo -Hu edxapp /edx/app/edxapp/venvs/edxapp/bin/pip install --upgrade --no-deps --force-reinstall \
    git+https://gitlab.com/iblstudios/ibl-edx-gdpr.git
```

#### Uninstall
```shell
sudo -Hu edxapp /edx/app/edxapp/venvs/edxapp/bin/pip uninstall ibl_edx_gdpr
```

### Django Setup

#### App Registration
In `lms/envs/common.py` and/or `cms/envs/common.py`:

Add `ibl_edx_gdpr` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = INSTALLED_APPS + (
    #...
    'ibl_edx_gdpr'
    #...
)
```

### Routing
In `lms/urls.py`:

(_Optional_) Add URL pattern for completion status endpoints if needed.

```python
urlpatterns += (
    url(r'^api/ibl/gdpr/', include('ibl_edx_gdpr.urls')),
)
```

### Settings


### Commands

### Endpoints

See [USAGE](USAGE.md) docs.
