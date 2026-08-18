To run the client application tutorial, you need an HTTP web server installed on your development computer. A great option is [http-server :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/http-party/http-server){:target="_blank"}. You can install it via [NPM :fontawesome-solid-external-link:{.external-link-icon}](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm){:target="_blank"}:

```bash
npm install -g http-server
```

1. Navigate into the application client directory:

    ```bash
    cd openvidu-livekit-tutorials/application-client/openvidu-js
    ```

2. Serve the application:

    ```bash
    http-server -p 5080 ./src
    ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080){:target="_blank"}. You should see a screen like this:

/// html | div.grid-container

/// html | div.grid-50
![Join screen of the JavaScript tutorial app](/assets/images/platform/tutorials/application-client/join-js.png){ loading=lazy }
///

/// html | div.grid-50
![Video call room of the JavaScript tutorial app](/assets/images/platform/tutorials/application-client/room-js.png){ loading=lazy }
///

///

--8<-- "tutorials/testing-other-devices.md"
