---
title: OpenVidu Meet WebComponent Commands & Events Tutorial
description: Learn how to build a video conferencing application using Node.js and JavaScript by integrating OpenVidu Meet WebComponent with advanced commands and event handling.
---

# OpenVidu Meet WebComponent Commands & Events Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/main/meet-webcomponent-commands-events){ .md-button target=\_blank }

This tutorial extends the [basic WebComponent tutorial](webcomponent.md) to add **advanced WebComponent functionality** through commands and event handling. It demonstrates how to interact with the OpenVidu Meet WebComponent programmatically and respond to meeting events.

The application includes all the features from the basic WebComponent tutorial, plus:

-   **WebComponent commands**: Control the meeting programmatically (e.g., end meeting for moderators).
-   **Event handling**: Listen to and respond to WebComponent events (joined, left, closed).
-   **Role-based UI**: Display different interface elements based on user role (moderator/speaker).
-   **Meeting header**: Show room information and controls above the WebComponent.
-   **Enhanced room management**: In-memory room tracking with unique names per room.

## Running this tutorial

#### 1. Run OpenVidu Meet

--8<-- "shared/tutorials/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b main
```

### 3. Run the application

To run this application, you need [Node.js :fontawesome-solid-external-link:{.external-link-icon}](https://nodejs.org/en/download){:target="\_blank"} installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-webcomponent-commands-events
```

2. Install dependencies

```bash
npm install
```

3. Run the application

```bash
npm start
```

