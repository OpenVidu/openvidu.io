# OpenVidu Meet Recordings Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.4.1/meet-recordings)

This tutorial extends the [advanced OpenVidu Meet WebComponent tutorial](https://openvidu.io/3.4.1/meet/embedded/tutorials/webcomponent-advanced/index.md) to add **recording management capabilities**. It demonstrates how to list, view, and delete recordings from your OpenVidu Meet meetings.

The application includes all the features from the basic tutorial, plus:

- **List recordings**: View all available recordings from past meetings, with optional filtering by room.
- **View recordings**: Play recordings directly in the browser using the OpenVidu Meet WebComponent.
- **Delete recordings**: Remove recordings from the server.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop**. You can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) .

Run this command in Docker Desktop's terminal:

```bash
docker compose -p openvidu-meet -f oci://openvidu/local-meet:3.4.1 up -y openvidu-meet-init
```

Info

For a detailed guide on how to run OpenVidu Meet locally, visit [Try OpenVidu Meet locally](https://openvidu.io/3.4.1/meet/deployment/local/index.md) .

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-meet-tutorials.git -b 3.4.1
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download) (≥ 18) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-recordings
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

This tutorial builds upon the [advanced OpenVidu Meet WebComponent tutorial](https://openvidu.io/3.4.1/meet/embedded/tutorials/webcomponent-advanced/index.md), adding recording management functionality. We'll focus on the new features and modifications related to recordings.

______________________________________________________________________

### Backend modifications

The main changes to the backend involve adding new endpoints for recording management in the `src/index.js` file:

- **`GET /recordings`**: List all recordings, with optional filtering by room.
- **`DELETE /recordings/:recordingId`**: Delete a specific recording.
- **`GET /recordings/:recordingId/url`**: Get the playback URL for a specific recording.

Let's see the code of each new endpoint:

______________________________________________________________________

#### List recordings

The `GET /recordings` endpoint retrieves the list of recordings, with optional room filtering:

```javascript
// List all recordings
app.get('/recordings', async (req, res) => {
    // Create the base path for recordings, including maxItems parameter
    let recordingsPath = `recordings?maxItems=100`; // (1)!

    const { room: roomName } = req.query; // (2)!
    if (roomName) {
        // If a room is specified, filter recordings by room
        recordingsPath += `&roomId=${roomName}`; // (3)!
    }

    try {
        const { recordings } = await httpRequest('GET', recordingsPath); // (4)!
        res.status(200).json({ recordings }); // (5)!
    } catch (error) {
        handleApiError(res, error, 'Error fetching recordings');
    }
});
```

1. Create the base path for fetching recordings, including a `maxItems` parameter to limit the number of recordings returned to 100.
1. Extract optional room name from query parameters for filtering.
1. If a room name is provided, it appends the `roomId` parameter to the recordings path to filter recordings by that room.
1. Fetch recordings using the OpenVidu Meet API by sending a `GET` request to the constructed `recordingsPath`.
1. The server returns a `200 OK` response with the list of recordings in JSON format.

This endpoint does the following:

1. Creates the base path for fetching recordings, including a `maxItems` parameter to limit the number of recordings returned to 100.
1. Extracts an optional room name from the query parameters for filtering. If a room name is provided, it appends the `roomId` parameter to the recordings path to filter recordings by that room.
1. Fetches recordings using the OpenVidu Meet API by sending a `GET` request to the constructed `recordingsPath`.
1. If successful, it returns a `200 OK` response with the list of recordings in JSON format. Otherwise, the error is handled by the `handleApiError` function.

______________________________________________________________________

#### Delete recording

The `DELETE /recordings/:recordingId` endpoint deletes the specified recording:

```javascript
// Delete a recording
app.delete('/recordings/:recordingId', async (req, res) => {
    const { recordingId } = req.params; // (1)!

    try {
        // Delete the recording using OpenVidu Meet API
        await httpRequest('DELETE', `recordings/${recordingId}`); // (2)!
        res.status(200).json({ message: `Recording '${recordingId}' deleted successfully` }); // (3)!
    } catch (error) {
        handleApiError(res, error, `Error deleting recording '${recordingId}'`);
    }
});
```

1. The `recordingId` parameter is obtained from the request parameters.
1. The recording is deleted using the OpenVidu Meet API by sending a `DELETE` request to the `recordings/:recordingId` endpoint.
1. The server returns a `200 OK` response with a success message.

This endpoint simply deletes the specified recording using the OpenVidu Meet API by sending a `DELETE` request to the `recordings/:recordingId` endpoint. If the deletion is successful, it returns a `200 OK` response with a success message. Otherwise, the error is handled by the `handleApiError` function.

______________________________________________________________________

#### Get recording URL

A new `GET /recordings/:recordingId/url` endpoint retrieves the recording URL for playback:

```javascript
// Get recording URL
app.get('/recordings/:recordingId/url', async (req, res) => {
    const { recordingId } = req.params; // (1)!

    try {
        // Fetch the recording URL using OpenVidu Meet API
        const { url } = await httpRequest('GET', `recordings/${recordingId}/url`); // (2)!
        res.status(200).json({ url }); // (3)!
    } catch (error) {
        handleApiError(res, error, `Error fetching URL for recording '${recordingId}'`);
    }
});
```

1. The `recordingId` parameter is obtained from the request parameters.
1. Fetch the recording URL from the OpenVidu Meet API by sending a `GET` request to the `recordings/:recordingId/url` endpoint.
1. The server returns a `200 OK` response with the recording URL.

This endpoint retrieves the playback URL for a specific recording by sending a `GET` request to the `recordings/:recordingId/url` endpoint. If successful, it returns a `200 OK` response with the recording URL. Otherwise, the error is handled by the `handleApiError` function.

______________________________________________________________________

### Frontend modifications

The frontend has been enhanced to include recording management functionality. The main changes are in the `public/js/app.js` file:

#### Additional state management

A new `Map` is created to store recordings indexed by their recording ID:

```javascript
const rooms = new Map();
const recordings = new Map(); // (1)!
```

1. Added a recordings map to store recording data indexed by recording ID.

______________________________________________________________________

#### Enhanced room list template

The room list template is updated to include a `View Recordings` button for each room:

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
                    class="btn btn-success btn-sm" 
                    onclick="listRecordingsByRoom('${room.roomName}');"
                >
                    View Recordings
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

This button calls the `listRecordingsByRoom()` function when clicked, passing the room name as an argument. This allows users to view recordings for that specific room.

```javascript
async function listRecordingsByRoom(roomName) {
    // Hide the home screen and show the recordings screen
    const homeScreen = document.querySelector('#home');
    homeScreen.hidden = true; // (1)!
    const recordingsScreen = document.querySelector('#recordings');
    recordingsScreen.hidden = false; // (2)!

    // Set the room name in the search input
    const roomNameInput = document.querySelector('#recordings-room-search');
    roomNameInput.value = roomName; // (3)!

    await listRecordings(); // (4)!
}
```

1. Hide the home screen
1. Show the recordings screen.
1. Pre-fill the room search input with the selected room name.
1. Call the `listRecordings()` function to fetch and display recordings for the room.

This function sets up the recordings view by hiding the home screen, showing the recordings screen, pre-filling the room search input with the selected room name, and calling the `listRecordings()` function to fetch and display recordings for that room.

______________________________________________________________________

#### Listing recordings

The `listRecordings()` function fetches and displays recordings, optionally filtering by room name:

```javascript
async function listRecordings() {
    // Filter recordings by room name if provided
    const roomName = document.querySelector('#recordings-room-search').value; // (1)!
    const recordingsUrl = '/recordings' + (roomName ? `?room=${roomName}` : ''); // (2)!

    try {
        let { recordings: recordingsList } = await httpRequest('GET', recordingsUrl); // (3)!
        // Filter completed recordings
        recordingsList = filterCompletedRecordings(recordingsList); // (4)!

        // Clear the previous recordings and populate the new ones
        recordings.clear();
        recordingsList.forEach((recording) => {
            recordings.set(recording.recordingId, recording); // (5)!
        });
        renderRecordings(); // (6)!
    } catch (error) {
        console.error('Error listing recordings:', error.message);

        // Show error message
        const recordingsErrorElement = document.querySelector('#no-recordings-or-error');
        recordingsErrorElement.textContent = 'Error loading recordings';
        recordingsErrorElement.hidden = false;
    }
}

function filterCompletedRecordings(recordingList) {
    return recordingList.filter((recording) => recording.status === 'complete'); // (7)!
}
```

1. Get the room name from the search input for filtering.
1. Build the API URL with optional room filter parameter.
1. Make a `GET` request to the `/recordings` endpoint to fetch the list of recordings.
1. Call the `filterCompletedRecordings()` function to filter out recordings not completed.
1. For each recording in the filtered list, add it to the `recordings` map indexed by recording ID.
1. Call the `renderRecordings()` function to display the list of recordings in the UI.
1. Filter recordings to include only those with 'complete' status.

The listRecordings() function performs the following actions:

1. Gets the room name from the search input field to optionally filter recordings by room.
1. Makes a `GET` request to the `/recordings` endpoint to fetch the list of recordings, including the room filter parameter if specified.
1. Filters the recordings to show only those with `complete` status using the `filterCompletedRecordings()` function.
1. For each recording in the filtered list, it adds the recording to the `recordings` map. This map is used to store the recordings indexed by their recording IDs to make it easier to access them later.
1. Calls the `renderRecordings()` function to display the list of recordings.
1. If an error occurs during the request, it logs the error and displays an appropriate error message.

The `renderRecordings()` function is responsible for updating the UI with the list of recordings:

```javascript
function renderRecordings() {
    // Clear the previous list of recordings
    const recordingsList = document.querySelector('#recordings-list ul'); // (1)!
    recordingsList.innerHTML = ''; // (2)!

    // Show or remove the "No recordings found" message
    const noRecordingsElement = document.querySelector('#no-recordings-or-error');
    if (recordings.size === 0) {
        noRecordingsElement.textContent = 'No recordings found for the filters applied.';
        noRecordingsElement.hidden = false;
        return;
    } else {
        noRecordingsElement.textContent = '';
        noRecordingsElement.hidden = true;
    }

    // Sort recordings by start date in ascending order
    const recordingsArray = Array.from(recordings.values());
    const sortedRecordings = sortRecordingsByDate(recordingsArray); // (3)!

    // Add recordings to the list element
    sortedRecordings.forEach((recording) => {
        const recordingItem = getRecordingListItemTemplate(recording); // (4)!
        recordingsList.innerHTML += recordingItem;
    });
}
```

1. Get the `ul` element where the list of recordings will be displayed.
1. Clear the previous list of recordings.
1. Sort recordings by start date in ascending order.
1. For each recording, get the HTML template for the recording list item.
1. Append the recording item to the list element.

The `renderRecordings()` function performs the following actions:

1. Clears the previous list of recordings by getting the `ul` element and setting its inner HTML to an empty string.
1. Checks if there are any recordings in the `recordings` map. If there are no recordings, it shows a message indicating that no recordings were found for the filters applied. Otherwise, it hides the message.
1. Sorts the recordings by start date in ascending order using the `sortRecordingsByDate()` function.
1. For each recording in the sorted list, it calls the `getRecordingListItemTemplate()` function to get the HTML template for the recording list item.
1. Appends the recording item to the list element.

The `getRecordingListItemTemplate()` function generates the HTML template for each recording list item:

```javascript
function getRecordingListItemTemplate(recording) {
    const recordingId = recording.recordingId; // (1)!
    const roomName = recording.roomName; // (2)!
    const startDate = recording.startDate ? new Date(recording.startDate).toLocaleString() : '-'; // (3)!
    const duration = recording.duration ? secondsToHms(recording.duration) : '-'; // (4)!
    const size = recording.size ? formatBytes(recording.size ?? 0) : '-'; // (5)!

    return `
        <li class="recording-container">
            <i class="fa-solid fa-file-video"></i>
            <div class="recording-info">
                <p class="recording-name">${roomName}</p>
                <p><span class="recording-info-tag">Start date: </span><span class="recording-info-value">${startDate}</span></p>
                <p><span class="recording-info-tag">Duration: </span><span class="recording-info-value">${duration}</span></p>
                <p><span class="recording-info-tag">Size: </span><span class="recording-info-value">${size}</span></p>
            </div>
            <div class="recording-actions">
                <button title="Play" class="icon-button" onclick="displayRecording('${recordingId}')">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button title="Delete recording" class="icon-button delete-button" onclick="deleteRecording('${recordingId}')">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}
