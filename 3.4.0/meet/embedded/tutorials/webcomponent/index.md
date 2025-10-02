# OpenVidu Meet WebComponent Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/main/meet-webcomponent-basic)

This tutorial extends the [Direct Link tutorial](../direct-link/) by integrating the **OpenVidu Meet WebComponent** directly into your application instead of using external links. It is built using **Node.js and Express** for the backend and plain **HTML/CSS/JavaScript** for the frontend.

At the end of this tutorial, you will have a fully functional video-call application with the following features:

- Users can create rooms.
- Users can delete rooms.
- Users can join a room as moderator or speaker.
- Users can chat with other participants.
- Moderators can record the meeting.
- Users may leave the room at any time.
- Moderators may end the meeting at any time, disconnecting all participants.
- Users can view the recordings of the meeting.

The application uses the [OpenVidu Meet API](../../reference/rest-api/) to create and delete rooms, and the [OpenVidu Meet WebComponent](../../reference/webcomponent/) to embed the video call interface directly into the application.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop**. You can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) .

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:latest up -y openvidu-meet-init
```

Info

For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally](../../../deployment/local/) .

Follow the instructions to [deploy OpenVidu Meet in a single server](../../../deployment/basic/) .

You can also explore more advanced deployment options in section [Advanced deployments](../../../deployment/advanced/) .

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b main
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-webcomponent-basic
```

1. Install dependencies

```bash
npm install
```

1. Run the application

```bash
npm start
```

Once the server is up and running, you can test the application by visiting [`http://localhost:6080`](http://localhost:6080). You should see a screen like this:

## Understanding the code

This tutorial builds upon the [Direct Link tutorial](../direct-link/), replacing external redirect links with an embedded OpenVidu Meet WebComponent. The backend remains identical, so we'll focus on the frontend modifications that enable WebComponent integration.

______________________________________________________________________

### Backend

The backend is identical to the [Direct Link tutorial](../direct-link/). It provides the same three REST API endpoints:

- **`POST /rooms`**: Create a new room with the given room name.
- **`GET /rooms`**: Get the list of rooms.
- **`DELETE /rooms/:roomId`**: Delete a room with the given room ID.

For detailed backend documentation, please refer to the [Direct Link tutorial backend section](../direct-link/#backend).

______________________________________________________________________

### Frontend modifications

The main changes in the frontend involve replacing direct links with embedded WebComponent functionality. The key modifications are in the `public/js/app.js` and `public/index.html` files.

#### Including the OpenVidu Meet WebComponent

To use the OpenVidu Meet WebComponent in your application, you need to include it in your HTML file by adding a script tag to the end of the `<body>` section:

```html
<!-- OpenVidu Meet WebComponent bundle -->
<script src="http://localhost:9080/v1/openvidu-meet.js"></script>
```

Configure the `src` URL

When [running OpenVidu locally](#run-openvidu-locally), the `src` URL shown above will work if you access the application from the same device where OpenVidu Meet is running. However, if you access the application from a different device, you need to replace `http://localhost:9080` with `https://xxx-yyy-zzz-www.openvidu-local.dev:9443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.).

*This is one advantage of [running OpenVidu locally](#run-openvidu-meet-locally), that you can test your application client with other devices in your local network very easily without worrying about SSL certificates. For more information, see [Accessing OpenVidu Meet from other computers or phones](../../../deployment/local/#accessing-openvidu-meet-from-other-computers-or-phones).*

If you are using a [production OpenVidu deployment](#deploy-openvidu-meet), you should configure the domain part of the `src` URL with the correct URL depending on your deployment.

______________________________________________________________________

#### Enhanced room list template

The room list template has been modified to use buttons instead of direct links, enabling WebComponent integration:

```javascript
function getRoomListItemTemplate(room) {
    return `
        <li class="list-group-item">
            <span>${room.roomName}</span>
            <div class="room-actions">
                <button
                    class="btn btn-primary btn-sm"
                    onclick="joinRoom('${room.moderatorUrl}');"
                >
                    Join as Moderator
                </button>
                <button
                    class="btn btn-secondary btn-sm"
                    onclick="joinRoom('${room.speakerUrl}');"
                >
                    Join as Speaker
                </button>
                <button 
                    title="Delete room"
                    class="icon-button delete-button"
                    onclick="deleteRoom('${room.roomId}');"
                >
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}
```

The key difference from the Direct Link tutorial is that instead of using anchor tags (`<a>`) with `href` attributes pointing to external URLs, this template uses buttons that call the `joinRoom()` function with the appropriate room URL.

______________________________________________________________________

#### Joining a room with WebComponent

When the user clicks the `Join as Moderator` or `Join as Speaker` button, the `joinRoom()` function is called, which handles embedding the OpenVidu Meet WebComponent:

```javascript
function joinRoom(roomUrl) {
    // Hide the home screen and show the room screen
    const homeScreen = document.querySelector('#home');
    homeScreen.hidden = true; // (1)!
    const roomScreen = document.querySelector('#room');
    roomScreen.hidden = false; // (2)!

    // Inject the OpenVidu Meet component into the meeting container specifying the room URL
    const meetingContainer = document.querySelector('#meeting-container');
    meetingContainer.innerHTML = `
        <openvidu-meet 
            room-url="${roomUrl}"
            leave-redirect-url="/"
        >
        </openvidu-meet>
    `; // (3)!
}
```

1. Hide the home screen to prepare for the meeting view.
1. Show the room screen where the WebComponent will be embedded.
1. Inject the OpenVidu Meet WebComponent into the meeting container with the specified room URL and a leave redirect URL.

The `joinRoom()` function hides the home screen and shows the room screen to provide a dedicated space for the video meeting. Then, it dynamically creates and injects the `<openvidu-meet>` WebComponent into the meeting container, setting the `room-url` attribute with the URL provided by the OpenVidu Meet API and configuring the `leave-redirect-url` attribute to return users to the home screen when they leave the meeting.

This approach provides a seamless user experience by keeping users within the same application while providing full video conferencing functionality through the embedded WebComponent.
