---
title: OpenVidu High Availability administration on Google Cloud Platform
description: Learn how to perform administrative tasks on an Google Cloud Platform OpenVidu High Availability deployment
---

# OpenVidu High Availability administration: Google Cloud Platform

The deployment of OpenVidu High Availability on Google Cloud Platform is automated using Infrastructure Manager in Google Cloud Console, with 4 Virtual Machine Instances as Master Nodes and any number of Media Nodes managed within a [Managed Instance Group :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/compute/docs/instance-groups?hl=en){:target=\_blank}. The Managed Instance Group of Media Nodes is configured to scale based on the target average CPU usage.

Internally, the Google Cloud Platform High Availability deployment mirrors the On Premises High Availability deployment, allowing you to follow the same administration and configuration guidelines provided in the [On Premises High Availability](../on-premises/admin.md) documentation. However, there are specific considerations unique to the Google Cloud Platform environment that are worth taking into account:

## Cluster shutdown and startup

You can start and stop the OpenVidu High Availability cluster at any time. The following sections detail the procedures:

=== "Shutting down the cluster"

    To shut down the cluster, you need to stop the Media Nodes and then stop the Master Nodes.

    1. Navigate to the [Google Cloud Platform Console :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/overview){:target=_blank}.
    2. Then click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on _"Edit"_.
        <figure markdown>
        ![Edit Button Location MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-mig-edit-tab.png){ .svg-img .dark-img }
        </figure>
    3. On this tab, go at the **Group Size & autoscaling** tab and change the _"Minimum"_ and _"Maximum"_ number of instances to 0.
        <figure markdown>
        ![Edit MIG](../../../../assets/images/self-hosting/shared/gcp-mig-instances-0.png){ .svg-img .dark-img }
        </figure>
    4. Click on save and wait, it needs the lambda function to run until is completed, you can check how is going in the _"VM instances"_ tab.
        <figure markdown>
        ![Save Edits MIG](../../../../assets/images/self-hosting/shared/gcp-mig-save.png){ .svg-img .dark-img }
        </figure>
    5. After confirming that all Media Node instances are terminated, in _"VM instances"_ tab select the instance called `<STACK_NAME>-master-node-1`. Click on it to go to the Master Node 1 instance. There, click on "Stop" to stop the instance.
        <figure markdown>
        ![Stop Master Node MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-stop-master-node.png){ .svg-img .dark-img }
        </figure>
    6. Repeat step 5 for all the Master Nodes.


=== "Starting up the cluster"

    To start the cluster, start the Master Nodes first and then the Media Nodes.

    1. Navigate to the [Google Cloud Platform Console :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/overview){:target=_blank}.
    2. In _"VM instances"_ tab select the instance called `<STACK_NAME>-master-node-1`, here click on start to start the Master Node 1.
        <figure markdown>
        ![Start Master Node](../../../../assets/images/self-hosting/ha/gcp/gcp-start-master-node.png){ .svg-img .dark-img }
        </figure>
    3. Wait until the instance is running.
    4. Repeat step 2 and 3 for all the Master Nodes until they are all up and running.
    5. Go to the _"Instance Groups"_ tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on _"Edit"_.
        <figure markdown>
        ![Edit Button Location MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-mig-edit-tab.png){ .svg-img .dark-img }
        </figure>
    5. Go to **Group Size & autoscaling** tab and change the _"Minimun"_ and _"Maximum"_ number of instances to your desired ones.
        <figure markdown>
        ![Edit MIG](../../../../assets/images/self-hosting/shared/gcp-mig-instances-1.png){ .svg-img .dark-img }
        </figure>
    6. Click on save and wait until is completed. You can check the progress in the _"Instances"_ tab.
        <figure markdown>
        ![Save Edits MIG](../../../../assets/images/self-hosting/shared/gcp-mig-save.png){ .svg-img .dark-img }
        </figure>

## Change the instance type

It is possible to change the instance type of both the Master Node and the Media Nodes. The following section details the procedures.

