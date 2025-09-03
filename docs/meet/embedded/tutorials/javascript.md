---
title: OpenVidu Meet Node.js and JavaScript Tutorial
description: Learn how to build a video conferencing application using Node.js and JavaScript by easily integrating OpenVidu Meet WebComponent.
---

# Node.js and JavaScript Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/main/meet-node){ .md-button target=\_blank }

This tutorials is a simple example of how to integrate **OpenVidu Meet** into a **Node.js** application. It is built using **Node.js and Express** for the backend and plain **HTML/CSS/JavaScript** for the frontend.

At the end of this tutorial, you will have a fully functional simple video-call application with the following features:

-   Users can create rooms.
-   Users can delete rooms.
-   Users can join a room as moderator or speaker.
-   Users can chat with other participants.
-   Moderators can record the meeting.
-   Users may leave the room at any time.
-   Moderators may end the meeting at any time, disconnecting all participants.
-   Users can view the recordings of the meeting.

The application uses the [OpenVidu Meet API](../../embedded/reference/rest-api.md) to create and delete rooms, and the [OpenVidu Meet WebComponent](../../embedded/reference/webcomponent.md) to create the video call interface and internal management.

## Running this tutorial

#### 1. Run OpenVidu Server

--8<-- "shared/tutorials/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b main
```

### 3. Run the application

To run this application, you need [Node.js :fontawesome-solid-external-link:{.external-link-icon}](https://nodejs.org/en/download){:target="\_blank"} installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-node
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

This application is designed to be beginner-friendly and consists of one essential backend file under the `src` directory:

-   `index.js`: This file holds the server application and defines the REST API endpoints.

And the following essential frontend files under the `public` directory:

-   `index.html`: This is the client application's main HTML file.
-   `app.js`: This is the main JavaScript file that interacts with the server application and handles the client application's logic and functionality.
-   `style.css`: This file contains the client application's styling.

---

### Backend

The server application is a simple Express app with a single file `index.js` that exports three endpoints:

-   **`POST /rooms`**: Create a new room with the given room name.
-   **`GET /rooms`**: Get the list of rooms.
-   **`DELETE /rooms/:roomName`**: Delete a room with the given room name.

Let's see the code of the `index.js` file:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/src/index.js#L1-L26' target='_blank'>index.js</a>" linenums="1"
import dotenv from 'dotenv';
import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config(); // (1)!

// Configuration
const SERVER_PORT = process.env.SERVER_PORT || 6080; // (2)!
const OV_MEET_SERVER_URL = process.env.OV_MEET_SERVER_URL || 'http://localhost:9080'; // (3)!
const OV_MEET_API_KEY = process.env.OV_MEET_API_KEY || 'meet-api-key'; // (4)!

const app = express(); // (5)!

app.use(cors()); // (6)!
app.use(express.json()); // (7)!
app.use(bodyParser.urlencoded({ extended: true }));

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(path.join(__dirname, '../public'))); // (8)!

// OpenVidu Meet rooms indexed by name
const rooms = new Map(); // (9)!
```

1. Load environment variables from `.env` file.
2. The port where the application will be listening.
3. The OpenVidu Meet server URL.
4. The OpenVidu Meet API key.
5. Initialize the Express application.
6. Enable CORS support.
7. Enable JSON body parsing.
8. Serve static files from the `public` directory.
9. Create a map to store OpenVidu Meet rooms indexed by name.

The `index.js` file imports the required dependencies and loads the necessary environment variables:

-   `SERVER_PORT`: The port where the application will be listening.
-   `OV_MEET_SERVER_URL`: The OpenVidu Meet server URL.
-   `OV_MEET_API_KEY`: The OpenVidu Meet API key.

Then the `express` application is initialized. CORS is allowed, JSON body parsing is enabled and static files are served from the `public` directory.

Finally, a map is created to store OpenVidu Meet rooms indexed by name.

Now let's see the code of each endpoint:

---

#### Create room

