 **NOTE** Ensure you are using the IBL Retirement App Oauth Credentials (Can be Obtained from the Admin Dashboard)

1. Get users available for retirements
    
    **GET** `/api/ibl/retirements/`
        
    **RESPONSE**:
   
    ```
        {
          "message": [
            "audit"
          ]
        }
    ```

2. Place a fresh user into retirements

   **POST** /api/ibl/retirements/place_in_retirements/`

   **BODY** 
    ```
    {
        "username":"discovery_worker"
    }
    ```

    **RESPONSE**: 
    ```
    # Fresh entry
    {
      "message": "beta added to retirements successfully"
    }
    
    # Existing entry
    {
      "message": "discovery_worker already in retirement"
    }
    
    ```

3. Complete retirement steps
   
    **POST** `/api/ibl/retirements/retire_user`
   
    **BODY** 
    ```
    {
        "username":"discovery_worker"
    }
    ```

    **RESPONSE**: 
    ```
    # Success
    {
      "message": "beta retired successfully"
    }
    
    ```
