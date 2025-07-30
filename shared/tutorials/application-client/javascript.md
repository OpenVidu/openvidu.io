To run the client application tutorial, you need an HTTP web server installed on your development computer. A great option is [http-server](https://github.com/http-party/http-server){:target="\_blank"}. You can install it via [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm){:target="\_blank"}:

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

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080){:target="\_blank"}. You should see a screen like this:

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/application-clients/join-js.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/application-clients/join-js.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/application-clients/room-js.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/application-clients/room-js.png" loading="lazy"/></a></p></div>

</div>

--8<-- "shared/tutorials/testing-other-devices.md"
