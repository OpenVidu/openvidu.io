To run the client application tutorial, you need [Node.js :fontawesome-solid-external-link:{.external-link-icon}](https://nodejs.org/en/download){:target="_blank"} installed on your development computer.

1. Navigate into the application client directory:

    ```bash
    cd openvidu-livekit-tutorials/application-client/openvidu-vue
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run the application:

    ```bash
    npm start
    ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080){:target="_blank"}. You should see a screen like this:

/// html | div.grid-container

/// html | div.grid-50
![Join screen of the Vue tutorial app](/assets/images/platform/tutorials/application-client/join-vue.png){ .round-corners loading=lazy }
///

/// html | div.grid-50
![Video call room of the Vue tutorial app](/assets/images/platform/tutorials/application-client/room-vue.png){ .round-corners loading=lazy }
///

///

--8<-- "tutorials/testing-other-devices.md"
