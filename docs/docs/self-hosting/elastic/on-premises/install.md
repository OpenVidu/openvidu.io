# OpenVidu Elastic Installation: On-premises

!!!info
    OpenVidu Elastic is part of **OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account){:target="_blank"} to get your license key.
    There's a 15-day free trial waiting for you!

This section contains the instructions to deploy a production-ready OpenVidu Elastic deployment on-premises. The deployment requires one Master Node and any number of Media Nodes. Media Nodes are elastic and can be scaled up and down according to the workload.

=== "Architecture overview"

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu Elastic On Premises](../../../../assets/images/self-hosting/elastic/on-premises/elastic-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Elastic On Premises</figcaption>
    </figure>

    - The Master Node acts as a Load Balancer, managing the traffic and distributing it among the Media Nodes and deployed services in the Master Node.
    - The Master Node has its own Caddy server acting as a Layer 4 (For TURN with TLS and RTMPS) and Layer 7 (For OpenVidu Dashboard, OpenVidu Call, etc., APIs) reverse proxy.
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.

For the Master Node, the following services are configured:

- **OpenVidu Dashboard**, a web application interface to visualize your Rooms, Ingress, and Egress services.
- **MinIO** as an S3 storage service for recordings.
- **Redis** as a shared database for OpenVidu Server PRO and Ingress/Egress services.
- **MongoDB** as a database for storing analytics and monitoring data.
- **Caddy** as a reverse proxy. It can be deployed with self-signed certificates, Let's Encrypt certificates, or custom certificates. Provides optional TLS for the TURN server.
- **OpenVidu V2 Compatibility (v2compatibility module)** is an optional service that provides an API designed to maintain compatibility for applications developed with OpenVidu version 2.
- **OpenVidu Call (Default Application module)**, an optional ready-to-use videoconferencing application.
- **Grafana, Mimir, Promtail, and Loki (Observability module)** form an optional observability stack for monitoring, allowing you to keep track of logs and deployment statistics for OpenVidu.

For the Media Nodes, the following services are configured:

- **OpenVidu Server PRO (LiveKit compatible).**
- **Ingress** and **Egress** services.
- **Prometheus and Loki (Observability module)**. Used to send metrics and logs to the observability stack.

## Prerequisites

- **At least 2 machines**, each with a minimum of **4GB RAM**, **4 CPU cores**, and **Linux** installed (Ubuntu is recommended). One machine will serve as the Master Node, while the others will function as Media Nodes.
- Significant disk space on the **Master Node, with 100GB recommended**, especially if you plan to record your sessions (Egress). Media Nodes require less space; however, account for the space needed for ongoing recordings on these nodes.
- **Each machine must be assigned a Public IP**. Additionally, the machine designated as the Master Node must have a **Fully Qualified Domain Name (FQDN)** that resolves to its Public IP.

## Port rules (Master Node)

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your Master Node.

**Inbound port rules**:

| Protocol    | Ports          | <div style="width:8em">Source</div> | Description                                                |
| ----------- | -------------- | --------------- | ---------------------------------------------------------- |
| TCP         | 80             | 0.0.0.0/0, ::/0 | Redirect HTTP traffic to HTTPS and Let's Encrypt validation. |
| TCP         | 443            | 0.0.0.0/0, ::/0 | Allows access to the following: <ul><li>Livekit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Call (Default Application).</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
| TCP         | 1935           | 0.0.0.0/0, ::/0 | (Optional), only needed if you want to ingest RTMP streams using Ingress service. |
| TCP         | 9000           | 0.0.0.0/0, ::/0 | (Optional), only needed if you want to expose MinIO publicly. |
| TCP         | 4443           | Media Nodes     | (Optional. Only needed when _'OpenVidu v2 Compatibility'_ module is used) Media Nodes need access to this port to reach OpenVidu V2 compatibility service |
| TCP         | 6080           | Media Nodes     | (Optional. Only needed when _'Default App'_ module is used) Media Nodes need access to this port to reach OpenVidu Call (Default Application). |
| TCP         | 3100           | Media Nodes     | (Optional. Only needed when _'Observability'_ module is used) Media Nodes need access to this port to reach Loki. |
| TCP         | 9009           | Media Nodes     | (Optional. Only needed when _'Observability'_ module is used) Media Nodes need access to this port to reach Mimir. |
| TCP         | 7000           | Media Nodes     | Media Nodes need access to this port to reach Redis Service. |
| TCP         | 9100           | Media Nodes     | Media Nodes need access to this port to reach MinIO. |
| TCP         | 20000          | Media Nodes     | Media Nodes need access to this port to reach MongoDB. |

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Port rules (Media Nodes)

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your Media Nodes:

**Inbound port rules**:

| Protocol    | <div style="width:8em">Ports</div>          | <div style="width:8em">Source</div> | Description                                                |
| ----------- | -------------- | --------------- | ---------------------------------------------------------- |
| UDP         | 443            | 0.0.0.0/0, ::/0   | STUN/TURN over UDP. |
| TCP         | 7881           | 0.0.0.0/0, ::/0   | (Optional). Only needed if you want to allow WebRTC over TCP. |
| UDP         | 7885           | 0.0.0.0/0, ::/0   | (Optional). Only needed if you want to ingest WebRTC using WHIP. |
| UDP         | 50000-60000    | 0.0.0.0/0, ::/0   | WebRTC Media traffic. |
| TCP         | 1935           | Master Node     | (Optional). Only needed if you want to ingest RTMP streams using Ingress service. Master Node needs access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
| TCP         | 5349           | Master Node     | (Optional). Only needed if you want to expose TURN service with TLS. Master Node needs access to this port to reach TURN service and expose it using TLS (TURNS). |
| TCP         | 7880           | Master Node     | LiveKit API. Master Node needs access to load balance LiveKit API and expose it through HTTPS. |
| TCP         | 8080           | Master Node     | (Optional). Only needed if you want to ingest WebRTC streams using WHIP. Master Node needs access to this port to reach WHIP HTTP service. |

## Guided Installation

Before the installation, ensure that all your machines meet the [prerequisites](#prerequisites) and the port rules for the [Master Node](#port-rules-master-node) and [Media Nodes](#port-rules-media-nodes) are correctly configured.

To install OpenVidu Elastic, **begin by generating the commands required for setting up all nodes in the cluster**. This is a simple and straightforward process; simply **run the following command on any machine that has Docker installed**:

```bash
docker run -it openvidu/openvidu-installer:latest \
    --deployment-type=elastic
```

--8<-- "docs/docs/self-hosting/shared/install-version.md"

A wizard will guide you through the installation process. You will be asked for the following information:

- **Write the 'Master Node' Private IP**: Write the private IP of the machine where you are going to install the Master Node.
- **Write your OpenVidu PRO License**: Write your OpenVidu PRO License.
!!!info
    If you don't have a license key for OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>, you can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target="_blank"}.
- **Select which certificate type to use**:
    - _Self Signed Certificate_: It will generate a self-signed certificate. It is not recommended for production environments, but it is useful for testing or development purposes.
    - _Let's Encrypt_: It will automatically generate a certificate for your domain. The Let's Encrypt email is required and will be asked later in the wizard.
    - _ZeroSSL_: It will automatically generate a certificate for your domain using ZeroSSL. An API Key is required and will be asked later in the wizard.
    - _Own Certificate_: It will ask you for the certificate and key files. Just copy and paste the content of the files when the wizard asks for them.
- **Domain name**: The domain name for your deployment. It must be an FQDN pointing to the machine where you are deploying OpenVidu.
- **(Optional) Turn domain name**: The domain name for your TURN server with TLS. It must be an FQDN pointing to the machine where you are deploying OpenVidu and must be different from the OpenVidu domain name. Recommended if users who are going to connect to your OpenVidu deployment are behind restrictive firewalls.
- **Select which RTC engine to use**: Select the WebRTC engine you want to use. You can choose between **Pion (The engine used by Livekit)** or **Mediasoup(Experimental)**.

    --8<-- "docs/docs/self-hosting/shared/mediasoup-warning.md"

- **Modules to enable**: Select the modules you want to enable. You can enable the following modules:
    - _Observability_: Grafana stack, which includes logs and monitoring stats.
    - _Default App_: OpenVidu Call, a ready-to-use videoconferencing application.
    - _OpenVidu V2 Compatibility_: Compatibility API for applications developed with OpenVidu v2.

The rest of the parameters are secrets, usernames, and passwords. If empty, the wizard will generate random values for them.

This command will output the following instructions, which you should follow:

1. **Firewall Configuration for 'Master Node'**: These rules are the same as those specified in the instructions. Depending on the modules you have selected, some rules defined at [Port rules (Master Node)](#port-rules-master-node) may not appear (Optional ports). Double-check and modify it if you see something that can be enabled/disabled in your current port rules.
2. **Installation Commands for 'Master Node'**: This is the command needed to install your Master Node. It should look like this:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
        --no-tty --install \
        --deployment-type='elastic' \
        --node-role='master-node' \
    ...
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    Execute that command in your Master Node to install it. When the installation process finishes, you will see the following output:

    ```
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    >                                                                             <
    >  🎉 OpenVidu Elastic 'Master Node' Installation Finished Successfully! 🎉   <
    >                                                                             <
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    ```

    The Master Node will be installed at `/opt/openvidu` and configured as a systemd service. You can start the service with the following command:

    ```bash
    systemctl start openvidu
    ```

3. **Firewall Configuration for 'Media Nodes'**: These rules are the same as those defined previously as with the Master Node. Double-check the [Port rules (Media Nodes)](#port-rules-media-nodes) and modify them if you see something that can be enabled/disabled in your current port rules.

4. **Installation Commands for 'Media Nodes'**: This is the command needed to install your Media Nodes. It should look like this:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_media_node.sh) \
        --no-tty --install \
        --deployment-type='elastic' \
        --node-role='media-node' \
    ...
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    Execute that command on your Media Nodes to install them. When the installation process finishes, you will see the following output:

    ```
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    >                                                                             <
    >  🎉 OpenVidu Elastic 'Media Node' Installation Finished Successfully! 🎉    <
    >                                                                             <
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    ```

    The Media Node in each machine will be installed at `/opt/openvidu` and configured as a systemd service. You can start the service with the following command:

    ```
    systemctl start openvidu
    ```

If everything goes well, all containers will be up and running without restarts, and you will be able to access any of the following services:

- OpenVidu Call (Default Application): [https://openvidu.example.io/](https://openvidu.example.io/){:target="_blank"}
- OpenVidu Dashboard: [https://openvidu.example.io/dashboard](https://openvidu.example.io/dashboard/){:target="_blank"}
- MinIO: [https://openvidu.example.io/minio-console](https://openvidu.example.io/minio-console/){:target="_blank"}
- Grafana: [https://openvidu.example.io/grafana](https://openvidu.example.io/grafana/){:target="_blank"}

OpenVidu Server PRO URL (LiveKit compatible) will be available also in:

- OpenVidu Server PRO: [https://openvidu.example.io/](https://openvidu.example.io/){:target="_blank"}
- LiveKit API: [https://openvidu.example.io/](https://openvidu.example.io/){:target="_blank"} and [wss://openvidu.example.io/](wss://openvidu.example.io/){:target="_blank"}

## Deployment Credentials

To point your applications to your OpenVidu deployment, check the file at `/opt/openvidu/.env`. All access credentials for all services are defined in this file.

Your authentication credentials and URL to point your applications would be:

- Applications developed with LiveKit SDK:
    - **URL**: The value in `.env` of `DOMAIN_OR_PUBLIC_IP` as a URL. It could be `wss://openvidu.example.io/` or `https://openvidu.example.io/` depending on the SDK you are using.
    - **API Key**: The value in `.env` of `LIVEKIT_API_KEY`
    - **API Secret**: The value in `.env` of `LIVEKIT_API_SECRET`

- Applications developed with OpenVidu v2:
    - **URL**: The value in `.env` of `DOMAIN_OR_PUBLIC_IP` as a URL. For example, `https://openvidu.example.io/`
    - **Username**: `OPENVIDUAPP`
    - **Password**: The value in `.env` of `LIVEKIT_API_SECRET`

## Non-interactive installation

To automate the installation process, you just need to execute the specified command in the [Guided Installation](#guided-installation) section and execute the generated commands.

Each installation command for each type of node looks like this:

=== "Master Node"

    The Master Node can be configured with multiple kinds of certificates. Here are the examples for each type of certificate:

    === "Let's Encrypt certificates"

        Example using Let's Encrypt certificates:

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
            --node-role='master-node' \
            --openvidu-pro-license='xxxxx' \
            --domain-name-or-ip='openvidu.example.io' \
            --enabled-modules='observability,v2compatibility,app' \
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
            --grafana-admin-user='xxxxx' \
            --grafana-admin-password='xxxxx' \
            --default-app-user='xxxxx' \
            --default-app-password='xxxxx' \
            --default-app-admin-user='xxxxx' \
            --default-app-admin-password='xxxxx' \
            --private-ip='1.2.3.4' \
            --certificate-type='letsencrypt' \
            --letsencrypt-email='example@example.io'
        ```

        --8<-- "docs/docs/self-hosting/shared/install-version.md"

        Notes:

        - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target="_blank"}.
        - `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

    === "Self-signed certificates"

        Example using self-signed certificates:

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
            --node-role='master-node' \
            --openvidu-pro-license='xxxxx' \
            --domain-name-or-ip='openvidu.example.io' \
            --enabled-modules='observability,v2compatibility,app' \
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
            --grafana-admin-user='xxxxx' \
            --grafana-admin-password='xxxxx' \
            --default-app-user='xxxxx' \
            --default-app-password='xxxxx' \
            --default-app-admin-user='xxxxx' \
            --default-app-admin-password='xxxxx' \
            --private-ip='1.2.3.4' \
            --certificate-type='selfsigned'
        ```

        --8<-- "docs/docs/self-hosting/shared/install-version.md"

        - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target="_blank"}.
        - `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.

    === "Custom certificates"

        Example using custom certificates:

        ```bash
        CERT_PRIVATE_KEY=$(cat privkey.pem | base64 -w 0)
        CERT_PUBLIC_KEY=$(cat fullchain.pem | base64 -w 0)

        # Optional, only if you want to enable TURN with TLS
        CERT_TURN_PRIVATE_KEY=$(cat turn-privkey.pem | base64 -w 0)
        CERT_TURN_PUBLIC_KEY=$(cat turn-fullchain.pem | base64 -w 0)

        sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
            --node-role='master-node' \
            --openvidu-pro-license='xxxxx' \
            --domain-name-or-ip='openvidu.example.io' \
            --enabled-modules='observability,v2compatibility,app' \
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
            --grafana-admin-user='xxxxx' \
            --grafana-admin-password='xxxxx' \
            --default-app-user='xxxxx' \
            --default-app-password='xxxxx' \
            --default-app-admin-user='xxxxx' \
            --default-app-admin-password='xxxxx' \
            --private-ip='1.2.3.4' \
            --certificate-type='owncert' \
            --owncert-private-key="$CERT_PRIVATE_KEY" \
            --owncert-public-key="$CERT_PUBLIC_KEY" \
            --turn-owncert-private-key="$CERT_TURN_PRIVATE_KEY" \
            --turn-owncert-public-key="$CERT_TURN_PUBLIC_KEY"
        ```

        --8<-- "docs/docs/self-hosting/shared/install-version.md"

        - Note that you just need to pass `--owncert-private-key` and `--owncert-public-key` with the content of the private and public key files in base64 format. The installation script will decode them and save them in the proper files.
        - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target="_blank"}.
        - `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP.
        - `--turn-owncert-private-key` and `--turn-owncert-public-key` are optional. You only need to pass them if you want to enable TURN with TLS.

=== "Media Node"

    To install a Media Node, you can use the following command:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_media_node.sh) \
        --node-role='media-node' \
        --openvidu-pro-license='xxxxx' \
        --domain-name-or-ip='openvidu.example.io' \
        --rtc-engine='pion' \
        --enabled-modules='observability,v2compatibility,app' \
        --turn-domain-name='turn.example.io' \
        --livekit-api-key='xxxxx' \
        --livekit-api-secret='xxxxx' \
        --master-node-private-ip='1.2.3.4' \
        --redis-password='xxxxx' \
        --minio-access-key='xxxxx' \
        --minio-secret-key='xxxxx' \
        --mongo-admin-user='xxxxx' \
        --mongo-admin-password='xxxxx'
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    - Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
    - The `--master-node-private-ip` is the private IP of the Master Node. Media Nodes should be able to reach the Master Node using this IP.
    - If no media appears in your conference, reinstall specifying the `--public-ip` parameter with your machine's public IP. OpenVidu usually auto-detects the public IP, but it can fail. This IP is used by clients to send and receive media.

You can run these commands in a CI/CD pipeline or in a script to automate the installation process.

Some notes about all commands:

- The argument `--turn-domain-name` is optional. You define it only if you want to enable TURN with TLS in case users are behind restrictive firewalls.
- At the argument `--enabled-modules`, you can enable the modules you want to deploy. You can enable `observability` (Grafana stack), `app` (Default App - OpenVidu Call), and `v2compatibility` (OpenVidu v2 compatibility API).

To start each node, remember to execute the following command in each node:

```bash
systemctl start openvidu
```

## Configuration and administration

Once you have OpenVidu deployed, you can check the [Configuration and Administration](../on-premises/admin.md) section to learn how to manage your OpenVidu Elastic deployment.
