Whenever you are satisfied with your input values, just click on _"Continue"_ and then in _"Create deployment"_. Now it will validate the deployment and create all the resources. Wait around 5 to 10 minutes for the instance to install OpenVidu.

!!! warning

    In case of failure, check the cloud build logs that appears on the top of the screen and redeploy with the changes that are causing the deployment to fail, if it is something about some API delete the deployment and deploy another one, it should work now. If it keeps failing contact us.
    
    <figure markdown>
    ![Google Cloud Platform input variables](../../../../assets/images/self-hosting/shared/gcp-cloud-build-logs.png){ .svg-img .dark-img }
    </figure>

When everything is ready, you can check the secrets on the [Secret Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/security/secret-manager) or by connecting through SSH to the instance:

=== "Check deployment outputs in GCP Secret Manager"

    1. Go to the [Secret Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/security/secret-manager).

    2. Once you are in the Secret Manager you will see all the secrets by their name.

        <figure markdown>
        ![Google Cloud Platform Secrets location](../../../../assets/images/self-hosting/shared/gcp-secrets-manager.png){ .svg-img .dark-img }
        </figure>

    3. Here click on the secret of your choice, choose the last version and then click on the _"3 dots"_ -> _"View secret value"_ to retrieve that secret.

        <figure markdown>
        ![Google Cloud Platform Secrets version](../../../../assets/images/self-hosting/shared/gcp-secrets-version.png){ .svg-img .dark-img }
        </figure>

=== "Check deployment outputs in the instance"

    SSH to the instance by gcloud command generated in the web console and navigate to the config folder `/opt/openvidu/config`. Files with the deployment outputs are:

    - `openvidu.env`
    - `meet.env`

    To find out the command go to [Compute Engine Instances :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/instances) and click on the arrow close to the SSH letters and then _"View gcloud command"_.
    <figure markdown>
    ![Google Cloud Platform gcloud command](../../../../assets/images/self-hosting/shared/gcp-gcloud-command.png){ .svg-img .dark-img }
    </figure>   

    To install gcloud in your shell follow the official [instructions :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/sdk/docs/install?hl=en#linux).