# openvidu-react

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-client/openvidu-react){ .md-button target=\_blank }

This tutorial is a simple video-call application built with **React** that allows:

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

To run the client application tutorial, you need [Node](https://nodejs.org/en/download){:target="\_blank"} installed on your development computer.

1. Navigate into the application client directory:

    ```bash
    cd openvidu-livekit-tutorials/application-client/openvidu-react
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run the application:

    ```bash
    npm start
    ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080){:target="\_blank"}. You should see a screen like this:

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/application-clients/join-react.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/join-react.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/application-clients/room-react.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/room-react.png" loading="lazy"/></a></p></div>

</div>

--8<-- "docs/docs/tutorials/shared/testing-other-devices.md"

## Understanding the code

This React project has been generated using the Vite. You may come across various configuration files and other items that are not essential for this tutorial. Our focus will be on the key files located within the `src/` directory:

-   `App.tsx`: This file defines the main application component. It is responsible for handling tasks such as joining a video call and managing the video calls themselves.
-   `App.css`: This file contains the styles for the main application component.
-   `VideoComponent.tsx`: This file defines the `VideoComponent`. This component is responsible for displaying video tracks along with participant's data. Its associated styles are in `VideoComponent.css`.
-   `AudioComponent.vue`: This file defines the `AudioComponent`. This component is responsible for displaying audio tracks.

To use the LiveKit JS SDK in a Vue application, you need to install the `livekit-client` package. This package provides the necessary classes and methods to interact with the LiveKit server. You can install it using the following command:

```bash
npm install livekit-client
```

Now let's see the code of the `App.tsx` file:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/App.tsx#L14-L51' target='_blank'>App.tsx</a>" linenums="14"
type TrackInfo = { // (1)!
    trackPublication: RemoteTrackPublication;
    participantIdentity: string;
};

// For local development, leave these variables empty
// For production, configure them with correct URLs depending on your deployment
let APPLICATION_SERVER_URL = ""; // (2)!
let LIVEKIT_URL = ""; // (3)!
configureUrls();

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

