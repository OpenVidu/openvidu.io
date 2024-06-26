1.  Download OpenVidu

    ```bash
    git clone https://github.com/OpenVidu/openvidu-local-deployment
    ```

2.  Configure the local deployment

    === ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

        ```powershell
        cd openvidu-local-deployment/community
        .\configure_lan_private_ip_windows.bat
        ```

    === ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

        ```bash
        cd openvidu-local-deployment/community
        ./configure_lan_private_ip_macos.sh
        ```

    === ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

        ```bash
        cd openvidu-local-deployment/community
        ./configure_lan_private_ip_linux.sh
        ```

3.  Run OpenVidu

    ```bash
    docker compose up
    ```
