1.  Download OpenVidu

    ```bash
    git clone https://github.com/OpenVidu/openvidu-local-deployment -b 3.3.0
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

3. Deploy a Storage Account in Azure and add a container with the name that you want.

4. Change in the egress.yaml the S3 configuration for the Azure configuration you will find commented and fill the configuration with your credentials

5.  Run OpenVidu

    ```bash
    docker compose up
    ```
