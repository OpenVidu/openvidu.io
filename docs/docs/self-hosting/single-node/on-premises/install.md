---
title: OpenVidu Single Node installation on-premises
description: Learn how to deploy OpenVidu Single Node on-premises
---

# <span class="openvidu-tag openvidu-community-tag" style="font-size: .5em">COMMUNITY</span> OpenVidu Single Node Installation: On-premises

This section contains the instructions to deploy a production-ready OpenVidu Meet <span class="openvidu-tag openvidu-community-tag" style="font-size: .5em">COMMUNITY</span> in a single node using Docker. 

## Requirements

Before starting the installation process, make sure you have the following prerequisites:

- Machine with **Linux installed (Ubuntu recommended)**.

### Hardware

The hardware requirements will depend on the number of users, size of the rooms, and rooms recordings.

Here are some scenarios to help you understand the minimum requirements for your deployment:

#### Scenario 1: Rooms without recording

- Hardware: **4GB RAM, 2 CPU cores and 30GB of disk**.
- Capacity: Up to 100 concurrent users in rooms with 8 users. The smallest the rooms, the more concurrent users you can handle.

#### Scenario 2: Rooms with recording

Recordings requires more CPU and disk space, so the requirements are higher. By default, every recording will consume 4 CPUs, so if you want to have multiple recordings at the same time, you will need to increase the number of CPUs in your machine. Each recording will consume around 500KB per second of video, so if you want to record a 1-hour meeting you will need around 1.8GB of disk space per recording.

- Hardware: **16GB RAM, 16 CPU cores and 200GB of disk**. 
- Capacity: This will allow you to have up to 4 recordings at the same time and will be able to store 100 hours of recordings.


### Network 

- **Public IP address** assigned to the machine.
- **Fully Qualified Domain Name (FQDN)** pointing to the public IP.
- **Opened ports**: 22 TCP (SSH), 80 TCP (HTTP), 443 TCP (HTTPS), 443 UDP (Media).
- **Free ports**: TODO (in a fresh ubuntu installation all these ports are free).

For better media quality and performance you can optionally open more ports: 

- **Additional ports**: 1935 TCP, 7881 TCP, 7885 UDP, 9000 TCP, 50000-60000 UDP., 

To allow the connection of users behind restrictive firewalls you can add an additional domain (pointing to the same public IP).


**Inbound port rules**:

| Protocol    | Ports          | <div style="width:8em">Source</div>          | Description                                                |
| ----------- | -------------- | --------------- | ---------------------------------------------------------- |
| TCP         | 80             | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
| TCP         | 443            | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu Dashboard.</li><li>OpenVidu Call (Default Application).</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
| UDP         | 443            | 0.0.0.0/0, ::/0 | STUN/TURN server over UDP. |
| TCP         | 1935           | 0.0.0.0/0, ::/0 | Needed if you want to ingest RTMP streams using Ingress service. |
| TCP         | 7881           | 0.0.0.0/0, ::/0 | Needed if you want to allow WebRTC over TCP. |
| UDP         | 7885           | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP protocol. |
| TCP         | 9000           | 0.0.0.0/0, ::/0 | Needed if you want to expose MinIO publicly. |
| UDP         | 50000 - 60000  | 0.0.0.0/0, ::/0 | WebRTC Media traffic. |

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Guided Installation

Execute the following command in the machine where you want to install OpenVidu Meet:

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install_openvidu_meet.sh)
```

--8<-- "shared/self-hosting/install-version.md"

A wizard will guide you through the installation process. You will be asked for the following information:

- **Domain name**: Domain name pointing to the public IP of your machine.
- **Additional Domain name (Optional)**: Another domain name pointing also to the same public IP.
- **Show credentials (Y)**: Whether to show the credentials at the end of the installation process.

When the installation process finishes, you will see the URLs and credentials to access OpenVidu Meet:

```
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
>                                                                             <
>  🎉 OpenVidu Meet Community Installation Finished Successfully! 🎉          <
>                                                                             <
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
>                                                                             <
>     * OpenVidu Meet 
         * URL: https://www.myserver.com                            <
>        * User: admin                                                        <
>        * password: xxxxxxx                                                  <
>                                                                             <
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
>                                                                             <
>  # Observability Services
>                      
>    * OpenVidu Dashboard: 
         * https://www.myserver.com/dashboard
>        * User: admin
>        * Password: xxxxxxx

>    * Grafana: 
         * https://www.myserver.com/grafana                          <
