---
title: Basic Recording Tutorial Azure
description: Learn how to record a room and manage recordings by extending a simple video-call application built upon Node.js server and JavaScript client.
---

# Basic Recording Tutorial Azure

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.3.0/advanced-features/openvidu-recording-basic-node-azure){ .md-button target=\_blank }

This tutorial is a simple video-call application, built upon [Node.js server](../application-server/node.md){:target="\_blank"} and [JavaScript client](../application-client/javascript.md){:target="\_blank"} tutorials, and extends them by adding recording capabilities:

- Start and stop recording a room.
- List all recordings in a room.
- Play a recording.
- Delete a recording.
- List all available recordings.

## Running this tutorial

#### 1. Run OpenVidu Server

--8<-- "shared/tutorials/run-openvidu-server-azure.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.3.0
```

### 3. Run the application

To run this application, you need [Node.js](https://nodejs.org/en/download){:target="\_blank"} (≥ 18) installed on your device.

1. Navigate into the application directory

```bash
cd openvidu-livekit-tutorials/advanced-features/openvidu-recording-basic-node-azure
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

## Understanding the code

This application consists of two essential backend files under the `src` directory:

- `index.js`: This file holds the server application and defines the REST API endpoints.
- `azure.blobstorage.service.js`: This file encapsulates the operations to interact with the Azure Blob Storage container.

And the following essential frontend files under the `public` directory:

- `index.html`: This is the client application's main HTML file.
- `app.js`: This is the main JavaScript file that interacts with the server application and handles the client application's logic and functionality.
- `style.css`: This file contains the client application's styling.
- `recordings.html`: This file defines the HTML for the general recording page.

---

### Backend

The server application extends the [Node.js server tutorial](../application-server/node.md){:target="\_blank"} by adding the following REST API endpoints:

- **`POST /recordings/start`**: Starts the recording of a room.
- **`POST /recordings/stop`**: Stops the recording of a room.
- **`GET /recordings`**: Lists all recordings stored in the Azure Container. This endpoint also allows filtering recordings by room ID.
- **`GET /recordings/:recordingName`**: Retrieves a recording from the Azure Container and returns it as a stream.
- **`DELETE /recordings/:recordingName`**: This endpoint deletes a recording from the Azure Container.

Before we dive into the code of each endpoint, let's first see the changes introduced in the `index.js` file:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L15-L26' target='_blank'>index.js</a>" linenums="15" hl_lines="5 6-7 15-18"
// Configuration
const SERVER_PORT = process.env.SERVER_PORT || 6080;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || "devkey";
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || "secret";
const LIVEKIT_URL = process.env.LIVEKIT_URL || "http://localhost:7880"; // (1)!
const RECORDING_FILE_PORTION_SIZE = 5 * 1024 * 1024; // (2)!

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.raw({ type: "application/webhook+json" }));

// Set the static files location
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(path.join(__dirname, "../public"))); // (3)!
```

1. The URL of the LiveKit server.
2. The portion size of the recording that will be sent to the client in each request. This value is set to `5 MB`.
3. Set the `public` directory as the static files location.

There are two new environment variables:

- `LIVEKIT_URL`: The URL of the LiveKit server.
- `RECORDING_FILE_PORTION_SIZE`: The portion size of the recording that will be sent to the client in each request.

Besides, the `index.js` file configures the server to serve static files from the `public` directory.

It also initializes the `EgressClient`, which will help interacting with [Egress API](https://docs.livekit.io/home/egress/api/){:target="\_blank"} to manage recordings, and the `AzureBlobStorageService`, which will help interacting with the Blob Container:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L33-L38' target='_blank'>index.js</a>" linenums="33"
const egressClient = new EgressClient(
  LIVEKIT_URL,
  LIVEKIT_API_KEY,
  LIVEKIT_API_SECRET
);
const azureBlobService = new AzureBlobService();
```

