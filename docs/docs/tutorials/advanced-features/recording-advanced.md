# openvidu-recording-advanced-node

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/advanced-features/openvidu-recording-advanced-node){ .md-button target=\_blank }

This tutorial improves the [basic recording tutorial](./recording-basic.md){target="\_blank"} by doing the following:

-   **Complete recording metadata**: Listen to webhook events and save all necessary metadata in a separate file.
-   **Real time recording status notification**: Implement a custom notification system to inform participants about the recording status by listening to webhook events and updating room metadata.
-   **Recording deletion notification**: Implement a custom notification system that alerts all participants of a recording's deletion by sending data messages.
-   **Direct access to recording files**: Add an additional method to allow access to recording files directly from the S3 bucket by creating a presigned URL.

## Running this tutorial

#### 1. Run OpenVidu Server

--8<-- "docs/docs/tutorials/shared/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.0.0
```

### 3. Run the application

To run this application, you need [Node](https://nodejs.org/es/download/){:target="\_blank"} installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-livekit-tutorials/advanced-features/openvidu-recording-advanced-node
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

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/advanced-features/recording1.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/advanced-features/recording1.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/advanced-features/recording2.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/advanced-features/recording2.png" loading="lazy"/></a></p></div>

</div>

!!! info "Accessing your application from other devices in your local network"

    One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application with other devices in your local network very easily without worrying about SSL certificates.

    Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:6443`](https://xxx-yyy-zzz-www.openvidu-local.dev:6443){target="_blank"}, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](../../self-hosting/local.md#accessing-your-local-deployment-from-other-devices-on-your-network){target="_blank"}.

    **Limitation**: Playing recordings with the `S3` strategy from other devices in your local network is not possible due to MinIO not being exposed. To play recordings from other devices, you need to change the environment variable `RECORDING_PLAYBACK_STRATEGY` to `PROXY`.

## Enhancements

### Refactoring backend

The backend has been refactored to prevent code duplication and improve readability. The main changes are:

-   Endpoints have been moved to the `controllers` folder, creating a controller for each set of related endpoints:

    -   `RoomController` for the room creation endpoint.
    -   `RecordingController` for the recording endpoints.
    -   `WebhookController` for the webhook endpoint.

-   The `index.js` file now simply sets the route for each controller:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/index.js#L21-L23' target='_blank'>index.js</a>" linenums="21"
    app.use("/token", roomController);
    app.use("/recordings", recordingController);
    app.use("/livekit/webhook", webhookController);
    ```

-   The configuration of environment variables and constants has been moved to the `config.js` file:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/config.js' target='_blank'>config.js</a>" linenums="1"
    export const SERVER_PORT = process.env.SERVER_PORT || 6080;
    export const APP_NAME = "openvidu-recording-advanced-node";

    // LiveKit configuration
    export const LIVEKIT_URL = process.env.LIVEKIT_URL || "http://localhost:7880";
    export const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || "devkey";
    export const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || "secret";

    // S3 configuration
    export const S3_ENDPOINT = process.env.S3_ENDPOINT || "http://localhost:9000";
    export const S3_ACCESS_KEY = process.env.S3_ACCESS_KEY || "minioadmin";
    export const S3_SECRET_KEY = process.env.S3_SECRET_KEY || "minioadmin";
    export const AWS_REGION = process.env.AWS_REGION || "us-east-1";
    export const S3_BUCKET = process.env.S3_BUCKET || "openvidu";

    export const RECORDINGS_PATH = process.env.RECORDINGS_PATH ?? "recordings/";
    export const RECORDINGS_METADATA_PATH = ".metadata/";
    export const RECORDING_PLAYBACK_STRATEGY = process.env.RECORDING_PLAYBACK_STRATEGY || "S3"; // PROXY or S3
    export const RECORDING_FILE_PORTION_SIZE = 5 * 1024 * 1024; // 5MB
    ```

-   Operations of the `EgressClient` and functions related to recording management have been moved to the `RecordingService` class within the `services` folder.

After refactoring and implementing the improvements, the backend of the application has the following structure:

```plaintext
src
├── controllers
│   ├── recording.controller.js
│   ├── room.controller.js
│   └── webhook.controller.js
├── services
│   ├── recording.service.js
│   ├── room.service.js
│   └── s3.service.js
├── config.js
├── index.js
```

Where `room.service.js` defines the `RoomService` class, that contains the logic to manage rooms using the `RoomServiceClient`.

---

### Adding room metadata

In order to store the recording status in the room metadata, we have to create the room explicitly the first time a user joins it, setting the metadata field with an object that contains the recording status. This object also contains the app name, which is used to identify webhook events related to the application. This is done in the `POST /token` endpoint:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/room.controller.js#L10-L38' target='_blank'>room.controller.js</a>" linenums="10" hl_lines="16-28"
roomController.post("/", async (req, res) => {
    const roomName = req.body.roomName;
    const participantName = req.body.participantName;

    if (!roomName || !participantName) {
        res.status(400).json({ errorMessage: "roomName and participantName are required" });
        return;
    }

    const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
        identity: participantName
    });
    at.addGrant({ room: roomName, roomJoin: true, roomRecord: true });
    const token = await at.toJwt();

    try {
        // Create room if it doesn't exist
        const exists = await roomService.exists(roomName); // (1)!

        if (!exists) {
            await roomService.createRoom(roomName); // (2)!
        }

        res.json({ token });
    } catch (error) {
        console.error("Error creating room.", error);
        res.status(500).json({ errorMessage: "Error creating room" });
    }
});
```

1. Check if the room exists.
2. Create the room if it doesn't exist.

After generating the access token with the required permissions, this endpoint does the following:

1. Checks if the room exists by calling the `exists` method of the `RoomService` with the `roomName` as a parameter. This method returns a boolean indicating whether the room obtained from the `getRoom` method is not `null`. This other method lists all active rooms that match the `roomName` by calling the `listRooms` method of the `RoomServiceClient` with an array containing the `roomName` as a parameter, and returns the first element of the list if it exists:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/room.service.js#L30-L38' target='_blank'>room.service.js</a>" linenums="30"
    async getRoom(roomName) {
        const rooms = await this.roomClient.listRooms([roomName]); // (1)!
        return rooms.length > 0 ? rooms[0] : null; // (2)!
    }

    async exists(roomName) {
        const room = await this.getRoom(roomName);
        return room !== null;
    }
    ```

    1. List all active rooms that match the `roomName` by calling the `listRooms` method of the `RoomServiceClient` with an array containing the `roomName` as a parameter.
    2. Return the first element of the list if it exists.

