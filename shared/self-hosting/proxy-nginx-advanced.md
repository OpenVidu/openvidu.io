We will use [Nginx :fontawesome-solid-external-link:{.external-link-icon}](https://www.nginx.com/){:target="_blank"} as the proxy server, but the configuration can be adapted to other proxy servers.

In this configuration, the proxy uses **SNI-based Layer 4 routing** to separate API and TURN traffic on port `443`. The API domain is routed to a local HTTP reverse-proxy server on port `7880`, which then forwards requests to the OpenVidu node. The TURN domain is forwarded directly to port `5349` on the OpenVidu node. This gives you an `http` block where you can add custom routing, rate limiting, access control, or additional headers.

The proxy needs these rules:

1. **Redirect HTTP to HTTPS** on port `80`.
2. **Proxy TLS traffic on port `443`** using SNI to route:
    - API domain → local `127.0.0.1:7880` → HTTP reverse-proxy → OpenVidu node on port `7880`.
    - TURN domain → OpenVidu node on port `5349`.
3. **Proxy TLS traffic on port `1935`** to the OpenVidu node on port `1945` (RTMP).

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

!!! info "Customizable HTTP block"
    The `http` block gives you full control over HTTP-level routing. You can add custom `location` blocks, rate limiting, access control, or additional headers to suit your infrastructure needs.
