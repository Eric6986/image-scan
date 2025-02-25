# ga4-oci-adb-analytics

![image_scan_to_call_oci_vision](image/image_scan_to_call_oci_vision.png)

## Prerequisite

1. **Login to OCI and open the OCI Cloud Shell console**

    - **Into the OCI Cloud Shell console**

    ![into_cloud_shell](image/into_cloud_shell.png)

    - **Setup the architecture**
    
    Into the Actions -> Architecture -> select the preferred architecture as x86_64 -> Confirm
    
    ![setup_architecture](image/setup_architecture.png)
    ![setup_architecture_x86](image/setup_architecture_x86.png)

2. **Setup the OCI function**

    You can clone the code locally or use the OCI Cloud Shell console to run the code.
    Following the below steps to setup your OCI function environment. (Setup link: https://cloud.oracle.com/functions/apps/ocid1.fnapp.oc1.ap-singapore-1.aaaaaaaarh44z52razt3qkk2vrfjdh3gm3ra45ojynymqv7fvlu6flvilr3q/gettingStarted)


    ```
    fn list contextfn

    fn use context ap-singapore-1fn use context ap-singapore-1

    fn update context oracle.compartment-id ocid1.compartment.oc1..aaaaaaaazkgkbvurmqmdmsbvgfalptpysl5tqbfpwjcu4gsfp3ajmrik6hoq

    fn update context registry sin.ocir.io/ax0s9dy3myes/image-scan

    ...
    ```

3. **Deploy the OCI function**

    ```
    cd image-scan

    fn -v deploy --app image_scan

    ```
    
    The command will automatically generate a docker image and push to your container registry image-scan/image-scan.
    The latest version of the image is `0.0.1`. The version number will auto increase when you deploy the function again.

4. **Setup the connector to retrieve the specific log then trigger OCI function**

    Go to the OCI Logging -> Connector -> Create Connector
    Setup the logging rule that can catch the image object be uploaded to the bucket 'Tbox-Media-Temp'

    ![connector](image/connector.png)

    You can modify the log rule to catch the specific log that you want to trigger the OCI function. For example, the specific prefix of the log, or particular bucket name.

    - **Log query condition example**

    ```
    search "ocid1.compartment.oc1..aaaaaaaazkgkbvurmqmdmsbvgfalptpysl5tqbfpwjcu4gsfp3ajmrik6hoq" |   logContent='*Tbox-Media-Temp*' and data.statusCode='200' and data.message='Object uploaded.'
    ```

    ![log_query_condition](image/log_query_condition.png)

    - **Function target in connector**

    ![connector_target](image/connector_target.png)
