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

3. Enable the Speech Processing agent

    Modify file [`openvidu-local-deployment/community/agent-speech-processing.yaml`](https://github.com/OpenVidu/openvidu-local-deployment/blob/3.3.0/community/agent-speech-processing.yaml){:target=_blank} to enable the Speech Processing agent. At least you need to set the following properties:

    ```yaml
    enabled: true
    
    live_captions:

        processing: automatic

        provider: YOUR_SPEECH_PROVIDER

        # Followed by your provider specific configuration
    ```

    !!! info
        Visit [**Supported AI providers**](../../ai/live-captions.md#supported-ai-providers) for more information about the available providers and their specific configuration. Many of them provide a free tier, so you can quickly test them without any cost!

4.  Run OpenVidu

    ```bash
    docker compose up
    ```
