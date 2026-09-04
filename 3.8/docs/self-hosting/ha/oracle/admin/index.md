# OpenVidu High Availability administration: Oracle Cloud Infrastructure

Oracle Cloud Infrastructure

The deployment of OpenVidu High Availability on Oracle Cloud Infrastructure is automated using the Terraform CLI, with 4 Compute instances as Master Nodes behind an [OCI Network Load Balancer](https://docs.oracle.com/en-us/iaas/Content/NetworkLoadBalancer/home.htm) , and any number of Media Nodes managed within an [OCI Instance Pool](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/creatinginstancepool.htm) . An OCI Function takes care of triggering scale-in actions, while the Instance Pool itself handles scale-out when more capacity is needed.

Internally, the Oracle Cloud Infrastructure High Availability deployment mirrors the On Premises High Availability deployment, allowing you to follow the same administration and configuration guidelines provided in the [On Premises High Availability](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the Oracle Cloud Infrastructure environment that are worth keeping in mind:

## Cluster shutdown and startup

The Master Nodes are 4 individual Compute instances, while the Media Nodes are part of an OCI Instance Pool. The process for starting and stopping these components differs:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes first and then stop the Master Nodes.

Gracefully stopping Media Nodes

Setting the Instance Pool size to 0 terminates the Media Nodes immediately without waiting for active Rooms to complete. The graceful drain that the scale-in OCI Function performs is **not** invoked on a manual pool resize.

Wait for your active Rooms to finish before stopping the cluster, or SSH into each Media Node and run `/usr/local/bin/graceful_shutdown.sh` to drain it before saving the change.

1. Navigate to the [OCI Instance Pools](https://cloud.oracle.com/compute/instance-pools) .

1. Click into the Instance Pool called `<STACK_NAME>-media-pool`, then click on *"Edit"*.

   Edit Instance Pool

1. Set the **Number of instances** to 0, then click *"Save changes"* and wait for the change to be applied.

   Set instances to 0

1. After confirming that all Media Node instances are terminated, go to [OCI Compute Instances](https://cloud.oracle.com/compute/instances) and stop each Master Node one by one. The Master Nodes are named `<STACK_NAME>-master-node-x`. Click each one and select *"Stop"*.

   Stop Master Node

   Info

   All 4 Master Nodes must be stopped to fully shut down the cluster. Stopping fewer than 4 leaves the deployment in a degraded state.

**Starting up the cluster**

To start the cluster, first start all 4 Master Nodes and then the Media Nodes.

1. Navigate to the [OCI Compute Instances](https://cloud.oracle.com/compute/instances) .

1. Select all the instances named `<STACK_NAME>-master-node-x`, then click *"Start"*. Wait until the instances are running.

   Start Master Node

1. Go to the [OCI Instance Pools](https://cloud.oracle.com/compute/instance-pools) and click the Instance Pool called `<STACK_NAME>-media-pool`, then click on *"Edit"*.

   Edit Instance Pool

1. Set the **Number of instances** to your desired value and click *"Save changes"*, then wait for the Instance Pool to apply the changes.

   Warning

   This **Number of instances** is just an initial set — it does **not** become a fixed size and does **not** raise `minNumberOfMediaNodes`. If you set it above `minNumberOfMediaNodes`, the scale-in OCI Function may terminate the extra Media Nodes back down to the minimum as soon as it detects low CPU usage.

## Change the instance shape

You can change the OCI Compute shape of both the Master Nodes and the Media Nodes. Since the Media Nodes belong to an Instance Pool, the process differs. The following section details the procedures:

**Master Nodes**

Warning

This procedure requires downtime, as it involves stopping all Master Nodes.

1. [Shutdown the cluster](#shutting-down-the-cluster).

   Info

   All 4 Master Nodes must run with the same shape. Changing only some of them will leave the cluster in an inconsistent state.

1. Go to the [OCI Compute Instances](https://cloud.oracle.com/compute/instances) and locate the resource named `<STACK_NAME>-master-node-1`. Click on it.

1. Click *"Edit"* next to the **Shape** field, select the new shape (or adjust OCPUs/Memory for Flex shapes) and click *"Save changes"*.

   Change Master Node shape

1. Repeat steps 2 and 3 for `<STACK_NAME>-master-node-2`, `<STACK_NAME>-master-node-3` and `<STACK_NAME>-master-node-4`, using the same shape and size on every Master Node.

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

Warning

This will replace the running Media Nodes without graceful shutdown. If you want to drain them gracefully, run `/usr/local/bin/graceful_shutdown.sh` on each Media Node and wait for it to finish before changing the Instance Configuration, since the Instance Pool will terminate existing instances and launch new ones with the updated configuration.

1. Navigate to the [OCI Instance Configurations](https://cloud.oracle.com/compute/instance-configurations) .

1. Locate the Instance Configuration used by `<STACK_NAME>-media-pool`, click on it, open the *"Actions"* menu and select *"Create duplicate"*. The form opens pre-filled with the current configuration — adjust the shape (or OCPUs/Memory for Flex shapes) and create the new Instance Configuration.

   Create Instance Configuration

   Warning

   **Only change the shape** (or OCPUs/Memory for Flex shapes). Do **not** modify any other field — the rest of the configuration must remain identical to the original so the Instance Pool keeps working as expected.

1. Go back to the [OCI Instance Pools](https://cloud.oracle.com/compute/instance-pools) , open `<STACK_NAME>-media-pool`, click *"Edit"*, and change the **Instance Configuration** to the one you just created. Click *"Save changes"* and wait for the Instance Pool to roll out the new configuration.

   Change Instance Configuration in Pool

1. Terminate the existing Media Nodes from the [OCI Compute Instances](https://cloud.oracle.com/compute/instances) page so the Instance Pool replaces them with new ones launched from the updated Instance Configuration. Old Media Nodes are **not** replaced automatically when the Instance Configuration changes — only newly launched instances use the new shape.

## Media Nodes Autoscaling Configuration

Warning

If you previously [changed the Media Node shape](#change-the-instance-shape) by creating a duplicated Instance Configuration manually from the OCI Console, Terraform is unaware of it. Running `terraform apply` will point the Instance Pool back to its own Instance Configuration (the original one, recreated by Terraform), and the manually duplicated Instance Configuration will be orphaned.

You can modify the autoscaling configuration of the Media Nodes via the `terraform.tfvars` file and `terraform apply`:

**Media Nodes Autoscaling Configuration**

1. Go to the `terraform.tfvars` file and change the values related to autoscaling, such as:

   - **scaleTargetCPU**
   - **minNumberOfMediaNodes**
   - **maxNumberOfMediaNodes**

1. Open a terminal and run the following command once you have updated the value(s):

   ```text
   terraform apply
   ```

1. Confirm the change that Terraform proposes (it will update the autoscaling configuration, and the scale-in OCI Function when `scaleTargetCPU` or `minNumberOfMediaNodes` change), and the changes will take effect.

   Terraform output autoscale change

## Fixed Number of Media Nodes

You can switch between **autoscaling mode** (autoscaling Instance Pool + scale-in OCI Function) and **fixed mode** (a static number of Media Nodes with no autoscaling) by changing the **`fixedNumberOfMediaNodes`** variable and running `terraform apply`.

Switching modes does **not** recreate the Master Nodes. Each Master Node carries a `scale-in-mode` freeform tag that Terraform flips in place (`elastic` ⇄ `fixed`), and the scale-in scripts on every node read this tag at runtime. The 4 Master Nodes and the Media Node Instance Configuration are therefore left untouched — only the scale-in OCI Function and the autoscaling configuration are created or destroyed, and the Instance Pool is resized.

Warning

Any Media Nodes terminated during these transitions are killed immediately without running the graceful shutdown — active Rooms on those nodes are cut.

**Activate Fixed Number of Media Nodes**

1. Go to the `terraform.tfvars` file and set:

   - **`fixedNumberOfMediaNodes`** to the desired number of Media Nodes (must be greater than 0).

1. Open a terminal and run:

   ```text
   terraform apply
   ```

1. Confirm the change that Terraform proposes. It will destroy the scale-in OCI Function and the autoscaling configuration, flip the Master Nodes' `scale-in-mode` tag to `fixed`, and resize the Instance Pool to the fixed number of Media Nodes.

   Terraform output activate fixed media nodes

## Activate Scale In

Switch a fixed-size deployment back to **autoscaling mode**, re-enabling automatic Media Node scaling and the scale-in OCI Function.

**Activate Scale In**

1. Go to the `terraform.tfvars` file and set:

   - **`fixedNumberOfMediaNodes`** to `0`.
   - **`scaleTargetCPU`** if you don't want the default.
   - **`minNumberOfMediaNodes`** if you don't want the default.
   - **`maxNumberOfMediaNodes`** if you don't want the default.

1. Open a terminal and run:

   ```text
   terraform apply
   ```

1. Confirm the change that Terraform proposes. It will recreate the scale-in OCI Function, re-attach the autoscaling configuration to the Instance Pool, and flip the Master Nodes' `scale-in-mode` tag back to `elastic`.

   Terraform output activate scale in

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises High Availability Administration](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Oracle Cloud Infrastructure deployment provides the capability to manage global configurations via the OCI Console using OCI Vault Secrets:

**Changing configuration through OCI Secret Manager**

1. Navigate to the [OCI Secrets Manager](https://cloud.oracle.com/security/secrets) in the OCI Console.

1. Click the secret you want to change.

1. Scroll down to *"Versions"* and click *"Create secret version"* to add a new version with the updated value.

   Create Secret Version

1. Enter the new secret value and click *"Create secret version"*.

   New Secret Version

1. [Shut down](#shutting-down-the-cluster) and [start up](#starting-up-the-cluster) the cluster to apply the changes to the OpenVidu High Availability deployment.

Changes will be applied automatically on all nodes of your OpenVidu High Availability deployment.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
