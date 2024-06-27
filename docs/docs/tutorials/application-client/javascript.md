# openvidu-js

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-client/openvidu-js){ .md-button target=\_blank }

This tutorial is a simple video-call application built with plain **JavaScript**, **HTML** and **CSS** that allows:

-   Joining a video call room by requesting a token from any [application server](../application-server/index.md).
-   Publishing your camera and microphone.
-   Subscribing to all other participants' video and audio tracks automatically.
-   Leaving the video call room at any time.

It uses the [LiveKit JS SDK](https://docs.livekit.io/client-sdk-js){:target="\_blank"} to connect to the LiveKit server and interact with the video call room.

## Running this tutorial

#### 1. Run OpenVidu Server

--8<-- "docs/docs/tutorials/shared/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

### 3. Run a server application

--8<-- "docs/docs/tutorials/shared/application-server-tabs.md"

### 4. Run the client application

To run the client application tutorial, you need an HTTP web server installed on your development computer. A great option is [http-server](https://github.com/indexzero/http-server){:target="\_blank"}. You can install it via [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm){:target="\_blank"}:

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

<div class="grid-50"><p><a class="glightbox" href="/assets/images/application-clients/join-js.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/join-js.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/application-clients/room-js.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/room-js.png" loading="lazy"/></a></p></div>

</div>

--8<-- "docs/docs/tutorials/shared/testing-other-devices.md"

## Understanding the code

This application is designed to be beginner-friendly and consists of only three essential files that are located in the `src` directory:

-   `app.js`: This is the main JavaScript file for the sample application. It uses the [LiveKit JS SDK](https://docs.livekit.io/client-sdk-js){:target="\_blank"} to connect to the LiveKit server and interact with the video call room.
-   `index.html`: This HTML file is responsible for creating the user interface. It contains the form to connect to a video call and the video call layout.
-   `styles.css`: This file contains CSS classes that are used to style the `index.html` page.

To use the LiveKit JS SDK in your application, you need to include the library in your HTML file. You can do this by adding the following script tag to the `<head>` section of your HTML file:

```html title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/index.html#L32' target='_blank'>index.html</a>" linenums="32"
<script src="https://cdn.jsdelivr.net/npm/livekit-client@2.1.5/dist/livekit-client.umd.js"></script>
```

Then, you can use the `LivekitClient` object in your JavaScript code by referencing it from the `window` object under `LivekitClient`. When accessing symbols from the class, you will need to prefix them with `LivekitClient.`. For example, `Room` becomes `LivekitClient.Room`.

Now let's see the code of the `app.js` file:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L1-L28' target='_blank'>app.js</a>" linenums="1"
// For local development, leave these variables empty
// For production, configure them with correct URLs depending on your deployment
var APPLICATION_SERVER_URL = ""; // (1)!
var LIVEKIT_URL = ""; // (2)!
configureUrls();

const LivekitClient = window.LivekitClient; // (3)!
var room; // (4)!

function configureUrls() {
    // If APPLICATION_SERVER_URL is not configured, use default value from local development
    if (!APPLICATION_SERVER_URL) {
        if (window.location.hostname === "localhost") {
            APPLICATION_SERVER_URL = "http://localhost:6080/";
        } else {
            APPLICATION_SERVER_URL = "https://" + window.location.hostname + ":6443/";
        }
    }

    // If LIVEKIT_URL is not configured, use default value from local development
    if (!LIVEKIT_URL) {
        if (window.location.hostname === "localhost") {
            LIVEKIT_URL = "ws://localhost:7880/";
        } else {
            LIVEKIT_URL = "wss://" + window.location.hostname + ":7443/";
        }
    }
}
```

1. The URL of the application server.
2. The URL of the LiveKit server.
3. The LivekitClient object, which is the entry point to the LiveKit JS SDK.
4. The room object, which represents the video call room.

The `app.js` file defines the following variables:

-   `APPLICATION_SERVER_URL`: The URL of the application server. This variable is used to make requests to the server to obtain a token for joining the video call room.
-   `LIVEKIT_URL`: The URL of the LiveKit server. This variable is used to connect to the LiveKit server and interact with the video call room.
-   `LivekitClient`: The LiveKit JS SDK object, which is the entry point to the LiveKit JS SDK.
-   `room`: The room object, which represents the video call room.

--8<-- "docs/docs/tutorials/shared/configure-urls.md"

---

### Joining a Room

After the user specifies their participant name and the name of the room they want to join, when they click the `Join` button, the `joinRoom()` function is called:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L30-L74' target='_blank'>app.js</a>" linenums="30"
async function joinRoom() {
    // Initialize a new Room object
    room = new LivekitClient.Room(); // (1)!

    // Specify the actions when events take place in the room
    // On every new Track received...
    room.on(LivekitClient.RoomEvent.TrackSubscribed, (track, _publication, participant) => {
        // (2)!
        addTrack(track, participant.identity);
    });

    // On every new Track destroyed...
    room.on(LivekitClient.RoomEvent.TrackUnsubscribed, (track, _publication, participant) => {
        // (3)!
        track.detach();
        document.getElementById(track.sid)?.remove();

        if (track.kind === "video") {
            removeVideoContainer(participant.identity);
        }
    });

    try {
        // Get the room name and participant name from the form
        const roomName = document.getElementById("room-name").value; // (4)!
        const userName = document.getElementById("participant-name").value;

        // Get a token from your application server with the room name and participant name
        const token = await getToken(roomName, userName); // (5)!

        // Connect to the room with the LiveKit URL and the token
        await room.connect(LIVEKIT_URL, token); // (6)!

        // Hide the 'Join room' page and show the 'Room' page
        document.getElementById("room-title").innerText = roomName; // (7)!
        document.getElementById("join").hidden = true;
        document.getElementById("room").hidden = false;

        // Publish your camera and microphone
        await room.localParticipant.enableCameraAndMicrophone(); // (8)!
        const localVideoTrack = this.room.localParticipant.videoTrackPublications.values().next().value.track;
        addTrack(localVideoTrack, userName, true);
    } catch (error) {
        console.log("There was an error connecting to the room:", error.message);
    }
}
```

1. Initialize a new `Room` object.
2. Event handling for when a new track is received in the room.
3. Event handling for when a track is destroyed.
4. Get the room name and participant name from the form.
5. Get a token from the application server with the room name and participant name.
6. Connect to the room with the LiveKit URL and the token.
7. Hide the "Join room" page and show the "Room" page.
8. Publish your camera and microphone.

The `joinRoom()` function performs the following actions:

1.  It creates a new `Room` object using `LivekitClient.Room()`. This object represents the video call room.
2.  Event handling is configured for different scenarios within the room. These events are fired when new tracks are subscribed to and when existing tracks are unsubscribed.

    -   **`LivekitClient.RoomEvent.TrackSubscribed`**: This event is triggered when a new track is received in the room. It handles the attachment of the track to the HTML page, assigning an ID, and appending it to the `layout-container` element. If the track is of kind `video`, a `video-container` is created and participant data is appended as well.

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L76-L88' target='_blank'>app.js</a>" linenums="76"
    function addTrack(track, participantIdentity, local = false) {
        const element = track.attach(); // (1)!
        element.id = track.sid;

        /* If the track is a video track, we create a container and append the video element to it
        with the participant's identity */
        if (track.kind === "video") {
            const videoContainer = createVideoContainer(participantIdentity, local);
            videoContainer.append(element);
            appendParticipantData(videoContainer, participantIdentity + (local ? " (You)" : ""));
        } else {
            document.getElementById("layout-container").append(element);
        }
    }
    ```

    1. Attach the track to an HTML element.

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L114-L134' target='_blank'>app.js</a>" linenums="114"
    function createVideoContainer(participantIdentity, local = false) {
        const videoContainer = document.createElement("div");
        videoContainer.id = `camera-${participantIdentity}`;
        videoContainer.className = "video-container";
        const layoutContainer = document.getElementById("layout-container");

        if (local) {
            layoutContainer.prepend(videoContainer);
        } else {
            layoutContainer.append(videoContainer);
        }

        return videoContainer;
    }

    function appendParticipantData(videoContainer, participantIdentity) {
        const dataElement = document.createElement("div");
        dataElement.className = "participant-data";
        dataElement.innerHTML = `<p>${participantIdentity}</p>`;
        videoContainer.prepend(dataElement);
    }
    ```

    -   **`LivekitClient.RoomEvent.TrackUnsubscribed`**: This event occurs when a track is destroyed, and it takes care of detaching the track from the HTML page and removing it from the DOM. If the track is a `video` track, `video-container` with the participant's identity is removed as well.

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L136-L139' target='_blank'>app.js</a>" linenums="136"
    function removeVideoContainer(participantIdentity) {
        const videoContainer = document.getElementById(`camera-${participantIdentity}`);
        videoContainer?.remove();
    }
    ```

    These event handlers are essential for managing the behavior of tracks within the video call.

    !!! info "Take a look at all events"

        You can take a look at all the events in the [Livekit Documentation](https://docs.livekit.io/client-sdk-js/enums/RoomEvent.html)

3.  It retrieves the room name and participant name from the form.
4.  It requests a token from the application server using the room name and participant name. This is done by calling the `getToken()` function:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L148-L180' target='_blank'>app.js</a>" linenums="148"
    /**
     * --------------------------------------------
     * GETTING A TOKEN FROM YOUR APPLICATION SERVER
     * --------------------------------------------
     * The method below request the creation of a token to
     * your application server. This prevents the need to expose
     * your LiveKit API key and secret to the client side.
     *
     * In this sample code, there is no user control at all. Anybody could
     * access your application server endpoints. In a real production
     * environment, your application server must identify the user to allow
     * access to the endpoints.
     */
    async function getToken(roomName, participantName) {
        const response = await fetch(APPLICATION_SERVER_URL + "token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                roomName,
                participantName
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Failed to get token: ${error.errorMessage}`);
        }

        const token = await response.json();
        return token.token;
    }
    ```

    This function sends a POST request using `fetch()` to the application server's `/token` endpoint. The request body contains the room name and participant name. The server responds with a token that is used to connect to the room.

5.  It connects to the room using the LiveKit URL and the token.
6.  It updates the UI to hide the "Join room" page and show the "Room" layout.
7.  It publishes the camera and microphone tracks to the room using `room.localParticipant.enableCameraAndMicrophone()`, which asks the user for permission to access their camera and microphone at the same time. The local video track is then added to the layout.

---

### Leaving the Room

When the user wants to leave the room, they can click the `Leave Room` button. This action calls the `leaveRoom()` function:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-js/src/app.js#L91-L105' target='_blank'>app.js</a>" linenums="91"
async function leaveRoom() {
    // Leave the room by calling 'disconnect' method over the Room object
    await room.disconnect(); // (1)!

    // Remove all HTML elements inside the layout container
    removeAllLayoutElements(); // (2)!

    // Back to 'Join room' page
    document.getElementById("join").hidden = false; // (3)!
    document.getElementById("room").hidden = true;
}

// (4)!
window.onbeforeunload = () => {
    room?.disconnect();
};
```

1. Disconnect the user from the room.
2. Remove all HTML elements inside the layout container.
3. Show the "Join room" page and hide the "Room" layout.
4. Call the `disconnect()` method on the `room` object when the user closes the tab or navigates to another page.

The `leaveRoom()` function performs the following actions:

-   It disconnects the user from the room by calling the `disconnect()` method on the `room` object.
-   It removes all HTML elements inside the layout container by calling the `removeAllLayoutElements()` function.
-   It shows the "Join room" page and hides the "Room" layout.

The `window.onbeforeunload` event is used to ensure that the user is disconnected from the room before the page is unloaded. This event is triggered when the user closes the tab or navigates to another page.
