## IBL EDX GDPR API
This is a wrapper edX app that performs the extra retirement steps once a user requires his account to be deactivated


#### Install
```
cd $(tutor config printroot)"/env/build/openedx/requirements
git clone --branch koa-tutor-plugin https://gitlab.com/iblstudios/ibl-edx-gdpr.git

#Enter the lms shell 
tutor local run lms bash
pip install -e ../requirement/iblstudios/ibl-edx-gdpr
```

#### Uninstall
```
#Enter the lms shell 
tutor local run lms bash
pip uninstall ibl_edx_gdpr
```

## Setup
* Add these variables to `ibl-edx-gdpr.yml` and enable the plugin `tutor plugins enable ibl-edx-gdpr` to be applied to `lms/envs/common.py`:

1. Enable retirement in LMS `/lms/envs/common.py` , ensure 
    ```
    FEATURES = {
        ...
        "ACCOUNT_DELETION": True,
        ...
    }
    ```

<<<<<<< HEAD

2. Set ``HOST = <your-edx-domain>``  in `lms/envs/common.py` to ensure the script works
    - Optional settings
    
        `IBL_GDPR_USE_HTTPS=False/True <either to connect to HOST using https or http>` 
=======
2. Set  ``HOST = <your-edx-domain>``  in `lms/envs/common.py` to ensure the script works

3. Configure in `lms.env.json`   SALT (For email and username hashing ) and RETIREMENT_SERVICE_WORKER_USERNAME 
   (Only user asides superusers, authorized to perform retirements)
   
    ```
        RETIRED_USER_SALTS = ['some-Complicated-something', 'some-Complicated-something']
        RETIREMENT_SERVICE_WORKER_USERNAME = ibl.retirement.user
    ```
>>>>>>> 7bcbb0f (plugin update and README.md)

4. `ibl_edx_gdpr` will be added to `INSTALLED_APPS` in `lms/envs/common.py` automatically. 
    
    ```python
    INSTALLED_APPS = [
        #...
        'ibl_edx_gdpr'
        #...
    ]
    ```

5. (_Optional_) The apps `urlpatterns` will be added to `lms/urls.py`  automatically.

    ```python
    urlpatterns += (
        url(r'^api/ibl/retirements/', include('ibl_edx_gdpr.urls')),
    )
    ```
6. Import retirement states
```
./manage.py lms ibl_retirement_states
```
7. Restart the lms

**NOTE**: After these steps are done, 
1. Retirement States Model would be automatically populated with the right RETIREMENT_STATES
2. A new user `ibl.retirement.user` would be created
3. A new Django Oauth Toolkit Application `IBL Retirement App` would be created, (use the credentials for calling the API)


Activate the plugin `tutor plugins enable ibl-edx-gdpr`
save the new configuration as shown in the terminal `config save`

Rebuild the image to apply the new config changes 

```tutor images build openedx --build-arg EDX_PLATFORM_REPOSITORY=https://github.com/edx/edx-platform.git --build-arg EDX_PLATFORM_VERSION=open-release/koa.3```

## USAGE
The application can easily retire a learner in two Scenario

### Scenario 1 (User in Retirement Pipeline )

Profile Deactivation/Retirement was/is initiated by the user in his user dashboard
   
* If user has already clicked the ``DELETE MY ACCOUNT`` button in his profile.
   ![img.png](img.png)


* Run the `ibl_complete_retirement` command
  
  ```
      ./manage.py lms ibl_complete_retirement --username ibltestuser
  
        b'Learner Retirement: (ibltestuser) Starting state RETIRING_ENROLLMENTS'
        b'Learner Retirement: (ibltestuser) State RETIRING_ENROLLMENTS completed in 0.11639761924743652 seconds'
        b'Learner Retirement: (ibltestuser) Progressing to state ENROLLMENTS_COMPLETE'
        b'Learner Retirement: (ibltestuser) Starting state RETIRING_LMS'
        b'Learner Retirement: (ibltestuser) State RETIRING_LMS completed in 0.10183119773864746 seconds'
        b'Learner Retirement: (ibltestuser) Progressing to state LMS_COMPLETE'
        b'Learner Retirement: (ibltestuser) Retirement complete for learner ibltestuser' 
    ```

### Scenario 2 (Manual Retirement)
User does not exist in retirement pipeline, we would need to deactivate/retire a user profile without needing the user to click deactivate` in account settings.

**Note** This is a more likely scenerio
* Add User to Retirement Pipeline
   ```ssh
   ./manage.py lms ibl_retire_user --username ibluser --user_email ibluser@ibleducation.com
   
   User successfully moved to the retirement pipeline
   ```
* Run the ibl_complete_retirement command
    ```ssh
      ./manage.py lms ibl_complete_retirement --username ibltestuser
  
        b'Learner Retirement: (ibltestuser) Starting state RETIRING_ENROLLMENTS'
        b'Learner Retirement: (ibltestuser) State RETIRING_ENROLLMENTS completed in 0.11639761924743652 seconds'
        b'Learner Retirement: (ibltestuser) Progressing to state ENROLLMENTS_COMPLETE'
        b'Learner Retirement: (ibltestuser) Starting state RETIRING_LMS'
        b'Learner Retirement: (ibltestuser) State RETIRING_LMS completed in 0.10183119773864746 seconds'
        b'Learner Retirement: (ibltestuser) Progressing to state LMS_COMPLETE'
        b'Learner Retirement: (ibltestuser) Retirement complete for learner ibltestuser'
      
    ```

## Using the API

See [USAGE](USAGE.md) for how to use with API, Go to admin, Applications and use the IBL Retirement App Credentials to 
authenticate with the API

## Debugging
1. JSONDecodeError
    * Check that the HOST variable is valid
    
2. Learner Retirement: Learner retire2@retire.com not found. Please check that the learner is present in UserRetirementStatus, is not already retired, and is in an appropriate state to be acted upon.
    * Run the `ìbl_retire_user` command passing the username and email as params

3. Connection Refused 
    * Check if the current can access the url set in ``HOST``
    * Turn off HTTPS by setting `IBL_GDPR_USE_HTTPS` to `False`

## Process Flow
![img_1.png](img_1.png)