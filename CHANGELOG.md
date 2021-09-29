# CHANGELOG

### 3 Mar 2022
- Replaces the `ibl.retirement.user` creation to use the edX `manage_user` interface instead

### 3 Mar 2022
- Raises `ImproperlyConfigured` error when `ibl_retirement_states.py` has not been run on installation
- Removed auto-configure states from the apps.ready()
### 15 OCT 2021
- Passed changes made to the response sent out after a retirement is completed
- Ensured a ibl.retirement.user and superusers/staffs can call the API

### 13 OCT 2021
- Connect to lms host using either HTTPS or HTTP

### 14 Sep 2021
- We now have events emitted when GDPR is triggered

### 13 Sep 2021
- Patch to ensure the original username, email and name are truly retired

## 1.0.1 - 2021/09/24
* Update package imports for tutor-koa/python3.
* Changes `setup.py` added entry points `lms.djangoapp` and `cms.djangoapp`.
* Changes `app.py` added functionality to update `urls` and `INSTALLED_APPS`.
* Added a new `tutor` directory to base dir containing `ibl-edx-gdpr.yml` plugin.
* Added a new `settings/commons.py` directory to `ibl_edx_gdpr` .
