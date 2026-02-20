# OpenVidu Meet WebComponent Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.5.0/meet-webcomponent-basic)

This tutorial extends the [Direct Link tutorial](https://openvidu.io/3.5.0/meet/embedded/tutorials/direct-link/index.md) by integrating the **OpenVidu Meet WebComponent** directly into your application instead of using external links. It is built using **Node.js and Express** for the backend and plain **HTML/CSS/JavaScript** for the frontend.

At the end of this tutorial, you will have a fully functional simple video-call application with the following features:

- Users can create rooms.
- Users can delete rooms.
- Users can join a room as moderator or speaker.
- Users can chat with other users.
- Users may leave the room at any time.
- Users can view the recordings of the meeting.
- Moderators can record the meeting.
- Moderators may end the meeting at any time, disconnecting all users.

The application uses the [OpenVidu Meet API](https://openvidu.io/3.5.0/meet/embedded/reference/rest-api/index.md) to create and delete rooms, and the [OpenVidu Meet WebComponent](https://openvidu.io/3.5.0/meet/embedded/reference/webcomponent/index.md) to embed the video call interface directly into the application.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop**. You can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) .

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:3.5.0 up -y openvidu-meet-init
```

Info

For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally](https://openvidu.io/3.5.0/meet/deployment/local/index.md) .

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.5.0
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

This tutorial builds upon the [Direct Link tutorial](https://openvidu.io/3.5.0/meet/embedded/tutorials/direct-link/index.md), replacing external redirect links with an embedded OpenVidu Meet WebComponent. The backend remains identical, so we'll focus on the frontend modifications that enable WebComponent integration.

______________________________________________________________________

### Backend

The backend is identical to the [Direct Link tutorial](https://openvidu.io/3.5.0/meet/embedded/tutorials/direct-link/index.md). It provides the same three REST API endpoints:

- **`POST /rooms`**: Create a new room with the given room name.
- **`GET /rooms`**: Get the list of rooms.
- **`DELETE /rooms/:roomId`**: Delete a room with the given room ID.

For detailed backend documentation, please refer to the [Direct Link tutorial backend section](https://openvidu.io/3.5.0/meet/embedded/tutorials/direct-link/#backend).

______________________________________________________________________

### Frontend modifications

The main changes in the frontend involve replacing direct links with embedded WebComponent functionality. The key modifications are in the `public/js/app.js` and `public/index.html` files.

#### Including the OpenVidu Meet WebComponent

To use the OpenVidu Meet WebComponent in your application, you need to include it in your HTML file by adding a script tag to the end of the `<body>` section:

```html
<!-- OpenVidu Meet WebComponent bundle -->
<script src="http://localhost:9080/v1/openvidu-meet.js"></script>
```

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

## Accessing this tutorial from other computers or phones

To access this tutorial from other computers or phones, follow these steps:

1. **Ensure network connectivity**: Make sure your device (computer or phone) is connected to the same network as the machine running OpenVidu Meet and this tutorial.

1. **Configure OpenVidu Meet for network access**: Start OpenVidu Meet by following the instructions in the [Accessing OpenVidu Meet from other computers or phones](https://openvidu.io/3.5.0/meet/deployment/local/#accessing-openvidu-meet-from-other-computers-or-phones) section.

1. **Update the OpenVidu Meet server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in your `.env` file to match the URL shown when OpenVidu Meet starts.

   ```text
   # Example for IP address 192.168.1.100
   OV_MEET_SERVER_URL=https://192-168-1-100.openvidu-local.dev:9443
   ```

1. **Update the OpenVidu Meet WebComponent script URL**: In the `public/index.html` file, update the `<script>` tag that includes the OpenVidu Meet WebComponent to use the same base URL as above.

   ```html
   <script src="http://192-168-1-100.openvidu-local.dev:9443/v1/openvidu-meet.js"></script>
   ```

1. **Restart the tutorial** to apply the changes:

   ```bash
   npm start
   ```

1. **Access the tutorial**: Open your browser and navigate to `https://192-168-1-100.openvidu-local.dev:6443` (replacing `192-168-1-100` with your actual private IP) on the computer where you started the tutorial or any device in the same network.

## Connecting this tutorial to an OpenVidu Meet production deployment

If you have a production deployment of OpenVidu Meet (installed in a server following [deployment steps](https://openvidu.io/3.5.0/meet/deployment/basic/index.md) ), you can connect this tutorial to it by following these steps:

1. **Update the server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in the `.env` file to point to your OpenVidu Meet production deployment URL.

   ```text
   # Example for a production deployment
   OV_MEET_SERVER_URL=https://your-openvidu-meet-domain.com
   ```

1. **Update the API key**: Ensure the `OV_MEET_API_KEY` environment variable in the `.env` file matches the API key configured in your production deployment. See [Generate an API Key](https://openvidu.io/3.5.0/meet/embedded/reference/rest-api/#generate-an-api-key) section to learn how to obtain it.

   ```text
   OV_MEET_API_KEY=your-production-api-key
   ```

1. **Update the OpenVidu Meet WebComponent script URL**: In the `public/index.html` file, update the `<script>` tag that includes the OpenVidu Meet WebComponent to use the same base URL as above.

   ```html
   <script src="https://your-openvidu-meet-domain.com/v1/openvidu-meet.js"></script>
   ```

1. **Restart the tutorial** to apply the changes:

   ```bash
   npm start
   ```

Make this tutorial accessible from other computers or phones

By default, this tutorial runs on `http://localhost:6080` and is only accessible from the local machine. If you want to access it from other computers or phones, you have the following options:

- **Use tunneling tools**: Configure tools like [VS Code port forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding) , [ngrok](https://ngrok.com/) , [localtunnel](https://localtunnel.github.io/www/) , or similar services to expose this tutorial to the internet with a secure (HTTPS) public URL.
- **Deploy to a server**: Upload this tutorial to a web server and configure it to be accessible with a secure (HTTPS) public URL. This can be done by updating the source code to manage SSL certificates or configuring a reverse proxy (e.g., Nginx, Apache) to serve it.