>        * User: admin
>        * Password: xxxxxxx
>
>
> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
```

Warning: Guide installation is the recommended way to install OpenVidu Single Node, but you can also install it in an advanced way configuring deployment options like certificate type, rtcengine (pion or mediasoup), service passwords, etc. Check the [Advanced installation](#advanced-installation) section for more information.

## Administration

### Starting, stopping, and restarting

--8<-- "shared/self-hosting/single-node/admin-start-stop.md"

### Configuration

Some configuration parameters can be changed in OpenVidu Meet using the config section in the web interface.

Other low level configuration parameters are defined in configuration files and can be changed only by modifying them directly and restarting OpenVidu Meet:

    1. Go to `/opt/openvidu/config` directory.
    2. Find and change the configuration parameter you want to modify, it could be any file: `openvidu.env`, `livekit.yaml`, `egress.yaml`, etc.
    3. Restart OpenVidu just by executing:

        ```
        systemctl restart openvidu
        ```

To know more about the configuration files, check the [OpenVidu Configuration In depth](./in-depth.md){:target="_blank"} section.

### Observability

You can check the health of OpenVidu Meet in the following ways:

- **OpenVidu Dashboard**: Web tool to see low level details of rooms, users, recodings, etc. (More info)
- **Grafana**: Web tool to see aggregated information (graphs) about rooms, users, recordings, etc. and service logs (More info)
- **Services health status**: Using docker tools (More info)
- **Services logs**: Using docker tools to access logs (More info)

You can see detailed information about these observability tools in the [OpenVidu Observability](./observability.md){:target="_blank"} section.

## OpenVidu Unistalling 

--8<-- "shared/self-hosting/single-node/admin-uninstall.md"

## Advanced installation

(Otra página)

Guided installation is the recommended way to install OpenVidu Single Node, but you can also install it in an advanced way configuring deployment options like certificate type, rtcengine (pion or mediasoup), service passwords, etc. 

=== "Let's Encrypt certificates"

    Example using Let's Encrypt certificates:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
        --no-tty --install \
        --domain-name='openvidu.example.io' \
        --enabled-modules='observability,app' \
        --turn-domain-name='turn.example.io' \
        --livekit-api-key='xxxxx' \
        --livekit-api-secret='xxxxx' \
        --dashboard-admin-user='xxxxx' \
        --dashboard-admin-password='xxxxx' \
        --redis-password='xxxxx' \
        --minio-access-key='xxxxx' \
        --minio-secret-key='xxxxx' \
        --mongo-admin-user='xxxxx' \
        --mongo-admin-password='xxxxx' \
        --mongo-replica-set-key='xxxxx' \
        --grafana-admin-user='xxxxx' \
        --grafana-admin-password='xxxxx' \
        --default-app-user='xxxxx' \
        --default-app-password='xxxxx' \
        --default-app-admin-user='xxxxx' \
        --default-app-admin-password='xxxxx' \
        --certificate-type='letsencrypt' \
        --letsencrypt-email='example@example.io'
    ```

    --8<-- "shared/self-hosting/install-version.md"

=== "Self-signed certificates"

    Example using self-signed certificates:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
        --no-tty --install \
        --domain-name='openvidu.example.io' \
        --enabled-modules='observability,app' \
        --turn-domain-name='turn.example.io' \
        --livekit-api-key='xxxxx' \
        --livekit-api-secret='xxxxx' \
        --dashboard-admin-user='xxxxx' \
        --dashboard-admin-password='xxxxx' \
        --redis-password='xxxxx' \
        --minio-access-key='xxxxx' \
        --minio-secret-key='xxxxx' \
        --mongo-admin-user='xxxxx' \
        --mongo-admin-password='xxxxx' \
        --mongo-replica-set-key='xxxxx' \
        --grafana-admin-user='xxxxx' \
        --grafana-admin-password='xxxxx' \
        --default-app-user='xxxxx' \
        --default-app-password='xxxxx' \
        --default-app-admin-user='xxxxx' \
        --default-app-admin-password='xxxxx' \
        --certificate-type='selfsigned' \
        --letsencrypt-email='example@example.io'
    ```

    --8<-- "shared/self-hosting/install-version.md"

=== "Custom certificates"

    Example using custom certificates:

    ```bash
    CERT_PRIVATE_KEY=$(cat privkey.pem | base64 -w 0)
    CERT_PUBLIC_KEY=$(cat fullchain.pem | base64 -w 0)

    # Optional, only if you want to enable TURN with TLS
    CERT_TURN_PRIVATE_KEY=$(cat turn-privkey.pem | base64 -w 0)
    CERT_TURN_PUBLIC_KEY=$(cat turn-fullchain.pem | base64 -w 0)

    sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
        --no-tty --install \
        --domain-name='openvidu.example.io' \
        --enabled-modules='observability,app' \
        --turn-domain-name='turn.example.io' \
        --livekit-api-key='xxxxx' \
        --livekit-api-secret='xxxxx' \
        --dashboard-admin-user='xxxxx' \
        --dashboard-admin-password='xxxxx' \
        --redis-password='xxxxx' \
        --minio-access-key='xxxxx' \
        --minio-secret-key='xxxxx' \
        --mongo-admin-user='xxxxx' \
        --mongo-admin-password='xxxxx' \
        --mongo-replica-set-key='xxxxx' \
        --grafana-admin-user='xxxxx' \
        --grafana-admin-password='xxxxx' \
        --default-app-user='xxxxx' \
        --default-app-password='xxxxx' \
        --default-app-admin-user='xxxxx' \
        --default-app-admin-password='xxxxx' \
        --certificate-type='owncert' \
        --owncert-private-key="$CERT_PRIVATE_KEY" \
        --owncert-public-key="$CERT_PUBLIC_KEY" \
        --turn-owncert-private-key="$CERT_TURN_PRIVATE_KEY" \
        --turn-owncert-public-key="$CERT_TURN_PUBLIC_KEY"
    ```

    --8<-- "shared/self-hosting/install-version.md"

    - Note that you just need to pass `--owncert-private-key` and `--owncert-public-key` with the content of the private and public key files in base64 format. The installation script will decode them and save them in the proper files.
    - `--turn-owncert-private-key` and `--turn-owncert-public-key` are optional. You only need to pass them if you want to enable TURN with TLS.

You can run that command in a CI/CD pipeline or in a script to automate the installation process.

Some notes about the command:

- The argument `--turn-domain-name` is optional. You define it only if you want to enable TURN with TLS in case users are behind restrictive firewalls.
- In the argument `--enabled-modules`, you can enable the modules you want to deploy. You can enable `observability` (Grafana stack) and `app` (Default App - OpenVidu Call).
- If no media appears in your conference, reinstall specifying the `--public-ip` parameter with your machine's public IP. OpenVidu usually auto-detects the public IP, but it can fail. This IP is used by clients to send and receive media.