2. Creates the room if it doesn't exist by calling the `createRoom` method of the `RoomService` with the `roomName` as a parameter. This method creates a room with the `roomName` and sets the metadata field with an object that contains the app name (defined in the `config.js` file) and the recording status initialized to `STOPPED`. To achieve this, the method calls the `createRoom` method of the `RoomServiceClient` with an object indicating the room name and metadata:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/room.service.js#L19-L28' target='_blank'>room.service.js</a>" linenums="19"
    async createRoom(roomName) {
        const roomOptions = {
            name: roomName,
            metadata: JSON.stringify({
                createdBy: APP_NAME, // (1)!
                recordingStatus: "STOPPED" // (2)!
            })
        };
        return this.roomClient.createRoom(roomOptions); // (3)!
    }
    ```

    1. Set the app name.
    2. Set the recording status to `STOPPED`.
    3. Create the room with the `roomOptions` object by calling the `createRoom` method of the `RoomServiceClient`.

---

### Handling webhook events

In previous tutorials, we listened to all webhook events and printed them in the console without doing anything else. In this tutorial, we have to first check if the webhook is related to the application and then act accordingly depending on the event type. This is done in the `POST /livekit/webhook` endpoint:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/webhook.controller.js#L14-L38' target='_blank'>webhook.controller.js</a>" linenums="14"
webhookController.post("/", async (req, res) => {
    try {
        const webhookEvent = await webhookReceiver.receive(req.body, req.get("Authorization"));
        const isWebhookRelatedToMe = await checkWebhookRelatedToMe(webhookEvent); // (1)!

        if (isWebhookRelatedToMe) {
            console.log(webhookEvent);
            const { event: eventType, egressInfo } = webhookEvent; // (2)!

            switch (eventType) {
                case "egress_started": // (3)!
                case "egress_updated":
                    await notifyRecordingStatusUpdate(egressInfo);
                    break;
                case "egress_ended": // (4)!
                    await handleEgressEnded(egressInfo);
                    break;
            }
        }
    } catch (error) {
        console.error("Error validating webhook event.", error);
    }

    res.status(200).send();
});
```

