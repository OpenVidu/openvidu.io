### Storage Account

You need to fill some parameters about the storage account that the deployment will use to save the recordings.

=== "Azure Storage Account configuration"
    
    The parameters in this section may look like this:

    <figure markdown>
    ![Azure Instance configuration](../../../../assets/images/self-hosting/shared/azure-storageaccount.png){ .svg-img .dark-img }
    </figure>

    **Storage Account Name** is used when upgrading OpenVidu version you want to save the recordings of the last deployment that you have used, it corresponds to the name of the storage account resource that was on the last OpenVidu deployment, leave it blank if you are not upgrading the version of OpenVidu.   
    **Container Name** is the name that you desire for the container that of the storage account where the recordings will be saved, if you leave it blank it will create the container with the name openvidu-appdata.