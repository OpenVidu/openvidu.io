---
title: Try OpenVidu Meet Locally
description: Deploy OpenVidu Meet on your local machine for development and testing purposes using Docker Desktop.
---
# Try OpenVidu Meet Locally

You can easily deploy **OpenVidu Meet** on your local machine to start developing or exploring its features right away.

This simplified local deployment is intended for **development and testing purposes only**. It enables you to launch **OpenVidu Meet** with a single command using **Docker**.

## Prerequisites

- A computer with **Windows**, **macOS**, or **Linux** installed.
- 4 CPU cores and 8 GB of RAM (16 GB recommended for better performance).
- At least 50 GB of free disk space. (OpenVidu only takes around 5.2 GB, but additional space may be needed for Docker Desktop.)

- Docker Desktop installed (see instructions below).
- Estimated download time: ~3–5 minutes on a 100 Mbps connection.

## Installing Docker Desktop

Docker is a popular platform for running containers, which are portable packages that include everything needed to run an application.

OpenVidu Meet uses containers to simplify the deployment. Docker Desktop provides an easy interface for managing containers and is available for **Windows**, **macOS**, and **Linux** which makes it a great choice for local development.

=== ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

    - Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/){:target="\_blank"}

=== ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

    - Install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/){:target="\_blank"}

=== ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

    - Install [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/){:target="\_blank"}

    Alternatively, you can install **Docker Engine** and **Docker Compose** instead of Docker Desktop:

    - Install [Docker](https://docs.docker.com/engine/install/#supported-platforms){:target="\_blank"}
    - Install [Docker Compose](https://docs.docker.com/compose/install/linux/){:target="\_blank"}

## Running OpenVidu Meet Locally

1. Open **Docker Desktop** and click on the **"Terminal"** button at the bottom right corner.

    ![Docker Desktop - Open Terminal](../../assets/images/meet/deployment/local-meet/open_terminal.png)

2. Copy and paste the following command into the terminal, depending on whether you want to deploy the **Community** or **Pro** edition:

    === "OpenVidu <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span>"

        Execute this command for the **Community Edition**:

        ```bash
        docker compose -p openvidu-meet -f oci://openvidu/local-meet:latest up -y openvidu-meet-init
        ```

        If you want to deploy a specific version, replace `latest` with the desired version tag (e.g., `3.4.0`).

        ![Docker Desktop - Run Command Community](../../assets/images/meet/deployment/local-meet/command_community.png)

    === "OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>"

        Execute this command for the **Pro Edition**:

        ```bash
        docker compose -p openvidu-meet-pro -f oci://openvidu/local-meet-pro:latest up -y openvidu-meet-init
        ```

        If you want to deploy a specific version, replace `latest` with the desired version tag (e.g., `3.4.0`).

        ![Docker Desktop - Run Command Community](../../assets/images/meet/deployment/local-meet/command_pro.png)

3. After pasting the command, press **Enter** to execute it.

This will start the deployment process, which may take a few minutes as it downloads the necessary Docker images and sets up the services.

The terminal will display logs showing the progress and show this message when it’s ready:

```
openvidu-meet-init-1  | Waiting for OpenVidu to start...
...
openvidu-meet-init-1  | Starting OpenVidu... Please be patient...
...
openvidu-meet-init-1  |
openvidu-meet-init-1  | ====================================================
openvidu-meet-init-1  | 🎉 OpenVidu Meet main is ready! 🎉
openvidu-meet-init-1  | ====================================================
openvidu-meet-init-1  |
openvidu-meet-init-1  | This version is only for local development purposes.
openvidu-meet-init-1  | DO NOT USE IT IN PRODUCTION!
openvidu-meet-init-1  |
openvidu-meet-init-1  | ------------------OpenVidu Meet---------------------
openvidu-meet-init-1  | > NOTE: Below are the default initial login credentials
openvidu-meet-init-1  | > for OpenVidu Meet. If you update them after deployment,
openvidu-meet-init-1  | > this message will not reflect those changes.
openvidu-meet-init-1  | ----------------------------------------------------
openvidu-meet-init-1  | 	- Access from this machine:
openvidu-meet-init-1  | 		- http://localhost:9080
openvidu-meet-init-1  | 	- Credentials:
openvidu-meet-init-1  | 		- Username: admin
openvidu-meet-init-1  | 		- Password: admin
openvidu-meet-init-1  | 		- API Key: meet-api-key
openvidu-meet-init-1  | ----------------------------------------------------
```

Now, you can access **OpenVidu Meet** by opening your web browser and navigating to [http://localhost:9080](http://localhost:9080) with the credentials provided in the logs.

=== "Access and Credentials"
    As this is a deployment for local development, these are the default credentials.

    - URL: [http://localhost:9080](http://localhost:9080)
        - Username: `admin`
        - Password: `admin`
        - API Key: `meet-api-key`

    You can change them later from the [OpenVidu Meet Users And Permissions](../../features/users-and-permissions/#modify-openvidu-meet-authentication).

Once installed, you will have a Container Group named **`openvidu-meet`** or **`openvidu-meet-pro`**. You can check it in **Docker Desktop → Containers**.

![Docker Desktop - Containers](../../assets/images/meet/deployment/local-meet/containers.png)

## Managing the deployment

You can manage the deployment directly from the **Docker Desktop interface**:

=== "Start"

    1. Go to **Docker Desktop → Containers** and find the container group named **`openvidu-meet`** or **`openvidu-meet-pro`** depending on the edition you deployed.
    3. Click the **Start** button to start the container group.

    ![Docker Desktop - Start Container](../../assets/images/meet/deployment/local-meet/start.png)

=== "Stop"

    1. Go to **Docker Desktop → Containers** and find the container group named **`openvidu-meet`** or **`openvidu-meet-pro`** depending on the edition you deployed.
    3. Click the **Stop** button to stop the container group.

    ![Docker Desktop - Stop Container](../../assets/images/meet/deployment/local-meet/stop.png)

=== "Review Logs"

    1. Go to **Docker Desktop → Containers** and find the container group named **`openvidu-meet`** or **`openvidu-meet-pro`** depending on the edition you deployed.
    2. Click on the container group to open its details. The logs will be shown after clicking on the container group.

    <div class="grid cards no-border no-shadow" markdown>

    - ![Select container group](../../assets/images/meet/deployment/local-meet/select_containers.png)
    - ![Check logs](../../assets/images/meet/deployment/local-meet/logs.png)

    </div>

=== "Remove"

    If you want to completely remove the deployment and all its data:

    1. Go to **Docker Desktop → Containers** and find the container group named **`openvidu-meet`** or **`openvidu-meet-pro`** depending on the edition you deployed.
    2. Click the **Delete** button to remove the container group.

        ![Docker Desktop - Remove Container](../../assets/images/meet/deployment/local-meet/remove.png)

    3. Go to **Docker Desktop → Images**.
    4. Remove the images related to **OpenVidu Meet**.

        ![Docker Desktop - Remove Images](../../assets/images/meet/deployment/local-meet/remove_images.png)

    5. Go to **Docker Desktop → Volumes**.
    6. Remove the volumes related to **OpenVidu Meet**.

        ![Docker Desktop - Remove Volumes](../../assets/images/meet/deployment/local-meet/remove_volumes.png)

## Testing from Other Devices (LAN Access)

To test OpenVidu Meet from other devices (e.g., smartphones or tablets) within your local network, you need to start the deployment setting up the `LAN_PRIVATE_IP` environment variable with your machine's private IP address.


=== "OpenVidu <span class="openvidu-tag openvidu-community-tag">COMMUNITY</span>"

    1. Find your private IP address (e.g., `192.168.1.100`).
    2. Set the environment variable `LAN_PRIVATE_IP` to your IP and run the local deployment command.

    === ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

        PowerShell command:

        ```powershell
        $env:LAN_PRIVATE_IP='<YOUR_PRIVATE_IP>'
        docker compose -p openvidu-meet -f oci://openvidu/local-meet:latest up -y openvidu-meet-init
        ```

    === ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

        Bash command:

        ```bash
        LAN_PRIVATE_IP='<YOUR_PRIVATE_IP>'
        docker compose -p openvidu-meet -f oci://openvidu/local-meet:latest up -y openvidu-meet-init
        ```

    === ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

        Bash command:

        ```bash
        LAN_PRIVATE_IP='<YOUR_PRIVATE_IP>'
        docker compose -p openvidu-meet -f oci://openvidu/local-meet:latest up -y openvidu-meet-init
        ```


=== "OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>"

    1. Find your private IP address (e.g., `192.168.1.100`).
    2. Set the environment variable `LAN_PRIVATE_IP` to your IP and run the local deployment command.

    === ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

        PowerShell command:

        ```powershell
        $env:LAN_PRIVATE_IP='<YOUR_PRIVATE_IP>'
        docker compose -p openvidu-meet-pro -f oci://openvidu/local-meet-pro:latest up -y openvidu-meet-init
        ```

    === ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

        Bash command:

        ```bash
        LAN_PRIVATE_IP='<YOUR_PRIVATE_IP>'
        docker compose -p openvidu-meet-pro -f oci://openvidu/local-meet-pro:latest up -y openvidu-meet-init
        ```

    === ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

        Bash command:

        ```bash
        LAN_PRIVATE_IP='<YOUR_PRIVATE_IP>'
        docker compose -p openvidu-meet-pro -f oci://openvidu/local-meet-pro:latest up -y openvidu-meet-init
        ```

For example, if your private IP is `192.168.1.100` you can access the OpenVidu Meet local deployment at
 `https://192-168-1-100.openvidu-local.dev:9443`{.no-break} from other devices in your local network.

!!! info
    The deployment includes a special certificate for the `*.openvidu-local.dev`{.no-break} which simplifies WebRTC development in LAN networks, but this certificate should not be used in production environments. For more information check [About openvidu-local.dev domain and SSL certificates](../../../docs/self-hosting/local/#about-openvidu-localdev-domain-and-ssl-certificates).

## Advanced Local Deployment

If you want to modify some configurations or to have more control over the local deployment, you can deploy the [OpenVidu Platform Local deployment](../../docs/self-hosting/local.md) which includes **OpenVidu Meet** as one of its services.