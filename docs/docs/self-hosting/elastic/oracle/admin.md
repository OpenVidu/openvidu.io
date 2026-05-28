---
title: OpenVidu Elastic administration on Oracle Cloud Infrastructure
description: Learn how to perform administrative tasks on an Oracle Cloud Infrastructure OpenVidu Elastic deployment
---

# OpenVidu Elastic administration: Oracle Cloud Infrastructure

<div class="provider-chip" markdown>

:custom-oracle-cloud-infrastructure:{ .provider-chip-icon } Oracle Cloud Infrastructure

</div>


The deployment of OpenVidu Elastic on Oracle Cloud Infrastructure is automated using the Terraform CLI, where Media Nodes are part of an [OCI Instance Pool :fontawesome-solid-external-link:{.external-link-icon}](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/creatinginstancepool.htm){:target=\_blank}. An OCI Function takes care of triggering scale-in actions, while the Instance Pool itself handles scale-out when more capacity is needed.

Internally, the Oracle Cloud Infrastructure Elastic deployment mirrors the On Premises Elastic deployment, allowing you to follow the same administration and configuration guidelines of the [On Premises Elastic](../on-premises/admin.md) documentation. However, there are specific considerations unique to the Oracle Cloud Infrastructure environment that are worth keeping in mind:

## Cluster shutdown and startup

The Master Node is a Compute instance, while the Media Nodes are part of an OCI Instance Pool. The process for starting and stopping these components differs:

=== "Shutting down the cluster"

    To shut down the cluster, you need to stop the Media Nodes and then stop the Master Node.

    1. Navigate to the [OCI Instance Pools :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instance-pools){:target=_blank}.
    2. Click into the Instance Pool called `<STACK_NAME>-media-node-pool`, then click on _"Edit"_.
        <figure markdown>
        ![Edit Instance Pool](../../../../assets/images/self-hosting/elastic/oracle/edit-instance-pool.png){ .svg-img .dark-img }
        </figure>
    3. Set the **Number of instances** to 0, then click _"Save changes"_ and wait for the change to be applied.
        <figure markdown>
        ![Set instances to 0](../../../../assets/images/self-hosting/elastic/oracle/instances-to-0.png){ .svg-img .dark-img }
        </figure>
    4. After confirming that all Media Node instances are terminated, go to [OCI Compute Instances :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instances){:target=_blank} and click the instance called `<STACK_NAME>-master-node`. There, click _"Stop"_ to stop the Master Node.
        <figure markdown>
        ![Stop Master Node](../../../../assets/images/self-hosting/elastic/oracle/stop-master-node.png){ .svg-img .dark-img }
        </figure>


=== "Starting up the cluster"

    To start the cluster, first start the Master Node and then the Media Nodes.

    1. Navigate to the [OCI Compute Instances :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instances){:target=_blank}.
    2. Select the instance named `<STACK_NAME>-master-node`, then click _"Start"_ to start the Master Node.
        <figure markdown>
        ![Start Master Node](../../../../assets/images/self-hosting/elastic/oracle/start-master-node.png){ .svg-img .dark-img }
        </figure>
    3. Wait until the instance is running.
    4. Go to the [OCI Instance Pools :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instance-pools){:target=_blank} and click the Instance Pool called `<STACK_NAME>-media-node-pool`, then click on _"Edit"_.
        <figure markdown>
        ![Edit Instance Pool](../../../../assets/images/self-hosting/elastic/oracle/edit-instance-pool.png){ .svg-img .dark-img }
        </figure>
    5. Set the **Number of instances** to your desired value and click _"Save changes"_, then wait for the Instance Pool to apply the changes.

## Change the instance shape

You can change the OCI Compute shape of both the Master Node and the Media Nodes. Since the Media Nodes belong to an Instance Pool, the process differs. The following section details the procedures:

