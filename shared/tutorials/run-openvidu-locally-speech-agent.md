1.  Download OpenVidu:

    ```bash
    git clone https://github.com/OpenVidu/openvidu-local-deployment -b 3.5.0
    ```

2.  Configure the local deployment:

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

3. Enable the Speech Processing agent:

    Modify file [`openvidu-local-deployment/community/agent-speech-processing.yaml` :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/OpenVidu/openvidu-local-deployment/blob/3.5.0/community/agent-speech-processing.yaml){:target=_blank} to enable the Speech Processing agent. At least you need to set the following properties:

    ```yaml
    enabled: true # Enables the agent

    live_captions:

        processing: automatic # Configures the agent to connect to new Rooms automatically

        provider: YOUR_SPEECH_PROVIDER # Configures the AI provider for speech-to-text processing

        # Followed by your provider specific configuration
    ```

    !!! info
        The default `provider` property is set to **`vosk`**, which is a local, open-source, and free-to-use option.<br>
        Visit [**Supported AI providers**](../../ai/live-captions.md#supported-ai-providers) to see the full list of available AI providers, both local and cloud-based.

4.  Run OpenVidu:

    ```bash
    docker compose up
    ```
