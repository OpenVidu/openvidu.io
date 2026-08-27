To run the client application tutorial, you need [Node.js :fontawesome-solid-external-link:{.external-link-icon}](https://nodejs.org/en/download){:target="_blank"} installed on your development computer.

1. Navigate into the application client directory:

    ```bash
    cd openvidu-livekit-tutorials/application-client/openvidu-electron
    ```

2. Install the required dependencies:

    ```bash
    npm install
    ```

3. Run the application:

    ```bash
    npm start
    ```

The application will seamlessly initiate as a native desktop program, adapting itself to the specific operating system you are using. Once the application is open, you should see a screen like this:

/// html | div.grid-container

/// html | div.grid-50
![Join screen of the Electron tutorial app](/assets/images/platform/tutorials/application-client/join-electron.png){ .round-corners loading=lazy }
///

/// html | div.grid-50
![Video call room of the Electron tutorial app](/assets/images/platform/tutorials/application-client/room-electron.png){ .round-corners loading=lazy }
///

///

!!! info "Running your application client from other devices in your local network"

    One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates. For more information, see section [Accessing your local deployment from other devices on your network](/docs/self-hosting/local.md#accessing-your-local-deployment-from-other-devices-on-your-network).
