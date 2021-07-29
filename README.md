## IBL EDX GDPR API
This is a wrapper edX app that performs the extra retirement steps once a user requires his account to be deactivated


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

[comment]: <> (2. Set RETIREMENT_STATES using the ``./manage.py lms ibl_retirement_states`` or via the API 'api/user_api/populate_retirement')

[comment]: <> (```)

[comment]: <> (RETIREMENT_STATES = [)

[comment]: <> (    'PENDING',)

[comment]: <> (    'LOCKING_ACCOUNT',)

[comment]: <> (    'LOCKING_COMPLETE',)

[comment]: <> (    # Use these states only when ENABLE_DISCUSSION_SERVICE is True.)

[comment]: <> (    'RETIRING_FORUMS',)

[comment]: <> (    'FORUMS_COMPLETE',)

[comment]: <> (    'RETIRING_EMAIL_LISTS',)

[comment]: <> (    'EMAIL_LISTS_COMPLETE',)

[comment]: <> (    'RETIRING_ENROLLMENTS',)

[comment]: <> (    'ENROLLMENTS_COMPLETE',)

[comment]: <> (    # Use these states only when ENABLE_STUDENT_NOTES is True.)

[comment]: <> (    'RETIRING_NOTES',)

[comment]: <> (    'NOTES_COMPLETE',)

[comment]: <> (    'RETIRING_LMS',)

[comment]: <> (    'LMS_COMPLETE',)

[comment]: <> (    'ERRORED',)

[comment]: <> (    'ABORTED',)

[comment]: <> (    'COMPLETE',)

[comment]: <> (])

[comment]: <> (```)

2. **Important**, configure SALT and Retirement service worker that would be used for email and username hashing
```
RETIRED_USER_SALTS = ['some-Complicated-something', 'some-Complicated-something']
RETIREMENT_SERVICE_WORKER_USERNAME = ibl.retirement.user
```

4. **IMPORTANT** Set a ``HOST = <your-edx-domain>``  to ensure the script works

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
INSTALLED_APPS = (
    #...
    'ibl_edx_gdpr'
    #...
)
```

### Routing
In `lms/urls.py`:


### Settings


### Commands
The application can easily retire a learner in two Scenerio

1. The user clicks the deactivate button in his profile.
    * Run the retire_learner() function
        ```python
       from ibl_edx_gdpr.client import RetirementClient
       client = RetirementClient()
      
      # Check users in retirement (Excludes users that have their username hashed already)
      client.get_learners_to_retire_usernames()
      >> ['azeem']
      
      # Retire the user
      client.retire_learner('azeem')
      b'Learner Retirement: (az) Starting state RETIRING_ENROLLMENTS'
        b'Learner Retirement: (az) State RETIRING_ENROLLMENTS completed in 0.11639761924743652 seconds'
        b'Learner Retirement: (az) Progressing to state ENROLLMENTS_COMPLETE'
        b'Learner Retirement: (az) Starting state RETIRING_LMS'
        b'Learner Retirement: (az) State RETIRING_LMS completed in 0.10183119773864746 seconds'
        b'Learner Retirement: (az) Progressing to state LMS_COMPLETE'
        b'Learner Retirement: (az) Retirement complete for learner az'
      
      ```
    


### Endpoints

