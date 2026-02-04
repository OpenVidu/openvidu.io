To access this tutorial from other computers or phones, follow these steps:

1.  **Ensure network connectivity**: Make sure your device (computer or phone) is connected to the same network as the machine running OpenVidu Meet and this tutorial.

2.  **Configure OpenVidu Meet for network access**: Start OpenVidu Meet by following the instructions in the [Accessing OpenVidu Meet from other computers or phones :fontawesome-solid-external-link:{.external-link-icon}](/meet/deployment/local.md#accessing-openvidu-meet-from-other-computers-or-phones){:target="_blank"} section.

3.  **Update the OpenVidu Meet server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in your `.env` file to match the URL shown when OpenVidu Meet starts.

    ```text
    # Example for IP address 192.168.1.100
    OV_MEET_SERVER_URL=https://192-168-1-100.openvidu-local.dev:9443/meet
    ```

4.  **Update the OpenVidu Meet WebComponent script URL**: In the `public/index.html` file, update the `<script>` tag that includes the OpenVidu Meet WebComponent to use the same base URL as above.

    ```html
    <script src="http://192-168-1-100.openvidu-local.dev:9443/meet/v1/openvidu-meet.js"></script>
    ```

5.  **Restart the tutorial** to apply the changes:

    ```bash
    npm start
    ```

6.  **Access the tutorial**: Open your browser and navigate to `https://192-168-1-100.openvidu-local.dev:6443` (replacing `192-168-1-100` with your actual private IP) on the computer where you started the tutorial or any device in the same network.