Once the server is up and running, you can test the application by visiting [`http://localhost:6080`](http://localhost:6080){:target="\_blank"}. You should see a screen like this:

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/home-js.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/home-js.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/room-js.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/room-js.png" loading="lazy"/></a></p></div>

</div>

## Understanding the code

This tutorial builds upon the [basic WebComponent tutorial](webcomponent.md), adding advanced WebComponent interaction capabilities and enhanced room management. We'll focus on the key differences and new functionality.

---

### Backend modifications

The main backend changes involve implementing in-memory room tracking with unique room names and enhanced validation.

#### Enhanced room storage

The backend now uses room names as unique identifiers by storing rooms in a map indexed by name:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-webcomponent-commands-events/src/index.js#L25-L26' target='_blank'>index.js</a>" linenums="25"
// OpenVidu Meet rooms indexed by name
const rooms = new Map(); // (1)!
```

1. Create a map to store OpenVidu Meet rooms indexed by name.

---

#### Enhanced room creation

The room creation endpoint now includes name uniqueness validation:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-webcomponent-commands-events/src/index.js#L28-L67' target='_blank'>index.js</a>" linenums="28" hl_lines="10-14 37"
// Create a new room
app.post('/rooms', async (req, res) => {
    const { roomName } = req.body; // (1)!

    if (!roomName) {
        res.status(400).json({ message: `'roomName' is required` }); // (2)!
        return;
    }

    // Check if the room name already exists
    if (rooms.has(roomName)) {
        res.status(400).json({ message: `Room '${roomName}' already exists` }); // (3)!
        return;
    }

    try {
        // Create a new OpenVidu Meet room using the API
        const room = await httpRequest('POST', 'rooms', {
            roomName, // (4)!
            config: {
                // (5)!
                // Default room configuration
                chat: {
                    enabled: true // Enable chat for this room
                },
                recording: {
                    enabled: true, // Enable recording for this room
                    allowAccessTo: 'admin_moderator_speaker' // Allow access to recordings for admin, moderator and speaker roles
                },
                virtualBackground: {
                    enabled: true // Enable virtual background for this room
                }
            }
        });

        console.log('Room created:', room);
        rooms.set(roomName, room); // (6)!
        res.status(201).json({ message: `Room '${roomName}' created successfully`, room }); // (7)!
    } catch (error) {
        handleApiError(res, error, `Error creating room '${roomName}'`);
    }
});
```

1. The `roomName` parameter is obtained from the request body.
2. If the `roomName` is not provided, the server returns a `400 Bad Request` response.
3. If there is already a room with the same name, the server returns a `400 Bad Request` response.
4. Specify the name of the room.
5. Set the configuration for the room, enabling chat, recording and virtual background.
6. The room is stored in the `rooms` map.
7. The server returns a `201 Created` response with the room object.

The key difference from the basic tutorial is the addition of room name uniqueness validation and an in-memory map to track rooms by name.

---

#### Enhanced room deletion

The deletion endpoint now recieves the room name as a parameter instead of the room ID, and deletes the room from both the in-memory map and the OpenVidu Meet API:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-webcomponent-commands-events/src/index.js#L76-L96' target='_blank'>index.js</a>" linenums="76"
// Delete a room
app.delete('/rooms/:roomName', async (req, res) => {
    const { roomName } = req.params; // (1)!

    // Check if the room exists
    const room = rooms.get(roomName); // (2)!
    if (!room) {
        res.status(404).json({ message: `Room '${roomName}' not found` }); // (3)!
        return;
    }

    try {
        // Delete the OpenVidu Meet room using the API
        await httpRequest('DELETE', `rooms/${room.roomId}`); // (4)!

        rooms.delete(roomName); // (5)!
        res.status(200).json({ message: `Room '${roomName}' deleted successfully` }); // (6)!
    } catch (error) {
        handleApiError(res, error, `Error deleting room '${roomName}'`);
    }
});
```

1. The `roomName` parameter is obtained from the request parameters.
2. Get the room from the `rooms` map.
3. If the room does not exist, the server returns a `404 Not Found` response.
4. The room is deleted using the OpenVidu Meet API by sending a `DELETE` request to the `rooms/:roomId` endpoint.
5. The room is removed from the `rooms` map.
6. The server returns a `200 OK` response with a success message.

This approach ensures data consistency between the in-memory map and the OpenVidu Meet API.

---

### Frontend modifications

The frontend changes focus on enhanced room management, WebComponent event handling, and role-based UI features.

#### Enhanced state management

The rooms map now uses room names as keys instead of IDs. Therefore, the frontend code has been updated to reflect this change.

---

#### Enhanced room template

The room template now passes additional parameters including role information:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-webcomponent-commands-events/public/js/app.js#L48-83' target='_blank'>app.js</a>" linenums="48" hl_lines="6-25"
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
                    onclick="deleteRoom('${room.roomName}');"
                >
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}
```

The template now provides the room name and user role to the `joinRoom()` function, enabling role-based functionality and proper room identification.

---

#### Advanced room joining with commands and events

The `joinRoom()` function has been significantly enhanced to handle WebComponent events and commands:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-webcomponent-commands-events/public/js/app.js#L131-198' target='_blank'>app.js</a>" linenums="131"
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
2. Show the room screen.
3. Hide the room header until the local participant joins.
4. Inject the OpenVidu Meet WebComponent into the meeting container with the specified room URL.
5. Add an event listener for the `joined` event, which is triggered when the local participant joins the room.
6. Set the room name in the header.
7. Show the end meeting button if the user is a moderator.
8. Call the `endMeeting()` method of the OpenVidu Meet WebComponent to end the meeting when the moderator clicks the `End Meeting` button.
9. Add an event listener for the `left` event, which is triggered when the local participant leaves the room.
10. Add an event listener for the `closed` event, which is triggered when the OpenVidu Meet component is closed.

The enhanced `joinRoom()` function now performs the following actions:

1. Hides the home screen and shows the room screen.
2. Hides the room header until the local participant joins.
3. Injects the OpenVidu Meet WebComponent into the meeting container with the specified room URL.
4. Configures event listeners for the OpenVidu Meet WebComponent to handle different events:

    - **`joined`**: This event is triggered when the local participant joins the room. It shows the room header with the room name and displays the `End Meeting` button if the user is a moderator. It also adds an event listener for the `End Meeting` button to call the `endMeeting()` method of the OpenVidu Meet WebComponent to end the meeting. This method disconnects all participants and ends the meeting for everyone.
    - **`left`**: This event is triggered when the local participant leaves the room. It hides the room header.
    - **`closed`**: This event is triggered when the OpenVidu Meet component is closed. It hides the room screen and shows the home screen.
