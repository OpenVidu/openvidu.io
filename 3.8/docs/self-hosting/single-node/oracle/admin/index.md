# OpenVidu Single Node **COMMUNITY** administration: Oracle Cloud Infrastructure

Oracle Cloud Infrastructure

Oracle Cloud Infrastructure OpenVidu Single Node deployments are internally identical to On Premises Single Node deployments, so you can follow the same instructions from [On Premises Single Node](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md) documentation for administration and configuration. The only difference is the underlying cloud infrastructure.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through the OCI Console

You can start and stop all services as explained in the [On Premises Single Node](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the Compute instance directly from the OCI Console. This will stop all services running in the instance and reduce Oracle Cloud Infrastructure costs.

**Stop OpenVidu Single Node**

1. Go to [OCI Compute Instances](https://cloud.oracle.com/compute/instances) .
1. There, you will find the Compute instance that runs OpenVidu.
1. Click the three-dots action menu next to the instance and select *"Stop"* to stop the instance (and therefore OpenVidu).

Stop OCI instance

**Start OpenVidu Single Node**

1. Go to [OCI Compute Instances](https://cloud.oracle.com/compute/instances) .
1. There, you will find the Compute instance that runs OpenVidu.
1. Click the three-dots action menu next to the instance and select *"Start"* to start the instance (and therefore OpenVidu).

Start OCI instance

## Change the instance shape

You can change the shape (instance type) of the OpenVidu Single Node instance to adapt it to your needs. To do this, follow these steps:

1. Go to [OCI Compute Instances](https://cloud.oracle.com/compute/instances) .

1. There, you will find the Compute instance that runs OpenVidu.

1. [Stop](#stop-openvidu-single-node) the instance if it is not already stopped. Wait for it to reach the **Stopped** state.

1. Click on the instance name to open its details, then click *"Edit"* next to the **Shape** field and select the new shape.

   **Change instance shape**

   Change OCI instance shape

1. Confirm the new shape and [start](#start-openvidu-single-node) the instance again.

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Single Node Administration](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Oracle Cloud Infrastructure deployment provides the capability to manage global configurations via the OCI Console using the Secrets via Secret Manager:

**Changing configuration through OCI Secret Manager**

1. Navigate to the [OCI Secrets Manager](https://cloud.oracle.com/security/secrets) in the OCI Console.

1. Click on the desired secret you want to change.

1. Scroll down to *"Versions"* and click on *"Create secret version"* to add a new version with the updated value.

   ```text
   ![Create Secret Version](../../../../assets/images/platform/self-hosting/single-node/oracle/create-secret-version.png){ .round-corners loading=lazy }
   ```

1. Enter the new secret value and click on *"Create secret version"*.

   ```text
   ![Create Secret Version](../../../../assets/images/platform/self-hosting/single-node/oracle/new-secret-version.png){ .round-corners loading=lazy }
   ```

1. Go to the [OCI Compute Instances](https://cloud.oracle.com/compute/instances) and click on [*Stop*](#stop-openvidu-single-node) → [*Start*](#start-openvidu-single-node) to apply the changes to the OpenVidu Single Node deployment.

Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
