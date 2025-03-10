=== "Nginx Configuration (With TLS for TURN)"

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
    ```
