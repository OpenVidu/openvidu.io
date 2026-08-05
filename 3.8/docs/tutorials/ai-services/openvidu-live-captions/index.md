# Live Captions tutorial

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/ai-services/openvidu-live-captions)

This tutorial is a simple variation of the [JavaScript client](https://openvidu.io/3.8/docs/tutorials/application-client/javascript/index.md) tutorial, adding **live captions** thanks to the use of OpenVidu [Live Captions service](https://openvidu.io/3.8/docs/ai/live-captions/index.md).

## Running this tutorial

### 1. Run OpenVidu Server

**Run OpenVidu locally**

1. Download OpenVidu:

   ```bash
   git clone https://github.com/OpenVidu/openvidu-local-deployment -b 3.8.0
   ```

1. Configure the local deployment:

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

1. Enable the Speech Processing agent:

   Modify file [`openvidu-local-deployment/community/agent-speech-processing.yaml`](https://github.com/OpenVidu/openvidu-local-deployment/blob/3.8.0/community/agent-speech-processing.yaml) to enable the Speech Processing agent. At least you need to set the following properties:

   ```yaml
   enabled: true # Enables the agent

   live_captions:

       processing: automatic # Configures the agent to connect to new Rooms automatically

       provider: YOUR_SPEECH_PROVIDER # Configures the AI provider for speech-to-text processing

       # Followed by your provider specific configuration
   ```

   Info

   The default `provider` property is set to **`vosk`**, which is a local, open-source, and free-to-use option.\
   Visit [**Supported AI providers**](https://openvidu.io/3.8/docs/ai/live-captions/#supported-ai-providers) to see the full list of available AI providers, both local and cloud-based.

1. Run OpenVidu:

   ```bash
   docker compose up
   ```

**Deploy OpenVidu**

To use a production-ready OpenVidu deployment, visit the official [deployment guide](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md).

Enable the Live Captions service

Once your deployment is up and running, enable the Live Captions service following the [official instructions](https://openvidu.io/3.8/docs/ai/live-captions/#how-to-enable-live-captions-service-in-your-openvidu-deployment).

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.8.0
```

### 3. Run a server application

**Node.js**

To run this server application, you need [Node.js](https://nodejs.org/en/download) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/node
   ```

1. Install dependencies

   ```bash
   npm install
   ```

1. Run the application

   ```bash
   npm start
   ```

For more information, check the [Node.js tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/node/index.md).

**Go**

To run this server application, you need [Go](https://go.dev/doc/install) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/go
   ```

1. Run the application

   ```bash
   go run main.go
   ```

For more information, check the [Go tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/go/index.md).

**Ruby**

To run this server application, you need [Ruby](https://www.ruby-lang.org/en/documentation/installation/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/ruby
   ```

1. Install dependencies

   ```bash
   bundle install
   ```

1. Run the application

   ```bash
   ruby app.rb
   ```

For more information, check the [Ruby tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/ruby/index.md).

**Java**

To run this server application, you need [Java](https://www.java.com/en/download/manual.jsp) and [Maven](https://maven.apache.org) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/java
   ```

1. Run the application

   ```bash
   mvn spring-boot:run
   ```

For more information, check the [Java tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/java/index.md).

**Python**

To run this server application, you need [Python 3](https://www.python.org/downloads/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/python
   ```

1. Create a python virtual environment

   ```bash
   python -m venv venv
   ```

1. Activate the virtual environment

   **Windows**

   ```powershell
   .\venv\Scripts\activate
   ```

   **macOS**

   ```bash
   . ./venv/bin/activate
   ```

   **Linux**

   ```bash
   . ./venv/bin/activate
   ```

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

1. Run the application

   ```bash
   python app.py
   ```

For more information, check the [Python tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/python/index.md).

**Rust**

To run this server application, you need [Rust](https://www.rust-lang.org/tools/install) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/rust
   ```

1. Run the application

   ```bash
   cargo run
   ```

For more information, check the [Rust tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/rust/index.md).

**PHP**

To run this server application, you need [PHP](https://www.php.net/manual/en/install.php) and [Composer](https://getcomposer.org/download/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/php
   ```

1. Install dependencies

   ```bash
   composer install
   ```

1. Run the application

   ```bash
   composer start
   ```

Warning

LiveKit PHP SDK requires library [BCMath](https://www.php.net/manual/en/book.bc.php) . This is available out-of-the-box in PHP for Windows, but a manual installation might be necessary in other OS. Run **`sudo apt install php-bcmath`** or **`sudo yum install php-bcmath`**

For more information, check the [PHP tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/php/index.md).

**.NET**

To run this server application, you need [.NET](https://dotnet.microsoft.com/en-us/download) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/dotnet
   ```

1. Run the application

   ```bash
   dotnet run
   ```

Warning

This .NET server application needs the `LIVEKIT_API_SECRET` env variable to be at least 32 characters long. Make sure to update it [here](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/b97db7278227470fd386337ffde49b2458315c6f/application-server/dotnet/appsettings.json#L11) and in your [OpenVidu Server](#1-run-openvidu-server).

For more information, check the [.NET tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/dotnet/index.md).

### 4. Run the client application

To run the client application tutorial, you need an HTTP web server installed on your development computer. A great option is [http-server](https://github.com/http-party/http-server) . You can install it via [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm):

```bash
npm install -g http-server
```

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/ai-services/openvidu-live-captions
   ```

1. Serve the application:

   ```bash
   http-server -p 5080 ./src
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

## Understanding the code

You can first take a look at the [JavaScript client tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/javascript/index.md), as this application shares the same codebase. The only thing added by this tutorial is a new handler for the [`Room`](https://docs.livekit.io/reference/client-sdk-js/classes/Room.html) object to receive transcription messages and display them as live captions in the HTML:

```javascript
room.registerTextStreamHandler("lk.transcription", async (reader, participantInfo) => { // (1)!
    const message = await reader.readAll(); // (2)!
    const isFinal = reader.info.attributes["lk.transcription_final"] === "true"; // (3)!
    const trackId = reader.info.attributes["lk.transcribed_track_id"]; // (4)!

    if (isFinal) {
      const speaker = participantInfo.identity == room.localParticipant.identity // (5)!
          ? "You" : participantInfo.identity;
      const timestamp = new Date().toLocaleTimeString();
      const captionsTextarea = document.getElementById("captions"); // (6)!
      captionsTextarea.value += `[${timestamp}] ${speaker}: ${message}\n`;
      captionsTextarea.scrollTop = captionsTextarea.scrollHeight;
    }
  }
);
```

1. Use method [Room.registerTextStreamHandler](https://docs.livekit.io/reference/client-sdk-js/classes/Room.html#registertextstreamhandler) to register a handler on topic `lk.transcription`. Transcription messages will arrive to this handler.
1. Await each transcription message.
1. Read attribute `lk.transcription_final` to determine if the transcription message is a final or an interim one. See [Final vs Interim transcriptions](https://openvidu.io/3.8/docs/ai/live-captions/#final-vs-interim-transcriptions).
1. You can also read attribute `lk.transcribed_track_id` to know which specific audio track has been transcribed.
1. Read property `participantInfo.identity` to get the identity of the participant that originated the transcription event.
1. Build your live caption message as desired and append it to the HTML.

Using method [Room.registerTextStreamHandler](https://docs.livekit.io/reference/client-sdk-js/classes/Room.html#registertextstreamhandler) we subscribe to topic `lk.transcription`. All transcription messages will arrive to this handler.

You can get the identity of the participant that originated the transcription event from the `participantInfo` object passed to the handler.

Apart from the message itself (which you get by awaiting method `reader.readAll()`) there are two main attributes in the transcription message (which you can access via `reader.info.attributes`):

- `lk.transcription_final`: Indicates whether the transcription message is final or interim. See [Final vs Interim transcriptions](https://openvidu.io/3.8/docs/ai/live-captions/#final-vs-interim-transcriptions) for more details.
- `lk.transcribed_track_id`: The ID of the audio track that has been transcribed. This is useful to know which specific participant's audio track has been transcribed, if necessary.

Once you have all the information about the transcription message, you can build your live caption text as desired and display it in the HTML (in this case, using a simple `<textarea>` element).
