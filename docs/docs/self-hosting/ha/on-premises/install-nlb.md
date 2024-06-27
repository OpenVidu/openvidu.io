# OpenVidu High Availability Installation: On-premises with Network Load Balancer

!!!info
    OpenVidu High Availability is part of **OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>**. Before deploying, you need to [create an OpenVidu account](https://openvidu.io/account){:target=_blank} to get your license key.
    There's a 15-day free trial waiting for you!

This section provides instructions for deploying a production-ready OpenVidu High Availability setup on-premises, utilizing a Network Load Balancer in front of the cluster. Network Load Balancing is a method of distributing incoming network traffic across multiple servers. It is a highly available, scalable, and fault-tolerant solution that ensures your OpenVidu deployment is always up and running. Compared to DNS Load Balancing, Network Load Balancing is more reliable for health checks and ensures that traffic is evenly distributed across all nodes.

**Advantages of Network Load Balancing:**

- **More control** over the load balancing process.
- **Possibility to use custom health checks** to determine the status of the nodes.

**Disadvantages of Network Load Balancing:**

- **More complex to set up** than DNS Load Balancing.
- **Requires a Load Balancer** to be deployed in front of the cluster.
- **More expensive** than DNS Load Balancing.

=== "Architecture overview"

    This is how the architecture of the deployment looks:

    <figure markdown>
    ![OpenVidu High Availability Architecture with Network Load Balancer](../../../../assets/images/self-hosting/ha/on-premises/ha-nlb-architecture.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu High Availability Architecture with Network Load Balancer</figcaption>
    </figure>

    - The Load Balancer must be a Network Load Balancer that supports TCP and UDP traffic.
    - The Load Balancer distributes traffic across all Master Nodes.
    - If RTMP or TURN with TLS is enabled, the Load Balancer must also distribute traffic across all Media Nodes. (You can use a different Load Balancer for this purpose)
    - WebRTC traffic (SRTP/SCTP/STUN/TURN) is routed directly to the Media Nodes.

For the Master Node, the following services are configured:

- **OpenVidu Dashboard**, a web application interface to visualize your Rooms, Ingress, and Egress services.
- **MinIO** as an S3 storage service for recordings.
- **Redis** as a shared database for OpenVidu Server PRO and Ingress/Egress services.
- **MongoDB** as a database for storing analytics and monitoring data.
- **Caddy** as an internal reverse proxy for all services.
- **OpenVidu V2 Compatibility (v2compatibility module)** is an optional service that provides an API designed to maintain compatibility for applications developed with OpenVidu version 2.
- **OpenVidu Call (Default Application module)**, an optional ready-to-use videoconferencing application.
- **Grafana, Mimir, Promtail, and Loki (Observability module)** form an optional observability stack for monitoring, allowing you to keep track of logs and deployment statistics for OpenVidu.

For the Media Nodes, the following services are configured:

- **OpenVidu Server PRO (LiveKit compatible).**
- **Ingress** and **Egress** services.
- **Prometheus, Promtail, and Loki (Observability module)**. Used to send metrics and logs to the observability stack.

## Prerequisites

- **At least 6 machines**:
    - 4 machines for the Master Nodes.
    - 2 machines for the Media Nodes.
- **Each machine must have**:
    - A minimum of **4GB RAM** and **4 CPU cores**.
    - **Linux** installed (Ubuntu is recommended).
- Significant disk space in all the **Master Nodes**, with 100GB recommended, especially if you plan to record your sessions (Egress). Media Nodes require less space; however, account for the space needed for ongoing recordings on these nodes.
- **Media Nodes must have a public IP**. This is required because Media traffic is sent directly to these nodes. Master Nodes can have private IPs and will be accessed through the Load Balancer.
- **A Load Balancer** that supports TCP and UDP traffic. You can use a hardware load balancer or a software load balancer like HAProxy, Nginx, or AWS Network Load Balancer.
- **A Fully Qualified Domain Name (FQDN)** pointing to the Load Balancer. This domain name will be used to access the OpenVidu services.

## Port rules (Master Nodes)

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your Master Nodes:

**Inbound port rules**:

| Protocol | <div style="width:8em">Ports</div>      | <div style="width:15em">Source</div>         | Description                                         |
|----------|-------------|---------------------------|---------------------------------------------------------------------------------------------------|
| TCP      | 7880         | Load Balancer           | Allows access to the following to the Load Balancer: <ul><li>Livekit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Call (Default Application).</li><li>WHIP API.</li><li>TURN with TLS.</li><li>Custom layouts</li></ul> |
| TCP      | 7946-7947   | Master Nodes              | (Optional) For Mimir and Loki cluster communication (Observability module).                       |
| TCP      | 9095-9096   | Master Nodes              | (Optional) For Mimir and Loki cluster communication (Observability module).                       |
| TCP      | 3100        | Media Nodes               | (Optional) For Loki (Observability module).                                                       |
| TCP      | 9009        | Media Nodes               | (Optional) For Mimir (Observability module).                                                      |
| TCP      | 4443        | Media Nodes | (Optional) For OpenVidu V2 compatibility service.                                                 |
| TCP      | 6080        | Media Nodes | (Optional) For OpenVidu Call (Default Application).                                               |
| TCP      | 7000-7001   | Master Nodes, Media Nodes | For internal Redis communication                                                                  |
| TCP      | 9100        | Master Nodes, Media Nodes | For internal Minio communication                                                                  |
| TCP      | 20000       | Master Nodes, Media Nodes | For internal Mongo communication                                                                  |

**Outbound port rules**:

Typically, all outbound traffic is allowed.

## Port rules (Media Nodes)

Ensure all these rules are configured in your firewall, security group, or any kind of network configuration that you have in your Media Nodes:

**Inbound port rules**:

| Protocol    | <div style="width:8em">Ports</div>          | <div style="width:8em">Source</div> | Description                                                |
| ----------- | -------------- | --------------- | ---------------------------------------------------------- |
| UDP         | 443            | 0.0.0.0/0, ::/0   | STUN/TURN over UDP. |
| TCP         | 7881           | 0.0.0.0/0, ::/0   | (Optional), only needed if you want to allow WebRTC over TCP. |
| UDP         | 7885           | 0.0.0.0/0, ::/0   | (Optional). Only needed if you want to ingest WebRTC using WHIP. |
| UDP         | 50000-60000    | 0.0.0.0/0, ::/0   | WebRTC Media traffic. |
| TCP         | 1935           | Load Balancer     | (Optional). Only needed if you want to ingest RTMP streams using Ingress service. Master Nodes need access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
| TCP         | 5349           | Load Balancer    | (Optional). Only needed if you want to expose TURN service with TLS. Master Nodes need access to this port to reach TURN service and expose it using TLS (TURNS). |
| TCP         | 7880           | Master Nodes     | LiveKit API. Master Nodes need access to load balance LiveKit API and expose it through HTTPS. |
| TCP         | 8080           | Master Nodes     | (Optional). Only needed if you want to ingest WebRTC streams using WHIP. Master Nodes need access to this port to reach WHIP HTTP service. |

## Guided Installation

Before the installation, ensure that all your machines meet the [prerequisites](#prerequisites) and the port rules for the [Master Nodes](#port-rules-master-nodes) and [Media Nodes](#port-rules-media-nodes) are correctly configured.

To install OpenVidu High Availability, **begin by generating the commands required for setting up all nodes in the cluster**. This is a simple and straightforward process; simply **run the following command on any machine that has Docker installed**:

```bash
docker run -it openvidu/openvidu-installer:latest \
    --deployment-type=ha
```

--8<-- "docs/docs/self-hosting/shared/install-version.md"

A wizard will guide you through the installation process. You will be asked for the following information:

- **Write all 'Master Node' Private IPs separated by commas**: Write the private IP of each Master Node separated by commas.
- **Write your OpenVidu PRO License**: Write your OpenVidu PRO License.
!!!info
    If you don't have a license key for OpenVidu <span class="openvidu-tag openvidu-pro-tag">PRO</span>, you can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target=_blank}.
- **Do you want to use an external load balancer?**: Select _**Yes**_. We will use a Network Load Balancer in front of the cluster.
- **Domain name**: The domain name for your deployment. It must be an FQDN pointing to the machine where you are deploying OpenVidu.
- **(Optional) TURN domain name**: The domain name for your TURN server with TLS. It must be an FQDN pointing to the Load Balancer you will use and must be different from the OpenVidu domain name. Recommended if users who are going to connect to your OpenVidu deployment are behind restrictive firewalls.
- **Select which RTC engine to use**: Select the WebRTC engine you want to use. You can choose between **Pion (The engine used by Livekit)** or **Mediasoup (Experimental)**.

    --8<-- "docs/docs/self-hosting/shared/mediasoup-warning.md"

- **Modules to enable**: Select the modules you want to enable. You can enable the following modules:
    - _Observability_: Grafana stack, which includes logs and monitoring stats.
    - _Default App_: OpenVidu Call, a ready-to-use videoconferencing application.
    - _OpenVidu V2 Compatibility_: Compatibility API for applications developed with OpenVidu v2.

The rest of the parameters are secrets, usernames, and passwords. If empty, the wizard will generate random values for them.

This command will output the following instructions, which you should follow:

1. **Firewall Configuration for 'Master Nodes'**: These rules are the same as the ones specified in the instructions. Depending on the modules you have selected, some rules defined at [Port rules (Master Nodes)](#port-rules-master-nodes) may not appear (Optional ports). Double-check and modify them if you see something that can be enabled/disabled in your current port rules.
2. **Installation Commands for 'Master Nodes'**: This is the command needed to install your Master Node. It should look like this:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/ha/latest/install_ov_master_node.sh) \
        --no-tty --install \
        --deployment-type='ha' \
        --node-role='master-node' \
    ...
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    Execute that command on all your Master Nodes to install them. When the installation process finishes, you will see the following output:

    ```
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    >                                                                             <
    >  🎉🎉 OpenVidu HA 'Master Node' Installation Finished Successfully! 🎉🎉    <
    >                                                                             <
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    ```

    The Master Node will be installed in `/opt/openvidu` and configured as a systemd service. To start the service, use the following command:

    ```bash
    systemctl start openvidu
    ```

    Your Master Nodes will be ready once all of them have been started.

3. **Firewall Configuration for 'Media Nodes'**: These rules are the same as the ones defined previously as with Master Nodes. Double-check the [Port rules (Media Nodes)](#port-rules-media-nodes) and modify them if you see something that can be enabled/disabled in your current port rules.

4. **Installation Commands for 'Media Nodes'**: This is the command needed to install your Media Nodes. It should look like this:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/ha/latest/install_ov_media_node.sh) \
        --no-tty --install \
        --deployment-type='ha' \
        --node-role='media-node' \
    ...
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    Execute that command on your Media Nodes to install them. When the installation process finishes, you will see the following output:

    ```
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    >                                                                             <
    >  🎉 OpenVidu HA 'Media Node' Installation Finished Successfully! 🎉         <
    >                                                                             <
    > - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <
    ```

    The Media Node in each machine will be installed at `/opt/openvidu` and configured as a systemd service. You can start the service with the following command:

    ```bash
    systemctl start openvidu
    ```

If everything goes well, all containers will be up and running without restarts, and you will be able to access any of the following services:

- OpenVidu Call (Default Application): [https://openvidu.example.io/](https://openvidu.example.io/){:target=_blank}
- OpenVidu Dashboard: [https://openvidu.example.io/dashboard](https://openvidu.example.io/dashboard/){:target=_blank}
- MinIO: [https://openvidu.example.io/minio-console](https://openvidu.example.io/minio-console/){:target=_blank}
- Grafana: [https://openvidu.example.io/grafana](https://openvidu.example.io/grafana/){:target=_blank}

OpenVidu Server PRO URL (LiveKit compatible) will be available also in:

- OpenVidu Server PRO: [https://openvidu.example.io/](https://openvidu.example.io/){:target=_blank}
- LiveKit API: [https://openvidu.example.io/](https://openvidu.example.io/){:target=_blank} and [wss://openvidu.example.io/](wss://openvidu.example.io/){:target=_blank}

## Load Balancer Configuration

To configure the Load Balancer, you must create a new TCP listener for each port that the Master Nodes use. The Load Balancer should be set up to distribute traffic evenly across all Master Nodes, targeting their private IP addresses. Additionally, optional features like RTMP and TURN with TLS should be directed to use the private IP addresses of the Media Nodes. This ensures that traffic for these services is properly routed to the Media Nodes.

Below is an example using NGINX as a Load Balancer:

=== "NGINX Load Balancer Configuration"

    Example configuration for NGINX Load Balancer:

    ```nginx
    events {
        worker_connections 10240;
    }

    stream {

        upstream openvidu_master_nodes {
            server <MASTER_NODE_IP_1>:7880;
            server <MASTER_NODE_IP_2>:7880;
            server <MASTER_NODE_IP_3>:7880;
            server <MASTER_NODE_IP_4>:7880;
        }

        # Optional: Only if you want to ingest RTMP
        upstream openvidu_media_nodes_rtmp {
            server <MEDIA_NODE_IP_1>:1935;
            server <MEDIA_NODE_IP_2>:1935;
            # Add more media nodes if needed
        }

        server {
            listen 443 ssl;
            server_name openvidu.example.com;
            ssl_protocols       TLSv1.2 TLSv1.3;
            ssl_certificate     /etc/nginx/ssl/openvidu-cert.pem;
            ssl_certificate_key /etc/nginx/ssl/openvidu-key.pem;

            proxy_connect_timeout 10s;
            proxy_timeout 30s;

            proxy_pass openvidu_master_nodes;
        }

        # Optional: Only if you want to ingest RTMP
        server {
            listen 1935 ssl;
            server_name openvidu.example.com;
            ssl_protocols       TLSv1.2 TLSv1.3;
            ssl_certificate     /etc/nginx/ssl/openvidu-cert.pem;
            ssl_certificate_key /etc/nginx/ssl/openvidu-key.pem;

            proxy_connect_timeout 10s;
            proxy_timeout 30s;

            proxy_pass openvidu_media_nodes_rtmp;
        }

    }
    ```

    - Notice that `openvidu.example.com` is the domain name you have chosen for your OpenVidu deployment and you should configure it in your DNS to point to the Load Balancer. Also, the `openvidu-cert.pem` and `openvidu-key.pem` must be valid SSL certificates for your domain.
    - Replace `<MASTER_NODE_IP_X>` with the private IP addresses of your Master Nodes and `<MEDIA_NODE_IP_X>` with the private IP addresses of your Media Nodes.

=== "NGINX Load Balancer Configuration (With TLS for TURN)"

    Example configuration for NGINX Load Balancer:

    ```nginx
    events {
        worker_connections 10240;
    }

    stream {

        upstream openvidu_master_nodes {
            server <MASTER_NODE_IP_1>:7880;
            server <MASTER_NODE_IP_2>:7880;
            server <MASTER_NODE_IP_3>:7880;
            server <MASTER_NODE_IP_4>:7880;
        }

        # Optional: Only if you want to ingest RTMP
        upstream openvidu_media_nodes_rtmp {
            server <MEDIA_NODE_IP_1>:1935;
            server <MEDIA_NODE_IP_2>:1935;
            # Add more media nodes if needed
        }

        upstream turn_tls {
            server <MEDIA_NODE_IP_1>:5349;
            server <MEDIA_NODE_IP_2>:5349;
            # Add more media nodes if needed
        }

        map $ssl_server_name $targetBackend {
            openvidu.example.com openvidu_master_nodes;
            turn.example.com turn_tls;
        }

        map $ssl_server_name $targetCert {
            openvidu.example.com /etc/nginx/ssl/openvidu-cert.pem;
            turn.example.com /etc/nginx/ssl/turn-cert.pem;
        }

        map $ssl_server_name $targetCertKey {
            openvidu.example.com /etc/nginx/ssl/openvidu-key.pem;
            turn.example.com /etc/nginx/ssl/turn-key.pem;
        }

        server {
            listen 443 ssl;
            ssl_protocols       TLSv1.2 TLSv1.3;
            ssl_certificate     $targetCert;
            ssl_certificate_key $targetCertKey;

            proxy_connect_timeout 10s;
            proxy_timeout 30s;

            proxy_pass $targetBackend;
        }

        # Optional: Only if you want to ingest RTMP
        server {
            listen 1935 ssl;
            ssl_protocols       TLSv1.2 TLSv1.3;
            ssl_certificate     $targetCert;
            ssl_certificate_key $targetCertKey;

            proxy_connect_timeout 10s;
            proxy_timeout 30s;

            proxy_pass openvidu_media_nodes_rtmp;
        }

    }
    ```

    - Notice that `openvidu.example.com` is the domain name you have chosen for your OpenVidu deployment and `turn.example.com` is the domain name you have chosen for your TURN with TLS. Both domains should be configured in your DNS to point to the Load Balancer. Also, the `openvidu-cert.pem`, `openvidu-key.pem`, `turn-cert.pem`, and `turn-key.pem` must be valid SSL certificates for your domains.
    - Replace `<MASTER_NODE_IP_X>` with the private IP addresses of your Master Nodes and `<MEDIA_NODE_IP_X>` with the private IP addresses of your Media Nodes.

## Deployment Credentials

To point your applications to your OpenVidu deployment, check the file at `/opt/openvidu/.env` of any Master Node. All access credentials of all services are defined in this file.

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

    To install a Master Node, you can use the following command:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/ha/latest/install_ov_master_node.sh) \
        --node-role='master-node' \
        --master-node-private-ip-list='10.5.0.1,10.5.0.2,10.5.0.3,10.5.0.4' \
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
        --mongo-replica-set-key='xxxxx' \
        --grafana-admin-user='xxxxx' \
        --grafana-admin-password='xxxxx' \
        --default-app-user='xxxxx' \
        --default-app-password='xxxxx' \
        --default-app-admin-user='xxxxx' \
        --default-app-admin-password='xxxxx' \
        --external-load-balancer
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    Notes:

    - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target=_blank}.
    - `--master-node-private-ip-list` is the list of private IPs of all Master Nodes separated by commas. It should not change, and Media Nodes should be able to reach all Master Nodes using these IPs.

=== "Media Node"

    To install a Media Node, you can use the following command:

    ```bash
    sh <(curl -fsSL http://get.openvidu.io/pro/ha/latest/install_ov_media_node.sh) \
        --node-role='media-node' \
        --domain-name-or-ip='openvidu.example.io' \
        --master-node-private-ip-list='10.5.0.1,10.5.0.2,10.5.0.3,10.5.0.4' \
        --openvidu-pro-license='xxxxx' \
        --rtc-engine='pion' \
        --enabled-modules='observability,v2compatibility,app' \
        --turn-domain-name='openvidu.example.io' \
        --livekit-api-key='xxxxx' \
        --livekit-api-secret='xxxxx' \
        --redis-password='xxxxx' \
        --minio-access-key='xxxxx' \
        --minio-secret-key='xxxxx' \
        --mongo-admin-user='xxxxx' \
        --mongo-admin-password='xxxxx'
    ```

    --8<-- "docs/docs/self-hosting/shared/install-version.md"

    - Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.
    - `--master-node-private-ip` must be the same list of private IPs of all Master Nodes separated by commas. It should not change, and Media Nodes should be able to reach all Master Nodes using these IPs.
    - If no media appears in your conference, reinstall specifying the `--public-ip` parameter with your machine's public IP. OpenVidu usually auto-detects the public IP, but it can fail. This IP is used by clients to send and receive media.
    - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account){:target=_blank}.

You can run these commands in a CI/CD pipeline or in a script to automate the installation process.

Some general notes about all commands:

- The argument `--turn-domain-name` is optional. You define it only if you want to enable TURN with TLS in case users are behind restrictive firewalls.
- In the argument `--enabled-modules`, you can enable the modules you want to deploy. You can enable `observability` (Grafana stack), `app` (Default App - OpenVidu Call), and `v2compatibility` (OpenVidu v2 compatibility API).

To start each node, remember to execute the following command in each node:

```bash
systemctl start openvidu
```

## Configuration and administration

Once you have OpenVidu deployed, you can check the [Configuration and Administration](../on-premises/admin.md) section to learn how to manage your OpenVidu High Availability deployment.
