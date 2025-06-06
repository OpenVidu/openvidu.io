In addition to these, an AWS deployment provides the capability to manage global configurations via the AWS Console using AWS Secrets created during the deployment. To manage configurations this way, follow these steps:

=== "Changing Configuration through AWS Secrets"

    1. Navigate to the [CloudFormation Dashboard](https://console.aws.amazon.com/cloudformation/home){:target=_blank} on AWS.
    2. Select the CloudFormation Stack that you used to deploy OpenVidu Single Node.
    3. In the _"Outputs"_ tab, click the Link at _"ServicesAndCredentials"_. This will open the AWS Secrets Manager which contains all the configurations of the OpenVidu Single Node deployment.
        <figure markdown>
        ![Select Secrets Manager](../../../../assets/images/self-hosting/single-node/aws/outputs.png){ .svg-img .dark-img }
        </figure>
    4. Click on the _"Retrieve secret value"_ button to get the JSON with all the information.
        <figure markdown>
        ![Retrieve Secret Value](../../../../assets/images/self-hosting/single-node/aws/1-secrets-retrieve.png){ .svg-img .dark-img }
        </figure>
    5. Modify the parameter you want to change and click on _"Save"_.
    6. Go to the EC2 Console and click on _"Reboot instance"_ to apply the changes to the Master Node.
        <figure markdown>
        ![Reboot Instance](../../../../assets/images/self-hosting/single-node/aws/reboot-instance.png){ .svg-img .dark-img }
        </figure>

    Changes will be applied automatically.
