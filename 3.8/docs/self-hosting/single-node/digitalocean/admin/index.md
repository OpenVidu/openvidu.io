# OpenVidu Single Node administration: DigitalOcean

DigitalOcean

DigitalOcean OpenVidu Single Node deployments are internally identical to On Premises Single Node deployments, so you can follow the same instructions from [On Premises Single Node](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md) documentation for administration and configuration. The only difference is that the deployment is automated with Terraform.

However, there are certain things worth mentioning:

## Start and stop OpenVidu through DigitalOcean web

You can start and stop all services as explained in the [On Premises Single Node](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/#starting-stopping-and-restarting-openvidu) section. But you can also start and stop the Droplet directly from DigitalOcean web. This will stop all services running in the droplet and reduce DigitalOcean costs.

**Stop OpenVidu Single Node**

1. Go to [DigitalOcean Droplets](https://cloud.digitalocean.com/droplets) .
1. There, you will find the Droplet that runs OpenVidu. Its name should be something like `<STACK_NAME>-vm-ce` (COMMUNITY) or `<STACK_NAME>-vm-ce-pro` (PRO).
1. In the Droplet section, click *"Power"* and then *"Turn Off"* to stop the Droplet (and therefore OpenVidu).

**OpenVidu COMMUNITY**

Stop droplet

**OpenVidu PRO**

Stop droplet

**Start OpenVidu Single Node**

1. Go to [DigitalOcean Droplets](https://cloud.digitalocean.com/droplets) .
1. There, you will find the Droplet that runs OpenVidu. Its name should be something like `<STACK_NAME>-vm-ce` (COMMUNITY) or `<STACK_NAME>-vm-ce-pro` (PRO).
1. In the Droplet section, click *"Power"* and then *"Turn On"* to start the Droplet (and therefore OpenVidu).

**OpenVidu COMMUNITY**

Start droplet

**OpenVidu PRO**

Start droplet

## Change the droplet size

You can change the droplet size of the OpenVidu Single Node to adapt it to your needs. To do this, follow these steps:

1. Go to [DigitalOcean Droplets](https://cloud.digitalocean.com/droplets) .

1. There, you will find the Droplet that runs OpenVidu. Its name should be something like `<STACK_NAME>-vm-ce` (COMMUNITY) or `<STACK_NAME>-vm-ce-pro` (PRO).

1. [Stop](#stop-openvidu-single-node) the droplet if it is not stopped.

1. Click on *"Upsize Droplet"* and change the size, then click on *"Resize"*.

   **OpenVidu COMMUNITY**

   Change droplet size

   **OpenVidu PRO**

   Change droplet size

## Administration and configuration

Regarding the administration of your deployment, you can follow the instructions in section [On Premises Single Node Administration](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/admin/index.md).

Regarding the configuration of your deployment, you can follow the instructions in section [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md). Additionally, the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) offer multiple resources to assist with specific configuration changes.

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
