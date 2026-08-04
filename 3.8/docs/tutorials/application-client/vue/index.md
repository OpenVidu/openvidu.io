# Vue Tutorial

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/application-client/openvidu-vue)

This tutorial is a simple video-call application built with **Vue** that allows:

- Joining a video call room by requesting a token from any [application server](https://openvidu.io/3.8/docs/tutorials/application-server/index.md).
- Publishing your camera and microphone.
- Subscribing to all other participants' video and audio tracks automatically.
- Leaving the video call room at any time.

It uses the [LiveKit JS SDK](https://docs.livekit.io/client-sdk-js) to connect to the LiveKit server and interact with the video call room.

## Running this tutorial

#### 1. Run OpenVidu Server

**Run OpenVidu locally**

1. Download OpenVidu

   ```bash
   git clone https://github.com/OpenVidu/openvidu-local-deployment -b 3.8.0
   ```

1. Configure the local deployment

   **Windows**

   ```powershell
   cd openvidu-local-deployment/community
   .\configure_lan_private_ip_windows.bat
   ```

   **macOS**

   ```bash
   cd openvidu-local-deployment/community
   ./configure_lan_private_ip_macos.sh
   ```

   **Linux**

   ```bash
   cd openvidu-local-deployment/community
   ./configure_lan_private_ip_linux.sh
   ```

1. Run OpenVidu

   ```bash
   docker compose up
   ```

**Deploy OpenVidu**

To use a production-ready OpenVidu deployment, visit the official [deployment guide](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md).

Configure Webhooks

All [application servers](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) have an endpoint to receive webhooks from OpenVidu. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/enable-webhooks/#send-webhooks-to-a-local-application-server) section for more information.

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.8.0
```

### 3. Run a server application

**Node.js**

To run this server application, you need [Node.js](https://nodejs.org/en/download) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/node
   ```

1. Install dependencies

   ```bash
   npm install
   ```

1. Run the application

   ```bash
   npm start
   ```

For more information, check the [Node.js tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/node/index.md).

**Go**

To run this server application, you need [Go](https://go.dev/doc/install) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/go
   ```

1. Run the application

   ```bash
   go run main.go
   ```

For more information, check the [Go tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/go/index.md).

**Ruby**

To run this server application, you need [Ruby](https://www.ruby-lang.org/en/documentation/installation/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/ruby
   ```

1. Install dependencies

   ```bash
   bundle install
   ```

1. Run the application

   ```bash
   ruby app.rb
   ```

For more information, check the [Ruby tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/ruby/index.md).

**Java**

To run this server application, you need [Java](https://www.java.com/en/download/manual.jsp) and [Maven](https://maven.apache.org) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/java
   ```

1. Run the application

   ```bash
   mvn spring-boot:run
   ```

For more information, check the [Java tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/java/index.md).

**Python**

To run this server application, you need [Python 3](https://www.python.org/downloads/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/python
   ```

1. Create a python virtual environment

   ```bash
   python -m venv venv
   ```

1. Activate the virtual environment

   **Windows**

   ```powershell
   .\venv\Scripts\activate
   ```

   **macOS**

   ```bash
   . ./venv/bin/activate
   ```

   **Linux**

   ```bash
   . ./venv/bin/activate
   ```

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

1. Run the application

   ```bash
   python app.py
   ```

For more information, check the [Python tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/python/index.md).

**Rust**

To run this server application, you need [Rust](https://www.rust-lang.org/tools/install) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/rust
   ```

1. Run the application

   ```bash
   cargo run
   ```

For more information, check the [Rust tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/rust/index.md).

**PHP**

To run this server application, you need [PHP](https://www.php.net/manual/en/install.php) and [Composer](https://getcomposer.org/download/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/php
   ```

1. Install dependencies

   ```bash
   composer install
   ```

1. Run the application

   ```bash
   composer start
   ```

Warning

LiveKit PHP SDK requires library [BCMath](https://www.php.net/manual/en/book.bc.php) . This is available out-of-the-box in PHP for Windows, but a manual installation might be necessary in other OS. Run **`sudo apt install php-bcmath`** or **`sudo yum install php-bcmath`**

For more information, check the [PHP tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/php/index.md).

**.NET**

To run this server application, you need [.NET](https://dotnet.microsoft.com/en-us/download) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/dotnet
   ```

1. Run the application

   ```bash
   dotnet run
   ```

Warning

This .NET server application needs the `LIVEKIT_API_SECRET` env variable to be at least 32 characters long. Make sure to update it [here](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/b97db7278227470fd386337ffde49b2458315c6f/application-server/dotnet/appsettings.json#L11) and in your [OpenVidu Server](#1-run-openvidu-server).

For more information, check the [.NET tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/dotnet/index.md).

### 4. Run the client application

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-vue
   ```

1. Install dependencies:

   ```bash
   npm install
   ```

1. Run the application:

   ```bash
   npm start
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

## Understanding the code

This Vue project has been generated using the Vue CLI tool. You may come across various configuration files and other items that are not essential for this tutorial. Our focus will be on the key files located within the `src/` directory:

- `App.vue`: This file defines the main application component along with its HTML template and styles. It is responsible for handling tasks such as joining a video call and managing the video calls themselves.
- `VideoComponent.vue`: This file defines the `VideoComponent`. This component is responsible for displaying video tracks along with participant's data.
- `AudioComponent.vue`: This file defines the `AudioComponent`. This component is responsible for displaying audio tracks.

To use the LiveKit JS SDK in a Vue application, you need to install the `livekit-client` package. This package provides the necessary classes and methods to interact with the LiveKit server. You can install it using the following command:

```bash
npm install livekit-client
```

Now let's see the code of the `App.vue` file:

```typescript
type TrackInfo = {
    // (1)!
    trackPublication: RemoteTrackPublication;
    participantIdentity: string;
};

// When running OpenVidu locally, leave these variables empty
// For other deployment type, configure them with correct URLs depending on your deployment
let APPLICATION_SERVER_URL = ""; // (2)!
let LIVEKIT_URL = ""; // (3)!
configureUrls();

function configureUrls() {
    // If APPLICATION_SERVER_URL is not configured, use default value from OpenVidu Local deployment
    if (!APPLICATION_SERVER_URL) {
        if (window.location.hostname === "localhost") {
            APPLICATION_SERVER_URL = "http://localhost:6080/";
        } else {
            APPLICATION_SERVER_URL = "https://" + window.location.hostname + ":6443/";
        }
    }

    // If LIVEKIT_URL is not configured, use default value from OpenVidu Local deployment
    if (!LIVEKIT_URL) {
        if (window.location.hostname === "localhost") {
            LIVEKIT_URL = "ws://localhost:7880/";
        } else {
            LIVEKIT_URL = "wss://" + window.location.hostname + ":7443/";
        }
    }
}

const room = ref<Room>(); // (4)!
const localTrack = ref<LocalVideoTrack>(); // (5)!
const remoteTracksMap: Ref<Map<string, TrackInfo>> = ref(new Map()); // (6)!

let participantName = ref("Participant" + Math.floor(Math.random() * 100)); // (7)!
let roomName = ref("Test Room"); // (8)!
```

1. `TrackInfo` type, which groups a track publication with the participant's identity.
1. The URL of the application server.
1. The URL of the LiveKit server.
1. The room object, which represents the video call room.
1. The local video track, which represents the user's camera.
1. Map that links track SIDs with `TrackInfo` objects. This map is used to store remote tracks and their associated participant identities.
1. The participant's name.
1. The room name.

The `App.vue` file defines the following variables:

- `APPLICATION_SERVER_URL`: The URL of the application server. This variable is used to make requests to the server to obtain a token for joining the video call room.
- `LIVEKIT_URL`: The URL of the LiveKit server. This variable is used to connect to the LiveKit server and interact with the video call room.
- `room`: The room object, which represents the video call room.
- `localTrack`: The local video track, which represents the user's camera.
- `remoteTracksMap`: A map that links track SIDs with `TrackInfo` objects. This map is used to store remote tracks and their associated participant identities.
- `participantName`: The participant's name.
- `roomName`: The room name.

Configure the URLs

When [running OpenVidu locally](#run-openvidu-locally), leave `APPLICATION_SERVER_URL` and `LIVEKIT_URL` variables empty. The function `configureUrls()` will automatically configure them with default values. However, for other deployment type, you should configure these variables with the correct URLs depending on your deployment.

______________________________________________________________________

### Joining a Room

After the user specifies their participant name and the name of the room they want to join, when they click the `Join` button, the `joinRoom()` function is called:

```typescript
async function joinRoom() {
    // Initialize a new Room object
    room.value = new Room(); // (1)!

    // Specify the actions when events take place in the room
    // On every new Track received...
    room.value.on(
        RoomEvent.TrackSubscribed,
        (_track: RemoteTrack, publication: RemoteTrackPublication, participant: RemoteParticipant) => {
            // (2)!
            remoteTracksMap.value.set(publication.trackSid, {
                trackPublication: publication,
                participantIdentity: participant.identity
            });
        }
    );

    // On every Track destroyed...
    room.value.on(RoomEvent.TrackUnsubscribed, (_track: RemoteTrack, publication: RemoteTrackPublication) => {
        // (3)!
        remoteTracksMap.value.delete(publication.trackSid);
    });

    try {
        // Get a token from your application server with the room name and participant name
        const token = await getToken(roomName.value, participantName.value); // (4)!

        // Connect to the room with the LiveKit URL and the token
        await room.value.connect(LIVEKIT_URL, token); // (5)!

        // Publish your camera and microphone
        await room.value.localParticipant.enableCameraAndMicrophone(); // (6)!
        localTrack.value = room.value.localParticipant.videoTrackPublications.values().next().value.videoTrack;
    } catch (error: any) {
        console.log("There was an error connecting to the room:", error.message);
        await leaveRoom();
    }

    // Add listener for beforeunload event to leave the room when the user closes the tab
    window.addEventListener("beforeunload", leaveRoom); // (7)!
}
```

1. Initialize a new `Room` object.
1. Event handling for when a new track is received in the room.
1. Event handling for when a track is destroyed.
1. Get a token from the application server with the room name and participant name from the form.
1. Connect to the room with the LiveKit URL and the token.
1. Publish your camera and microphone.
1. Add a listener for the `beforeunload` event to leave the room when the user closes the tab.

The `joinRoom()` function performs the following actions:

1. It creates a new `Room` object. This object represents the video call room.

   Info

   When the room object is defined, the HTML template is automatically updated hiding the "Join room" page and showing the "Room" layout.

1. Event handling is configured for different scenarios within the room. These events are fired when new tracks are subscribed to and when existing tracks are unsubscribed.

   - **`RoomEvent.TrackSubscribed`**: This event is triggered when a new track is received in the room. It manages the storage of the new track in the `remoteTracksMap`, which links track SIDs with `TrackInfo` objects containing the track publication and the participant's identity.
   - **`RoomEvent.TrackUnsubscribed`**: This event occurs when a track is destroyed, and it takes care of removing the track from the `remoteTracksMap`.

   These event handlers are essential for managing the behavior of tracks within the video call. You can further extend the event handling as needed for your application.

   Take a look at all events

   You can take a look at all the events in the [Livekit Documentation](https://docs.livekit.io/client-sdk-js/enums/RoomEvent.html)

1. It requests a token from the application server using the room name and participant name. This is done by calling the `getToken()` function:

   ```typescript
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
               roomName,
               participantName
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

1. It connects to the room using the LiveKit URL and the token.

1. It publishes the camera and microphone tracks to the room using `room.localParticipant.enableCameraAndMicrophone()`, which asks the user for permission to access their camera and microphone at the same time. The local video track is then stored in the `localTrack` variable.

1. It adds a listener for the `beforeunload` event to leave the room when the user closes the tab.

______________________________________________________________________

### Displaying Video and Audio Tracks

In order to display participants' video and audio tracks, the main component integrates the `VideoComponent` and `AudioComponent`.

```html
<div id="layout-container">
    <VideoComponent v-if="localTrack" :track="localTrack" :participantIdentity="participantName" :local="true" />
    <template v-for="remoteTrack of remoteTracksMap.values()" :key="remoteTrack.trackPublication.trackSid">
        <VideoComponent
            v-if="remoteTrack.trackPublication.kind === 'video'"
            :track="remoteTrack.trackPublication.videoTrack!"
            :participantIdentity="remoteTrack.participantIdentity"
        />
        <AudioComponent v-else :track="remoteTrack.trackPublication.audioTrack!" hidden />
    </template>
</div>
```

This code snippet does the following:

- We use the `v-if` directive to conditionally display the local video track using the `VideoComponent`. The `local` property is set to `true` to indicate that the video track belongs to the local participant.

  Info

  The audio track is not displayed for the local participant because there is no need to hear one's own audio.

- Then, we use the `v-for` directive to iterate over the `remoteTracksMap`. For each remote track, we create a `VideoComponent` or an `AudioComponent` depending on the track's kind (video or audio). The `participantIdentity` property is set to the participant's identity, and the `track` property is set to the video or audio track. The `hidden` attribute is added to the `AudioComponent` to hide the audio tracks from the layout.

Let's see now the code of the `VideoComponent.vue` file:

```typescript
const props = withDefaults(
    defineProps<{
        track: LocalVideoTrack | RemoteVideoTrack; // (1)!
        participantIdentity: string; // (2)!
        local?: boolean; // (3)!
    }>(),
    {
        local: false
    }
);

const videoElement = ref<HTMLMediaElement | null>(null); // (4)!

onMounted(() => {
    if (videoElement.value) {
        props.track.attach(videoElement.value); // (5)!
    }
});

onUnmounted(() => {
    props.track.detach(); // (6)!
});
```

1. The video track object, which can be a `LocalVideoTrack` or a `RemoteVideoTrack`.
1. The participant identity associated with the video track.
1. A boolean flag that indicates whether the video track belongs to the local participant.
1. The reference to the video element in the HTML template.
1. Attach the video track to the video element when the component is mounted.
1. Detach the video track when the component is unmounted.

The `VideoComponent` does the following:

- It defines the properties `track`, `participantIdentity`, and `local` using the `defineProps()` function:

  - `track`: The video track object, which can be a `LocalVideoTrack` or a `RemoteVideoTrack`.
  - `participantIdentity`: The participant identity associated with the video track.
  - `local`: A boolean flag that indicates whether the video track belongs to the local participant. This flag is set to `false` by default.

- It creates a reference to the video element in the HTML template.

- It attaches the video track to the video element when the component is mounted.

- It detaches the video track when the component is unmounted.

Finally, let's see the code of the `AudioComponent.vue` file:

```typescript
const props = defineProps<{
    track: LocalAudioTrack | RemoteAudioTrack; // (1)!
}>();
const audioElement = ref<HTMLMediaElement | null>(null); // (2)!

onMounted(() => {
    if (audioElement.value) {
        props.track.attach(audioElement.value); // (3)!
    }
});

onUnmounted(() => {
    props.track.detach(); // (4)!
});
```

1. The audio track object, which can be a `LocalAudioTrack` or a `RemoteAudioTrack`, although in this case, it will always be a `RemoteAudioTrack`.
1. The reference to the audio element in the HTML template.
1. Attach the audio track to the audio element when the component is mounted.
1. Detach the audio track when the component is unmounted.

The `AudioComponent` is similar to the `VideoComponent` but is used to display audio tracks. It defines the `track` property using the `defineProps()` function and creates a reference to the audio element in the HTML template. The audio track is attached to the audio element when the component is mounted and detached when the component is unmounted.

______________________________________________________________________

### Leaving the Room

When the user wants to leave the room, they can click the `Leave Room` button. This action calls the `leaveRoom()` function:

```typescript
async function leaveRoom() {
    // Leave the room by calling 'disconnect' method over the Room object
    await room.value?.disconnect(); // (1)!

    // Empty all variables
    room.value = undefined; // (2)!
    localTrack.value = undefined;
    remoteTracksMap.value.clear();

    window.removeEventListener("beforeunload", leaveRoom); // (3)!
}

onUnmounted(() => {
    // (4)!
    // On component unmount, leave the room
    leaveRoom();
});
```

1. Disconnect the user from the room.
1. Reset all variables to their initial state.
1. Remove the `beforeunload` event listener.
1. Call the `leaveRoom()` function when the component is unmounted.

The `leaveRoom()` function performs the following actions:

- It disconnects the user from the room by calling the `disconnect()` method on the `Room` object.
- It resets all variables to their initial state.
- It removes the `beforeunload` event listener.

The `leaveRoom()` function is also called when the component is unmounted using the `onUnmounted()` lifecycle hook. This ensures that the user leaves the room when the component is no longer needed.