The `POST /rooms` endpoint creates a new room. It receives the room name as a parameter and returns the newly created room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/src/index.js#L28-L68' target='_blank'>index.js</a>" linenums="28"
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
            preferences: {
                // (5)!
                chatPreferences: {
                    enabled: true // Enable chat for this room
                },
                recordingPreferences: {
                    enabled: true, // Enable recording for this room
                    allowAccessTo: 'admin-moderator-speaker' // Allow access to recordings for admin, moderator and speaker roles
                },
                virtualBackgroundPreferences: {
                    enabled: true // Enable virtual background for this room
                }
            }
        });

        console.log('Room created:', room);
        rooms.set(roomName, room); // (6)!
        res.status(201).json({ message: `Room '${roomName}' created successfully`, room }); // (7)!
    } catch (error) {
        console.error(`Error while creating room '${roomName}':`, error);
        res.status(500).json({ message: `Error creating room '${roomName}'` }); // (8)!
    }
});
```

1. The `roomName` parameter is obtained from the request body.
2. If the `roomName` is not provided, the server returns a `400 Bad Request` response.
3. If there is already a room with the same name, the server returns a `400 Bad Request` response.
4. Specify the name of the room.
5. Set the preferences for the room, enabling chat, recording and virtual background.
6. The room is stored in the `rooms` map.
7. The server returns a `201 Created` response with the room object.
8. If an error occurs during room creation, the server returns a `500 Internal Server Error` response.

This endpoint does the following:

1. The `roomName` parameter is obtained from the request body. If it is not provided, the server returns a `400 Bad Request` response.
2. The server checks if the room name already exists in the `rooms` map. If it does, a `400 Bad Request` response is returned with an appropriate error message.
3. A new room is created using the OpenVidu Meet API by sending a `POST` request to the `rooms` endpoint. The request includes the room name and additional preferences:

    - **Chat Preferences**: Enables chat functionality for the room.
    - **Recording Preferences**: Enables recording for the room and allows access to recordings for the roles `admin`, `moderator` and `speaker`.
    - **Virtual Background Preferences**: Enables virtual background functionality for the room.

    To send requests to the OpenVidu Meet API, we use the `httpRequest` function:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/src/index.js#L104-L123' target='_blank'>index.js</a>" linenums="104"
    // Function to make HTTP requests to OpenVidu Meet API
    const httpRequest = async (method, path, body) => {
        // (1)!
        const response = await fetch(`${OV_MEET_SERVER_URL}/api/v1/${path}`, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': OV_MEET_API_KEY // Include the API key in the header for authentication
            },
            body: body ? JSON.stringify(body) : undefined // (2)!
        });

        const responseBody = await response.json(); // (3)!

        if (!response.ok) {
            console.error('Error while performing request to OpenVidu Meet API:', responseBody);
            throw new Error('Failed to perform request to OpenVidu Meet API'); // (4)!
        }

        return responseBody; // (5)!
    };
    ```

    1. Perform an HTTP request to the OpenVidu Meet API in the specified method and path.
    2. Include the body in the request if provided.
    3. Parse the response body as JSON.
    4. If the response is not OK, throw an error with the message from the response.
    5. Return the response body.

    This function makes HTTP requests to the OpenVidu Meet API using the `fetch` function. It receives the HTTP method, path and body as parameters. The API key is included in the request headers for authentication.

    If the response status is `204 No Content`, it does not return anything. Otherwise, it parses the response body as JSON and checks if the response is OK. If not, it throws an error with the message from the response.

4. The room name is added to the room object for easier access, and the room is stored in the `rooms` map.
5. If the room is successfully created, the server returns a `201 Created` response with the room object. Otherwise, the server logs the error and returns a `500 Internal Server Error` response with an appropriate error message.

---

#### List rooms

The `GET /rooms` endpoint retrieves the list of rooms created in the application:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/src/index.js#L70-L74' target='_blank'>index.js</a>" linenums="70"
// List all rooms
app.get('/rooms', (_req, res) => {
    const roomsArray = Array.from(rooms.values()); // (1)!
    res.status(200).json({ rooms: roomsArray }); // (2)!
});
```

1. Get the values of the `rooms` map and convert it to an array.
2. The server returns a `200 OK` response with the list of rooms.

This endpoint retrieves the list of rooms by converting the values of the `rooms` map to an array and returning it in a JSON object with the property `rooms`.

---

#### Delete room

The `DELETE /room/:roomName` endpoint deletes the specified room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/src/index.js#L76-L97' target='_blank'>index.js</a>" linenums="76"
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
        console.error(`Error while deleting room '${roomName}':`, error);
        res.status(500).json({ message: `Error deleting room '${roomName}'` }); // (7)!
    }
});
```

