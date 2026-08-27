### Storage Account

You need to fill some parameters about the storage account that the deployment will use to save the recordings.

!!! warning

    Recordings are not available in OpenVidu v2 Compatibility mode (v2compat) for OpenVidu Azure deployments.

!!! info
    Port `9000` is MinIO's port. This deployment stores recordings and application data in Azure Blob Storage instead of MinIO, so MinIO is not deployed and port `9000` does not need to be open.

=== "Azure Storage Account configuration"
    
    Parameters in this section look like this:

    ![Azure Instance configuration](/assets/images/platform/self-hosting/shared/azure/storageaccount.png){ .round-corners loading=lazy }

    **Storage Account Name**: leave blank to create a new Storage Account for this deployment. You can specify an already existing Storage Account name  if you want (remember it must belong to the same resource group as your deployment).

    **Container Name** is the name that you desire for the container that of the storage account where the recordings will be saved. If you leave it blank it will create the container with name `openvidu-appdata`.