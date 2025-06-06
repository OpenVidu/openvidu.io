### Resource Group and Stack Name

Select your **Subscription** and the **Resource Group** where you want to deploy OpenVidu.

<figure markdown>
![Azure Instance configuration](../../../../assets/images/self-hosting/shared/azure-stack-resource-group.png){ .svg-img .dark-img }
</figure>

!!! warning

    It is highly recommended to deploy OpenVidu in a brand new Azure Resource Group. Reusing an existing Resource Group can lead to conflicts. The only reason to reuse an existing Resource Group is to use the same **IP** and **Azure Blob Storage Account** as a previous OpenVidu deployment. The rest of resources are not reusable and should be eliminated before deploying OpenVidu in the same Resource Group.

Select the **Region** and choose a descriptive **Stack Name**. It will be used as a prefix in the name of all the resources created by the template.

<figure markdown>
![Azure Instance configuration](../../../../assets/images/self-hosting/shared/azure-stack-name-region.png){ .svg-img .dark-img }
</figure>