1. The `roomName` parameter is obtained from the request parameters.
2. Get the room from the `rooms` map.
3. If the room does not exist, the server returns a `404 Not Found` response.
4. The room is deleted using the OpenVidu Meet API by sending a `DELETE` request to the `rooms/:roomId` endpoint.
5. The room is removed from the `rooms` map.
6. The server returns a `200 OK` response with a success message.
7. If an error occurs during room deletion, the server returns a `500 Internal Server Error` response with an appropriate error message.

This endpoint does the following:

1. The `roomName` parameter is obtained from the request parameters.
2. The server checks if the room exists in the `rooms` map. If it does not, a `404 Not Found` response is returned with an appropriate error message.
3. The room is deleted using the OpenVidu Meet API by sending a `DELETE` request to the `rooms/:roomId` endpoint.
4. The room is removed from the `rooms` map.
5. If the room is successfully deleted, the server returns a `200 OK` response with a success message. Otherwise, the server logs the error and returns a `500 Internal Server Error` response with an appropriate error message.

---

### Frontend

The client application consists of only three essential files that are located in the `public` directory:

-   `app.js`: This is the main JavaScript file for the sample application. It contains the logic for listing, creating and deleting rooms, joining a room, and handling the events triggered by the OpenVidu Meet WebComponent.
-   `index.html`: This HTML file is responsible for creating the user interface. It contains the list of created rooms, a form to create a new room, and the OpenVidu Meet WebComponent to access the video call.
-   `styles.css`: This file contains CSS classes that are used to style the `index.html` page.

To use the OpenVidu Meet WebComponent in your application, you need to include it in your HTML file. You can do this by adding a script tag to the end of the `<body>` section of the HTML file, indicating the corresponding URL in the `src` attribute:

```html title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/index.html#L72-L73' target='_blank'>index.html</a>" linenums="72"
<!-- OpenVidu Meet WebComponent bundle -->
<script src="http://localhost:9080/v1/openvidu-meet.js"></script>
```

