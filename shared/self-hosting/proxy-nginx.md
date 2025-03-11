=== "Nginx Configuration (withouth optional TURN domain)"

    If you only configure the main domain `openvidu.example.com` to be served by OpenVidu, you simply need to:

    1. Configure a rule to redirect HTTP traffic to HTTPS in port 80.
    2. Configure a rule to proxy all Layer 7 HTTPS incoming proxy traffic in port 443 to the OpenVidu Master Node in port 7880.
    3. Configure a rule to proxy all Layer 4 TLS incoming proxy traffic in port 1935 to the OpenVidu Master Node in port 1945.

    As RTMP is a Layer 4 protocol, you need to configure a separate `stream` block in the Nginx configuration file, while the rest of the rules can be configured in the `http` block.

    The following is an example of an Nginx configuration file that includes all the rules mentioned above:

    ```nginx
    events {
        worker_connections 10240;
    }

    http {

        upstream api_backend {
            server <MASTER_NODE_PRIVATE_IP>:7880;
        }

        # Redirect HTTP to HTTPS
        server {
            listen 80;
            listen [::]:80;
            return 301 https://$host$request_uri;
        }

        # HTTPS Layer 7 proxy
        server {
            listen 443 ssl;
            listen [::]:443 ssl;
            ssl_protocols TLSv1.2 TLSv1.3;

            ssl_certificate /etc/nginx/ssl/openvidu-cert.pem;
            ssl_certificate_key /etc/nginx/ssl/openvidu-privkey.pem;

            location / {
                # Proxy to OpenVidu
                proxy_pass http://api_backend;

                # Add WebSocket support
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";

                # Proxy headers
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;

                # Timeouts
                proxy_connect_timeout 10s;
                proxy_read_timeout 30s;
                proxy_send_timeout 30s;
            }
        }
    }

    stream {

        upstream rtmp_backend {
            server <MASTER_NODE_PRIVATE_IP>:1945;
        }

        # RTMP Layer 4 proxy
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

    You can create an `stream` block for the HTTPS rule as well for consistency instead of creating an `http` block. In this way all rules are in the `stream` block. The rules would be these:

    1. Configure a rule to redirect HTTP traffic to HTTPS in port 80.
    2. Configure a rule to proxy all Layer 4 TLS incoming proxy traffic in port 443 to the OpenVidu Master Node in port 7880.
    3. Configure a rule to proxy all Layer 4 TLS incoming proxy traffic in port 1935 to the OpenVidu Master Node in port 1945.

    The following is an example of an Nginx configuration file that includes all the rules mentioned above:

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
