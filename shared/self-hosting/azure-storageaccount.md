### Storage Account

You need to fill some parameters about the storage account that the deployment will use to save the recordings.

!!! warning

    Recordings are not available in OpenVidu 2.0 Compatibility mode (v2compat) in OpenVidu 3.2.0 deployed in Azure.

=== "Azure Storage Account configuration"
    
    The parameters in this section may look like this:

    <figure markdown>
    ![Azure Instance configuration](../../../../assets/images/self-hosting/shared/azure-storageaccount.png){ .svg-img .dark-img }
    </figure>

    **Storage Account Name**, leave blank so a new Storage Account is created for this deployment. Specify an existing account name if this new desployment has to point to the storage account created in a previous deployment (to be able to access to existing recordings), remember it has to exists in the same resource group you are deploying.

    **Container Name** is the name that you desire for the container that of the storage account where the recordings will be saved, if you leave it blank it will create the container with the name openvidu-appdata.