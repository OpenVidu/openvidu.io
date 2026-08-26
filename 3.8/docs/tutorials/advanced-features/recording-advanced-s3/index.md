# Advanced Recording Tutorial S3

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/advanced-features/openvidu-recording-advanced-node)

This tutorial improves the [basic recording tutorial](https://openvidu.io/3.8/docs/tutorials/advanced-features/recording-basic-s3/index.md) by doing the following:

- **Complete recording metadata**: Listen to webhook events and save all necessary metadata in a separate file.
- **Real time recording status notification**: Implement a custom notification system to inform participants about the recording status by listening to webhook events and updating room metadata.
- **Recording deletion notification**: Implement a custom notification system that alerts all participants of a recording's deletion by sending data messages.
- **Direct access to recording files**: Add an additional method to allow access to recording files directly from the S3 bucket by creating a presigned URL.

Recordings are always persisted in some kind of storage system. This type of storage depends on your OpenVidu deployment:

- When running OpenVidu **locally** or **On-Premises**, recordings are stored in a **local S3 Minio bucket**.
- When running OpenVidu in **AWS**, recordings are stored in an **AWS S3 bucket**.
- When running OpenVidu in **Azure**, recordings are stored in an **Azure Blob Storage container**. If this is your case, follow the [Recording Advanced Azure tutorial](https://openvidu.io/3.8/docs/tutorials/advanced-features/recording-advanced-azure/index.md) instead.

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

1. Deploy OpenVidu Single Node in AWS following these instructions [to deploy in AWS](https://openvidu.io/3.8/docs/self-hosting/single-node/aws/install/index.md).

   CPUs to be able to record

   Make sure you deploy with at least 4 CPUs in the Virtual Machine of AWS.

1. Point the tutorial to your AWS deployment:

   - Modify file [`.env`](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/advanced-features/openvidu-recording-advanced-node/.env) to update the LiveKit and AWS configuration to the values of your AWS deployment. You can get the values of `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` from the [Configure your application to use the deployment](https://openvidu.io/3.8/docs/self-hosting/single-node/aws/install/#configure-your-application-to-use-the-deployment) section. You can get the values of `S3_ENDPOINT`, `AWS_REGION` and `S3_BUCKET` from the `openvidu.env` file of your deployment by making ssh to the instance. For the `S3_ACCESS_KEY` and `S3_SECRET_KEY` you will need to create an access key in the IAM section of AWS to be able to use them in the tutorial (check [Manage access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) ).
   - Modify file [`app.js`](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/advanced-features/openvidu-recording-advanced-node/public/app.js#L3) to update the value of `LIVEKIT_URL` with your `LIVEKIT_URL`.

Warning

If you are using self-signed certificate you will need to add this line in the first line after the imports on the [`index.js`](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/advanced-features/openvidu-recording-advanced-node/src/index.js) `process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"; // Disable TLS verification for local testing`

Configure Webhooks

All [application servers](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) have an endpoint to receive webhooks from OpenVidu. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/enable-webhooks/#send-webhooks-to-a-local-application-server) section for more information.

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.8.0
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-livekit-tutorials/advanced-features/openvidu-recording-advanced-node
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

Video call room of the recording tutorial app with recording controls

List of recordings of the room in the recording tutorial app

Accessing your application from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:6443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

**Limitation**: Playing recordings with the `S3` strategy from other devices in your local network is not possible due to MinIO not being exposed. To play recordings from other devices, you need to change the environment variable `RECORDING_PLAYBACK_STRATEGY` to `PROXY`.

## Enhancements

### Refactoring backend

The backend has been refactored to prevent code duplication and improve readability. The main changes are:

- Endpoints have been moved to the `controllers` folder, creating a controller for each set of related endpoints:

  - `RoomController` for the room creation endpoint.
  - `RecordingController` for the recording endpoints.
  - `WebhookController` for the webhook endpoint.

- The `index.js` file now simply sets the route for each controller:

  ```javascript
  app.use("/token", roomController);
  app.use("/recordings", recordingController);
  app.use("/livekit/webhook", webhookController);
  ```

- The configuration of environment variables and constants has been moved to the `config.js` file:

  ```javascript
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

- Operations of the `EgressClient` and functions related to recording management have been moved to the `RecordingService` class within the `services` folder.

After refactoring and implementing the improvements, the backend of the application has the following structure:

```text
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

______________________________________________________________________

### Adding room metadata

In order to store the recording status in the room metadata, we have to create the room explicitly the first time a user joins it, setting the metadata field with an object that contains the recording status. This object also contains the app name, which is used to identify webhook events related to the application. This is done in the `POST /token` endpoint:

```javascript
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
1. Create the room if it doesn't exist.

After generating the access token with the required permissions, this endpoint does the following:

1. Checks if the room exists by calling the `exists` method of the `RoomService` with the `roomName` as a parameter. This method returns a boolean indicating whether the room obtained from the `getRoom` method is not `null`. This other method lists all active rooms that match the `roomName` by calling the `listRooms` method of the `RoomServiceClient` with an array containing the `roomName` as a parameter, and returns the first element of the list if it exists:

   ```javascript
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
   1. Return the first element of the list if it exists.

1. Creates the room if it doesn't exist by calling the `createRoom` method of the `RoomService` with the `roomName` as a parameter. This method creates a room with the `roomName` and sets the metadata field with an object that contains the app name (defined in the `config.js` file) and the recording status initialized to `STOPPED`. To achieve this, the method calls the `createRoom` method of the `RoomServiceClient` with an object indicating the room name and metadata:

   ```javascript
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
   1. Set the recording status to `STOPPED`.
   1. Create the room with the `roomOptions` object by calling the `createRoom` method of the `RoomServiceClient`.

______________________________________________________________________

### Handling webhook events

In previous tutorials, we listened to all webhook events and printed them in the console without doing anything else. In this tutorial, we have to first check if the webhook is related to the application and then act accordingly depending on the event type. This is done in the `POST /livekit/webhook` endpoint:

```javascript
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
1. Destructure the event type and egress info from the webhook event.
1. If the event type is `egress_started` or `egress_updated`, notify the recording status update.
1. If the event type is `egress_ended`, handle the egress ended.

After receiving the webhook event, this endpoint does the following:

1. Checks if the webhook is related to the application by calling the `checkWebhookRelatedToMe` function with the webhook event as a parameter. This function returns a boolean indicating whether the app name obtained from the metadata field of the room related to the webhook event is equal to the app name defined in the `config.js` file:

   ```javascript
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
   1. Check if the room and metadata fields exist.
   1. If the room or metadata fields don't exist, get the room name from the room, egress info, or ingress info.
   1. Get the room info by calling the `getRoom` method of the `RoomService` with the `roomName` as a parameter.
   1. Parse the metadata field of the room info.
   1. Return whether the app name is equal to the app name defined in the `config.js` file.

1. Destructures the event type and egress info from the webhook event.

1. If the event type is `egress_started` or `egress_updated`, calls the `notifyRecordingStatusUpdate` function with the egress info as a parameter. This function notifies all participants in the room related to the egress info about the recording status update. See the [Notifying recording status update](#notifying-recording-status-update) section for more information.

1. If the event type is `egress_ended`, calls the `handleEgressEnded` function with the egress info as a parameter. This function saves the recording metadata in a separate file (see the [Saving recording metadata](#saving-recording-metadata) section) and notifies all participants in the room related to the egress info that the recording has been stopped:

   ```javascript
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
   1. Notify all participants in the room that the recording has been stopped.

______________________________________________________________________

### Notifying recording status update

When the recording status changes, all participants in the room have to be notified. This is done by updating the metadata field of the room with the new recording status, which will trigger the `RoomEvent.RoomMetadataChanged` event in the client side. This is implemented in the `notifyRecordingStatusUpdate` function:

```javascript
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
1. Get the recording status from the egress info status.
1. Update the room metadata with the new recording status.

After getting the room name from the egress info, this function does the following:

1. Gets the recording status by calling the `getRecordingStatus` method of the `RecordingService` with the egress info status as a parameter. This method returns the recording status based on the egress info status:

   ```javascript
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

1. Updates the room metadata with the new recording status by calling the `updateRoomMetadata` method of the `RoomService` with the `roomName` and `recordingStatus` as parameters. This method updates the metadata field of the room with an object that contains the app name and the new recording status by calling the `updateRoomMetadata` method of the `RoomServiceClient` with the `roomName` and a stringified object as parameters:

   ```javascript
   async updateRoomMetadata(roomName, recordingStatus) {
       const metadata = {
           createdBy: APP_NAME,
           recordingStatus // (1)!
       };
       return this.roomClient.updateRoomMetadata(roomName, JSON.stringify(metadata)); // (2)!
   }
   ```

   1. Update the recording status.
   1. Update the room metadata with the new metadata by calling the `updateRoomMetadata` method of the `RoomServiceClient` with the `roomName` and a stringified object as parameters.

______________________________________________________________________

### Saving recording metadata

When the recording ends, the metadata related to the recording has to be saved in a separate file. This is done in the `saveRecordingMetadata` function:

```javascript
async saveRecordingMetadata(egressInfo) {
    const recordingInfo = this.convertToRecordingInfo(egressInfo); // (1)!
    const key = this.getMetadataKey(recordingInfo.name); // (2)!
    await s3Service.uploadObject(key, recordingInfo); // (3)!
}
```

1. Convert the egress info to a recording info object.
1. Get the metadata key from the recording info name.
1. Upload the recording metadata to the S3 bucket.

This method does the following:

1. Converts the egress info to a recording info object by calling the `convertToRecordingInfo` method:

   ```javascript
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

   Getting recording metadata

   In this tutorial, we can access detailed information about the recording directly from the metadata file stored in the S3 bucket, without needing to make additional requests. This is made possible by saving all the necessary data retrieved from the egress info object. Compared to the [basic recording tutorial](https://openvidu.io/3.8/docs/tutorials/advanced-features/recording-basic-s3/index.md), we are now storing additional details such as the **recording name**, **duration** and **size**.

1. Gets the metadata key from the recordings path and the recordings metadata path, both defined in the `config.js` file, and the recording name replacing the `.mp4` extension with `.json`:

   ```javascript
   getMetadataKey(recordingName) {
       return RECORDINGS_PATH + RECORDINGS_METADATA_PATH + recordingName.replace(".mp4", ".json");
   }
   ```

1. Uploads the recording metadata to the S3 bucket by calling the `uploadObject` method of the `S3Service` with the `key` and `recordingInfo` as parameters. This method uploads an object to the S3 bucket by sending a `PutObjectCommand` with the key and the stringified object as parameters:

   ```javascript
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

______________________________________________________________________

### Notifying recording deletion

When a recording is deleted, all participants in the room have to be notified. This is done by sending a data message to all participants in the room. To achieve this, the `DELETE /recordings/:recordingName` endpoint has been modified as follows:

```javascript
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
1. Check if the room exists.
1. Send a data message to the room indicating that the recording was deleted.

Before deleting the recording, we get the room name from the recording metadata. After deleting the recording, we check if the room exists and, if it does, send a data message to the room indicating that the recording was deleted. This is done by calling the `sendDataToRoom` method of the `RoomService` with the `roomName` and an object containing the `recordingName` as parameters:

```javascript
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
1. Sets the topic to `RECORDING_DELETED`.
1. Sets the destination SIDs to an empty array (all participants in the room).
1. Sends the data message to the room by calling the `sendData` method of the `RoomServiceClient` with the `roomName`, `data`, `DataPacket_Kind.RELIABLE` and `options` as parameters.

This method does the following:

1. Encodes the raw data by calling the `encode` method of the `TextEncoder` with the stringified raw data as a parameter.
1. Sets the topic of the data message to `RECORDING_DELETED`.
1. Sets the destination SIDs to an empty array, which means that the message will be sent to all participants in the room.
1. Sends the data message to the room by calling the `sendData` method of the `RoomServiceClient` with the `roomName`, `data`, `DataPacket_Kind.RELIABLE` and `options` as parameters. The `DataPacket_Kind.RELIABLE` parameter indicates that the message will be sent reliably.

______________________________________________________________________

### Accessing recording files directly from the S3 bucket

In this tutorial, we have added an additional method to allow access to recording files directly from the S3 bucket by creating a presigned URL. To accomplish this, we have created a new endpoint (`GET /recordings/:recordingName/url`) to get the recording URL depending on the playback strategy defined in the environment variable `RECORDING_PLAYBACK_STRATEGY`, whose value can be `PROXY` or `S3`:

```javascript
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
1. Return the `GET /recordings/:recordingName` endpoint URL if the playback strategy is `PROXY`.
1. Create a presigned URL to access the recording directly from the S3 bucket if the playback strategy is `S3`.

This endpoint does the following:

1. Extracts the `recordingName` parameter from the request.

1. Checks if the recording exists. If it does not exist, it returns a `404` error.

1. If the playback strategy is `PROXY`, it returns the `GET /recordings/:recordingName` endpoint URL to get the recording file from the backend.

1. If the playback strategy is `S3`, it creates a presigned URL to access the recording directly from the S3 bucket by calling the `getRecordingUrl` method of the `RecordingService` with the `recordingName` as a parameter. This method simply calls the `getObjectUrl` method of the `S3Service` with the key of the recording as a parameter:

   ```javascript
   async getObjectUrl(key) {
       const params = {
           Bucket: S3_BUCKET,
           Key: key
       };
       const command = new GetObjectCommand(params);
       return getSignedUrl(this.s3Client, command, { expiresIn: 86400 }); // 24 hours
   }
   ```

   This method creates a presigned URL to access the object in the S3 bucket by calling the `getSignedUrl` function from the [@aws-sdk/s3-request-presigner](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/Package/-aws-sdk-s3-request-presigner/) package, indicating the `S3Client`, `GetObjectCommand` and the expiration time in seconds as parameters. In this case, the expiration time is set to 24 hours.

   Presigned URLs

   Presigned URLs are URLs that provide access to an S3 object for a limited time. This is useful when you want to share an object with someone for a limited time without providing them with your AWS credentials.

   Compared to the proxy strategy, accessing recording files directly from the S3 bucket via presigned URLs is more efficient, as it reduces server load. However, it presents a security risk, as the URL, once generated, can be used by anyone until it expires.

______________________________________________________________________

### Handling new room events in the client side

In the client side, we have to handle the new room events related to the recording status and the recording deletion. This is done by listening to the `RoomEvent.RoomMetadataChanged` and `RoomEvent.DataReceived` events in the `joinRoom` method:

```javascript
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

```javascript
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
