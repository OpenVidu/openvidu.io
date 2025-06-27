### Storage Account

You need to fill some parameters about the storage account that the deployment will use to save the recordings.

!!! warning

    Recordings are not available in OpenVidu v2 Compatibility mode (v2compat) for OpenVidu Azure deployments.

=== "Azure Storage Account configuration"
    
    Parameters in this section look like this:

    <figure markdown>
    ![Azure Instance configuration](../../../../assets/images/self-hosting/shared/azure-storageaccount.png){ .svg-img .dark-img }
    </figure>

    **Storage Account Name**: leave blank to create a new Storage Account for this deployment. You can specify an already existing Storage Account name  if you want (remember it must belong to the same resource group as your deployment).

    **Container Name** is the name that you desire for the container that of the storage account where the recordings will be saved. If you leave it blank it will create the container with name `openvidu-appdata`.