!!! warning "Configure the `src` URL"

    When [running OpenVidu locally](#run-openvidu-locally), the `src` URL shown above will work if you access the application from the same device where OpenVidu Meet and OpenVidu are running. However, if you access the application from a different device, you need to replace `http://localhost:9080` with `https://xxx-yyy-zzz-www.openvidu-local.dev:9443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.).

    _This is one advantage of [running OpenVidu locally](#run-openvidu-locally), that you can test your application client with other devices in your local network very easily without worrying about SSL certificates. For more information, see section [Accessing your local deployment from other devices on your network](../../../docs/self-hosting/local.md#accessing-your-local-deployment-from-other-devices-on-your-network)._

    On the other hand, when using another [OpenVidu deployment type](#deploy-openvidu), you should configure the domain part of the `src` URL with the correct URL depending on your deployment.

Now let's see the code of the `app.js` file grouped by sections:

---

#### Listing rooms

The list of rooms is displayed in the `index.html` file as soon as the page loads. This is done by calling the `fetchRooms()` function, which fetches the list of rooms from the server and updates the UI accordingly.

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/js/app.js#L1-L23' target='_blank'>app.js</a>" linenums="1"
const rooms = new Map(); // (1)!

document.addEventListener('DOMContentLoaded', async () => {
    await fetchRooms(); // (2)!
});

async function fetchRooms() {
    try {
        const { rooms: roomsList } = await httpRequest('GET', '/rooms'); // (3)!

        roomsList.forEach((room) => {
            rooms.set(room.roomName, room); // (4)!
        });
        renderRooms(); // (5)!
    } catch (error) {
        console.error('Error fetching rooms:', error);

        // Show error message
        const roomsErrorElement = document.querySelector('#no-rooms-or-error');
        roomsErrorElement.textContent = 'Error loading rooms';
        roomsErrorElement.hidden = false;
    }
}
```

1. Create a map to store the rooms.
2. When the DOM content is loaded, call the `fetchRooms()` function to fetch the list of rooms from the server.
3. Make a `GET` request to the `/rooms` endpoint to fetch the list of rooms.
4. For each room in the list, add it to the `rooms` map.
5. Call the `renderRooms()` function to display the list of rooms.

The `fetchRooms()` function performs the following actions:

1. Makes a `GET` request to the `/rooms` endpoint to fetch the list of rooms.

    To send requests to the backend, we use the `httpRequest` function:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/js/app.js#L196-L213' target='_blank'>app.js</a>" linenums="196"
    // Function to make HTTP requests to the backend
    async function httpRequest(method, path, body) {
        // (1)!
        const response = await fetch(path, {
            method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: body ? JSON.stringify(body) : undefined // (2)!
        });

        const responseBody = await response.json(); // (3)!

        if (!response.ok) {
            throw new Error('Failed to perform request to backend: ' + responseBody.message); // (4)!
        }

        return responseBody; // (5)!
    }
    ```

    1. Perform an HTTP request to the backend in the specified method and path.
    2. Include the body in the request if provided.
    3. Parse the response body as JSON.
    4. If the response is not OK, throw an error with the message from the response.
    5. Return the response body.

    This function makes HTTP requests to the server API using the `fetch` function. It receives the HTTP method, path and body as parameters. Then, it parses the response body as JSON and checks if the response is OK. If not, it throws an error with the message from the response.

2. For each room in the list, it adds the room to the `rooms` map. This map is used to store the rooms indexed by their names to make it easier to access them later.
3. Calls the `renderRooms()` function to display the list of rooms.
4. If an error occurs during the request, it logs the error and displays an appropriate error message.

The `renderRooms()` function is responsible for updating the UI with the list of rooms:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/js/app.js#L25-L79' target='_blank'>app.js</a>" linenums="25"
function renderRooms() {
    // Clear the previous list of rooms
    const roomsList = document.querySelector('#rooms-list ul'); // (1)!
    roomsList.innerHTML = ''; // (2)!

    // Show or remove the "No rooms found" message
    const noRoomsElement = document.querySelector('#no-rooms-or-error');
    if (rooms.size === 0) {
        noRoomsElement.textContent = 'No rooms found. Please create a new room.';
        noRoomsElement.hidden = false;
        return;
    } else {
        noRoomsElement.textContent = '';
        noRoomsElement.hidden = true;
    }

    // Add rooms to the list element
    Array.from(rooms.values()).forEach((room) => {
        const roomItem = getRoomListItemTemplate(room); // (3)!
        roomsList.innerHTML += roomItem; // (4)!
    });
}

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
                        'speaker',
                    );"
                >
                    Join as Speaker
                </button>
                <button title="Delete room" class="icon-button delete-button" onclick="deleteRoom('${room.roomName}');">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}
```

1. Get the `ul` element where the list of rooms will be displayed.
2. Clear the previous list of rooms.
3. For each room, get the HTML template for the room list item.
4. Append the room item to the list element.

The `renderRooms()` function performs the following actions:

1. Clears the previous list of rooms by getting the `ul` element and setting its inner HTML to an empty string.
2. Checks if there are any rooms in the `rooms` map. If there are no rooms, it shows a message indicating that no rooms were found. Otherwise, it hides the message.
3. For each room in the `rooms` map, it calls the `getRoomListItemTemplate()` function to get the HTML template for the room list item.
4. Appends the room item to the list element.

The `getRoomListItemTemplate()` function generates the HTML template for each room list item. It includes buttons to join the room as a moderator or speaker, and a button to delete the room. The buttons call the `joinRoom()` and `deleteRoom()` functions respectively, passing the room name and other necessary parameters.

---

#### Creating a room

After the user specifies the room name and clicks the `Create Room` button, the `createRoom()` function is called:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/js/app.js#L81-L113' target='_blank'>app.js</a>" linenums="81"
async function createRoom() {
    // Clear previous error message
    const errorDiv = document.querySelector('#create-room-error');
    errorDiv.textContent = '';
    errorDiv.hidden = true;

    try {
        const roomName = document.querySelector('#room-name').value; // (1)!

        const { room } = await httpRequest('POST', '/rooms', {
            roomName
        }); // (2)!

        // Add new room to the list
        rooms.set(roomName, room); // (3)!
        renderRooms(); // (4)!

        // Reset the form
        const createRoomForm = document.querySelector('#create-room form');
        createRoomForm.reset(); // (5)!
    } catch (error) {
        console.error('Error creating room:', error);

        // Show error message
        if (error.message.includes('already exists')) {
            errorDiv.textContent = 'Room name already exists';
        } else {
            errorDiv.textContent = 'Error creating room';
        }

        errorDiv.hidden = false;
    }
}
```

1. Get the room name from the input field.
2. Make a `POST` request to the `/rooms` endpoint to create a new room with the specified name.
3. Add the new room to the `rooms` map.
4. Call the `renderRooms()` function to update the list of rooms.
5. Reset the form to clear the input field.

The `createRoom()` function performs the following actions:

1. Clears any previous error messages.
2. Gets the room name from the input field.
3. Makes a `POST` request to the `/rooms` endpoint to create a new room with the specified name.
4. If the room is successfully created, it adds the new room to the `rooms` map and calls the `renderRooms()` function to update the list of rooms.
5. Resets the form to clear the input field.
6. If an error occurs during room creation, it logs the error and displays an appropriate error message.

---

#### Deleting a room

When the user clicks the delete room button, the `deleteRoom()` function is called:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/js/app.js#L115-L125' target='_blank'>app.js</a>" linenums="115"
async function deleteRoom(roomName) {
    try {
        await httpRequest('DELETE', `/rooms/${roomName}`); // (1)!

        // Remove the room from the list
        rooms.delete(roomName); // (2)!
        renderRooms(); // (3)!
    } catch (error) {
        console.error('Error deleting room:', error);
    }
}
```

1. Make a `DELETE` request to the `/rooms/:roomName` endpoint to delete the specified room.
2. Remove the room from the `rooms` map.
3. Call the `renderRooms()` function to update the list of rooms.

The `deleteRoom()` function simply makes a `DELETE` request to the `/rooms/:roomName` endpoint to delete the specified room. If the room is successfully deleted, it removes the room from the `rooms` map and calls the `renderRooms()` function to update the list of rooms. If an error occurs during room deletion, it logs the error to the console.

---

#### Joining a room

When the user clicks the `Join as Moderator` or `Join as Speaker` button, the `joinRoom()` function is called:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-meet-tutorials/blob/main/meet-node/public/js/app.js#L127-L194' target='_blank'>app.js</a>" linenums="127"
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
    meet.once('JOINED', () => {
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
    meet.once('LEFT', (event) => {
        // (9)!
        console.log('Local participant left the room. Reason:', event.reason);

        // Hide the room header
        roomHeader.hidden = true;
    });

    // Event listener for when the OpenVidu Meet component is closed
    meet.once('CLOSED', () => {
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
5. Add an event listener for the `JOINED` event, which is triggered when the local participant joins the room.
6. Set the room name in the header.
7. Show the end meeting button if the user is a moderator.
8. Call the `endMeeting()` method of the OpenVidu Meet WebComponent to end the meeting when the moderator clicks the `End Meeting` button.
9. Add an event listener for the `LEFT` event, which is triggered when the local participant leaves the room.
10. Add an event listener for the `CLOSED` event, which is triggered when the OpenVidu Meet component is closed.

The `joinRoom()` function performs the following actions:

1. Hides the home screen and shows the room screen.
2. Hides the room header until the local participant joins.
3. Injects the OpenVidu Meet WebComponent into the meeting container with the specified room URL.
4. Configures event listeners for the OpenVidu Meet WebComponent to handle different events:

    - **`JOINED`**: This event is triggered when the local participant joins the room. It shows the room header with the room name and displays the `End Meeting` button if the user is a moderator. It also adds an event listener for the `End Meeting` button to call the `endMeeting()` method of the OpenVidu Meet WebComponent to end the meeting. This method disconnects all participants and ends the meeting for everyone.
    - **`LEFT`**: This event is triggered when the local participant leaves the room. It hides the room header.
    - **`CLOSED`**: This event is triggered when the OpenVidu Meet component is closed. It hides the room screen and shows the home screen.