1. Check if the webhook is related to the application.
2. Destructure the event type and egress info from the webhook event.
3. If the event type is `egress_started` or `egress_updated`, notify the recording status update.
4. If the event type is `egress_ended`, handle the egress ended.

After receiving the webhook event, this endpoint does the following:

1. Checks if the webhook is related to the application by calling the `checkWebhookRelatedToMe` function with the webhook event as a parameter. This function returns a boolean indicating whether the app name obtained from the metadata field of the room related to the webhook event is equal to the app name defined in the `config.js` file:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/webhook.controller.js#L40-L55' target='_blank'>webhook.controller.js</a>" linenums="40"
    const checkWebhookRelatedToMe = async (webhookEvent) => {
        const { room, egressInfo, ingressInfo } = webhookEvent; // (1)!
        let roomInfo = room;
        // (2)!
        if (!room || !room.metadata) {
            const roomName = room?.name ?? egressInfo?.roomName ?? ingressInfo?.roomName; // (3)!
            roomInfo = await roomService.getRoom(roomName); // (4)!

            if (!roomInfo) {
                return false;
            }
        }

        const metadata = roomInfo.metadata ? JSON.parse(roomInfo.metadata) : null; // (5)!
        return metadata?.createdBy === APP_NAME; // (6)!
    };
    ```

    1. Destructure the room, egress info, and ingress info from the webhook event.
    2. Check if the room and metadata fields exist.
    3. If the room or metadata fields don't exist, get the room name from the room, egress info, or ingress info.
    4. Get the room info by calling the `getRoom` method of the `RoomService` with the `roomName` as a parameter.
    5. Parse the metadata field of the room info.
    6. Return whether the app name is equal to the app name defined in the `config.js` file.

2. Destructures the event type and egress info from the webhook event.

3. If the event type is `egress_started` or `egress_updated`, calls the `notifyRecordingStatusUpdate` function with the egress info as a parameter. This function notifies all participants in the room related to the egress info about the recording status update. See the [Notifying recording status update](#notifying-recording-status-update) section for more information.

4. If the event type is `egress_ended`, calls the `handleEgressEnded` function with the egress info as a parameter. This function saves the recording metadata in a separate file (see the [Saving recording metadata](#saving-recording-metadata) section) and notifies all participants in the room related to the egress info that the recording has been stopped:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/webhook.controller.js#L57-L65' target='_blank'>webhook.controller.js</a>" linenums="57"
    const handleEgressEnded = async (egressInfo) => {
        try {
            await recordingService.saveRecordingMetadata(egressInfo); // (1)!
        } catch (error) {
            console.error("Error saving recording metadata.", error);
        }

        await notifyRecordingStatusUpdate(egressInfo); // (2)!
    };
    ```

    1. Save the recording metadata.
    2. Notify all participants in the room that the recording has been stopped.

---

### Notifying recording status update

When the recording status changes, all participants in the room have to be notified. This is done by updating the metadata field of the room with the new recording status, which will trigger the `RoomEvent.RoomMetadataChanged` event in the client side. This is implemented in the `notifyRecordingStatusUpdate` function:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/webhook.controller.js#L67-L76' target='_blank'>webhook.controller.js</a>" linenums="67"
const notifyRecordingStatusUpdate = async (egressInfo) => {
    const roomName = egressInfo.roomName; // (1)!
    const recordingStatus = recordingService.getRecordingStatus(egressInfo.status); // (2)!

    try {
        await roomService.updateRoomMetadata(roomName, recordingStatus); // (3)!
    } catch (error) {
        console.error("Error updating room metadata.", error);
    }
};
```

1. Get the room name from the egress info.
2. Get the recording status from the egress info status.
3. Update the room metadata with the new recording status.

After getting the room name from the egress info, this function does the following:

1. Gets the recording status by calling the `getRecordingStatus` method of the `RecordingService` with the egress info status as a parameter. This method returns the recording status based on the egress info status:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/recording.service.js#L135-L148' target='_blank'>recording.service.js</a>" linenums="135"
    getRecordingStatus(egressStatus) {
        switch (egressStatus) {
            case EgressStatus.EGRESS_STARTING:
                return "STARTING";
            case EgressStatus.EGRESS_ACTIVE:
                return "STARTED";
            case EgressStatus.EGRESS_ENDING:
                return "STOPPING";
            case EgressStatus.EGRESS_COMPLETE:
                return "STOPPED";
            default:
                return "FAILED";
        }
    }
    ```

    We distinguish between the following recording statuses:

    - `STARTING`: The recording is starting.
    - `STARTED`: The recording is active.
    - `STOPPING`: The recording is stopping.
    - `STOPPED`: The recording has stopped.
    - `FAILED`: The recording has failed.