The `POST /token` endpoint has been modified to add the `roomRecord` permission to the access token, so that participants can start recording a room:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L45-L62' target='_blank'>index.js</a>" linenums="45" hl_lines="14"
app.post("/token", async (req, res) => {
  const roomName = req.body.roomName;
  const participantName = req.body.participantName;

  if (!roomName || !participantName) {
    return res
      .status(400)
      .json({ errorMessage: "roomName and participantName are required" });
  }

  const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
    identity: participantName,
  });
  at.addGrant({ roomJoin: true, room: roomName, roomRecord: true }); // (1)!
  const token = await at.toJwt();

  return res.json({ token });
});
```

1. Add the `roomRecord` permission to the access token.

Now let's explore the code for each recording feature:

#### Start recording

The `POST /recordings/start` endpoint starts the recording of a room. It receives the name of the room to record as parameter and returns the recording metadata:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L79-L117' target='_blank'>index.js</a>" linenums="79"
app.post("/recordings/start", async (req, res) => {
  const { roomName } = req.body;

  if (!roomName) {
    return res.status(400).json({ errorMessage: "roomName is required" });
  }

  const activeRecording = await getActiveRecordingByRoom(roomName); // (1)!

  // Check if there is already an active recording for this room
  if (activeRecording) {
    return res
      .status(409)
      .json({ errorMessage: "Recording already started for this room" }); // (2)!
  }

  // Use the EncodedFileOutput to save the recording to an MP4 file
  // The room name, time and room ID in the file path help to organize the recordings
  const fileOutput = new EncodedFileOutput({
    // (3)!
    fileType: EncodedFileType.MP4, // (4)!
    filepath: `RoomComposite-{room_name}-{time}-{room_id}`, // (5)!
    disableManifest: true,
  });

  try {
    // Start a RoomCompositeEgress to record all participants in the room
    const egressInfo = await egressClient.startRoomCompositeEgress(roomName, {
      // (6)!
      file: fileOutput,
    });
    const recording = {
      name: egressInfo.fileResults[0].filename.split("/").pop(), // (7)!
      startedAt: Number(egressInfo.startedAt) / 1_000_000,
    };
    res.json({ message: "Recording started", recording }); // (8)!
  } catch (error) {
    console.error("Error starting recording.", error);
    res.status(500).json({ errorMessage: "Error starting recording" });
  }
});
```

