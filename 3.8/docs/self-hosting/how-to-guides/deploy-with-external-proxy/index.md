# How to deploy and configure OpenVidu with an existing external proxy

By default, OpenVidu is deployed with an internal [Caddy server](https://caddyserver.com/) to configure and manage SSL certificates. However, there are certain scenarios where using an external proxy might be preferable:

- You wish to manage SSL certificates manually.
- A specific proxy server is required for enhanced security.
- You need to integrate a proxy server already in your infrastructure.

If none of these scenarios apply to you and you prefer to use the default internal Caddy server, please refer to the [official installation guides](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md).

For those needing to deploy OpenVidu using an external proxy, this guide offers detailed steps to deploy it and configure the external proxy.

- [External Proxy for OpenVidu Single Node](#single-node)
- [External Proxy for OpenVidu Elastic](#elastic)
- [External Proxy for OpenVidu High Availability](#high-availability)

**Single Node**

Note

The Single Node deployment with an external proxy is based on the same instructions as the [Single Node Deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/install/index.md) (both the COMMUNITY and PRO editions), but with some modifications to the installation command and port rules. We recommend reading the installation guide before proceeding with this guide for a better understanding of the deployment.

This is what the architecture of the deployment looks like:

OpenVidu Single Node On Premises Architecture with External Proxy

**1. Prerequisites**

To deploy OpenVidu with an external proxy, ensure you have the following prerequisites:

- **A machine with at least 4GB RAM and 4 CPU cores** and **Linux installed (Ubuntu recommended)**. This machine will serve as the OpenVidu server.
- An additional machine for the proxy server is recommended. Alternatively, you can use the same machine as OpenVidu, but be aware that the proxy server will consume resources. Note that [some ports will be used by OpenVidu](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/install/#port-rules), except for the ports utilized by the proxy server (TCP 80, 443, and 1935).
- **Generous disk space (100GB recommended)** if you are going to record your sessions.
- The machine where OpenVidu is installed **must have a Public IP or a reachable IP from the users**.
- The proxy server also **must have a Public IP or a reachable IP from the users**.
- A domain name for your OpenVidu deployment pointing to the machine where the proxy server is running. In this guide, we will use `openvidu.example.io`.
- A domain name for the TURN server pointing to the machine where the proxy server is running. In this guide, we will use `turn.example.io`.

**2. Port Rules**

You can follow the same rule ports of the [Single Node Deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/on-premises/install/#port-rules) but some ports are used by the proxy server and others are not needed. The inbound rules for the OpenVidu proxy would be as follows:

**OpenVidu Machine**

**Inbound Rules**

| Protocol | Ports       | Source          | Description                                                                                                        |
| -------- | ----------- | --------------- | ------------------------------------------------------------------------------------------------------------------ |
| TCP      | 7880        | External proxy  | Allows access to the following: - LiveKit API. - OpenVidu Dashboard. - OpenVidu Meet. - WHIP API. - Custom layouts |
| TCP      | 5349        | External proxy  | TURN with TLS.                                                                                                     |
| TCP      | 1945        | External proxy  | Needed if you want to ingest RTMP streams using Ingress service.                                                   |
| UDP      | 443         | 0.0.0.0/0, ::/0 | STUN/TURN server over UDP.                                                                                         |
| TCP      | 9000        | 0.0.0.0/0, ::/0 | Needed if you want to expose MinIO publicly.                                                                       |
| TCP      | 7881        | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Pion.                                                                |
| UDP      | 7885        | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP.                                                                    |
| UDP      | 50000-60000 | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over UDP.                                                                          |
| TCP      | 50000-60000 | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Mediasoup.                                                           |

**Outbound Rules**

Typically, all outbound traffic is allowed.

**Proxy Server**

**Inbound Rules**

| Protocol | Ports | Source          | Description                                         |
| -------- | ----- | --------------- | --------------------------------------------------- |
| TCP      | 80    | 0.0.0.0/0, ::/0 | HTTP redirection to HTTPS.                          |
| TCP      | 443   | 0.0.0.0/0, ::/0 | HTTPS access to the OpenVidu API and TURN with TLS. |
| TCP      | 1935  | 0.0.0.0/0, ::/0 | RTMP with TLS.                                      |

**3. Install OpenVidu Single Node with `--external-proxy` flag**

To deploy OpenVidu with an external proxy, you must use the CLI installation command with the `--external-proxy` flag. The command to install OpenVidu with an external proxy is as follows:

**Single Node COMMUNITY**

```bash
sh <(curl -fsSL http://get.openvidu.io/community/singlenode/latest/install.sh) \
    --no-tty --install \
    --domain-name='openvidu.example.io' \
    --turn-domain-name='turn.example.io' \
    --enabled-modules='observability,openviduMeet' \
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
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --external-proxy
```

**Single Node PRO**

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/singlenode/latest/install.sh) \
    --no-tty --install \
    --openvidu-pro-license='xxxxx' \
    --domain-name='openvidu.example.io' \
    --turn-domain-name='turn.example.io' \
    --enabled-modules='observability,openviduMeet,v2compatibility' \
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
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --external-proxy
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

Notes:

- Replace `openvidu.example.io` with your FQDN.
- Replace `turn.example.io` with your TURN server FQDN.
- In **PRO** edition, the `--openvidu-pro-license` parameter is mandatory. You can get your license key [here](https://openvidu.io/account/) .
- In **PRO** edition, depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

**4. Configure the external proxy**

We will use [Nginx](https://www.nginx.com/) as the proxy server, but the configuration can be adapted to other proxy servers.

In this configuration, the proxy uses **SNI-based Layer 4 routing** to separate API and TURN traffic on port `443`. The API domain is routed to a local HTTP reverse-proxy server on port `7880`, which then forwards requests to the OpenVidu node. The TURN domain is forwarded directly to port `5349` on the OpenVidu node. This gives you an `http` block where you can add custom routing, rate limiting, access control, or additional headers.

The proxy needs these rules:

1. **Redirect HTTP to HTTPS** on port `80`.
1. **Proxy TLS traffic on port `443`** using SNI to route:
   - API domain → local `127.0.0.1:7880` → HTTP reverse-proxy → OpenVidu node on port `7880`.
   - TURN domain → OpenVidu node on port `5349`.
1. **Proxy TLS traffic on port `1935`** to the OpenVidu node on port `1945` (RTMP).

The following is an example Nginx configuration file:

```nginx
events {
    worker_connections 10240;
}

stream {

    upstream api_backend {
        server 127.0.0.1:7880;
    }

    upstream turn_backend {
        server <SINGLE_NODE_PRIVATE_IP>:5349;
    }

    upstream rtmp_backend {
        server <SINGLE_NODE_PRIVATE_IP>:1945;
    }

    # Use SNI to determine which upstream server to proxy to
    map $ssl_server_name $upstream {
        openvidu.example.io api_backend;
        turn.example.io turn_backend;
    }

    # Use SNI to determine which certificate to use
    map $ssl_server_name $certificate {
        openvidu.example.io /etc/nginx/ssl/openvidu-cert.pem;
        turn.example.io /etc/nginx/ssl/turn-cert.pem;
    }

    # Use SNI to determine which private key to use
    map $ssl_server_name $private_key {
        openvidu.example.io /etc/nginx/ssl/openvidu-privkey.pem;
        turn.example.io /etc/nginx/ssl/turn-privkey.pem;
    }

    # Proxy for API and TURN
    server {
        listen 443 ssl;
        listen [::]:443 ssl;
        ssl_protocols TLSv1.2 TLSv1.3;

        proxy_connect_timeout 10s;
        proxy_timeout 30s;

        ssl_certificate $certificate;
        ssl_certificate_key $private_key;

        proxy_pass $upstream;
    }

    # RTMP
    server {
        listen 1935 ssl;
        listen [::]:1935 ssl;
        ssl_protocols TLSv1.2 TLSv1.3;

        proxy_connect_timeout 10s;
        proxy_timeout 30s;

        ssl_certificate /etc/nginx/ssl/openvidu-cert.pem;
        ssl_certificate_key /etc/nginx/ssl/openvidu-privkey.pem;

        proxy_pass rtmp_backend;
    }
}

# Redirect HTTP to HTTPS and reverse proxy API traffic
http {
    server {
        listen 80;
        listen [::]:80;
        return 301 https://$host$request_uri;
    }

    upstream api_http_backend {
        server <SINGLE_NODE_PRIVATE_IP>:7880;
    }

    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    server {
        listen 7880;

        location / {
            proxy_pass http://api_http_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
        }
    }
}
```

Customizable HTTP block

The `http` block gives you full control over HTTP-level routing. You can add custom `location` blocks, rate limiting, access control, or additional headers to suit your infrastructure needs.

Notes:

- Replace `openvidu.example.io` and `turn.example.io` with your domain names. These domain names must be configured in your DNS to point to the proxy server.
- Replace `<SINGLE_NODE_PRIVATE_IP>` with the private IP of the OpenVidu server.
- You can also have a proxy in the same machine as OpenVidu, simply replace `<SINGLE_NODE_PRIVATE_IP>` with `127.0.0.1`.

If you want to force all traffic including WebRTC to go through the external proxy, check the [Force media traffic through port 443](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/force-single-port/index.md) guide.

**Elastic**

Note

The Elastic deployment with an external proxy is based on the same instructions as the [Elastic Deployment](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/index.md), but with some modifications to the installation command and port rules. We recommend reading the [Elastic Deployment](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/index.md) guide before proceeding with this guide for a better understanding of the deployment.

This is what the architecture of the deployment looks like:

OpenVidu Elastic On Premises Architecture with External Proxy

**1. Prerequisites**

To deploy OpenVidu Elastic with an external proxy, ensure you have the following prerequisites:

- **At least 2 machines** for OpenVidu, each with a minimum of **4GB RAM**, **4 CPU cores**, and **Linux** installed (Ubuntu is recommended). One machine will serve as the Master Node, while the others will function as Media Nodes.
- An additional machine for the proxy server is recommended. Alternatively, you can use the same machine as the Master Node, but be aware that the proxy server will consume resources. Note that [some ports will be used by OpenVidu](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/#port-rules-master-node), except for the ports utilized by the proxy server (TCP 80, 443, and 1935).
- Significant disk space on the **Master Node, with 100GB recommended**, especially if you plan to record your sessions (Egress). Media Nodes require less space; however, account for the space needed for ongoing recordings on these nodes.
- **Each machine must have a Public IP or a reachable IP from the users**.
- **The proxy server must have a Public IP or a reachable IP from the users**.
- **A domain name for your OpenVidu deployment pointing to the proxy server**. In this guide, we will use `openvidu.example.io`.
- **A domain name for the TURN server pointing to the proxy server**. In this guide, we will use `turn.example.io`.

**2. Port Rules**

You can follow the same rule ports of the Elastic Deployment for the [Master Node](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/#port-rules-master-node) and for the [Media Nodes](https://openvidu.io/3.8/docs/self-hosting/elastic/on-premises/install/#port-rules-media-nodes) but some ports are used by the proxy server and others are not needed. The inbound rules for the OpenVidu proxy would be as follows:

**Master Node**

**Inbound Rules**

| Protocol | Ports | Source         | Description                                                                                                                                                                                         |
| -------- | ----- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TCP      | 7880  | External Proxy | Allows access to the following: - Livekit API. - OpenVidu v2 Compatibility API - OpenVidu Dashboard. - OpenVidu Meet. - WHIP API. - Custom layouts                                                  |
| TCP      | 5349  | External Proxy | TURN with TLS.                                                                                                                                                                                      |
| TCP      | 1945  | External Proxy | Needed if you want to ingest RTMP streams using Ingress service.                                                                                                                                    |
| TCP      | 4443  | Media Nodes    | Needed when *'OpenVidu v2 Compatibility'* module is used (`v2compatibility` in `ENABLED_MODULES` global parameter). Media Nodes need access to this port to reach OpenVidu V2 compatibility service |
| TCP      | 9080  | Media Nodes    | Needed when *'OpenVidu Meet'* module is used (`openviduMeet` in `ENABLED_MODULES` global parameter). Media Nodes need access to this port to reach OpenVidu Meet.                                   |
| TCP      | 3100  | Media Nodes    | Needed when *'Observability'* module is used (`observability` in `ENABLED_MODULES` global parameter) Media Nodes need access to this port to reach Loki.                                            |
| TCP      | 7880  | Media Nodes    | Media Nodes need access to this port for Ingress, Egress and Agents to reach load balanced LiveKit API.                                                                                             |
| TCP      | 9009  | Media Nodes    | Needed when *'Observability'* module is used. (`observability` in `ENABLED_MODULES` global parameter) Media Nodes need access to this port to reach Mimir.                                          |
| TCP      | 7000  | Media Nodes    | Media Nodes need access to this port to reach Redis Service.                                                                                                                                        |
| TCP      | 9100  | Media Nodes    | Media Nodes need access to this port to reach MinIO.                                                                                                                                                |
| TCP      | 20000 | Media Nodes    | Media Nodes need access to this port to reach MongoDB.                                                                                                                                              |

**Outbound Rules**

Typically, all outbound traffic is allowed.

**Media Nodes**

**Inbound Rules**

| Protocol | Ports       | Source          | Description                                                                                                                                                           |
| -------- | ----------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UDP      | 443         | 0.0.0.0/0, ::/0 | STUN/TURN over UDP.                                                                                                                                                   |
| TCP      | 7881        | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Pion.                                                                                                                   |
| UDP      | 7885        | 0.0.0.0/0, ::/0 | Needed if you want to ingest WebRTC using WHIP.                                                                                                                       |
| UDP      | 50000-60000 | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over UDP.                                                                                                                             |
| TCP      | 50000-60000 | 0.0.0.0/0, ::/0 | Needed for WebRTC media traffic over TCP with Mediasoup.                                                                                                              |
| TCP      | 1935        | Master Node     | Needed if you want to ingest RTMP streams using Ingress service. Master Node needs access to this port to reach Ingress RTMP service and expose it using TLS (RTMPS). |
| TCP      | 5349        | Master Node     | Needed if you have configured TURN with a domain for TLS. Master Node needs access to this port to reach TURN service and expose it using TLS (TURNS).                |
| TCP      | 7880        | Master Node     | LiveKit API. Master Node needs access to load balance LiveKit API and expose it through HTTPS.                                                                        |
| TCP      | 8080        | Master Node     | Needed if you want to ingest WebRTC streams using WHIP. Master Node needs access to this port to reach WHIP HTTP service.                                             |

**Outbound Rules**

Typically, all outbound traffic is allowed.

**Proxy Server**

And the inbound rules for the proxy server would be as follows:

| Protocol | Ports | Source          | Description                                         |
| -------- | ----- | --------------- | --------------------------------------------------- |
| TCP      | 80    | 0.0.0.0/0, ::/0 | HTTP redirection to HTTPS.                          |
| TCP      | 443   | 0.0.0.0/0, ::/0 | HTTPS access to the OpenVidu API and TURN with TLS. |
| TCP      | 1935  | 0.0.0.0/0, ::/0 | RTMP with TLS.                                      |

**3. Install OpenVidu Elastic with `--external-proxy` flag**

To deploy OpenVidu Elastic with an external proxy, you must use the CLI installation command with the `--external-proxy` flag. The command to install OpenVidu Elastic with an external proxy is as follows:

**Install Master Node**

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_master_node.sh) \
    --no-tty --install \
    --node-role='master-node' \
    --openvidu-pro-license='xxxxx' \
    --domain-name='openvidu.example.io' \
    --turn-domain-name='turn.example.io' \
    --enabled-modules='observability,v2compatibility,openviduMeet' \
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
    --meet-initial-admin-password='xxxxx' \
    --meet-initial-api-key='xxxxx' \
    --private-ip='<MASTER_NODE_PRIVATE_IP>' \
    --external-proxy
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

Notes:

- `--openvidu-pro-license` is mandatory. You can get a 15-day free trial license key by [creating an OpenVidu account](https://openvidu.io/account/) .
- Replace `openvidu.example.io` with your FQDN.
- Replace `turn.example.io` with your TURN server FQDN.
- `--private-ip` is very important. It should not change and Media Nodes should be able to reach the Master Node using this IP. Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
- Depending on the RTC engine, the argument `--rtc-engine` can be `pion` or `mediasoup`.

**Install Media Nodes**

To install a Media Node, you can use the following command:

```bash
sh <(curl -fsSL http://get.openvidu.io/pro/elastic/latest/install_ov_media_node.sh) \
    --no-tty --install \
    --node-role='media-node' \
    --master-node-private-ip='<MASTER_NODE_PRIVATE_IP>' \
    --redis-password='xxxxx'
```

Note

In case you want to deploy a specific version, just replace `latest` with the desired version. For example: `3.8.0`.

- The `--master-node-private-ip` is the private IP of the Master Node. Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
- The `--redis-password` is the password used to connect to the Redis service. Replace `xxxxx` with the same password used in the Master Node installation.

**4. Configure the external proxy**

We will use [Nginx](https://www.nginx.com/) as the proxy server, but the configuration can be adapted to other proxy servers.

In this configuration, the proxy uses **SNI-based Layer 4 routing** to separate API and TURN traffic on port `443`. The API domain is routed to a local HTTP reverse-proxy server on port `7880`, which then forwards requests to the OpenVidu node. The TURN domain is forwarded directly to port `5349` on the OpenVidu node. This gives you an `http` block where you can add custom routing, rate limiting, access control, or additional headers.

The proxy needs these rules:

1. **Redirect HTTP to HTTPS** on port `80`.
1. **Proxy TLS traffic on port `443`** using SNI to route:
   - API domain → local `127.0.0.1:7880` → HTTP reverse-proxy → OpenVidu node on port `7880`.
   - TURN domain → OpenVidu node on port `5349`.
1. **Proxy TLS traffic on port `1935`** to the OpenVidu node on port `1945` (RTMP).

The following is an example Nginx configuration file:

```nginx
events {
    worker_connections 10240;
}

stream {

    upstream api_backend {
        server 127.0.0.1:7880;
    }

    upstream turn_backend {
        server <MASTER_NODE_PRIVATE_IP>:5349;
    }

    upstream rtmp_backend {
        server <MASTER_NODE_PRIVATE_IP>:1945;
    }

    # Use SNI to determine which upstream server to proxy to
    map $ssl_server_name $upstream {
        openvidu.example.io api_backend;
        turn.example.io turn_backend;
    }

    # Use SNI to determine which certificate to use
    map $ssl_server_name $certificate {
        openvidu.example.io /etc/nginx/ssl/openvidu-cert.pem;
        turn.example.io /etc/nginx/ssl/turn-cert.pem;
    }

    # Use SNI to determine which private key to use
    map $ssl_server_name $private_key {
        openvidu.example.io /etc/nginx/ssl/openvidu-privkey.pem;
        turn.example.io /etc/nginx/ssl/turn-privkey.pem;
    }

    # Proxy for API and TURN
    server {
        listen 443 ssl;
        listen [::]:443 ssl;
        ssl_protocols TLSv1.2 TLSv1.3;

        proxy_connect_timeout 10s;
        proxy_timeout 30s;

        ssl_certificate $certificate;
        ssl_certificate_key $private_key;

        proxy_pass $upstream;
    }

    # RTMP
    server {
        listen 1935 ssl;
        listen [::]:1935 ssl;
        ssl_protocols TLSv1.2 TLSv1.3;

        proxy_connect_timeout 10s;
        proxy_timeout 30s;

        ssl_certificate /etc/nginx/ssl/openvidu-cert.pem;
        ssl_certificate_key /etc/nginx/ssl/openvidu-privkey.pem;

        proxy_pass rtmp_backend;
    }
}

# Redirect HTTP to HTTPS and reverse proxy API traffic
http {
    server {
        listen 80;
        listen [::]:80;
        return 301 https://$host$request_uri;
    }

    upstream api_http_backend {
        server <MASTER_NODE_PRIVATE_IP>:7880;
    }

    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    server {
        listen 7880;

        location / {
            proxy_pass http://api_http_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
        }
    }
}
```

Customizable HTTP block

The `http` block gives you full control over HTTP-level routing. You can add custom `location` blocks, rate limiting, access control, or additional headers to suit your infrastructure needs.

Notes:

- Replace `openvidu.example.io` and `turn.example.io` with your domain names. These domain names must be configured in your DNS to point to the proxy server.
- Replace `<MASTER_NODE_PRIVATE_IP>` with the private IP of the Master Node.
- You can also have a proxy in the same machine as the Master Node, simply replace `<MASTER_NODE_PRIVATE_IP>` with `127.0.0.1`.

If you want to force all traffic including WebRTC to go through the external proxy, check the [Force media traffic through port 443](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/force-single-port/index.md) guide.

**High Availability**

The High Availability deployment already has a way to configure an external proxy (described as a Network Load Balancer), which is explained [in this section](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/install-nlb/index.md).