2. Updates the room metadata with the new recording status by calling the `updateRoomMetadata` method of the `RoomService` with the `roomName` and `recordingStatus` as parameters. This method updates the metadata field of the room with an object that contains the app name and the new recording status by calling the `updateRoomMetadata` method of the `RoomServiceClient` with the `roomName` and a stringified object as parameters:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/room.service.js#L40-L46' target='_blank'>room.service.js</a>" linenums="40"
    async updateRoomMetadata(roomName, recordingStatus) {
        const metadata = {
            createdBy: APP_NAME,
            recordingStatus // (1)!
        };
        return this.roomClient.updateRoomMetadata(roomName, JSON.stringify(metadata)); // (2)!
    }
    ```

    1. Update the recording status.
    2. Update the room metadata with the new metadata by calling the `updateRoomMetadata` method of the `RoomServiceClient` with the `roomName` and a stringified object as parameters.

---

### Saving recording metadata

When the recording ends, the metadata related to the recording has to be saved in a separate file. This is done in the `saveRecordingMetadata` function:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/recording.service.js#L116-L120' target='_blank'>recording.service.js</a>" linenums="116"
async saveRecordingMetadata(egressInfo) {
    const recordingInfo = this.convertToRecordingInfo(egressInfo); // (1)!
    const key = this.getMetadataKey(recordingInfo.name); // (2)!
    await s3Service.uploadObject(key, recordingInfo); // (3)!
}
```

1. Convert the egress info to a recording info object.
2. Get the metadata key from the recording info name.
3. Upload the recording metadata to the S3 bucket.

This method does the following:

1.  Converts the egress info to a recording info object by calling the `convertToRecordingInfo` method:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/recording.service.js#L122-L133' target='_blank'>recording.service.js</a>" linenums="122"
    convertToRecordingInfo(egressInfo) {
        const file = egressInfo.fileResults[0];
        return {
            id: egressInfo.egressId,
            name: file.filename.split("/").pop(),
            roomName: egressInfo.roomName,
            roomId: egressInfo.roomId,
            startedAt: Number(egressInfo.startedAt) / 1_000_000,
            duration: Number(file.duration) / 1_000_000_000,
            size: Number(file.size)
        };
    }
    ```

    !!! info "Getting recording metadata"

        In this tutorial, we can access detailed information about the recording directly from the metadata file stored in the S3 bucket, without needing to make additional requests. This is made possible by saving all the necessary data retrieved from the egress info object. Compared to the [basic recording tutorial](./recording-basic.md){:target="\_blank"}, we are now storing additional details such as the **recording name**, **duration** and **size**.

2.  Gets the metadata key from the recordings path and the recordings metadata path, both defined in the `config.js` file, and the recording name replacing the `.mp4` extension with `.json`:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/recording.service.js#L154-L156' target='_blank'>recording.service.js</a>" linenums="154"
    getMetadataKey(recordingName) {
        return RECORDINGS_PATH + RECORDINGS_METADATA_PATH + recordingName.replace(".mp4", ".json");
    }
    ```