function App() {
    const [room, setRoom] = useState<Room | undefined>(undefined); // (4)!
    const [localTrack, setLocalTrack] = useState<LocalVideoTrack | undefined>(undefined); // (5)!
    const [remoteTracks, setRemoteTracks] = useState<TrackInfo[]>([]); // (6)!

    const [participantName, setParticipantName] = useState("Participant" + Math.floor(Math.random() * 100)); // (7)!
    const [roomName, setRoomName] = useState("Test Room"); // (8)!
```

1. `TrackInfo` type, which groups a track publication with the participant's identity.
2. The URL of the application server.
3. The URL of the LiveKit server.
4. The room object, which represents the video call room.
5. The local video track, which represents the user's camera.
6. The remote tracks array.
7. The participant's name.
8. The room name.

The `App.tsx` file defines the following variables:

-   `APPLICATION_SERVER_URL`: The URL of the application server. This variable is used to make requests to the server to obtain a token for joining the video call room.
-   `LIVEKIT_URL`: The URL of the LiveKit server. This variable is used to connect to the LiveKit server and interact with the video call room.
-   `room`: The room object, which represents the video call room.
-   `localTrack`: The local video track, which represents the user's camera.
-   `remoteTracks`: An array of `TrackInfo` objects, which group a track publication with the participant's identity.
-   `participantName`: The participant's name.
-   `roomName`: The room name.

--8<-- "docs/docs/tutorials/shared/configure-urls.md"

---

### Joining a Room

After the user specifies their participant name and the name of the room they want to join, when they click the `Join` button, the `joinRoom()` function is called:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/App.tsx#L53-L89' target='_blank'>App.tsx</a>" linenums="53"
async function joinRoom() {
    // Initialize a new Room object
    const room = new Room(); // (1)!
    setRoom(room);

    // Specify the actions when events take place in the room
    // On every new Track received...
    room.on(
        RoomEvent.TrackSubscribed,
        (_track: RemoteTrack, publication: RemoteTrackPublication, participant: RemoteParticipant) => {
            // (2)!
            setRemoteTracks((prev) => [
                ...prev,
                { trackPublication: publication, participantIdentity: participant.identity }
            ]);
        }
    );

    // On every Track destroyed...
    room.on(RoomEvent.TrackUnsubscribed, (_track: RemoteTrack, publication: RemoteTrackPublication) => {
        // (3)!
        setRemoteTracks((prev) => prev.filter((track) => track.trackPublication.trackSid !== publication.trackSid));
    });

    try {
        // Get a token from your application server with the room name and participant name
        const token = await getToken(roomName, participantName); // (4)!

        // Connect to the room with the LiveKit URL and the token
        await room.connect(LIVEKIT_URL, token); // (5)!

        // Publish your camera and microphone
        await room.localParticipant.enableCameraAndMicrophone(); // (6)!
        setLocalTrack(room.localParticipant.videoTrackPublications.values().next().value.videoTrack);
    } catch (error) {
        console.log("There was an error connecting to the room:", (error as Error).message);
        await leaveRoom();
    }
}
```

1. Initialize a new `Room` object.
2. Event handling for when a new track is received in the room.
3. Event handling for when a track is destroyed.
4. Get a token from the application server with the room name and participant name from the form.
5. Connect to the room with the LiveKit URL and the token.
6. Publish your camera and microphone.

The `joinRoom()` function performs the following actions:

1.  It creates a new `Room` object. This object represents the video call room.

    !!! info

        When the room object is defined, the HTML template is automatically updated hiding the "Join room" page and showing the "Room" layout.

2.  Event handling is configured for different scenarios within the room. These events are fired when new tracks are subscribed to and when existing tracks are unsubscribed.

    -   **`RoomEvent.TrackSubscribed`**: This event is triggered when a new track is received in the room. It manages the storage of the new track in the `remoteTracks` array as a `TrackInfo` object containing the track publication and the participant's identity.

    -   **`RoomEvent.TrackUnsubscribed`**: This event occurs when a track is destroyed, and it takes care of removing the track from the `remoteTracks` array.

    These event handlers are essential for managing the behavior of tracks within the video call. You can further extend the event handling as needed for your application.

    !!! info "Take a look at all events"

        You can take a look at all the events in the [Livekit Documentation](https://docs.livekit.io/client-sdk-js/enums/RoomEvent.html)

3.  It requests a token from the application server using the room name and participant name. This is done by calling the `getToken()` function:

    ```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/App.tsx#L101-L133' target='_blank'>App.tsx</a>" linenums="101"
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
    async function getToken(roomName: string, participantName: string) {
        const response = await fetch(APPLICATION_SERVER_URL + "token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                roomName: roomName,
                participantName: participantName
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Failed to get token: ${error.errorMessage}`);
        }

        const data = await response.json();
        return data.token;
    }
    ```

    This function sends a POST request using `fetch()` to the application server's `/token` endpoint. The request body contains the room name and participant name. The server responds with a token that is used to connect to the room.

4.  It connects to the room using the LiveKit URL and the token.
5.  It publishes the camera and microphone tracks to the room using `room.localParticipant.enableCameraAndMicrophone()`, which asks the user for permission to access their camera and microphone at the same time. The local video track is then stored in the `localTrack` variable.

---

### Displaying Video and Audio Tracks

In order to display participants' video and audio tracks, the main component integrates the `VideoComponent` and `AudioComponent`.

```html title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/App.tsx#L187-L205' target='_blank'>App.tsx</a>" linenums="187"
<div id="layout-container">
    {localTrack && (
        <VideoComponent track={localTrack} participantIdentity={participantName} local={true} />
    )}
    {remoteTracks.map((remoteTrack) =>
        remoteTrack.trackPublication.kind === "video" ? (
            <VideoComponent
                key={remoteTrack.trackPublication.trackSid}
                track={remoteTrack.trackPublication.videoTrack!}
                participantIdentity={remoteTrack.participantIdentity}
            />
        ) : (
            <AudioComponent
                key={remoteTrack.trackPublication.trackSid}
                track={remoteTrack.trackPublication.audioTrack!}
            />
        )
    )}
