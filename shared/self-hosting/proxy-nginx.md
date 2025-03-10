=== "Nginx Configuration"

    ```nginx
    events {
        worker_connections 10240;
    }

    # Redirect HTTP to HTTPS
    http {
        server {
            listen 80;
            listen [::]:80;
            return 301 https://$host$request_uri;
        }
    }

    stream {

        upstream api_backend {
            server <MASTER_NODE_PRIVATE_IP>:7880;
        }

        upstream rtmp_backend {
            server <MASTER_NODE_PRIVATE_IP>:1945;
        }

        # Proxy for API and TURN
        server {
            listen 443 ssl;
            listen [::]:443 ssl;
            ssl_protocols TLSv1.2 TLSv1.3;

            proxy_connect_timeout 10s;
            proxy_timeout 30s;

            ssl_certificate /etc/nginx/ssl/openvidu-cert.pem;
            ssl_certificate_key /etc/nginx/ssl/openvidu-privkey.pem;

            proxy_pass api_backend;
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

    ```