3.  Uploads the recording metadata to the S3 bucket by calling the `uploadObject` method of the `S3Service` with the `key` and `recordingInfo` as parameters. This method uploads an object to the S3 bucket by sending a `PutObjectCommand` with the key and the stringified object as parameters:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/s3.service.js#L34-L42' target='_blank'>s3.service.js</a>" linenums="34"
    async uploadObject(key, body) {
        const params = {
            Bucket: S3_BUCKET,
            Key: key,
            Body: JSON.stringify(body)
        };
        const command = new PutObjectCommand(params);
        return this.run(command);
    }
    ```

---

### Notifying recording deletion

When a recording is deleted, all participants in the room have to be notified. This is done by sending a data message to all participants in the room. To achieve this, the `DELETE /recordings/:recordingName` endpoint has been modified as follows:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/recording.controller.js#L129-L154' target='_blank'>recording.controller.js</a>" linenums="129" hl_lines="14-19"
recordingController.delete("/:recordingName", async (req, res) => {
    const { recordingName } = req.params;
    const exists = await recordingService.existsRecording(recordingName);

    if (!exists) {
        res.status(404).json({ errorMessage: "Recording not found" });
        return;
    }

    try {
        const { roomName } = await recordingService.getRecordingMetadata(recordingName); // (1)!
        await recordingService.deleteRecording(recordingName);

        // Notify to all participants that the recording was deleted
        const existsRoom = await roomService.exists(roomName); // (2)!

        if (existsRoom) {
            await roomService.sendDataToRoom(roomName, { recordingName }); // (3)!
        }

        res.json({ message: "Recording deleted" });
    } catch (error) {
        console.error("Error deleting recording.", error);
        res.status(500).json({ errorMessage: "Error deleting recording" });
    }
});
```

1. Get the room name from the recording metadata.
2. Check if the room exists.
3. Send a data message to the room indicating that the recording was deleted.

Before deleting the recording, we get the room name from the recording metadata. After deleting the recording, we check if the room exists and, if it does, send a data message to the room indicating that the recording was deleted. This is done by calling the `sendDataToRoom` method of the `RoomService` with the `roomName` and an object containing the `recordingName` as parameters:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/room.service.js#L48-L60' target='_blank'>room.service.js</a>" linenums="48"
async sendDataToRoom(roomName, rawData) {
    const data = encoder.encode(JSON.stringify(rawData)); // (1)!
    const options = {
        topic: "RECORDING_DELETED", // (2)!
        destinationSids: [] // (3)!
    };

    try {
        await this.roomClient.sendData(roomName, data, DataPacket_Kind.RELIABLE, options); // (4)!
    } catch (error) {
        console.error("Error sending data to room", error);
    }
}
```

1. Encodes the raw data.
2. Sets the topic to `RECORDING_DELETED`.
3. Sets the destination SIDs to an empty array (all participants in the room).
4. Sends the data message to the room by calling the `sendData` method of the `RoomServiceClient` with the `roomName`, `data`, `DataPacket_Kind.RELIABLE` and `options` as parameters.

This method does the following:

1. Encodes the raw data by calling the `encode` method of the `TextEncoder` with the stringified raw data as a parameter.
2. Sets the topic of the data message to `RECORDING_DELETED`.
3. Sets the destination SIDs to an empty array, which means that the message will be sent to all participants in the room.
4. Sends the data message to the room by calling the `sendData` method of the `RoomServiceClient` with the `roomName`, `data`, `DataPacket_Kind.RELIABLE` and `options` as parameters. The `DataPacket_Kind.RELIABLE` parameter indicates that the message will be sent reliably.

---

### Accessing recording files directly from the S3 bucket

In this tutorial, we have added an additional method to allow access to recording files directly from the S3 bucket by creating a presigned URL. To accomplish this, we have created a new endpoint (`GET /recordings/:recordingName/url`) to get the recording URL depending on the playback strategy defined in the environment variable `RECORDING_PLAYBACK_STRATEGY`, whose value can be `PROXY` or `S3`:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/controllers/recording.controller.js#L104-L127' target='_blank'>recording.controller.js</a>" linenums="104"
recordingController.get("/:recordingName/url", async (req, res) => {
    const { recordingName } = req.params;
    const exists = await recordingService.existsRecording(recordingName); // (1)!

    if (!exists) {
        res.status(404).json({ errorMessage: "Recording not found" });
        return;
    }

    // If the recording playback strategy is "PROXY", return the endpoint URL
    if (RECORDING_PLAYBACK_STRATEGY === "PROXY") {
        res.json({ recordingUrl: `/recordings/${recordingName}` }); // (2)!
        return;
    }

    try {
        // If the recording playback strategy is "S3", return a signed URL to access the recording directly from S3
        const recordingUrl = await recordingService.getRecordingUrl(recordingName); // (3)!
        res.json({ recordingUrl });
    } catch (error) {
        console.error("Error getting recording URL.", error);
        res.status(500).json({ errorMessage: "Error getting recording URL" });
    }
});
```

