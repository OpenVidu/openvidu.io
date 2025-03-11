=== "Nginx Configuration"

    If you have installed OpenVidu with both domains (`openvidu.example.io` and `turn.example.io`) and both domains are pointing to the same proxy, the proxy needs to be configured as a Layer 4 proxy (TCP) because the TURN and HTTP traffic share the same port (443). We will use the Server Name Indication (SNI) of the TLS handshake to discern the traffic. The rules would be as follows:

    1. Configure a redirect rule to redirect HTTP traffic to HTTPS in port 80.
    2. Configure a rule to proxy all Layer 4 TLS incoming proxy traffic in port 443 to the OpenVidu Master Node in port 7880 for domain `openvidu.example.io`. This is for the HTTP traffic of the OpenVidu API and other services.
    3. Configure a rule to proxy all Layer 4 TLS incoming proxy traffic in port 443 to the OpenVidu Master Node in port 5349 for domain `turn.example.io`. This is for the TURN service.
    4. Configure a rule to proxy all Layer 4 TLS incoming proxy traffic in port 1935 to the OpenVidu Master Node in port 1945 for RTMP traffic.

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
