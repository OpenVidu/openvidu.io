When you are satisfied with your input values, click _"Continue"_ and then _"Create deployment"_. The deployment will be validated and all resources will be created. Wait around 5 to 10 minutes for the instance to install OpenVidu.

!!! warning

    In case of failure, check the Cloud Build logs that appear at the top of the screen and redeploy after applying the required changes. If the issue is related to an API, delete the deployment and create a new one. If it keeps failing, contact us.
    
    <figure markdown>
    ![Google Cloud Platform input variables](../../../../assets/images/self-hosting/shared/gcp-cloud-build-logs.png){ .svg-img .dark-img }
    </figure>

When everything is ready, you can check the secrets on the [Secret Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/security/secret-manager){:target=_blank} or by connecting through SSH to the instance:

=== "Check deployment outputs in GCP Secret Manager"

    1. Go to the [Secret Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/security/secret-manager){:target=_blank}.

    2. Once you are in Secret Manager, you will see all secrets by name.

        <figure markdown>
        ![Google Cloud Platform Secrets location](../../../../assets/images/self-hosting/shared/gcp-secrets-manager.png){ .svg-img .dark-img }
        </figure>

    3. Click the secret you want, select the latest version, and then click _"3 dots"_ -> _"View secret value"_ to retrieve it.

        <figure markdown>
        ![Google Cloud Platform Secrets version](../../../../assets/images/self-hosting/shared/gcp-secrets-version.png){ .svg-img .dark-img }
        </figure>

=== "Check deployment outputs in the instance"

    SSH into the instance using the `gcloud` command generated in the web console, then navigate to the `/opt/openvidu/config` folder. Files with the deployment outputs are:

    - `openvidu.env`
    - `meet.env`

    To find the command, go to [Compute Engine Instances :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/instances){target="\_blank"}, click the arrow next to **SSH**, and then click _"View gcloud command"_.
    <figure markdown>
    ![Google Cloud Platform gcloud command](../../../../assets/images/self-hosting/shared/gcp-gcloud-command.png){ .svg-img .dark-img }
    </figure>   

    To install `gcloud` in your shell, follow the official [instructions :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/sdk/docs/install?hl=en#linux){:target="_blank"}.