=== "Master Node"

    !!! warning

        This procedure requires downtime, as it involves stopping the Master Node.

    1. [Shutdown the cluster](#shutting-down-the-cluster).

        !!! info

            You can stop only the Master Node instance to change its shape, but it is recommended to stop the whole cluster to avoid any issues.
    2. Go to the [OCI Compute Instances :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instances){:target=_blank} and locate the resource with the name `<STACK_NAME>-master-node` and click on it.
    3. Click _"Edit"_ next to the **Shape** field, select the new shape (or adjust OCPUs/Memory for Flex shapes) and click _"Save changes"_.
        <figure markdown>
        ![Change Master Node shape](../../../../assets/images/self-hosting/elastic/oracle/change-shape-master.png){ .svg-img .dark-img }
        </figure>
    4. [Start the cluster](#starting-up-the-cluster).

=== "Media Nodes"

    !!! warning
        This will replace the running Media Nodes without graceful shutdown. If you want to drain them gracefully, run `/usr/local/bin/graceful_shutdown.sh` on each Media Node and wait for it to finish before changing the Instance Configuration, since the Instance Pool will terminate existing instances and launch new ones with the updated configuration.

    1. Navigate to the [OCI Instance Configurations :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instance-configurations){:target=_blank}.
    2. Locate the Instance Configuration used by `<STACK_NAME>-media-node-pool`, click on it and select _"Create new instance configuration"_ (or edit if your workflow allows it) with the new shape, OCPUs and memory.
        <figure markdown>
        ![Create Instance Configuration](../../../../assets/images/self-hosting/elastic/oracle/create-instance-configuration.png){ .svg-img .dark-img }
        </figure>
    3. Go back to the [OCI Instance Pools :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/compute/instance-pools){:target=_blank}, open `<STACK_NAME>-media-node-pool`, click _"Edit"_, and change the **Instance Configuration** to the one you just created. Click _"Save changes"_ and wait for the Instance Pool to roll out the new configuration.
        <figure markdown>
        ![Change Instance Configuration in Pool](../../../../assets/images/self-hosting/elastic/oracle/change-instance-configuration.png){ .svg-img .dark-img }
        </figure>

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes via the `terraform.tfvars` file and `terraform apply`:

=== "Media Nodes Autoscaling Configuration"

    1. Go to the `terraform.tfvars` file and change the values related to autoscaling, such as:
        - **scaleTargetCPU**
        - **minNumberOfMediaNodes**
        - **maxNumberOfMediaNodes**

    2. Open a terminal and run the following command once you have updated the value(s):
    ```
    terraform apply
    ```
    3. Confirm the change that Terraform proposes (it will redeploy the OCI Function with the new values), and the changes will take effect.
        <figure markdown>
        ![Terraform output autoscale change](../../../../assets/images/self-hosting/elastic/oracle/terraform-output-autoscale-change.png){ .svg-img .dark-img }
        </figure>

## Fixed Number of Media Nodes

If you prefer to maintain a fixed number of Media Nodes instead of relying on the OCI Function for dynamic scaling, you can do so by setting **`minNumberOfMediaNodes`** and **`maxNumberOfMediaNodes`** to the same value:

=== "Set a fixed number of Media Nodes"

    1. Open the `terraform.tfvars` file and set the variables related to autoscaling to the same value:
        - **`minNumberOfMediaNodes`** = `<desired number>`
        - **`maxNumberOfMediaNodes`** = `<desired number>`
        - **`initialNumberOfMediaNodes`** = `<desired number>`

    2. Run:
    ```
    terraform apply
    ```
    3. Confirm the change that Terraform proposes. The Instance Pool will reconcile its size to the new value.

    !!! warning

        Reducing the number will terminate the surplus Media Nodes. If you want to stop them gracefully, run the `/usr/local/bin/graceful_shutdown.sh` script in each Media Node before applying the change.

### Deactivate scale-in

If you want a fixed number of Media Nodes you will probably want to deactivate the OCI Function that controls scale-in actions. To do so, disable its trigger:

=== "Deactivate scale-in"

    1. Navigate to the [OCI Functions :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/functions/applications){:target=_blank}, open the Application created by the stack, and locate the function in charge of the scale-in (named `<STACK_NAME>-scale-in`).
    2. Disable its scheduled trigger so it stops executing. You can re-enable it whenever you want the cluster to scale in again.
        <figure markdown>
        ![Disable Scale-in Function](../../../../assets/images/self-hosting/elastic/oracle/disable-scalein-function.png){ .svg-img .dark-img }
        </figure>

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Elastic Administration](../on-premises/admin.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](../../configuration/changing-config.md). Additionally, the [How to Guides](../../how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, an Oracle Cloud Infrastructure deployment provides the capability to manage global configurations via the OCI Console using OCI Vault Secrets:

=== "Changing configuration through OCI Secret Manager"

    1. Navigate to the [OCI Secrets Manager :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/security/secrets){:target="_blank"} in the OCI Console.
    2. Click the secret you want to change.
    3. Scroll down to _"Versions"_ and click _"Create secret version"_ to add a new version with the updated value.
            <figure markdown>
            ![Create Secret Version](../../../../assets/images/self-hosting/elastic/oracle/create-secret-version.png){ .svg-img .dark-img }
            </figure>
    4. Enter the new secret value and click _"Create secret version"_.
            <figure markdown>
            ![New Secret Version](../../../../assets/images/self-hosting/elastic/oracle/new-secret-version.png){ .svg-img .dark-img }
            </figure>
    5. [Shut down](#shutting-down-the-cluster) and [start up](#starting-up-the-cluster) the cluster to apply the changes to the OpenVidu Elastic deployment.

    Changes will be applied automatically.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
