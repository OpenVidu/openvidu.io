---
title: OpenVidu Meet WebComponent Commands & Events Tutorial
description: Learn how to build a video conferencing application using Node.js and JavaScript by integrating OpenVidu Meet WebComponent with advanced commands and event handling.
---

# OpenVidu Meet WebComponent Commands & Events Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.4.0/meet-webcomponent-commands-events){ .md-button target=\_blank }

This tutorial extends the [basic WebComponent tutorial](webcomponent.md) to add **advanced WebComponent functionality** through commands and event handling. It demonstrates how to interact with the OpenVidu Meet WebComponent programmatically and respond to meeting events.

The application includes all the features from the basic WebComponent tutorial, plus:

-   **WebComponent commands**: Control the meeting programmatically (e.g., end meeting for moderators).
-   **Event handling**: Listen to and respond to WebComponent events (joined, left, closed).
-   **Role-based UI**: Display different interface elements based on user role (moderator/speaker).
-   **Meeting header**: Show room information and controls above the WebComponent.
-   **Enhanced room management**: In-memory room tracking with unique names per room.

## Running this tutorial

#### 1. Run OpenVidu Meet

--8<-- "shared/tutorials/run-openvidu-meet.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.4.0
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

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/webcomponent-advanced-home.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/webcomponent-advanced-home.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/meet/tutorials/webcomponent-advanced-room.png" data-type="image" data-desc-position="bottom"><img src="../../../../assets/images/meet/tutorials/webcomponent-advanced-room.png" loading="lazy"/></a></p></div>

</div>

## Understanding the code

This tutorial builds upon the [basic WebComponent tutorial](webcomponent.md), adding advanced WebComponent interaction capabilities and enhanced room management. We'll focus on the key differences and new functionality.

---

### Backend

The backend is identical to previous tutorials. It provides the same three REST API endpoints:

-   **`POST /rooms`**: Create a new room with the given room name.
-   **`GET /rooms`**: Get the list of rooms.
-   **`DELETE /rooms/:roomId`**: Delete a room with the given room ID.

For detailed backend documentation, please refer to the [Direct Link tutorial backend section](direct-link.md#backend).

---

### Frontend modifications

The frontend changes focus on enhanced room management, WebComponent event handling, and role-based UI features.

#### Enhanced room template

The room template now passes additional parameters including role information:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.4.0/meet-webcomponent-commands-events/public/js/app.js#L48-83' target='_blank'>app.js</a>" linenums="48" hl_lines="6-25"
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

---

#### Advanced room joining with commands and events

The `joinRoom()` function has been significantly enhanced to handle WebComponent events and commands:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/3.4.0/meet-webcomponent-commands-events/public/js/app.js#L126-193' target='_blank'>app.js</a>" linenums="126"
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

## Accessing this tutorial from other computers or phones

--8<-- "shared/tutorials/access-tutorial-from-other-devices.md"

## Connecting this tutorial to an OpenVidu Meet production deployment

--8<-- "shared/tutorials/connect-tutorial-to-production-deployment.md"
