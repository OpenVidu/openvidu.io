# How to deploy and configure OpenVidu with an existing external proxy

By default, OpenVidu is deployed with an internal [Caddy server](https://caddyserver.com/){:target="_blank"} to configure and manage SSL certificates. However, there are certain scenarios where using an external proxy might be preferable:

- You wish to manage SSL certificates manually.
- A specific proxy server is required for enhanced security.
- You need to integrate a proxy server already in your infrastructure.

If none of these scenarios apply to you and you prefer to use the default internal Caddy server, please refer to the [official installation guides](../deployment-types.md){:target="_blank"}.

For those needing to deploy OpenVidu using an external proxy, this guide offers detailed steps to deploy it and configure the external proxy.

- [External Proxy for OpenVidu Single Node](#single-node)
- [External Proxy for OpenVidu Elastic](#elastic)
- [External Proxy for OpenVidu High Availability](#high-availability)

=== "Single Node"

    !!! note
        The Single Node deployment with an external proxy is based on the same instructions as the [Single Node <span class='openvidu-tag openvidu-community-tag'>COMMUNITY</span> Deployment](../single-node/on-premises/install.md){:target="_blank"} and the [Single Node <span class='openvidu-tag openvidu-pro-tag'>PRO</span> Deployment](../single-node/on-premises/install-pro.md){:target="_blank"}, but with some modifications to the installation command and port rules. We recommend you to read the installation guides before proceeding with this guide to have a better understanding of the deployment.

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu Single Node On Premises Architecture with External Proxy](../../../assets/images/self-hosting/how-to-guides/external-proxy/single-node-external-proxy.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Single Node On Premises Architecture with External Proxy</figcaption>
    </figure>

    **1. Prerequisites**

    To deploy OpenVidu with an external proxy, ensure you have the following prerequisites:


    - **A machine with at least 4GB RAM and 4 CPU cores** and **Linux installed (Ubuntu recommended)**. This machine will serve as the OpenVidu server.
    - An additional machine for the proxy server is recommended. Alternatively, you can use the same machine as OpenVidu, but be aware that the proxy server will consume resources. Note that [some ports will be used by OpenVidu](../single-node/on-premises/install.md#port-rules){:target="_blank"}, except for the ports utilized by the proxy server (TCP 80, 443, and 1935).
    - **Generous disk space (100GB recommended)** if you are going to record your sessions.
    - The machine where OpenVidu is installed **must have a Public IP or a reachable IP from the users**.
    - The proxy server also **must have a Public IP or a reachable IP from the users**.
    - A domain name for your OpenVidu deployment pointing to the machine where the proxy server is running. In this guide, we will use `openvidu.example.io`.
    - Optionally (but recommended), you need an additional domain name pointing to the proxy machine where the proxy server is running. It will be used for TURN with TLS which is useful in case your users are behind restrictive firewalls to be able to connect to OpenVidu. In this guide, we will use `turn.example.io`.

    **2. Port Rules**

    You can follow the same rule ports of the [Single Node Deployment](../single-node/on-premises/install.md#port-rules){:target="_blank"} but some ports are used by the proxy server and others are not needed. The inbound rules for the OpenVidu proxy would be as follows:

    === "OpenVidu Machine"

        **Inbound Rules**

        | Protocol    | Ports          | <div style="width:8em">Source</div>          | Description                                                |
        | ----------- | -------------- | --------------- | ---------------------------------------------------------- |
        | TCP         | 7880            | External proxy | Allows access to the following: <ul><li>LiveKit API.</li><li>OpenVidu Dashboard.</li><li>OpenVidu Call (Default Application).</li><li>WHIP API.</li><li>Custom layouts</li></ul> |
        | TCP         | 1945           | External proxy | Needed if you want to ingest RTMP streams using Ingress service. |
        | TCP         | 5349           | External proxy | Optional and needed only if you have a domain for TURN and you want to use TURN with TLS |
        | UDP         | 443            | 0.0.0.0/0, ::/0 | STUN/TURN server over UDP. |
        | TCP         | 7881           | 0.0.0.0/0, ::/0 | Needed if you want to allow WebRTC over TCP. |
        | UDP         | 7885           | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP protocol. |
        | TCP         | 9000           | 0.0.0.0/0, ::/0 | Needed if you want to expose MinIO publicly. |
        | UDP         | 50000 - 60000  | 0.0.0.0/0, ::/0 | WebRTC Media traffic. |

        **Outbound Rules**

        Typically, all outbound traffic is allowed.

    === "Proxy Server"

        **Inbound Rules**

        | Protocol    | Ports          | <div style="width:8em">Source</div>          | Description                                                |
        | ----------- | -------------- | --------------- | ---------------------------------------------------------- |
        | TCP         | 80             | 0.0.0.0/0, ::/0 | HTTP redirection to HTTPS. |
        | TCP         | 443            | 0.0.0.0/0, ::/0 | HTTPS access to the OpenVidu API and TURN with TLS. |
        | TCP         | 1935           | 0.0.0.0/0, ::/0 | RTMP with TLS. |


    **3. Install OpenVidu Single Node with `--external-proxy` flag**

    To deploy OpenVidu with an external proxy, you must use the CLI installation command with the `--external-proxy` flag. The command to install OpenVidu with an external proxy is as follows:

    === "Single Node <span class='openvidu-tag openvidu-community-tag'>COMMUNITY</span>"

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
            --no-tty --install \
            --domain-name='openvidu.example.io' \
            --turn-domain-name='turn.example.io' \
            --enabled-modules='observability,app' \
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
            --external-proxy
        ```

    === "Single Node <span class='openvidu-tag openvidu-pro-tag'>PRO</span>"

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
            --no-tty --install \
            --openvidu-pro-license='xxxxx' \
            --domain-name='openvidu.example.io' \
            --turn-domain-name='turn.example.io' \
            --enabled-modules='observability,app,v2compatibility' \
            --rtc-engine='pion' \
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
            --external-proxy
        ```

    --8<-- "shared/self-hosting/install-version.md"

    Notes:

    - Replace `openvidu.example.io` with your FQDN.
    - The `turn-domain-name` parameter is optional. You define it only if you want to enable TURN with TLS in case users are behind restrictive firewalls.If you don't have a TURN server, you can remove it from the command. If you want to use TURN with TLS, replace `turn.example.io` with your TURN server FQDN.
    - In <span class='openvidu-tag openvidu-pro-tag'>PRO</span> edition, the `--openvidu-pro-license` parameter is mandatory. You can get your license key [here](/account/){:target="_blank"}.
    - In <span class='openvidu-tag openvidu-pro-tag'>PRO</span> edition, depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

    **4. Configure the external proxy**

    We will use [Nginx](https://www.nginx.com/){:target="_blank"} as the proxy server, but the configuration can be adapted to other proxy servers. The configuration for the proxy server is as follows:

    --8<-- "shared/self-hosting/proxy-nginx-turn-tls.md"

        - Replace `openvidu.example.io` and `turn.example.io` with your domain names. These domain names must be configured in your DNS to point to the proxy server.
        - Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the OpenVidu server.
        - You can also have a proxy in the same machine as OpenVidu, simply replace `<MASTER_NODE_PRIVATE_IP>` with `127.0.0.1`.

    --8<-- "shared/self-hosting/proxy-nginx.md"

        - Replace `openvidu.example.io` with your domain name. This domain name must be configured in your DNS to point to the proxy server.
        - Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the OpenVidu server.
        - You can also have a proxy in the same machine as OpenVidu, simply replace `<MASTER_NODE_PRIVATE_IP>` with `127.0.0.1`.

=== "Elastic"

    !!! note
        The Elastic deployment with an external proxy is based on the same instructions as the [Elastic Deployment](../elastic/on-premises/install.md){:target="_blank"}, but with some modifications to the installation command and port rules. We recommend you to read the [Elastic Deployment](../elastic/on-premises/install.md){:target="_blank"} guide before proceeding with this guide to have a better understanding of the deployment.

    This is how the architecture of the deployment looks like:

    <figure markdown>
    ![OpenVidu Elastic On Premises Architecture with External Proxy](../../../assets/images/self-hosting/how-to-guides/external-proxy/elastic-external-proxy.svg){ .svg-img .dark-img }
    <figcaption>OpenVidu Elastic On Premises Architecture with External Proxy</figcaption>
    </figure>

    **1. Prerequisites**

    To deploy OpenVidu Elastic with an external proxy, ensure you have the following prerequisites:

    - **At least 2 machines** for OpenVidu, each with a minimum of **4GB RAM**, **4 CPU cores**, and **Linux** installed (Ubuntu is recommended). One machine will serve as the Master Node, while the others will function as Media Nodes.
    - An additional machine for the proxy server is recommended. Alternatively, you can use the same machine as the Master Node, but be aware that the proxy server will consume resources. Note that [some ports will be used by OpenVidu](../elastic/on-premises/install.md#port-rules-master-node){:target="_blank"}, except for the ports utilized by the proxy server (TCP 80, 443, and 1935).
    - Significant disk space on the **Master Node, with 100GB recommended**, especially if you plan to record your sessions (Egress). Media Nodes require less space; however, account for the space needed for ongoing recordings on these nodes.
    - **Each machine must have a Public IP or a reachable IP from the users**.
    - **The proxy server must have a Public IP or a reachable IP from the users**.
    - **A domain name for your OpenVidu deployment pointing to the proxy server**. In this guide, we will use `openvidu.example.io`.
    - Optionally (but recommended), you need an additional domain name pointing to the proxy server. It will be used for TURN with TLS which is useful in case your users are behind restrictive firewalls. In this guide, we will use `turn.example.io`.

    **2. Port Rules**

    You can follow the same rule ports of the Elastic Deployment for the [Master Node](../elastic/on-premises/install.md#port-rules-master-node) and for the [Media Nodes](../elastic/on-premises/install.md#port-rules-media-nodes) but some ports are used by the proxy server and others are not needed. The inbound rules for the OpenVidu proxy would be as follows:

    === "Master Node"

        **Inbound Rules**

        | Protocol    | Ports          | <div style="width:8em">Source</div> | Description                                                |
        | ----------- | -------------- | --------------- | ---------------------------------------------------------- |
        | TCP         | 7880            | External Proxy | Allows access to the following: <ul><li>Livekit API.</li><li>OpenVidu v2 Compatibility API</li><li>OpenVidu Dashboard.</li><li>OpenVidu Call (Default Application).</li><li>WHIP API.</li><li>Custom layouts</li></ul> |
        | TCP         | 1935           | External Proxy | Needed if you want to ingest RTMP streams using Ingress service. |
        | TCP         | 5349           | External proxy | Optional and needed only if you have a domain for TURN and you want to use TURN with TLS |
        | TCP         | 4443           | Media Nodes     | Needed when _'OpenVidu v2 Compatibility'_ module is used (`v2compatibility` in `ENABLED_MODULES` global parameter). Media Nodes need access to this port to reach OpenVidu V2 compatibility service |
        | TCP         | 6080           | Media Nodes     | Needed when _'Default App'_  module is used (`app` in `ENABLED_MODULES` global parameter). Media Nodes need access to this port to reach OpenVidu Call (Default Application). |
        | TCP         | 3100           | Media Nodes     | Needed when _'Observability'_ module is used (`observability` in `ENABLED_MODULES` global parameter) Media Nodes need access to this port to reach Loki. |
        | TCP         | 9009           | Media Nodes     | Needed when _'Observability'_ module is used. (`observability` in `ENABLED_MODULES` global parameter) Media Nodes need access to this port to reach Mimir. |
        | TCP         | 7000           | Media Nodes     | Media Nodes need access to this port to reach Redis Service. |
        | TCP         | 9100           | Media Nodes     | Media Nodes need access to this port to reach MinIO. |
        | TCP         | 20000          | Media Nodes     | Media Nodes need access to this port to reach MongoDB. |

        **Outbound Rules**

        Typically, all outbound traffic is allowed.

    === "Media Nodes"

        **Inbound Rules**

        | Protocol    | <div style="width:8em">Ports</div>          | <div style="width:8em">Source</div> | Description                                                |
        | ----------- | -------------- | --------------- | ---------------------------------------------------------- |
        | UDP         | 443            | 0.0.0.0/0, ::/0   | STUN/TURN over UDP. |
        | TCP         | 7881           | 0.0.0.0/0, ::/0   | Needed if you want to allow WebRTC over TCP. |
        | UDP         | 7885           | 0.0.0.0/0, ::/0   | Needed if you want to ingest WebRTC using WHIP. |
        | UDP         | 50000-60000    | 0.0.0.0/0, ::/0   | WebRTC Media traffic. |
        | TCP         | 1935           | Master Node     | Needed if you want to ingest RTMP streams using Ingress service. Master Node needs access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
        | TCP         | 5349           | Master Node     | Needed if you have configured TURN with a domain for TLS. Master Node needs access to this port to reach TURN service and expose it using TLS (TURNS). |
        | TCP         | 7880           | Master Node     | LiveKit API. Master Node needs access to load balance LiveKit API and expose it through HTTPS. |
        | TCP         | 8080           | Master Node     | Needed if you want to ingest WebRTC streams using WHIP. Master Node needs access to this port to reach WHIP HTTP service. |

        **Outbound Rules**

        Typically, all outbound traffic is allowed.

    === "Proxy Server"

        And the inbound rules for the proxy server would be as follows:

        | Protocol    | Ports          | <div style="width:8em">Source</div>          | Description                                                |
        | ----------- | -------------- | --------------- | ---------------------------------------------------------- |
        | TCP         | 80             | 0.0.0.0/0, ::/0 | HTTP redirection to HTTPS. |
        | TCP         | 443            | 0.0.0.0/0, ::/0 | HTTPS access to the OpenVidu API and TURN with TLS. |
        | TCP         | 1935           | 0.0.0.0/0, ::/0 | RTMP with TLS. |

    **3. Install OpenVidu Elastic with `--external-proxy` flag**

    To deploy OpenVidu Elastic with an external proxy, you must use the CLI installation command with the `--external-proxy` flag. The command to install OpenVidu Elastic with an external proxy is as follows:

    === "Install Master Node"

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
            --no-tty --install \
            --node-role='master-node' \
            --openvidu-pro-license='xxxxx' \
            --domain-name='openvidu.example.io' \
            --turn-domain-name='turn.example.io' \
            --enabled-modules='observability,v2compatibility,app' \
            --rtc-engine='pion' \
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
            --private-ip='<MASTER_NODE_PRIVATE_IP>' \
            --external-proxy
        ```

        --8<-- "shared/self-hosting/install-version.md"

        Notes:

        - `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](/account/){:target="_blank"}.
        - Replace `openvidu.example.io` with your FQDN.
        - The `turn-domain-name` parameter is optional. You define it only if you want to enable TURN with TLS in case users are behind restrictive firewalls. If you don't have a TURN server, you can remove it from the command. If you want to use TURN with TLS, replace `turn.example.io` with your TURN server FQDN.
        - `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP. Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
        - Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

    === "Install Media Nodes"

        To install a Media Node, you can use the following command:

        ```bash
        sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_media_node.sh) \
            --no-tty --install \
            --node-role='media-node' \
            --master-node-private-ip='<MASTER_NODE_PRIVATE_IP>' \
            --redis-password='xxxxx'
        ```

        --8<-- "shared/self-hosting/install-version.md"

        - The `--master-node-private-ip` is the private IP of the Master Node. Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
        - The `--redis-password` is the password used to connect to the Redis service. Replace `xxxxx` with the same password used in the Master Node installation.

    **4. Configure the external proxy**

    We will use [Nginx](https://www.nginx.com/){:target="_blank"} as the proxy server, but the configuration can be adapted to other proxy servers. The configuration for the proxy server is as follows:

    --8<-- "shared/self-hosting/proxy-nginx-turn-tls.md"

        - Replace `openvidu.example.io` and `turn.example.io` with your domain names. These domain names must be configured in your DNS to point to the proxy server.
        - Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
        - You can also have a proxy in the same machine as the Master Node, simply replace `<MASTER_NODE_PRIVATE_IP>` with `127.0.0.1`.

    --8<-- "shared/self-hosting/proxy-nginx.md"

        - Replace `openvidu.example.io` with your domain name. This domain name must be configured in your DNS to point to the proxy server.
        - Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
        - You can also have a proxy in the same machine as the Master Node, simply replace `<MASTER_NODE_PRIVATE_IP>` with `127.0.0.1`.

=== "High Availability"

    The High Availability deployment already has a way to configure an external proxy (described as a Network Load Balancer), which is explained  [in this section](../ha/on-premises/install-nlb.md){:target="_blank"}.

# Can I force all traffic including WebRTC to go through the external proxy?

Yes, but you need to use a domain name for TURN (`--turn-domain-name` parameter) and ensure that the following ports are explicitly closed in OpenVidu:

**Single Node closed Ports**

**Node**|**Port**|**Protocol**
---|---|---
OpenVidu Server|443|UDP
OpenVidu Server|50000-60000|UDP

**Elastic and High Availability closed Ports**

**Node**|**Port**|**Protocol**
---|---|---
Media Node|443|UDP
Media Node|50000-60000|UDP

This configuration will force traffic to use TURN, so all traffic will go through the external proxy using the TURN domain name configured in the installation process. But you need to understand some considerations:

- Media over UDP using WebRTC does not mean that the media is not encrypted. WebRTC encrypts the media using SRTP and DTLS. WebRTC is designed to be encrypted by default.

- Media going through 443 with TLS has a penalty in the media quality and CPU usage. This is because of the TLS roundtrip, TCP being used and media processed twice by the TURN server and the Media Server. This can lead to a worse user experience and higher CPU usage in the Media Server. We recommend using this configuration only if it is strictly necessary.
