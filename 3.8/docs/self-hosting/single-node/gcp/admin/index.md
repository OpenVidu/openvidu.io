# OpenVidu Single Node administration: Google Cloud Platform

Google Cloud Platform

Google Cloud Platform OpenVidu Single Node deployments are internally identical to On Premises Single Node deployments, so you can follow the same instructions from [On Premises Single Node](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md) documentation for administration and configuration. The only difference is that the deployment is automated with Terraform from Google Cloud Platform.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through Google Cloud Platform Console

You can start and stop all services as explained in the [On Premises Single Node](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the Virtual Machine instance directly from Google Cloud Platform Console. This will stop all services running in the instance and reduce Google Cloud Platform costs.

**Stop OpenVidu Single Node**

1. Go to [GCP Compute Engine Instances](https://console.cloud.google.com/compute/instances) of Google Cloud Platform.
1. There, you will find the Virtual Machine that runs OpenVidu. Its name should be something like `<STACK_NAME>-vm-ce` (COMMUNITY) or `<STACK_NAME>-vm-pro` (PRO). Click on it.
1. In the Virtual Machine section, click the stop button to stop the Virtual Machine (and therefore OpenVidu).

Stop instance

**Start OpenVidu Single Node**

1. Go to [GCP Compute Engine Instances](https://console.cloud.google.com/compute/instances) of Google Cloud Platform.
1. There, you will find the Virtual Machine that runs OpenVidu. Its name should be something like `<STACK_NAME>-vm-ce` (COMMUNITY) or `<STACK_NAME>-vm-pro` (PRO). Click on it.
1. In the Virtual Machine section, click the start button to start the Virtual Machine (and therefore OpenVidu).

Start instance

## Change the instance type

You can change the instance type of the OpenVidu Single Node instance to adapt it to your needs. To do this, follow these steps:

1. Go to [GCP Compute Engine Instances](https://console.cloud.google.com/compute/instances) of Google Cloud Platform.

1. There, you will find the Virtual Machine that runs OpenVidu. Its name should be something like `<STACK_NAME>-vm-ce` (COMMUNITY) or `<STACK_NAME>-vm-pro` (PRO). Click on it.

1. Stop the instance if it is not stopped. Wait for it to stop.

1. Click on *"Edit"*, scroll down and change the **Machine Type**.

   **Change instance type**

   Change instance type

1. Select the new instance type and click on *"Save"*.

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Single Node Administration](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

**Changing configuration through Secrets Manager**

1. Navigate to the [GCP Secrets Manager](https://console.cloud.google.com/security/secret-manager) on Google Cloud Platform.

1. Click on the desired secret you want to change and click on *"New Version"*.

   Google Cloud Platform Secrets Manager New Version Secret

1. Enter the new secret value on *"Secret Value"* field and click on *"Add new version"*.

   Google Cloud Platform Secrets Manager New Version Secret Create

1. Go to the Instance resource of OpenVidu and click on [*Stop*](#stop-openvidu-single-node) -> [*Start*](#start-openvidu-single-node) to apply the changes to the OpenVidu Single Node deployment.

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
