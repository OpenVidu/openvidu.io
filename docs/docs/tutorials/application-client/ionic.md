# openvidu-ionic

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-client/openvidu-ionic){ .md-button target=\_blank }

This tutorial is a simple video-call application built with **Ionic**, using **Angular** and **Capacitor**, that allows:

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

1.  Navigate into the application client directory:

    ```bash
    cd openvidu-livekit-tutorials/application-client/openvidu-angular
    ```

2.  Install the required dependencies:

    ```bash
    npm install
    ```

3.  Serve the application:

    You have two options for running the client application: **browser-based** or **mobile device-based**:

    === ":fontawesome-solid-desktop:{.icon .lg-icon .tab-icon} Browser"

        To run the application in a browser, you will need to start the Ionic server. To do so, run the following command:

        ```bash
        npm start
        ```

        Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080){:target="\_blank"}. You should see a screen like this:

        !!! info "Mobile appearance"

            To show the app with a mobile device appearance, open the dev tools in your browser and find the button to adapt the viewport to a mobile device aspect ratio. You may also choose predefined types of devices to see the behavior of your app in different resolutions.

        <div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/application-clients/join-ionic-web.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/application-clients/join-ionic-web.png" loading="lazy"/></a></p></div>

        <div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/application-clients/room-ionic-web.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/application-clients/room-ionic-web.png" loading="lazy"/></a></p></div>

        --8<-- "docs/docs/tutorials/shared/testing-other-devices.md"

    === ":fontawesome-solid-mobile-screen-button:{.icon .lg-icon .tab-icon} Mobile"

        Running the tutorial on a mobile device presents additional challenges compared to running it in a browser, mainly due to the application being launched on a different device, such as an Android smartphone or iPhone, rather than our computer. To overcome these challenges, the following steps need to be taken:

        1. **Localhost limitations:**

            The usage of `localhost` in our Ionic app is restricted, preventing seamless communication between the application client and the server.

        2. **Serve over local network:**

            The application must be served over our local network to enable communication between the device and the server.

        3. **Secure connection requirement for WebRTC API:**

            The WebRTC API demands a secure connection for functionality outside of localhost, necessitating the serving of the application over HTTPS.

        If you run [OpenVidu locally](#run-openvidu-locally) you don't need to worry about this. OpenVidu will handle all of the above requirements for you. For more information, see section [Accessing your app from other devices in your network](../../self-hosting/local.md#accessing-your-local-deployment-from-other-devices-on-your-network).

        Now, let's explore how to run the application on a mobile device:

        !!! warning "Requirements"

            Before running the application on a mobile device, make sure that the device is connected to the same network as your PC and the mobile is connected to the PC via USB.

        === ":fontawesome-brands-android:{.icon .lg-icon .tab-icon} Android"

            ```bash
            npm run android
            ```

        === ":fontawesome-brands-apple:{.icon .lg-icon .tab-icon} iOS"

            You will need [Ruby](https://www.ruby-lang.org/en/documentation/installation/){target="_blank"} and [Cocoapods](https://guides.cocoapods.org/using/getting-started.html){target="_blank"} installed in your computer.

            The app must be signed with a development team. To do so, open the project in **Xcode** and select a development team in the **Signing & Capabilities** editor.

            ```bash
            npm run ios
            ```

        The script will ask you for the device you want to run the application on. You should select the real device you have connected to your computer.

        Once the mobile device has been selected, the script will launch the application on the device and you will see a screen like this:

        <div class="grid-container">

        <div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/application-clients/join-ionic-device.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/application-clients/join-ionic-device.png" loading="lazy"/></a></p></div>

        <div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/application-clients/room-ionic-device.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/application-clients/room-ionic-device.png" loading="lazy"/></a></p></div>

        </div>

## Understanding the code

This Ionic project has been created using the Ionic CLI tool. You may come across various configuration files and other items that are not essential for this tutorial. Our focus will be on the key files located within the `src/app/` directory:

-   `app.component.ts`: This file defines the `AppComponent`, which serves as the main component of the application. It is responsible for handling tasks such as joining a video call and managing the video calls themselves.
-   `app.component.html`: This HTML file is associated with the `AppComponent`, and it dictates the structure and layout of the main application component.
-   `app.component.scss`: The CSS file linked to `AppComponent`, which controls the styling and appearance of the application's main component.
-   `VideoComponent`: Component responsible for displaying video tracks along with participant's data. It is defined in the `video.component.ts` file within the `video` directory, along with its associated HTML and CSS files.
-   `AudioComponent`: Component responsible for displaying audio tracks. It is defined in the `audio.component.ts` file within the `audio` directory, along with its associated HTML and CSS files.

To use the LiveKit JS SDK in an Ionic application, you need to install the `livekit-client` package. This package provides the necessary classes and methods to interact with the LiveKit server. You can install it using the following command:

```bash
npm install livekit-client
```

Now let's see the code of the `app.component.ts` file:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/app.component.ts#L36-L120' target='_blank'>app.component.ts</a>" linenums="36"
type TrackInfo = { // (1)!
    trackPublication: RemoteTrackPublication;
    participantIdentity: string;
};

// For local development launching app in web browser, leave these variables empty
// For production or when launching app in device, configure them with correct URLs
var APPLICATION_SERVER_URL = ''; // (2)!
var LIVEKIT_URL = ''; // (3)!

@Component({ // (4)!
    selector: 'app-root',
    templateUrl: 'app.component.html',
    styleUrl: 'app.component.scss',
    standalone: true,
    imports: [
        IonApp,
        VideoComponent,
        AudioComponent,
        ReactiveFormsModule,
        IonHeader,
        IonToolbar,
        IonTitle,
        IonButtons,
        IonButton,
        IonFab,
        IonFabButton,
        IonIcon,
        IonContent,
        IonList,
        IonItem,
        IonInput,
        IonFooter,
    ],
})
export class AppComponent implements OnDestroy {
    roomForm = new FormGroup({ // (5)!
        roomName: new FormControl('Test Room', Validators.required),
        participantName: new FormControl('Participant' + Math.floor(Math.random() * 100), Validators.required),
    });

    room = signal<Room | undefined>(undefined); // (6)!
    localTrack = signal<LocalVideoTrack | undefined>(undefined); // (7)!
    remoteTracksMap = signal<Map<string, TrackInfo>>(new Map()); // (8)!

    constructor(private httpClient: HttpClient) {
        this.configureUrls();
        addIcons({
            logoGithub,
            book,
            settings,
        });
    }

    configureUrls() {
        const deviceMode = this.platform.is('hybrid');

        // If APPLICATION_SERVER_URL is not configured and app is not launched in device mode,
        // use default value from local development
        if (!APPLICATION_SERVER_URL) {
            if (deviceMode) {
                APPLICATION_SERVER_URL = 'https://{YOUR-LAN-IP}.openvidu-local.dev:6443/';
            } else {
                if (window.location.hostname === 'localhost') {
                    APPLICATION_SERVER_URL = 'http://localhost:6080/';
                } else {
                    APPLICATION_SERVER_URL = 'https://' + window.location.hostname + ':6443/';
                }
            }
        }

        // If LIVEKIT_URL is not configured and app is not launched in device mode,
        // use default value from local development
        if (!LIVEKIT_URL) {
            if (deviceMode) {
                LIVEKIT_URL = 'wss://{YOUR-LAN-IP}.openvidu-local.dev:7443/';
            } else {
                if (window.location.hostname === 'localhost') {
                    LIVEKIT_URL = 'ws://localhost:7880/';
                } else {
                    LIVEKIT_URL = 'wss://' + window.location.hostname + ':7443/';
                }
            }
        }
    }
```

1. `TrackInfo` type, which groups a track publication with the participant's identity.
2. The URL of the application server.
3. The URL of the LiveKit server.
4. Angular component decorator that defines the `AppComponent` class and associates the HTML and CSS files with it.
5. The `roomForm` object, which is a form group that contains the `roomName` and `participantName` fields. These fields are used to join a video call room.
6. The room object, which represents the video call room.
7. The local video track, which represents the user's camera.
8. Map that links track SIDs with `TrackInfo` objects. This map is used to store remote tracks and their associated participant identities.

The `app.component.ts` file defines the following variables:

-   `APPLICATION_SERVER_URL`: The URL of the application server. This variable is used to make requests to the server to obtain a token for joining the video call room.
-   `LIVEKIT_URL`: The URL of the LiveKit server. This variable is used to connect to the LiveKit server and interact with the video call room.
-   `roomForm`: A form group that contains the `roomName` and `participantName` fields. These fields are used to join a video call room.
-   `room`: The room object, which represents the video call room.
-   `localTrack`: The local video track, which represents the user's camera.
-   `remoteTracksMap`: A map that links track SIDs with `TrackInfo` objects. This map is used to store remote tracks and their associated participant identities.

!!! warning "Configure the URLs"

    For local development launching the app in a web browser, leave `APPLICATION_SERVER_URL` and `LIVEKIT_URL` variables empty. The function `configureUrls()` will automatically configure them with default values. However, for production or when launching the app in a mobile device, you should configure these variables with the correct URLs depending on your deployment.

    You can also configure these variables once the application has been launched by clicking on the settings button in the bottom right corner of the screen.

---

### Joining a Room

After the user specifies their participant name and the name of the room they want to join, when they click the `Join` button, the `joinRoom()` method is called:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/app.component.ts#L166-L215' target='_blank'>app.component.ts</a>" linenums="166"
async joinRoom() {
    // Initialize a new Room object
    const room = new Room();
    this.room.set(room); // (1)!

    // Specify the actions when events take place in the room
    // On every new Track received...
    this.room.on(
        RoomEvent.TrackSubscribed,
        (_track: RemoteTrack, publication: RemoteTrackPublication, participant: RemoteParticipant) => { // (2)!
            this.remoteTracksMap.update((map) => {
                map.set(publication.trackSid, {
                    trackPublication: publication,
                    participantIdentity: participant.identity,
                });
                return map;
            });
        }
    );

    // On every new Track destroyed...
    room.on(RoomEvent.TrackUnsubscribed, (_track: RemoteTrack, publication: RemoteTrackPublication) => { // (3)!
        this.remoteTracksMap.update((map) => {
            map.delete(publication.trackSid);
            return map;
        });
    });

    try {
        // Get the room name and participant name from the form
        const roomName = this.roomForm.value.roomName!; // (4)!
        const participantName = this.roomForm.value.participantName!;

        // Get a token from your application server with the room name and participant name
        const token = await this.getToken(roomName, participantName); // (5)!

        // Connect to the room with the LiveKit URL and the token
        await room.connect(LIVEKIT_URL, token); // (6)!

        // Publish your camera and microphone
        await room.localParticipant.enableCameraAndMicrophone(); // (7)!
        this.localTrack.set(room.localParticipant.videoTrackPublications.values().next().value.videoTrack);
    } catch (error: any) {
        console.log(
            'There was an error connecting to the room:',
            error?.error?.errorMessage || error?.message || error
        );
        await this.leaveRoom();
    }
}
```

1. Initialize a new `Room` object.
2. Event handling for when a new track is received in the room.
3. Event handling for when a track is destroyed.
4. Get the room name and participant name from the form.
5. Get a token from the application server with the room name and participant name.
6. Connect to the room with the LiveKit URL and the token.
7. Publish your camera and microphone.

The `joinRoom()` method performs the following actions:

1.  It creates a new `Room` object. This object represents the video call room.

    !!! info

        When the room object is defined, the HTML template is automatically updated hiding the "Join room" page and showing the "Room" layout.

2.  Event handling is configured for different scenarios within the room. These events are fired when new tracks are subscribed to and when existing tracks are unsubscribed.

    -   **`RoomEvent.TrackSubscribed`**: This event is triggered when a new track is received in the room. It manages the storage of the new track in the `remoteTracksMap`, which links track SIDs with `TrackInfo` objects containing the track publication and the participant's identity.

    -   **`RoomEvent.TrackUnsubscribed`**: This event occurs when a track is destroyed, and it takes care of removing the track from the `remoteTracksMap`.

    These event handlers are essential for managing the behavior of tracks within the video call. You can further extend the event handling as needed for your application.

    !!! info "Take a look at all events"

        You can take a look at all the events in the [Livekit Documentation](https://docs.livekit.io/client-sdk-js/enums/RoomEvent.html)

3.  It retrieves the room name and participant name from the form.
4.  It requests a token from the application server using the room name and participant name. This is done by calling the `getToken()` method:

    ```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/app.component.ts#L232-L250' target='_blank'>app.component.ts</a>" linenums="232"
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
    async getToken(roomName: string, participantName: string): Promise<string> {
        const response = await lastValueFrom(
            this.httpClient.post<{ token: string }>(APPLICATION_SERVER_URL + 'token', { roomName, participantName })
        );
        return response.token;
    }
    ```

    This function sends a POST request using [HttpClient](https://angular.io/api/common/http/HttpClient){:target="\_blank"} to the application server's `/token` endpoint. The request body contains the room name and participant name. The server responds with a token that is used to connect to the room.

5.  It connects to the room using the LiveKit URL and the token.
6.  It publishes the camera and microphone tracks to the room using `room.localParticipant.enableCameraAndMicrophone()`, which asks the user for permission to access their camera and microphone at the same time. The local video track is then stored in the `localTrack` variable.

---

### Displaying Video and Audio Tracks

In order to display participants' video and audio tracks, the `app.component.html` file integrates the `VideoComponent` and `AudioComponent`.

```html title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/app.component.html#L73-L91' target='_blank'>app.component.html</a>" linenums="73"
<div id="layout-container">
    @if (localTrack()) {
    <video-component
        [track]="localTrack()!"
        [participantIdentity]="roomForm.value.participantName!"
        [local]="true"
    ></video-component>
    }
    @for (remoteTrack of remoteTracksMap().values(); track remoteTrack.trackPublication.trackSid) {
        @if (remoteTrack.trackPublication.kind === 'video') {
        <video-component
            [track]="remoteTrack.trackPublication.videoTrack!"
            [participantIdentity]="remoteTrack.participantIdentity"
        ></video-component>
        } @else {
        <audio-component [track]="remoteTrack.trackPublication.audioTrack!" hidden></audio-component>
        }
    }
</div>
```

This code snippet does the following:

-   We use the Angular `@if` block to conditionally display the local video track using the `VideoComponent`. The `local` property is set to `true` to indicate that the video track belongs to the local participant.

    !!! info

        The audio track is not displayed for the local participant because there is no need to hear one's own audio.

-   Then, we use the Angular `@for` block to iterate over the `remoteTracksMap`. For each remote track, we create a `VideoComponent` or an `AudioComponent` depending on the track's kind (video or audio). The `participantIdentity` property is set to the participant's identity, and the `track` property is set to the video or audio track. The `hidden` attribute is added to the `AudioComponent` to hide the audio tracks from the layout.

Let's see now the code of the `video.component.ts` file:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/video/video.component.ts#L4-L27' target='_blank'>video.component.ts</a>" linenums="3"
// (1)!
@Component({
    selector: "video-component",
    standalone: true,
    imports: [],
    templateUrl: "./video.component.html",
    styleUrl: "./video.component.css"
})
export class VideoComponent implements AfterViewInit, OnDestroy {
    videoElement = viewChild<ElementRef<HTMLVideoElement>>("videoElement"); // (2)!

    track = input.required<LocalVideoTrack | RemoteVideoTrack>(); // (3)!
    participantIdentity = input.required<string>(); // (4)!
    local = input(false); // (5)!

    ngAfterViewInit() {
        if (this.videoElement()) {
            this.track().attach(this.videoElement()!.nativeElement); // (6)!
        }
    }

    ngOnDestroy() {
        this.track().detach(); // (7)!
    }
}
```

1. Angular component decorator that defines the `VideoComponent` class and associates the HTML and CSS files with it.
2. The reference to the video element in the HTML template.
3. The video track object, which can be a `LocalVideoTrack` or a `RemoteVideoTrack`.
4. The participant identity associated with the video track.
5. A boolean flag that indicates whether the video track belongs to the local participant.
6. Attach the video track to the video element when the track is set.
7. Detach the video track when the component is destroyed.

The `VideoComponent` does the following:

-   It defines the properties `track`, `participantIdentity`, and `local` as inputs of the component:

    -   `track`: The video track object, which can be a `LocalVideoTrack` or a `RemoteVideoTrack`.
    -   `participantIdentity`: The participant identity associated with the video track.
    -   `local`: A boolean flag that indicates whether the video track belongs to the local participant. This flag is set to `false` by default.

-   It creates a reference to the video element in the HTML template.
-   It attaches the video track to the video element when the view is initialized.
-   It detaches the video track when the component is destroyed.

Finally, let's see the code of the `audio.component.ts` file:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/audio/audio.component.ts#L4-L25' target='_blank'>audio.component.ts</a>" linenums="3"
// (1)!
@Component({
    selector: "audio-component",
    standalone: true,
    imports: [],
    templateUrl: "./audio.component.html",
    styleUrl: "./audio.component.css"
})
export class AudioComponent implements AfterViewInit, OnDestroy {
    audioElement = viewChild<ElementRef<HTMLAudioElement>>("audioElement"); // (2)!

    track = input.required<LocalAudioTrack | RemoteAudioTrack>(); // (3)!

    ngAfterViewInit() {
        if (this.audioElement()) {
            this.track().attach(this.audioElement()!.nativeElement); // (4)!
        }
    }

    ngOnDestroy() {
        this.track().detach(); // (5)!
    }
}
```

1. Angular component decorator that defines the `AudioComponent` class and associates the HTML and CSS files with it.
2. The reference to the audio element in the HTML template.
3. The audio track object, which can be a `RemoteAudioTrack` or a `LocalAudioTrack`, although in this case, it will always be a `RemoteAudioTrack`.
4. Attach the audio track to the audio element when view is initialized.
5. Detach the audio track when the component is destroyed.

The `AudioComponent` class is similar to the `VideoComponent` class, but it is used to display audio tracks. It attaches the audio track to the audio element when view is initialized and detaches the audio track when the component is destroyed.

---

### Leaving the room

When the user wants to leave the room, they can click the `Leave Room` button. This action calls the `leaveRoom()` method:

```typescript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/src/app/app.component.ts#L217-L230' target='_blank'>app.component.ts</a>" linenums="217"
async leaveRoom() {
    // Leave the room by calling 'disconnect' method over the Room object
    await this.room()?.disconnect(); // (1)!

    // Reset all variables
    this.room.set(undefined); // (2)!
    this.localTrack.set(undefined);
    this.remoteTracksMap.set(new Map());
}

async ngOnDestroy() { // (3)!
    // On window closed or component destroyed, leave the room
    await this.leaveRoom();
}
```

1. Disconnect the user from the room.
2. Reset all variables.
3. Call the `leaveRoom()` method when the component is destroyed.

The `leaveRoom()` method performs the following actions:

-   It disconnects the user from the room by calling the `disconnect()` method on the `room` object.
-   It resets all variables.

The `ngOnDestroy()` lifecycle hook is used to ensure that the user leaves the room when the component is destroyed.

---

### Specific mobile requirements

In order to be able to test the application on an Android or iOS device, the application must ask for the necessary permissions to access the device's camera and microphone. These permissions are requested when the user joins the video call room.

=== ":fontawesome-brands-android:{.icon .lg-icon .tab-icon} Android"

    The application must include the following permissions in the `AndroidManifest.xml` file located in the `android/app/src/main/AndroidManifest.xml` directory:

    ```xml title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/android/app/src/main/AndroidManifest.xml#L41-L43' target='_blank'>AndroidManifest.xml</a>" linenums="41"
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
    ```

=== ":fontawesome-brands-apple:{.icon .lg-icon .tab-icon} iOS"

    The application must include the following permissions in the `Info.plist` file located in the `ios/App/App/Info.plist` directory:

    ```xml title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ionic/ios/App/App/Info.plist#L48-L51' target='_blank'>Info.plist</a>" linenums="48"
    <key>NSCameraUsageDescription</key>
    <string>This Application uses your camera to make video calls.</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>This Application uses your microphone to make calls.</string>
    ```