```

1. Retrieve the recording ID.
1. Retrieve the room name associated with the recording.
1. Format the start date for display.
1. Convert the duration from seconds to a human-readable format using the `secondsToHms()` helper function.
1. Format the file size using the `formatBytes()` helper function.

This function creates an HTML list item containing the recording's metadata, including the room name associated with the recording, start date, duration, and file size, along with buttons to play and delete the recording. The buttons call the `displayRecording()` and `deleteRecording()` functions respectively, passing the recording ID as an argument. The recording information is formatted using helper functions like `secondsToHms()` for duration and `formatBytes()` for file size to provide a user-friendly display.

______________________________________________________________________

#### Playing recording

When the user clicks the play button for a recording, the `displayRecording()` function is called:

```javascript
async function displayRecording(recordingId) {
    // Hide the recordings screen and show the display recording screen
    const recordingsScreen = document.querySelector('#recordings');
    recordingsScreen.hidden = true; // (1)!
    const displayRecordingScreen = document.querySelector('#display-recording');
    displayRecordingScreen.hidden = false; // (2)!

    // Get the recording media URL and set it to the source of the video element
    const recordingUrl = await getRecordingUrl(recordingId); // (3)!

    // Inject the OpenVidu Meet component into the display recording container specifying the recording URL
    displayRecordingScreen.innerHTML = `
        <openvidu-meet 
            recording-url="${recordingUrl}"
        >
        </openvidu-meet>
    `; // (4)!
}

