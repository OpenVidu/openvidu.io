If you have a production deployment of OpenVidu Meet (installed in a server following [deployment steps :fontawesome-solid-external-link:{.external-link-icon}](/meet/deployment/basic.md){:target="\_blank"}), you can connect this tutorial to it by following these steps:

1. **Update the server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in the `.env` file to point to your OpenVidu Meet production deployment URL.

    ```text
    # Example for a production deployment
    OV_MEET_SERVER_URL=https://your-openvidu-meet-domain.com/meet
    ```

2. **Update the API key**: Ensure the `OV_MEET_API_KEY` environment variable in the `.env` file matches the API key configured in your production deployment. See [Generate an API Key :fontawesome-solid-external-link:{.external-link-icon}](/meet/embedded/reference/rest-api.md#generate-an-api-key){:target="\_blank"} section to learn how to obtain it.

    ```text
    OV_MEET_API_KEY=your-production-api-key
    ```

3. **Update the OpenVidu Meet WebComponent script URL**: In the `public/index.html` file, update the `<script>` tag that includes the OpenVidu Meet WebComponent to use the same base URL as above.

    ```html
    <script src="https://your-openvidu-meet-domain.com/meet/v1/openvidu-meet.js"></script>
    ```

4. **Restart the tutorial** to apply the changes:

    ```bash
    npm start
    ```

!!! warning "Make this tutorial accessible from other computers or phones"

    By default, this tutorial runs on `http://localhost:6080` and is only accessible from the local machine. If you want to access it from other computers or phones, you have the following options:

    - **Use tunneling tools**: Configure tools like [VS Code port forwarding :fontawesome-solid-external-link:{.external-link-icon}](https://code.visualstudio.com/docs/debugtest/port-forwarding){:target="_blank"}, [ngrok :fontawesome-solid-external-link:{.external-link-icon}](https://ngrok.com/){:target="_blank"}, [localtunnel :fontawesome-solid-external-link:{.external-link-icon}](https://localtunnel.github.io/www/){:target="_blank"}, or similar services to expose this tutorial to the internet with a secure (HTTPS) public URL.
    - **Deploy to a server**: Upload this tutorial to a web server and configure it to be accessible with a secure (HTTPS) public URL. This can be done by updating the source code to manage SSL certificates or configuring a reverse proxy (e.g., Nginx, Apache) to serve it.