</div>
```

This code snippet does the following:

-   If the property `localTrack` is defined, we display the local video track using the `VideoComponent`. The `local` property is set to `true` to indicate that the video track belongs to the local participant.

    !!! info

        The audio track is not displayed for the local participant because there is no need to hear one's own audio.

-   Then, we iterate over the `remoteTracks` array and, for each remote track, we create a `VideoComponent` or an `AudioComponent` depending on the track's kind (video or audio). The `participantIdentity` property is set to the participant's identity, and the `track` property is set to the video or audio track.

Let's see now the code of the `VideoComponent.txs` file:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/components/VideoComponent.tsx#L5-L32' target='_blank'>VideoComponent.tsx</a>" linenums="5"
interface VideoComponentProps {
    track: LocalVideoTrack | RemoteVideoTrack; // (1)!
    participantIdentity: string; // (2)!
    local?: boolean; // (3)!
}

function VideoComponent({ track, participantIdentity, local = false }: VideoComponentProps) {
    const videoElement = useRef<HTMLVideoElement | null>(null); // (4)!

    useEffect(() => {
        if (videoElement.current) {
            track.attach(videoElement.current); // (5)!
        }

        return () => {
            track.detach(); // (6)!
        };
    }, [track]);

    return (
        <div id={"camera-" + participantIdentity} className="video-container">
            <div className="participant-data">
                <p>{participantIdentity + (local ? " (You)" : "")}</p>
            </div>
            <video ref={videoElement} id={track.sid}></video>
        </div>
    );
}
```

1. The video track object, which can be a `LocalVideoTrack` or a `RemoteVideoTrack`.
2. The participant identity associated with the video track.
3. A boolean flag that indicates whether the video track belongs to the local participant.
4. The reference to the video element in the HTML template.
5. Attach the video track to the video element when the component is mounted.
6. Detach the video track when the component is unmounted.

The `VideoComponent` does the following:

-   It defines the properties `track`, `participantIdentity`, and `local` as props of the component:

    -   `track`: The video track object, which can be a `LocalVideoTrack` or a `RemoteVideoTrack`.
    -   `participantIdentity`: The participant identity associated with the video track.
    -   `local`: A boolean flag that indicates whether the video track belongs to the local participant. This flag is set to `false` by default.

-   It creates a reference to the video element in the HTML template.
-   It attaches the video track to the video element when the component is mounted.
-   It detaches the video track when the component is unmounted.

Finally, let's see the code of the `AudioComponent.tsx` file:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/components/AudioComponent.tsx#L4-L22' target='_blank'>AudioComponent.tsx</a>" linenums="5"
interface AudioComponentProps {
    track: LocalAudioTrack | RemoteAudioTrack; // (1)!
}

function AudioComponent({ track }: AudioComponentProps) {
    const audioElement = useRef<HTMLAudioElement | null>(null); // (2)!

    useEffect(() => {
        if (audioElement.current) {
            track.attach(audioElement.current); // (3)!
        }

        return () => {
            track.detach(); // (4)!
        };
    }, [track]);

    return <audio ref={audioElement} id={track.sid} />;
}
```

1. The audio track object, which can be a `LocalAudioTrack` or a `RemoteAudioTrack`, although in this case, it will always be a `RemoteAudioTrack`.
2. The reference to the audio element in the HTML template.
3. Attach the audio track to the audio element when the component is mounted.
4. Detach the audio track when the component is unmounted.

The `AudioComponent` is similar to the `VideoComponent` but is used to display audio tracks. It defines the `track` property as a prop for the component and creates a reference to the audio element in the HTML template. The audio track is attached to the audio element when the component is mounted and detached when the component is unmounted.

---

### Leaving the Room

When the user wants to leave the room, they can click the `Leave Room` button. This action calls the `leaveRoom()` function:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-react/src/App.tsx#L91-L99' target='_blank'>App.tsx</a>" linenums="91"
async function leaveRoom() {
    // Leave the room by calling 'disconnect' method over the Room object
    await room?.disconnect(); // (1)!

    // Reset the state
    setRoom(undefined); // (2)!
    setLocalTrack(undefined);
    setRemoteTracks([]);
}
```

1. Disconnect the user from the room.
2. Reset all variables to their initial state.

The `leaveRoom()` function performs the following actions:

-   It disconnects the user from the room by calling the `disconnect()` method on the `Room` object.
-   It resets all variables to their initial state.