async function getRecordingUrl(recordingId) {
    try {
        const { url } = await httpRequest('GET', `/recordings/${recordingId}/url`); // (5)!
        return url;
    } catch (error) {
        console.error('Error fetching recording URL:', error.message);
        return null;
    }
}
```

1. Hide the recordings list screen.
1. Show the recording playback screen.
1. Fetch the recording URL from the backend using the `getRecordingUrl()` function.
1. Inject the OpenVidu Meet WebComponent with the `recording-url` attribute for playback.
1. Make a `GET` request to the `/recordings/:recordingId/url` endpoint to retrieve the recording URL.

The `displayRecording()` function handles the playback of a specific recording by first hiding the recordings list screen and showing the display recording screen. It then fetches the recording URL from the backend using the `getRecordingUrl()` helper function, which makes a `GET` request to the `/recordings/:recordingId/url` endpoint. Finally, it injects the OpenVidu Meet WebComponent into the display container with the `recording-url` attribute set to the fetched URL, enabling the recording to be played directly in the browser. If an error occurs during URL fetching, it logs the error to the console and returns null.

______________________________________________________________________

#### Deleting recording

When the user clicks the delete recording button, the `deleteRecording()` function is called:

```javascript
async function deleteRecording(recordingId) {
    try {
        await httpRequest('DELETE', `/recordings/${recordingId}`); // (1)!

        // Remove the recording from the list
        recordings.delete(recordingId); // (2)!
        renderRecordings(); // (3)!
    } catch (error) {
        console.error('Error deleting recording:', error.message);
    }
}
```

1. Make a `DELETE` request to the `/recordings/:recordingId` endpoint to delete the specified recording.
1. Remove the recording from the `recordings` map.
1. Call the `renderRecordings()` function to update the list of recordings.

The `deleteRecording()` function simply makes a `DELETE` request to the `/recordings/:recordingId` endpoint to delete the specified recording. If the recording is successfully deleted, it removes the recording from the `recordings` map and calls the `renderRecordings()` function to update the list of recordings. If an error occurs during recording deletion, it logs the error to the console.

## Accessing this tutorial from other computers or phones

To access this tutorial from other computers or phones, follow these steps:

1. **Ensure network connectivity**: Make sure your device (computer or phone) is connected to the same network as the machine running OpenVidu Meet and this tutorial.

1. **Configure OpenVidu Meet for network access**: Start OpenVidu Meet by following the instructions in the [Accessing OpenVidu Meet from other computers or phones](https://openvidu.io/3.4.1/meet/deployment/local/#accessing-openvidu-meet-from-other-computers-or-phones) section.

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

If you have a production deployment of OpenVidu Meet (installed in a server following [deployment steps](https://openvidu.io/3.4.1/meet/deployment/basic/index.md) ), you can connect this tutorial to it by following these steps:

1. **Update the server URL**: Modify the `OV_MEET_SERVER_URL` environment variable in the `.env` file to point to your OpenVidu Meet production deployment URL.

   ```text
   # Example for a production deployment
   OV_MEET_SERVER_URL=https://your-openvidu-meet-domain.com
   ```

1. **Update the API key**: Ensure the `OV_MEET_API_KEY` environment variable in the `.env` file matches the API key configured in your production deployment. See [Generate an API Key](https://openvidu.io/3.4.1/meet/embedded/reference/rest-api/#generate-an-api-key) section to learn how to obtain it.

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