1. The `getActiveRecordingByRoom` function retrieves the active recording for a room.
2. If there is already an active recording for the room, the server returns a `409 Conflict` status code.
3. Use the `EncodedFileOutput` class to export the recording to an external file.
4. Define the file type as `MP4`.
5. Define the file path where the recording will be stored. The `{room_name}`, `{time}` and `{room_id}` templates will be replaced by the actual room name, timestamp and room ID, respectively. Check out all available [filename templates](https://docs.livekit.io/home/egress/outputs/#filename-templating){:target="\_blank"}.
6. Start a `RoomCompositeEgress` to record all participants in the room by calling the `startRoomCompositeEgress` method of the `EgressClient` with the `roomName` and `fileOutput` as parameters.
7. Extract the recording name from the `fileResults` array.
8. Return the recording metadata to the client.

This endpoint does the following:

1.  Obtains the `roomName` parameter from the request body. If it is not available, it returns a `400` error.
2.  Check if there is already an active recording for the room. If there is, it returns a `409` error to prevent starting a new recording. To accomplish this, we use the `getActiveRecordingByRoom` function, which lists all active egresses for a specified room by calling the `listEgress` method of the `EgressClient` with the `roomName` and `active` parameters, and then returns the egress ID of the first active egress found:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L231-L240' target='_blank'>index.js</a>" linenums="231"
    const getActiveRecordingByRoom = async (roomName) => {
      try {
        // List all active egresses for the room
        const egresses = await egressClient.listEgress({
          roomName,
          active: true,
        });
        return egresses.length > 0 ? egresses[0].egressId : null;
      } catch (error) {
        console.error("Error listing egresses.", error);
        return null;
      }
    };
    ```

3.  Initializes an `EncodedFileOutput` object to export the recording to an external file. It sets the file type as `MP4` and defines the file path where the recording will be stored. The `{room_name}`, `{time}` and `{room_id}` templates will be replaced by the actual room name, timestamp and room ID, respectively. Check out all available [filename templates](https://docs.livekit.io/home/egress/outputs/#filename-templating){:target="\_blank"}.
4.  Starts a `RoomCompositeEgress` to record all participants in the room by calling the `startRoomCompositeEgress` method of the `EgressClient` with `roomName` and `fileOutput` as parameters.
5.  Extracts the recording name from the `fileResults` array.
6.  Returns the recording metadata to the client.

#### Stop recording

The `POST /recordings/stop` endpoint stops the recording of a room. It receives the room name of the room to stop recording as a parameter and returns the updated recording metadata:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L120-L148' target='_blank'>index.js</a>" linenums="120"
app.post("/recordings/stop", async (req, res) => {
  const { roomName } = req.body;

  if (!roomName) {
    return res.status(400).json({ errorMessage: "roomName is required" });
  }

  const activeRecording = await getActiveRecordingByRoom(roomName); // (1)!

  // Check if there is an active recording for this room
  if (!activeRecording) {
    return res
      .status(409)
      .json({ errorMessage: "Recording not started for this room" }); // (2)!
  }

  try {
    // Stop the egress to finish the recording
    const egressInfo = await egressClient.stopEgress(activeRecording); // (3)!
    const file = egressInfo.fileResults[0];
    const recording = {
      name: file.filename.split("/").pop(),
    };
    return res.json({ message: "Recording stopped", recording }); // (4)!
  } catch (error) {
    console.error("Error stopping recording.", error);
    return res.status(500).json({ errorMessage: "Error stopping recording" });
  }
});
```

1. The `getActiveRecordingByRoom` function retrieves the active recording for a room.
2. If there is no active recording for the room, the server returns a `409 Conflict` status code.
3. Stop the egress to finish the recording by calling the `stopEgress` method of the `EgressClient` with the egress ID (`activeRecording`) as a parameter.
4. Return the updated recording metadata to the client.

This endpoint does the following:

1. Obtains the `roomName` parameter from the request body. If it is not available, it returns a `400` error.
2. Retrieves all active egresses for the room. If there is no active egress for the room, it returns a `409` error to prevent stopping a non-existent recording.
3. Extracts the `egressId` from the active egress.
4. Stops the egress to finish the recording by calling the `stopEgress` method of the `EgressClient` with the egress ID (`activeRecording`) as a parameter.
5. Returns the updated recording metadata to the client.

#### List recordings

The `GET /recordings` endpoint lists all recordings stored in the Azure Container. This endpoint also allows filtering recordings by room name or room ID:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node/src/index.js#L152-L173' target='_blank'>index.js</a>" linenums="152"
app.get("/recordings", async (req, res) => {
  const roomId = req.query.roomId?.toString(); // (1)!
  try {
    const azureResponse = await azureBlobService.listObjects(); // (2)!
    let recordings = [];
    if (azureResponse.length > 0) {
      recordings = azureResponse.map((obj) => ({
        // (3)!
        name: obj.name,
      }));
    }
    // Filter recordings by room ID
    recordings = recordings.filter((recording) => // (4)!
      roomId ? recording.name.includes(roomId) : true
    ); 
    return res.json({ recordings }); // (5)!
  } catch (error) {
    console.error("Error listing recordings.", error);
    return res.status(500).json({ errorMessage: "Error listing recordings" });
  }
});
```

1. Obtain the `roomId` query parameter for later filtering, if available.
2. List all Egress video files in the Azure Container.
3. Map all of the recording names from the Azure response.
4. Filter the recordings by room ID, if available.
5. Return the list of recordings to the client.

This endpoint does the following:

1.  Obtains the `roomId` query parameter for later filtering, if available.
2.  Lists all Egress video files in the Azure Container. To accomplish this, we use the `listObjects` method of the `AzureBlobService` with the `RECORDINGS_PATH` parameter.
3.  Extracts the recording names from the Azure response.
4.  Filters the recordings by room ID, if available. The room ID is part of the recording name, so we can filter with a quick check.
5.  Returns the list of recordings to the client.

#### Get recording

The `GET /recordings/:recordingName` endpoint retrieves a specific portion of a recording from the Azure Container and returns it as a stream. The server sends the recording file in portions of `5 MB` each time the client requests a range of the recording file. This is done to prevent loading the entire recording file into memory and to allow the client to play the recording while it is being downloaded and seek to a specific time:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L173-L203' target='_blank'>index.js</a>" linenums="173"
app.get("/recordings/:recordingName", async (req, res) => {
  const { recordingName } = req.params;
  const { range } = req.headers;
  const exists = await azureBlobService.exists(recordingName); // (1)!

  if (!exists) {
    return res.status(404).json({ errorMessage: "Recording not found" });
  }

  try {
    // Get the recording file from azure
    const { stream, size, start, end } = await getRecordingStream(
      // (2)!
      recordingName,
      range
    );

    // Set response headers
    res.status(206); // (3)!
    res.setHeader("Cache-Control", "no-cache"); // (4)!
    res.setHeader("Content-Type", "video/mp4"); // (5)!
    res.setHeader("Accept-Ranges", "bytes"); // (6)!
    res.setHeader("Content-Range", `bytes ${start}-${end}/${size}`); // (7)!
    res.setHeader("Content-Length", end - start + 1); // (8)!

    // Pipe the recording file to the response
    stream.pipe(res).on("finish", () => res.end()); // (9)!
  } catch (error) {
    console.error("Error getting recording.", error);
    return res.status(500).json({ errorMessage: "Error getting recording" });
  }
});
```

1. Check if the recording exists in the Azure Container.
2. Get the recording file from the Azure Container.
3. Set the response status code to `206 Partial Content`.
4. Set the `Cache-Control` header as `no-cache`.
5. Set the `Content-Type` header as `video/mp4`.
6. Set the `Accept-Ranges` header as `bytes`.
7. Set the `Content-Range` header with the start and end of the recording file and its size.
8. Set the `Content-Length` header as the size of the recording file portion.
9. Pipe the recording file to the response.

This endpoint does the following:

1.  Extracts the `recordingName` parameter from the request.
2.  Checks if the recording exists in the Azure Container by calling the `exists` method of the `AzureBlobService` with the `recordingName` as a parameter. If the recording does not exist, it returns a `404` error.
3.  Gets the requested range of the recording file by calling the `getRecordingStream` function:

    ```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L242-L255' target='_blank'>index.js</a>" linenums="242"
    const getRecordingStream = async (recordingName, range) => {
      const size = await azureBlobService.getObjectSize(recordingName);

      // Get the requested range
      const parts = range?.replace(/bytes=/, "").split("-"); // (1)!
      const start = range ? parseInt(parts[0], 10) : 0; // (2)!
      const endRange = parts[1]
        ? parseInt(parts[1], 10)
        : start + RECORDING_FILE_PORTION_SIZE; // (3)!
      const end = Math.min(endRange, size - 1); // (4)!

      const stream = await azureBlobService.getObject(recordingName, { start, end }); // (5)!
      return { stream, size, start, end };
    };
    ```

    1. Get the size of the recording file.
    2. Get the start of the requested range.
    3. Get the end of the requested range or set it to the start plus the established portion size.
    4. Get the minimum between the end of the requested range and the size of the recording file minus one.
    5. Get the recording file from the Azure Container with the requested range.

    This function does the following:

    1.  Gets the size of the recording file by calling the `getObjectSize` method of the `AzureBlobService` with the `recordingName` as a parameter.
    2.  Extracts the start of the requested range from the `range` header.
    3.  Extracts the end of the requested range from the `range` header. If the end is not provided, it sets the end to the start plus the established portion size.
    4.  Gets the minimum between the end of the requested range and the size of the recording file minus one. This is done to prevent requesting a range that exceeds the recording file size.
    5.  Gets the recording file from the Azure Container with the requested range by calling the `getObject` method of the `AzureBlobService` with the `recordingName` and `range` as parameters.

4.  Sets the response headers:

    - `Cache-Control`: `no-cache`.
    - `Content-Type`: `video/mp4`.
    - `Accept-Ranges`: `bytes`.
    - `Content-Range`: The start and end of the recording file and its size.
    - `Content-Length`: The size of the recording file portion.

5.  Pipes the recording file to the response.

#### Delete recording

The `DELETE /recordings/:recordingName` endpoint deletes a recording from the Azure Container:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/index.js#L206-L222' target='_blank'>index.js</a>" linenums="206"
app.delete("/recordings/:recordingName", async (req, res) => {
  const { recordingName } = req.params;
  const exists = await azureBlobService.exists(recordingName); // (1)!

  if (!exists) {
    return res.status(404).json({ errorMessage: "Recording not found" });
  }

  try {
    // Delete the recording file from Azure
    await Promise.all([azureBlobService.deleteObject(recordingName)]); // (2)!
    res.json({ message: "Recording deleted" });
  } catch (error) {
    console.error("Error deleting recording.", error);
    res.status(500).json({ errorMessage: "Error deleting recording" });
  }
});
```

1. Check if the recording exists in the Azure Container.
2. Delete the recording file from the Azure Container.

This endpoint does the following:

1.  Extracts the `recordingName` parameter from the request.
2.  Checks if the recording exists in the Azure Container by calling the `exists` method of the `AzureBlobService` with the `recordingName` as a parameter. If the recording does not exist, it returns a `404` error.
3.  Deletes the recording file from the Azure Container by calling the `deleteObject` method of the `AzureBlobService` with the object's `recordingName` as a parameter.

---

#### Azure Blob Storage Service

Finally, let's take a look at the `azure.blobstorage.service.js` file, which encapsulates the operations to interact with the Azure Container:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/src/azure.blobstorage.service.js' target='_blank'>azure.blobstorage.service.js</a>" linenums="6"
// Azure configuration
const AZURE_ACCOUNT_NAME = process.env.AZURE_ACCOUNT_NAME || "devstoreaccount"; // (1)!
const AZURE_ACCOUNT_KEY =
    process.env.AZURE_ACCOUNT_KEY || "nokey"; // (2)!
const AZURE_CONTAINER_NAME =
    process.env.AZURE_CONTAINER_NAME || "openvidu-appdata"; // (3)!

const AZURE_ENDPOINT =
    process.env.AZURE_ENDPOINT ||
    `https://${AZURE_ACCOUNT_NAME}.blob.core.windows.net`; // (4)!

export class AzureBlobService {
    static instance;

    constructor() {
        if (AzureBlobService.instance) {
            return AzureBlobService.instance;
        }
        // (5)!
        const sharedKeyCredential = new StorageSharedKeyCredential(
            AZURE_ACCOUNT_NAME,
            AZURE_ACCOUNT_KEY
        );

        this.blobServiceClient = new BlobServiceClient(
            AZURE_ENDPOINT,
            sharedKeyCredential
        );

        this.containerClient = this.blobServiceClient.getContainerClient(
            AZURE_CONTAINER_NAME
        );

        AzureBlobService.instance = this;
        return this;
    }

    async exists(key) { // (6)!
        const blobClient = this.containerClient.getBlobClient(key);
        return await blobClient.exists();
    }

    async getObjectSize(key) { // (8)!
        const props = await this.headObject(key);
        return props.contentLength;
    }

    async headObject(key) { // (7)!
        const blobClient = this.containerClient.getBlobClient(key);
        const props = await blobClient.getProperties();
        return props;
    }

    async getObject(key, range) { // (9)!
        const blobClient = this.containerClient.getBlobClient(key);
        const downloadOptions = range
            ? {
                rangeGetContentMD5: false,
                range: {
                    offset: range.start,
                    count: range.end - range.start + 1,
                },
            }
            : {};

        const response = await blobClient.download(
            downloadOptions.range?.offset ?? 0,
            downloadOptions.range?.count
        );

        return response.readableStreamBody;
    }

    async listObjects() { // (10)!
        const result = [];
        for await (const blob of this.containerClient.listBlobsFlat()) {
            result.push(blob);
        }
        return result;
    }

    async deleteObject(key) { // (11)!
        const blobClient = this.containerClient.getBlobClient(key);
        return await blobClient.deleteIfExists();
    }
}
```

1. The Storage Account Name of Azure.
2. The access key of Azure Blob Storage.
3. The name of Azure Container.
4. The URL of Azure endpoint.
5. Initialize the `Clients` with the provided configuration.
6. Check if an object exists in the Azure Container.
7. Retrieve the metadata of an object in the Azure Container.
8. Retrieve the size of an object in the Azure Container.
9. Retrieve a specified range of bytes from an object in the Azure Container.
10. List objects in the Azure Container that match a regex pattern.
11. Delete an object from the Azure Container.

This file loads environment variables for the Azure configuration:

- `AZURE_ACCOUNT_NAME`: The name of the Azure Storage Account.
- `AZURE_ACCOUNT_KEY`: The access key of Azure Blob Storage.
- `AZURE_CONTAINER_NAME`: The name of the Azure Container.
- `AZURE_ENDPOINT`: The URL of Azure endpoint.

Then, it defines the `AzureBlobService` class as a singleton, which initializes the `Clients` with the provided configuration. The class encapsulates the following methods to interact with the Azure Container:

- `exists`: Checks if an object exists in the Azure Container.
- `getObjectSize`: Retrieves the size of an object in the Azure Container.
- `headObject`: Retrieves the metadata of an object in the Azure Container.
- `getObject`: Retrieves an object from the Azure Container.
- `listObjects`: Lists objects in the Azure Container that match a regex pattern.
- `deleteObject`: Deletes an object from the Azure Container.
---

### Frontend

The client application extends the [JavaScript client tutorial](../application-client/javascript.md){:target="\_blank"} by adding recording features, introducing new buttons to facilitate actions such as starting and stopping recording a room, as well as listing, playing and deleting recordings. When these newly introduced buttons are interacted with, the client triggers requests to the REST API endpoints of the server application.

In order to update the user interface of all participants in the room according to the recording status, the client application subscribes to the `RoomEvent.RecordingStatusChanged` event, which is triggered when the room changes from being recorded to not being recorded, and vice versa. When this event is triggered, the `updateRecordingInfo` function is called to update the recording information of the room displayed on the screen. This function is also called when a participant joins the room, using the current value of the `room.recording` property at that moment. This is done in the `joinRoom` function of the `app.js` file:

!!! warning "Limitations of the `RoomEvent.RecordingStatusChanged` event"

    By using the `RoomEvent.RecordingStatusChanged` event, we can only detect when the recording has started or stopped, but not other states like `starting`, `stopping` or `failed`. Additionally, when the recording stops, the event is not triggered until the recorder participant leaves the room, causing a delay of 20 seconds approximately between the stop and when participants are notified.

    To overcome these limitations, you can follow the steps described in the [advanced recording tutorial](./recording-advanced-azure.md){:target="\_blank"}, where we implement a custom notification system. This system informs participants about the recording status by listening to webhook events and updating room metadata.

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/public/app.js#L20-L87' target='_blank'>app.js</a>" linenums="20" hl_lines="32-37 62-63"
async function joinRoom() {
  // Disable 'Join' button
  document.getElementById("join-button").disabled = true;
  document.getElementById("join-button").innerText = "Joining...";

  // Initialize a new Room object
  room = new LivekitClient.Room();

  // Specify the actions when events take place in the room
  // On every new Track received...
  room.on(
    LivekitClient.RoomEvent.TrackSubscribed,
    (track, _publication, participant) => {
      addTrack(track, participant.identity);
    }
  );

  // On every new Track destroyed...
  room.on(
    LivekitClient.RoomEvent.TrackUnsubscribed,
    (track, _publication, participant) => {
      track.detach();
      document.getElementById(track.sid)?.remove();

      if (track.kind === "video") {
        removeVideoContainer(participant.identity);
      }
    }
  );

  // When recording status changes...
  room.on(
    LivekitClient.RoomEvent.RecordingStatusChanged,
    async (isRecording) => {
      await updateRecordingInfo(isRecording);
    }
  );

  try {
    // Get the room name and participant name from the form
    const roomName = document.getElementById("room-name").value;
    const userName = document.getElementById("participant-name").value;

    // Get a token from your application server with the room name and participant name
    const token = await getToken(roomName, userName);

    // Connect to the room with the LiveKit URL and the token
    await room.connect(LIVEKIT_URL, token);

    // Hide the 'Join room' page and show the 'Room' page
    document.getElementById("room-title").innerText = roomName;
    document.getElementById("join").hidden = true;
    document.getElementById("room").hidden = false;

    // Publish your camera and microphone
    await room.localParticipant.enableCameraAndMicrophone();
    const localVideoTrack = this.room.localParticipant.videoTrackPublications
      .values()
      .next().value.track;
    addTrack(localVideoTrack, userName, true);

    // Update recording info
    await updateRecordingInfo(room.isRecording);
  } catch (error) {
    console.log("There was an error connecting to the room:", error.message);
    await leaveRoom();
  }
}
```

The `updateRecordingInfo` function updates the recording information of the room by changing the recording button's text and color according to the recording status. It also shows or hides the alert message that informs the user that the room is being recorded. Finally, it updates the recording list by calling the `listRecordings` function.

This function retrieves all recordings available for the room from the backend and displays their relevant information by invoking the `showRecordingList` function:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/public/app.js#L337-L370' target='_blank'>app.js</a>" linenums="337"
function showRecordingList(recordings) {
  const recordingsList = document.getElementById("recording-list");

  if (recordings.length === 0) {
    recordingsList.innerHTML = "<span>There are no recordings available</span>";
  } else {
    recordingsList.innerHTML = "";
  }

  recordings.forEach((recording) => {
    const recordingName = recording.name;

    const recordingContainer = document.createElement("div");
    recordingContainer.className = "recording-container";
    recordingContainer.id = recordingName;

    recordingContainer.innerHTML = `
            <i class="fa-solid fa-file-video"></i>
            <div class="recording-info">
                <p class="recording-name">${recordingName}</p>
            </div>
            <div class="recording-actions">
                <button title="Play" class="icon-button" onclick="displayRecording('${recordingName}')">
                    <i class="fa-solid fa-play"></i>
                </button>
                <button title="Delete" class="icon-button delete-button" onclick="deleteRecording('${recordingName}')">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        `;

    recordingsList.append(recordingContainer);
  });
}
```

The `showRecordingList` function creates a new `div` element for each recording available in the room and appends it to the `recording-list` container. Each `div` element contains the recording name, as well as buttons to play and delete the recording.

!!! info "Recording deletion"

    When a recording is deleted, it is removed from the recording list, but only for the user who initiated the deletion. Other users will continue to see the recording in their list until it is refreshed.

    In the [advanced recording tutorial](./recording-advanced-azure.md){:target="\_blank"}, we show how to implement a custom notification system that alerts all participants of a recording's deletion by sending data messages.

When the user clicks the play button, the `displayRecording` function is called to play the recording. This function opens a dialog window with an embedded video element and sets the source of the video to the [get recording endpoint](#get-recording) of the server application:

```javascript title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/public/app.js#L372-L379' target='_blank'>app.js</a>" linenums="372"
function displayRecording(recordingName) {
  const recordingVideoDialog = document.getElementById(
    "recording-video-dialog"
  );
  recordingVideoDialog.showModal();
  const recordingVideo = document.getElementById("recording-video");
  recordingVideo.src = `/recordings/${recordingName}`;
}
```

```html title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/advanced-features/openvidu-recording-basic-node-azure/public/index.html#L94-L99' target='_blank'>index.html</a>" linenums="94"
<dialog id="recording-video-dialog">
    <video id="recording-video" autoplay controls></video>
    <button class="btn btn-secondary" id="close-recording-video-dialog" onclick="closeRecording()">
        Close
    </button>
</dialog>
```

---

#### General recording page

The `recordings.html` file defines the HTML for the general recording page. This page lists all available recordings from all rooms and allows the user to filter them by room name. It also provides buttons to play and delete each recording.

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/advanced-features/recording3.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/advanced-features/recording3.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="../../../../assets/images/advanced-features/recording4.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="../../../../assets/images/advanced-features/recording4.png" loading="lazy"/></a></p></div>

</div>
