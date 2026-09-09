# Electron Tutorial

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/application-client/openvidu-js)

This tutorial is a simple video-call application built with **Electron** that allows:

- Joining a video call room by requesting a token from any [application server](https://openvidu.io/3.8/docs/tutorials/application-server/index.md).
- Publishing your camera and microphone.
- Subscribing to all other participants' video and audio tracks automatically.
- Leaving the video call room at any time.

It uses the [LiveKit JS SDK](https://docs.livekit.io/reference/client-sdk-js/) to connect to the LiveKit server and interact with the video call room.

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

For more information, check the [Node.js tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/node/index.md) .

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

For more information, check the [Go tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/go/index.md) .

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

For more information, check the [Ruby tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/ruby/index.md) .

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

For more information, check the [Java tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/java/index.md) .

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

For more information, check the [Python tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/python/index.md) .

**Rust**

To run this server application, you need [Rust](https://rust-lang.org/tools/install/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/rust
   ```

1. Run the application

   ```bash
   cargo run
   ```

For more information, check the [Rust tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/rust/index.md) .

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

For more information, check the [PHP tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/php/index.md) .

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

This .NET server application needs the `LIVEKIT_API_SECRET` env variable to be at least 32 characters long. Make sure to update it [here](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/application-server/dotnet/appsettings.json#L11) and in your [OpenVidu Server](#1-run-openvidu-server).

For more information, check the [.NET tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/dotnet/index.md) .

### 4. Run the client application

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-electron
   ```

1. Install the required dependencies:

   ```bash
   npm install
   ```

1. Run the application:

   ```bash
   npm start
   ```

The application will seamlessly initiate as a native desktop program, adapting itself to the specific operating system you are using. Once the application is open, you should see a screen like this:

Join screen of the Electron tutorial app

Video call room of the Electron tutorial app

Running your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

## Understanding the code

This Electron project has been created using **electron-forge**. As an Electron application, the code is divided into two main parts, the **main process** and the **renderer process**. The most important files are located within the `src/` directory:

- `index.js`: This file is the entry point (main process) for the Electron application. It creates the main window and loads the `index.html` file.
- `app.js`: This file constitutes the renderer process code, responsible for the application UI and logic. It uses the [LiveKit JS SDK](https://docs.livekit.io/reference/client-sdk-js/) to connect to the LiveKit server and interact with the video call room.
- `index.html`: This HTML file is responsible for creating the user interface. It contains the form to connect to a video call and the video call layout.
- `styles.css`: This file contains CSS classes that are used to style the `index.html` page.

To use the LiveKit JS SDK in an Electron application, you need to install the `livekit-client` package. This package provides the necessary classes and methods to interact with the LiveKit server. You can install it using the following command:

```bash
npm install livekit-client
```

Now let's see the code of the `app.js` file:

```javascript
const { Room, RoomEvent } = require("livekit-client"); // (1)!

// Configure these constants with correct URLs depending on your deployment
const APPLICATION_SERVER_URL = "http://localhost:6080/"; // (2)!
const LIVEKIT_URL = "ws://localhost:7880/"; // (3)!

var room; // (4)!
```

1. Import the `Room` and `RoomEvent` classes from the `livekit-client` package.
1. The URL of the application server.
1. The URL of the LiveKit server.
1. The room object, which represents the video call room.

The `app.js` file defines the following variables:

- `APPLICATION_SERVER_URL`: The URL of the application server. This variable is used to make requests to the server to obtain a token for joining the video call room.
- `LIVEKIT_URL`: The URL of the LiveKit server. This variable is used to connect to the LiveKit server and interact with the video call room.
- `room`: The room object, which represents the video call room.

Configure the URLs

You should configure `APPLICATION_SERVER_URL` and `LIVEKIT_URL` constants with the correct URLs depending on your deployment.

______________________________________________________________________

### Joining a Room

After the user specifies their participant name and the name of the room they want to join, when they click the `Join` button, the `joinRoom()` function is called:

```javascript
async function joinRoom() {
    // Disable 'Join' button
    document.getElementById("join-button").disabled = true;
    document.getElementById("join-button").innerText = "Joining...";

    // Initialize a new Room object
    room = new Room(); // (1)!

    // Specify the actions when events take place in the room
    // On every new Track received...
    room.on(RoomEvent.TrackSubscribed, (track, _publication, participant) => {
        // (2)!
        addTrack(track, participant.identity);
    });

    // On every new Track destroyed...
    room.on(RoomEvent.TrackUnsubscribed, (track, _publication, participant) => {
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
1. Event handling for when a new track is received in the room.
1. Event handling for when a track is destroyed.
1. Get the room name and participant name from the form.
1. Get a token from the application server with the room name and participant name.
1. Connect to the room with the LiveKit URL and the token.
1. Hide the "Join room" page and show the "Room" page.
1. Publish your camera and microphone.

The `joinRoom()` function performs the following actions:

1. It creates a new `Room` object. This object represents the video call room.

1. Event handling is configured for different scenarios within the room. These events are fired when new tracks are subscribed to and when existing tracks are unsubscribed.

   - **`RoomEvent.TrackSubscribed`**: This event is triggered when a new track is received in the room. It handles the attachment of the track to the HTML page, assigning an ID, and appending it to the `layout-container` element. If the track is of kind `video`, a `video-container` is created and participant data is appended as well.

   ```javascript
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

   ```javascript
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

   - **`RoomEvent.TrackUnsubscribed`**: This event occurs when a track is destroyed, and it takes care of detaching the track from the HTML page and removing it from the DOM. If the track is a `video` track, `video-container` with the participant's identity is removed as well.

   ```javascript
   function removeVideoContainer(participantIdentity) {
       const videoContainer = document.getElementById(`camera-${participantIdentity}`);
       videoContainer?.remove();
   }
   ```

   These event handlers are essential for managing the behavior of tracks within the video call.

   Take a look at all events

   You can take a look at all the events in the [Room events reference](https://openvidu.io/3.8/docs/reference/client-sdk/#room-events)

1. It retrieves the room name and participant name from the form.

1. It requests a token from the application server using the room name and participant name. This is done by calling the `getToken()` function:

   ```javascript
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

1. It connects to the room using the LiveKit URL and the token.

1. It updates the UI to hide the "Join room" page and show the "Room" layout.

1. It publishes the camera and microphone tracks to the room using `room.localParticipant.enableCameraAndMicrophone()`, which asks the user for permission to access their camera and microphone at the same time. The local video track is then added to the layout.

______________________________________________________________________

### Leaving the Room

When the user wants to leave the room, they can click the `Leave Room` button. This action calls the `leaveRoom()` function:

```javascript
async function leaveRoom() {
    // Leave the room by calling 'disconnect' method over the Room object
    await room.disconnect(); // (1)!

    // Remove all HTML elements inside the layout container
    removeAllLayoutElements(); // (2)!

    // Back to 'Join room' page
    document.getElementById("join").hidden = false; // (3)!
    document.getElementById("room").hidden = true;

    // Enable 'Join' button
    document.getElementById("join-button").disabled = false;
    document.getElementById("join-button").innerText = "Join!";
}

// (4)!
window.onbeforeunload = () => {
    room?.disconnect();
};
```

1. Disconnect the user from the room.
1. Remove all HTML elements inside the layout container.
1. Show the "Join room" page and hide the "Room" layout.
1. Call the `disconnect()` method on the `room` object when the user closes the tab or navigates to another page.

The `leaveRoom()` function performs the following actions:

- It disconnects the user from the room by calling the `disconnect()` method on the `room` object.
- It removes all HTML elements inside the layout container by calling the `removeAllLayoutElements()` function.
- It shows the "Join room" page and hides the "Room" layout.

The `window.onbeforeunload` event is used to ensure that the user is disconnected from the room before the page is unloaded. This event is triggered when the user closes the tab or navigates to another page.
