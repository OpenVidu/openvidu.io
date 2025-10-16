# OpenVidu Meet Webhooks Tutorial

[Source code](https://github.com/OpenVidu/openvidu-meet-tutorials/tree/3.4.0/meet-webhooks)

This tutorial extends the [recordings tutorial](../recordings/) to add **real-time updates** through webhooks and Server-Sent Events (SSE). It demonstrates how to receive and process OpenVidu Meet webhooks to provide live status updates for rooms and recordings.

The application includes all the features from the recordings tutorial, plus:

- **Real-time room status updates**: Live updates when meetings start or end.
- **Live recording updates**: Instant updates when recordings are completed.
- **Webhook validation**: Secure webhook processing with signature verification.
- **Room status badges**: Visual indicators showing room status (open, active, closed).
- **Server-Sent Events**: Efficient real-time communication between server and client.

## Running this tutorial

#### 1. Run OpenVidu Meet

You need **Docker Desktop**. You can install it on [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) , [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) or [Linux](http://docs.docker.com/desktop/setup/install/linux/) .

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

To run this application, you need [Node.js](https://nodejs.org/en/download) (≥ 18) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-meet-tutorials/meet-webhooks
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

This tutorial builds upon the [recordings tutorial](../recordings/), adding real-time functionality through webhooks and Server-Sent Events. We'll focus on the new webhook handling capabilities and live update features.

______________________________________________________________________

### Backend modifications

The main backend changes involve implementing webhook processing, SSE communication, and security validation.

#### Server-Sent Events setup

The backend now includes SSE support for real-time client notifications:

```javascript
import bodyParser from 'body-parser';
import cors from 'cors';
import crypto from 'crypto';
import dotenv from 'dotenv';
import express from 'express';
import SSE from 'express-sse'; // (1)!
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

// Configuration
const SERVER_PORT = process.env.SERVER_PORT || 6080;
const OV_MEET_SERVER_URL = process.env.OV_MEET_SERVER_URL || 'http://localhost:9080';
const OV_MEET_API_KEY = process.env.OV_MEET_API_KEY || 'meet-api-key';
const MAX_WEBHOOK_AGE = 120 * 1000; // 2 minutes in milliseconds

// Create SSE instance for real-time notifications
const sse = new SSE(); // (2)!
```

1. Import the `express-sse` library for Server-Sent Events functionality.
1. Create an SSE instance to manage real-time notifications to connected clients.

This code sets up the backend to support Server-Sent Events (SSE), enabling the server to push real-time notifications to connected clients. It imports the `express-sse` library and initializes an SSE instance for managing live event streams.

______________________________________________________________________

#### SSE endpoint for client subscriptions

A new endpoint allows clients to subscribe to real-time notifications:

```javascript
// SSE endpoint for real-time notifications
app.get('/events', sse.init); // (1)!
```

1. Create an SSE endpoint that clients can connect to for receiving real-time webhook notifications.

This endpoint enables clients to establish a persistent connection for receiving live updates about room status changes and recording completions.

______________________________________________________________________

#### Webhook processing endpoint

A new endpoint handles incoming webhooks from OpenVidu Meet:

```javascript
// Webhook endpoint to receive events from OpenVidu Meet
app.post('/webhook', (req, res) => {
    const body = req.body;
    const headers = req.headers;

    if (!isWebhookEventValid(body, headers)) {
        // (1)!
        console.error('Invalid webhook signature');
        return res.status(401).send('Invalid webhook signature');
    }

    console.log('Webhook received:', body);

    // Broadcast the webhook event to all connected SSE clients
    sse.send(body); // (2)!

    res.status(200).send();
});
```

1. Validate the webhook signature and timestamp to ensure authenticity and prevent replay attacks.
1. Broadcast the validated webhook event to all connected SSE clients for real-time updates.

This endpoint receives webhook events from OpenVidu Meet, validates their authenticity, and broadcasts them to all connected clients through Server-Sent Events.

______________________________________________________________________

#### Webhook signature validation

A security function validates webhook authenticity:

```javascript
// Helper function to validate webhook event signature
const isWebhookEventValid = (body, headers) => {
    const signature = headers['x-signature']; // (1)!
    const timestamp = parseInt(headers['x-timestamp'], 10); // (2)!

    if (!signature || !timestamp || isNaN(timestamp)) {
        return false; // (3)!
    }

    const current = Date.now();
    const diffTime = current - timestamp;
    if (diffTime >= MAX_WEBHOOK_AGE) {
        // Webhook event too old
        return false; // (4)!
    }

    const signedPayload = `${timestamp}.${JSON.stringify(body)}`; // (5)!
    const expectedSignature = crypto.createHmac('sha256', OV_MEET_API_KEY).update(signedPayload, 'utf8').digest('hex'); // (6)!

    return crypto.timingSafeEqual(Buffer.from(expectedSignature, 'hex'), Buffer.from(signature, 'hex')); // (7)!
};
```

1. Extract the webhook signature from the `x-signature` header.
1. Extract and parse the timestamp from the `x-timestamp` header.
1. Return false if required headers are missing or invalid.
1. Reject webhooks older than the maximum allowed age to prevent replay attacks.
1. Create the signed payload by combining timestamp and JSON body.
1. Generate the expected signature using HMAC-SHA256 with the API key.
1. Use timing-safe comparison to validate the signature against the expected value.

This function implements webhook security by validating both the cryptographic signature and the timestamp to ensure webhooks are authentic and recent.

______________________________________________________________________

### Frontend modifications

The frontend has been enhanced with real-time update capabilities and improved visual feedback for room status.

#### Real-time notifications setup

The application now establishes an SSE connection on page load:

```javascript
document.addEventListener('DOMContentLoaded', async () => {
    await fetchRooms();
    // Start listening for webhook notifications
    startWebhookNotifications(); // (1)!
});
```

1. Call `startWebhookNotifications()` to establish SSE connection for real-time updates.

______________________________________________________________________

#### Server-Sent Events connection

A new function establishes and manages the SSE connection:

```javascript
// Function to start listening for webhook events via Server-Sent Events
function startWebhookNotifications() {
    const eventSource = new EventSource('/events'); // (1)!

    eventSource.onopen = (_event) => {
        console.log('Connected to webhook notifications'); // (2)!
    };

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data); // (3)!
            handleWebhookNotification(data); // (4)!
        } catch (error) {
            console.error('Error parsing SSE message:', error);
        }
    };

    eventSource.onerror = (event) => {
        console.error('SSE connection error:', event); // (5)!
        // The browser will automatically try to reconnect
    };
}
```

1. Create an `EventSource` connection to the `/events` SSE endpoint.
1. Log successful connection establishment.
1. Parse incoming SSE messages as JSON webhook data.
1. Process webhook notifications through the `handleWebhookNotification()` function.
1. Handle connection errors with automatic browser reconnection.

This function creates a persistent connection to receive real-time webhook notifications from the server by creating an `EventSource` instance to the `/events` endpoint. When a message is received, it parses the JSON data and calls `handleWebhookNotification()` to process the event. The function also handles connection errors, allowing the browser to automatically attempt reconnection.

______________________________________________________________________

#### Webhook notification processing

A new function processes incoming webhook notifications and updates the UI accordingly:

```javascript
// Function to handle webhook notifications and update UI
function handleWebhookNotification(webhookData) {
    const { event, data } = webhookData; // (1)!
    console.log(`Webhook '${event}' received for room '${data.roomName}':`, webhookData);

    switch (event) {
        case 'meetingStarted':
            // Update rooms map with updated room info and re-render if on home screen
            if (isOnHomeScreen()) {
                // (2)!
                rooms.set(data.roomId, data);
                renderRooms(); // (3)!
            }
            break;
        case 'meetingEnded':
            // Update rooms map with updated room info and re-render if on home screen
            if (isOnHomeScreen()) {
                rooms.set(data.roomId, data);
                renderRooms();
            }
            break;
        case 'recordingEnded':
            // Add recording to list and re-render if on recordings screen
            if (isOnRecordingsScreen(data.roomName)) {
                // (4)!
                recordings.set(data.recordingId, data);
                renderRecordings(); // (5)!
            }
            break;
    }
}
```

1. Extract the event type and data from the webhook payload.
1. Check if the user is currently on the home screen before updating room status.
1. Update the rooms map and re-render the room list with new status information.
1. Check if the user is viewing recordings for the relevant room before adding new recordings.
1. Update the recordings map and re-render the recordings list with new recording data.

This function processes different webhook event types and updates the appropriate UI elements only when the user is viewing the relevant screen:

- For `meetingStarted` and `meetingEnded` events, it updates the room status and re-renders the room list if the user is on the home screen.
- For `recordingEnded` events, it adds the new recording to the list and re-renders the recordings list if the user is viewing recordings for the relevant room.

In order to determine the current screen context, new utility functions have been introduced:

```javascript
// Helper functions to detect current screen
function isOnHomeScreen() {
    const homeScreen = document.querySelector('#home');
    return homeScreen && !homeScreen.hidden; // (1)!
}

function isOnRecordingsScreen(roomName) {
    const recordingsScreen = document.querySelector('#recordings');
    if (!recordingsScreen || recordingsScreen.hidden) {
        return false; // (2)!
    }

    // Check if the room filter matches room name
    const roomSearchInput = document.querySelector('#recordings-room-search');
    const roomFilter = roomSearchInput ? roomSearchInput.value.trim() : '';
    return !roomFilter || roomName.startsWith(roomFilter); // (3)!
}
```

1. Check if the home screen is currently visible to determine if room updates should be applied.
1. Return false if the recordings screen is not visible.
1. Check if the room name matches the current filter to determine if recording updates are relevant.

These helper functions ensure that UI updates are only applied when users are viewing the relevant sections, optimizing performance and preventing unnecessary re-renders:

- `isOnHomeScreen()`: Checks if the home screen is currently visible.
- `isOnRecordingsScreen(roomName)`: Checks if the recordings screen is visible and if the room name matches the current filter.

______________________________________________________________________

#### Enhanced room status display

The room template has been updated to include visual status indicators:

```javascript
function getRoomListItemTemplate(room) {
    const roomStatus = room.status === 'active_meeting' ? 'ACTIVE' : room.status === 'open' ? 'OPEN' : 'CLOSED'; // (1)!
    const roomStatusBadgeClass =
        room.status === 'active_meeting' ? 'bg-primary' : room.status === 'open' ? 'bg-success' : 'bg-warning'; // (2)!

    return `
        <li class="list-group-item">
            <div class="room-info">
                <span>${room.roomName}</span>
                <span class="badge ${roomStatusBadgeClass}">${roomStatus}</span>
            </div>
            <div class="room-actions">
                <!-- buttons remain the same -->
            </div>
        </li>
    `;
}
```

1. Map room status values to user-friendly display text.
1. Assign appropriate CSS classes for visual styling based on room status.

The room template now includes status badges that provide immediate visual feedback about room state:

- **ACTIVE** (blue badge): Meeting is currently in progress
- **OPEN** (green badge): Room is available for joining
- **CLOSED** (yellow badge): Room is closed and cannot be joined

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

1. **Restart the application** to apply the changes:

   ```bash
   npm start
   ```

1. **Make the tutorial accessible to OpenVidu Meet deployment**: As OpenVidu Meet needs to send webhooks to this tutorial, it must be accessible from the internet. To achieve this, you have the following options:

   - **Using tunneling tools**: Configure tools like [VS Code port forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding) , [ngrok](https://ngrok.com/) , [localtunnel](https://localtunnel.github.io/www/) , or similar services to expose this tutorial to the internet with a secure (HTTPS) public URL.
   - **Deploying to a public server**: Upload this tutorial to a web server and configure it to be accessible with a secure (HTTPS) public URL. This can be done by updating the source code to manage SSL certificates or configuring a reverse proxy (e.g., Nginx, Apache) to serve it.

   A the end, you should have a public URL (e.g., `https://your-tutorial-domain.com:XXXX`) that points to this tutorial.

1. **Configure webhooks in OpenVidu Meet**: Set up webhooks in your OpenVidu Meet production deployment to point to this tutorial. Follow the instructions in the [Webhooks configuration](../../reference/webhooks/#configuration) section to learn how to configure a webhook URL. Use the public URL of this tutorial followed by `/webhook` (e.g., `https://your-tutorial-domain.com:XXXX/webhook`).

1. **Access the tutorial**: Access the tutorial in your web browser using its public URL (e.g., `https://your-tutorial-domain.com:XXXX`).
