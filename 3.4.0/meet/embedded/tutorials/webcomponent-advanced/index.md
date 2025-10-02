# OpenVidu Meet WebComponent Commands & Events Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.4.0/meet-webcomponent-commands-events)

This tutorial extends the [basic WebComponent tutorial](../webcomponent/) to add **advanced WebComponent functionality** through commands and event handling. It demonstrates how to interact with the OpenVidu Meet WebComponent programmatically and respond to meeting events.

The application includes all the features from the basic WebComponent tutorial, plus:

- **WebComponent commands**: Control the meeting programmatically (e.g., end meeting for moderators).
- **Event handling**: Listen to and respond to WebComponent events (joined, left, closed).
- **Role-based UI**: Display different interface elements based on user role (moderator/speaker).
- **Meeting header**: Show room information and controls above the WebComponent.
- **Enhanced room management**: In-memory room tracking with unique names per room.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop** (you can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) ).

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:3.4.0 up -y openvidu-meet-init
```

Info

For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally](../../../deployment/local/) .

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.4.0
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-webcomponent-commands-events
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

This tutorial builds upon the [basic WebComponent tutorial](../webcomponent/), adding advanced WebComponent interaction capabilities and enhanced room management. We'll focus on the key differences and new functionality.

______________________________________________________________________

### Backend

The backend is identical to previous tutorials. It provides the same three REST API endpoints:

- **`POST /rooms`**: Create a new room with the given room name.
- **`GET /rooms`**: Get the list of rooms.
- **`DELETE /rooms/:roomId`**: Delete a room with the given room ID.

For detailed backend documentation, please refer to the [Direct Link tutorial backend section](../direct-link/#backend).

______________________________________________________________________

### Frontend modifications

The frontend changes focus on enhanced room management, WebComponent event handling, and role-based UI features.

#### Enhanced room template

The room template now passes additional parameters including role information:

```javascript
function getRoomListItemTemplate(room) {
    return `
        <li class="list-group-item">
            <span>${room.roomName}</span>
            <div class="room-actions">
                <button
                    class="btn btn-primary btn-sm"
                    onclick="joinRoom(
                        '${room.roomName}', 
                        '${room.moderatorUrl}', 
                        'moderator'
                    );"
                >
                    Join as Moderator
                </button>
                <button
                    class="btn btn-secondary btn-sm"
                    onclick="joinRoom(
                        '${room.roomName}', 
                        '${room.speakerUrl}', 
                        'speaker'
                    );"
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

The template now provides the room name and user role to the `joinRoom()` function, enabling role-based functionality and proper room identification.

______________________________________________________________________

#### Advanced room joining with commands and events

The `joinRoom()` function has been significantly enhanced to handle WebComponent events and commands:

```javascript
function joinRoom(roomName, roomUrl, role) {
    console.log(`Joining room as ${role}`);

    // Hide the home screen and show the room screen
    const homeScreen = document.querySelector('#home');
    homeScreen.hidden = true; // (1)!
    const roomScreen = document.querySelector('#room');
    roomScreen.hidden = false; // (2)!

    // Hide the room header until the local participant joins
    const roomHeader = document.querySelector('#room-header');
    roomHeader.hidden = true; // (3)!

    // Inject the OpenVidu Meet component into the meeting container specifying the room URL
    const meetingContainer = document.querySelector('#meeting-container');
    meetingContainer.innerHTML = `
        <openvidu-meet 
            room-url="${roomUrl}"
        >
        </openvidu-meet>
    `; // (4)!

    // Add event listeners for the OpenVidu Meet component
    const meet = document.querySelector('openvidu-meet');

    // Event listener for when the local participant joins the room
    meet.once('joined', () => {
        // (5)!
        console.log('Local participant joined the room');

        // Show the room header with the room name
        roomHeader.hidden = false;
        const roomNameHeader = document.querySelector('#room-name-header');
        roomNameHeader.textContent = roomName; // (6)!

        // Show end meeting button only for moderators
        const endMeetingButton = document.querySelector('#end-meeting-btn');
        if (role === 'moderator') {
            endMeetingButton.hidden = false; // (7)!
        } else {
            endMeetingButton.hidden = true;
        }

        // Event listener for ending the meeting
        if (role === 'moderator') {
            endMeetingButton.addEventListener('click', () => {
                console.log('Ending meeting');
                meet.endMeeting(); // (8)!
            });
        }
    });

    // Event listener for when the local participant leaves the room
    meet.once('left', (event) => {
        // (9)!
        console.log('Local participant left the room. Reason:', event.reason);

        // Hide the room header
        roomHeader.hidden = true;
    });

    // Event listener for when the OpenVidu Meet component is closed
    meet.once('closed', () => {
        // (10)!
        console.log('OpenVidu Meet component closed');

        // Hide the room screen and show the home screen
        roomScreen.hidden = true;
        homeScreen.hidden = false;
    });
}
```

1. Hide the home screen.
1. Show the room screen.
1. Hide the room header until the local participant joins.
1. Inject the OpenVidu Meet WebComponent into the meeting container with the specified room URL.
1. Add an event listener for the `joined` event, which is triggered when the local participant joins the room.
1. Set the room name in the header.
1. Show the end meeting button if the user is a moderator.
1. Call the `endMeeting()` method of the OpenVidu Meet WebComponent to end the meeting when the moderator clicks the `End Meeting` button.
1. Add an event listener for the `left` event, which is triggered when the local participant leaves the room.
1. Add an event listener for the `closed` event, which is triggered when the OpenVidu Meet component is closed.

The enhanced `joinRoom()` function now performs the following actions:

1. Hides the home screen and shows the room screen.

1. Hides the room header until the local participant joins.

1. Injects the OpenVidu Meet WebComponent into the meeting container with the specified room URL.

1. Configures event listeners for the OpenVidu Meet WebComponent to handle different events:

   - **`joined`**: This event is triggered when the local participant joins the room. It shows the room header with the room name and displays the `End Meeting` button if the user is a moderator. It also adds an event listener for the `End Meeting` button to call the `endMeeting()` method of the OpenVidu Meet WebComponent to end the meeting. This method disconnects all participants and ends the meeting for everyone.
   - **`left`**: This event is triggered when the local participant leaves the room. It hides the room header.
   - **`closed`**: This event is triggered when the OpenVidu Meet component is closed. It hides the room screen and shows the home screen.

## Accessing this tutorial from other computers or phones

To access this tutorial from other computers or phones, follow these steps:

1. **Ensure network connectivity**: Make sure your device (computer or phone) is connected to the same network as the machine running OpenVidu Meet and this tutorial.

1. **Configure OpenVidu Meet for network access**: Start OpenVidu Meet by following the instructions in the [Accessing OpenVidu Meet from other computers or phones](../../../deployment/local/#accessing-openvidu-meet-from-other-computers-or-phones) section.

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

If you have a production deployment of OpenVidu Meet (installed in a server following [deployment steps](../../../deployment/basic/) ), you can connect this tutorial to it by following these steps:

1. **Update the server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in the `.env` file to point to your OpenVidu Meet production deployment URL.

   ```text
   # Example for a production deployment
   OV_MEET_SERVER_URL=https://your-openvidu-meet-domain.com
   ```

1. **Update the API key**: Ensure the `OV_MEET_API_KEY` environment variable in the `.env` file matches the API key configured in your production deployment. See [Generate an API Key](../../reference/rest-api/#generate-an-api-key) section to learn how to obtain it.

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
