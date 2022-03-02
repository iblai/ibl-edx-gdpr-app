# CHANGELOG

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