=== "Master Nodes"

    !!! warning

        This procedure requires downtime, as it involves stopping the Master Node.

    1. [Shutdown the cluster](#shutting-down-the-cluster).
    2. Go to the [Google Cloud Platform Console :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/overview){:target="_blank"} and locate the resource with the name `<STACK_NAME>-master-node-1` and click on it.
    3. Click on _"Edit"_ and inside change the _"Machine Type"_. Then select the size you desire and click on _"Save"_
        <figure markdown>
        ![Change instance type master](../../../../assets/images/self-hosting/shared/gcp-change-master-node-size.png){ .svg-img .dark-img }
        </figure>
    4. Repeat steps 2 and 3 for all the Master Nodes just in case you want to resize all of them, if not just do it for the ones you want.
    5. [Start the cluster](#starting-up-the-cluster).

=== "Media Nodes"

    !!! info

        This will delete the media nodes without the graceful delete option, if you want to stop them gracefully check the [Shutdown the Cluster](#shutting-down-the-cluster) tab

    1. Go to the _"Instance Group"_ tab and select the resource called `<STACK_NAME>-media-node-group` and click on the _"Template"_.
        <figure markdown>
        ![Select Template MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-template.png){ .svg-img .dark-img }
        </figure>
    2. To change the size click on _"Create similar"_ and create a new one with the desired size.
        <figure markdown>
        ![Create Similar Template](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-create-similar.png){ .svg-img .dark-img }
        </figure>
    3. Go back to the _"Instace Group"_ and click on _"Edit"_
        <figure markdown>
        ![Edit Button Location MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-mig-edit-tab.png){ .svg-img .dark-img }
        </figure>
    4. In _"Instace template & overrides"_ change the template for the one you've created previously and then _"Save"_.
        <figure markdown>
        ![Change Template MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-change-template.png){ .svg-img .dark-img }
        </figure>
    5. Delete the old sized instances.
        <figure markdown>
        ![Delete old sized instances MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-delete-old-instances.png){ .svg-img .dark-img }
        </figure>

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes by adjusting the scaling signals of the Managed Instance Group:

=== "Media Nodes Autoscaling Configuration"

    1. Go to the [Google Cloud Platform Console :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/overview){:target=_blank}.
    2. Go to the _"Instance Groups"_ tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on _"Edit"_.
        <figure markdown>
        ![Edit Button Location MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-mig-edit-tab.png){ .svg-img .dark-img }
        </figure>
    3. On this tab, go to _"Group size & autoscaling"_ and change the tab called _"Autoscaling signals"_
    5. In the _"Default"_ box you will find a section called _"Rules"_. Here you can add new rules or modify existing ones.
        
        !!! warning

            Currently there is only one rule to scale out. We are actively working in providing a graceful scale in process for Media Nodes to avoid active Rooms disruption.

        <figure markdown>
        ![Signals MIG](../../../../assets/images/self-hosting/shared/gcp-signals.png){ .svg-img .dark-img }
        </figure>

    !!! info

        OpenVidu High Availability is by default configured with a _"Target tracking scaling"_ policy that scales based on the target average CPU usage. However, you can configure different autoscaling policies according to your needs. For more information on the various types of autoscaling policies and how to implement them, refer to the [Google Cloud Platform
        MIG documentation :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/compute/docs/autoscaler?hl=en#autoscaling_policy){:target=_blank}.

## Fixed Number of Media Nodes

If you prefer to maintain a fixed number of Media Nodes instead of allowing the Managed Instance Group to perform dynamic scaling:

=== "Set Fixed Number of Media Nodes"

    1. Go to the [Google Cloud Platform Console :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/compute/overview){:target=_blank}.
    2. Go to the _"Instance Groups"_ tab, and there click into the Managed Instance Group resource called `<STACK_NAME>-media-node-group` and click on _"Edit"_.
        <figure markdown>
        ![Edit Button Location MIG](../../../../assets/images/self-hosting/ha/gcp/gcp-ha-mig-edit-tab.png){ .svg-img .dark-img }
        </figure>
    3. On this tab, go to _"Group size & autoscaling"_ and change the _"Auto-scaling mode"_ to **Off**, then set the _"Number of instances"_ on the top to the value of fixed number of Media Nodes you want. In this case is set to 3. Click on save next and wait to be applied
        <figure markdown>
        ![Fixed Number Media Nodes](../../../../assets/images/self-hosting/shared/gcp-fixed-media-nodes.png){ .svg-img .dark-img }
        </figure>

    !!! info

        This will delete the media nodes if you have set them to less than the number of media nodes that existed, if you want to stop them gracefully check the [Shutdown the Cluster](#shutting-down-the-cluster) tab.

### Deactivate Scale In
If you want a fixed number of Media Nodes you probably want to deactivate the Cloud Run Function that controls scale in actions. Follow these steps to do it:

=== "Deactivate Cloud Run Function"

    1. Go to the [Cloud Scheduler Jobs](https://console.cloud.google.com/cloudscheduler){:target="_blank"} and select the scheduler that controls the trigger of the Cloud Run Function you want to deactivate, then click on _"Pause"_ and it will not execute more until you click on _"Resume"_ whenever you want to make the cluster scale in again.
        <figure markdown>
        ![Deactivate Scale In](../../../../assets/images/self-hosting/ha/gcp/gcp-scalein-deactivate.png){ .svg-img .dark-img }
        </figure>

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises High Availability Administration](../on-premises/admin.md) section.

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](../../configuration/changing-config.md). Additionally, the [How to Guides](../../how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a Google Cloud Platform deployment provides the capability to manage global configurations via the Google Cloud Platform Console using Secrets Manager created during the deployment:

=== "Changing configuration through Secrets Manager"

    1. Navigate to the [GCP Secrets Manager :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/security/secret-manager){:target=_blank} on Google Cloud Platform.
    2. Click on the desired secret you want to change and click on _"New Version"_.
        <figure markdown>
        ![Google Cloud Platform Secrets Manager New Version Secret](../../../../assets/images/self-hosting/shared/gcp-secrets-new-version.png){ .svg-img .dark-img }
        </figure>
    3. Enter the new secret value on _"Secret Value"_ field and click on _"Add new version"_.
        <figure markdown>
        ![Google Cloud Platform Secrets Manager New Version Secret Create](../../../../assets/images/self-hosting/shared/gcp-secrets-create-version.png){ .svg-img .dark-img }
        </figure>
    4. Go to the Master Node resource you've want to change the secrets on and click on _"Stop"_ -> _"Start"_ to apply the changes to the OpenVidu High Availability deployment.

    Changes will be applied automatically in all the nodes of your OpenVidu High Availability deployment.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.