1. Check if the recording exists.
2. Return the `GET /recordings/:recordingName` endpoint URL if the playback strategy is `PROXY`.
3. Create a presigned URL to access the recording directly from the S3 bucket if the playback strategy is `S3`.

This endpoint does the following:

1.  Extracts the `recordingName` parameter from the request.
2.  Checks if the recording exists. If it does not exist, it returns a `404` error.
3.  If the playback strategy is `PROXY`, it returns the `GET /recordings/:recordingName` endpoint URL to get the recording file from the backend.
4.  If the playback strategy is `S3`, it creates a presigned URL to access the recording directly from the S3 bucket by calling the `getRecordingUrl` method of the `RecordingService` with the `recordingName` as a parameter. This method simply calls the `getObjectUrl` method of the `S3Service` with the key of the recording as a parameter:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/src/services/s3.service.js#L78-L85' target='_blank'>s3.service.js</a>" linenums="78"
    async getObjectUrl(key) {
        const params = {
            Bucket: S3_BUCKET,
            Key: key
        };
        const command = new GetObjectCommand(params);
        return getSignedUrl(this.s3Client, command, { expiresIn: 86400 }); // 24 hours
    }
    ```

    This method creates a presigned URL to access the object in the S3 bucket by calling the `getSignedUrl` function from the [@aws-sdk/s3-request-presigner](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/Package/-aws-sdk-s3-request-presigner/){target="\_blank"} package, indicating the `S3Client`, `GetObjectCommand` and the expiration time in seconds as parameters. In this case, the expiration time is set to 24 hours.

    !!! info "Presigned URLs"

        Presigned URLs are URLs that provide access to an S3 object for a limited time. This is useful when you want to share an object with someone for a limited time without providing them with your AWS credentials.

        Compared to the proxy strategy, accessing recording files directly from the S3 bucket via presigned URLs is more efficient, as it reduces server load. However, it presents a security risk, as the URL, once generated, can be used by anyone until it expires.

---

### Handling new room events in the client side

In the client side, we have to handle the new room events related to the recording status and the recording deletion. This is done by listening to the `RoomEvent.RoomMetadataChanged` and `RoomEvent.DataReceived` events in the `joinRoom` method:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/public/app.js#L44-L57' target='_blank'>app.js</a>" linenums="42"
async function joinRoom() {
    // ...
    // When recording status changes...
    room.on(LivekitClient.RoomEvent.RoomMetadataChanged, async (metadata) => {
        const { recordingStatus } = JSON.parse(metadata);
        await updateRecordingInfo(recordingStatus);
    });

    // When a message is received...
    room.on(LivekitClient.RoomEvent.DataReceived, async (payload, _participant, _kind, topic) => {
        // If the message is a recording deletion notification, remove the recording from the list
        if (topic === "RECORDING_DELETED") {
            const { recordingName } = JSON.parse(new TextDecoder().decode(payload));
            deleteRecordingContainer(recordingName);
        }
    });
    // ...
}
```

When a new `RoomEvent.RoomMetadataChanged` event is received, we parse the metadata to get the recording status and update the recording info accordingly. The `updateRecordingInfo` function has been updated to handle the new recording statuses.

In addition to handling this event, we need to update the recording info in the UI the first time a user joins the room. Once the user has joined, we retrieve the current room metadata and update the UI accordingly. Recordings will be listed unless the recording status is `STOPPED` or `FAILED`, to prevent listing recordings twice:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/advanced-features/openvidu-recording-advanced-node/public/app.js#L80-L87' target='_blank'>app.js</a>" linenums="78"
async function joinRoom() {
    // ...
    // Update recording info
    const { recordingStatus } = JSON.parse(room.metadata);
    await updateRecordingInfo(recordingStatus);

    if (recordingStatus !== "STOPPED" && recordingStatus !== "FAILED") {
        const roomId = await room.getSid();
        await listRecordings(room.name, roomId);
    }
    // ...
}
```

When a new `RoomEvent.DataReceived` event is received, we check if the topic of the message is `RECORDING_DELETED`. If it is, we decode the payload using a `TextDecoder` and parse the message to get the recording name. Then, we remove the recording from the list by calling the `deleteRecordingContainer` function.
