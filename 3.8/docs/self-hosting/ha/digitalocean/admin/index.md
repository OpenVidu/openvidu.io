# OpenVidu High Availability administration: DigitalOcean

DigitalOcean

The OpenVidu High Availability deployment on DigitalOcean is fully automated using the Terraform CLI. It provisions 4 Droplets for the Master Nodes, while Media Nodes are managed through a [Fixed Droplet Autoscale Pool](https://docs.digitalocean.com/products/droplets/concepts/autoscale-pools/) .

Internally, the DigitalOcean High Availability deployment mirrors the On Premises High Availability deployment, allowing you to follow the same administration and configuration guidelines of the [On Premises High Availability](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/index.md) documentation. However, there are specific considerations unique to the DigitalOcean environment that are worth keeping in mind:

## Cluster shutdown and startup

You can start and stop the OpenVidu High Availability cluster at any time. The following sections detail the procedures:

**Shutting down the cluster**

To shut down the cluster, you need to stop the Media Nodes and then stop the Master Nodes.

1. Navigate to the [DigitalOcean Autoscale Pools Web](https://cloud.digitalocean.com/droplets-autoscale) .
1. Click into the Droplet Autoscale Pool resource called `<STACK_NAME>-media-node-pool`, go to *"Settings"* and click on *"Edit"* in the **Autoscale Pool Configuration**. Edit Button Location Autoscale Pool
1. Drop down the **Number of Droplets** to 0, click *"Save"* and wait for it to apply the changes.
1. After confirming that all Media Node instances are terminated, in the *"Droplets"* tab select the droplet called `<STACK_NAME>-master-node-1`. Click on it to go to the Master Node 1 instance, then click *"Power"* and then *"Turn off"* the droplet. Turn Off Master Node 1
1. Repeat step 4 for all Master Nodes.

**Starting up the cluster**

To start the cluster, start the Master Nodes first and then the Media Nodes.

1. Navigate to the [DigitalOcean Droplet Web](https://cloud.digitalocean.com/droplets) .
1. Select the droplet named `<STACK_NAME>-master-node-1`, then go to *"Power"* and then *"Turn on"* the droplet. Turn on Master Node 1
1. Wait until the instance is running.
1. Repeat steps 2 and 3 until all Master Nodes are up and running.
1. Go back to the *"Autoscale Pools"* tab, then click the Droplet Autoscale Pool resource called `<STACK_NAME>-media-node-pool`, go to *"Settings"* and click on *"Edit"* in the **Autoscale Pool Configuration**. Edit Button Location Autoscale Pool
1. Change the number to the number of media nodes you want and click *"Save"*, then wait for the change to be applied.

## Change the instance size

It is possible to change the instance size of both the Master Node and the Media Nodes. However, since the Media Nodes are part of an Autoscale Pool, the process differs. The following section details the procedures:

**Master Nodes**

Warning

This procedure requires downtime, as it involves stopping the Master Node.

1. [Shutdown the cluster](#shutting-down-the-cluster).

   Info

   You can stop only the Master Node droplet to change its droplet size, but it is recommended to stop the whole cluster to avoid any issues.

1. Go to the [DigitalOcean Droplet Web](https://cloud.digitalocean.com/droplets) and locate the resource with the name `<STACK_NAME>-master-node-1` and click on it.

1. Click on *"Upsize"* and select the Droplet size you desire and click on *"Resize"*

   Change droplet size master 1

1. Repeat step 3 on every Master Node.

1. [Start the cluster](#starting-up-the-cluster).

**Media Nodes**

Warning

This will delete the media nodes without the graceful delete option. You can stop them gracefully by manually running the `/usr/local/bin/graceful_shutdown.sh` script and waiting for it to finish. You have to do it in all the media nodes because the autoscale pool will delete all media nodes and create new ones.

1. Navigate to the [DigitalOcean Autoscale Pools Web](https://cloud.digitalocean.com/droplets-autoscale) .
1. Click into the Droplet Autoscale Pool resource called `<STACK_NAME>-media-node-pool`, go to *"Settings"* and click on *"Edit"* in the **Droplet Configuration**. Edit Droplet Configuration Location Autoscale Pool
1. Scroll down to the **Choose a Droplet Plan** section and change the size to the one you prefer, then click on *"Edit Autoscale Pool"* and wait for the changes to apply. Edit Autoscale Pool

## Media Nodes Autoscaling Configuration

You can modify the autoscaling configuration of the Media Nodes via `terraform.tfvars` file and `terraform apply`:

**Media Nodes Autoscaling Configuration**

1. Go to the `terraform.tfvars` file and change the config related to autoscaling, such as:

   - **scaleTargetCPU**
   - **minNumberOfMediaNodes**
   - **maxNumberOfMediaNodes**

1. Open a terminal and write the following command once you've changed the value/s.

   ```text
   terraform apply
   ```

1. Say yes to the proposed change that Terraform is suggesting (the changes are the autoscale function redeploying with the new values), and your changes will be applied. Terraform output autoscale change

## Change Fixed Number of Media Nodes

You can change the fixed number of Media Nodes **in case you put a number of fixed Media Nodes** by following these steps:

**Change Fixed Number of Media Nodes**

1. Go to the [DigitalOcean Autoscale Pools Web](https://cloud.digitalocean.com/droplets-autoscale) .
1. Click into the Droplet Autoscale Pool resource called `<STACK_NAME>-media-node-pool`, go to *"Settings"* and click on *"Edit"* in the **Autoscale Pool Configuration**. Edit Button Location Autoscale Pool
1. Change the number to the desired value and click *"Save"*, then wait for the Autoscale Pool to apply the changes.

Warning

This will delete the media nodes if you have set them to less than the number of media nodes that existed. You can stop them gracefully by manually running the `/usr/local/bin/graceful_shutdown.sh` script and waiting for it to finish. You have to do it in all the media nodes because the autoscale pool deletes all and creates new ones.

### Activate Scale In when Fixed Number of Media Nodes

You can activate or deactivate the scale in when you decide you need autoscale option activated or not.

**Activate Scale In**

1. Go to the `terraform.tfvars` file and change the config related to autoscaling, such as:

   - **fixedNumberOfMediaNodes needs to be set to 0**.
   - **scaleTargetCPU** if you don't want the default.
   - **minNumberOfMediaNodes** if you don't want the default.
   - **maxNumberOfMediaNodes** if you don't want the default.

1. Open a terminal and write the following command once you've changed the value/s.

   ```text
   terraform apply
   ```

1. Say yes to the proposed change that Terraform is suggesting (the changes are destroying the fixed number of media nodes and deploying the scale-in function), and your changes will be applied. Terraform output autoscale change

**Deactivate Scale In**

1. Go to the `terraform.tfvars` file and change the config related to autoscaling, such as:

   - **fixedNumberOfMediaNodes needs to be set to your desired value**.

1. Open a terminal and write the following command once you've changed the value/s.

   ```text
   terraform apply
   ```

1. Say yes to the proposed change that Terraform is suggesting (the changes are destroying the scale-in function and all the media nodes and deploying the fixed number of media nodes pool), and your changes will be applied. Terraform output autoscale change

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises High Availability Administration](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

In addition to these, a DigitalOcean deployment provides the capability to manage global configurations by downloading `secrets.env` file of the bucket and changing it, then upload it again. Here are the detailed steps:

**Changing configuration through secrets.env**

1. Navigate to the [DigitalOcean Spaces Object Storage](https://cloud.digitalocean.com/spaces) and click on the cluster data bucket that you are using for the deployment.

1. Download the `secrets.env` file that is in the bucket. Secrets.env download

1. Open it and edit the credential values of your choice.

1. Upload the edited `secrets.env` to the bucket, select private file and replace it. Secrets.env upload

   Secrets.env replace

1. Restart Master Node 1 by shutting it down and then starting it again. Changes will be applied automatically in all the nodes of your OpenVidu High Availability deployment.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
