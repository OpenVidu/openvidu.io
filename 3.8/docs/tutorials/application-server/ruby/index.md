# Ruby Server Tutorial

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/application-server/ruby)

This is a minimal server application built for Ruby with [Sinatra](https://sinatrarb.com/) that allows:

- Generating LiveKit tokens on demand for any [application client](https://openvidu.io/3.8/docs/tutorials/application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/) .

It internally uses [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby) .

## Running this tutorial

### 1. Run OpenVidu Server

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

To use a production-ready OpenVidu deployment, visit the official [deployment guide](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md).

Configure Webhooks

All [application servers](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) have an endpoint to receive webhooks from OpenVidu. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/enable-webhooks/#send-webhooks-to-a-local-application-server) section for more information.

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.8.0
```

### 3. Run the server application

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

### 4. Run a client application to test against this server

**JavaScript**

To run the client application tutorial, you need an HTTP web server installed on your development computer. A great option is [http-server](https://github.com/http-party/http-server) . You can install it via [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) :

```bash
npm install -g http-server
```

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-js
   ```

1. Serve the application:

   ```bash
   http-server -p 5080 ./src
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

Join screen of the JavaScript tutorial app

Video call room of the JavaScript tutorial app

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

For more information, check the [JavaScript tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/javascript/index.md) .

**React**

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-react
   ```

1. Install dependencies:

   ```bash
   npm install
   ```

1. Run the application:

   ```bash
   npm start
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

Join screen of the React tutorial app

Video call room of the React tutorial app

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

For more information, check the [React tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/react/index.md) .

**Angular**

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-angular
   ```

1. Install the required dependencies:

   ```bash
   npm install
   ```

1. Serve the application:

   ```bash
   npm start
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

Join screen of the Angular tutorial app

Video call room of the Angular tutorial app

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

For more information, check the [Angular tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/angular/index.md) .

**Vue**

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-vue
   ```

1. Install dependencies:

   ```bash
   npm install
   ```

1. Run the application:

   ```bash
   npm start
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

Join screen of the Vue tutorial app

Video call room of the Vue tutorial app

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

For more information, check the [Vue tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/vue/index.md) .

**Electron**

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-electron
   ```

1. Install the required dependencies:

   ```bash
   npm install
   ```

1. Run the application:

   ```bash
   npm start
   ```

The application will seamlessly initiate as a native desktop program, adapting itself to the specific operating system you are using. Once the application is open, you should see a screen like this:

Join screen of the Electron tutorial app

Video call room of the Electron tutorial app

Running your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

For more information, check the [Electron tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/electron/index.md) .

**Ionic**

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
   cd openvidu-livekit-tutorials/application-client/openvidu-ionic
   ```

1. Install the required dependencies:

   ```bash
   npm install
   ```

1. Serve the application:

   You have two options for running the client application: **browser-based** or **mobile device-based**:

   **Browser**

   To run the application in a browser, you will need to start the Ionic server. To do so, run the following command:

   ```bash
   npm start
   ```

   Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080). You should see a screen like this:

   Mobile appearance

   To show the app with a mobile device appearance, open the dev tools in your browser and find the button to adapt the viewport to a mobile device aspect ratio. You may also choose predefined types of devices to see the behavior of your app in different resolutions.

   Join screen of the Ionic tutorial app in a browser

   Video call room of the Ionic tutorial app in a browser

   Accessing your application client from other devices in your local network

   One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

   Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

   **Mobile**

   Running the tutorial on a mobile device presents additional challenges compared to running it in a browser, mainly due to the application being launched on a different device, such as an Android smartphone or iPhone, rather than our computer. To overcome these challenges, the following steps need to be taken:

   1. **Localhost limitations:**

      The usage of `localhost` in our Ionic app is restricted, preventing seamless communication between the application client and the server.

   1. **Serve over local network:**

      The application must be served over our local network to enable communication between the device and the server.

   1. **Secure connection requirement for WebRTC API:**

      The WebRTC API demands a secure connection for functionality outside of localhost, necessitating the serving of the application over HTTPS.

   If you run [OpenVidu locally](#run-openvidu-locally) you don't need to worry about this. OpenVidu will handle all of the above requirements for you. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

   Now, let's explore how to run the application on a mobile device:

   Requirements

   Before running the application on a mobile device, make sure that the device is connected to the same network as your PC and the mobile is connected to the PC via USB or Wi-Fi.

   **Android device**

   ```bash
   npm run android
   ```

   **iOS device**

   You will need [Ruby](https://www.ruby-lang.org/en/documentation/installation/) and [Cocoapods](https://guides.cocoapods.org/using/getting-started.html) installed in your computer.

   The app must be signed with a development team. To do so, open the project in **Xcode** and select a development team in the **Signing & Capabilities** editor.

   ```bash
   npm run ios
   ```

   The script will ask you for the device you want to run the application on. You should select the real device you have connected to your computer.

   Once the mobile device has been selected, the script will launch the application on the device and you will see a screen like this:

   URL configuration of the Ionic tutorial app

   This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

   Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

   Join screen of the Ionic tutorial app on a mobile device

   Video call room of the Ionic tutorial app on a mobile device

For more information, check the [Ionic tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/ionic/index.md) .

**Android**

To run the client application tutorial, you need [Android Studio](https://developer.android.com/studio) installed on your development computer.

1. Open Android Studio and import the project located at `openvidu-livekit-tutorials/application-client/openvidu-android`.
1. Run the application in an emulator or a physical device by clicking the "Run" button in Android Studio. Check out the [official documentation](https://developer.android.com/studio/run) for further information.

The application will initiate as a native Android program. Once the application is opened, you should see a screen like this:

URL configuration of the Android tutorial app

This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

Connecting real Android device to application server running in you local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client in a real Android device and be able to reach the application server very easily without worrying about SSL certificates if they are both running in the same local network. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

Join screen of the Android tutorial app

Video call room of the Android tutorial app

For more information, check the [Android tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/android/index.md) .

**iOS**

To run the client application tutorial, you need [Xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12) installed on your MacOS.

1. Launch Xcode and open the `OpenViduIOS.xcodeproj` that you can find under `openvidu-livekit-tutorials/application-client/openvidu-ios`.
1. Run the application in an emulator or a physical device by clicking on the menu Product > Run or by ⌘R.

Emulator limitations

Publishing the camera track is not supported by iOS Simulator.

If you encounter code signing issues, make sure you change the **Team** and **bundle id** from the previous step.

The application will initiate as a native iOS application. Once the app is opened, you should see a screen like this:

URL configuration of the iOS tutorial app

This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

Connecting real iOS device to application server running in you local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client in a real iOS device and be able to reach the application server very easily without worrying about SSL certificates if they are both running in the same local network. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

Join screen of the iOS tutorial app

Video call room of the iOS tutorial app

For more information, check the [iOS tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/ios/index.md) .

## Understanding the code

The application is a simple Ruby app using the popular Sinatra web library. It has a single file `app.rb` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/livekit/webhook` : receive LiveKit webhook events.

Let's see the code of the `app.rb` file:

```ruby
require 'sinatra'
require 'sinatra/cors'
require 'sinatra/json'
require 'livekit' # (1)!
require './env.rb'

SERVER_PORT = ENV['SERVER_PORT'] || 6080 # (2)!
LIVEKIT_API_KEY = ENV['LIVEKIT_API_KEY'] || 'devkey' # (3)!
LIVEKIT_API_SECRET = ENV['LIVEKIT_API_SECRET'] || 'secret' # (4)!

set :port, SERVER_PORT # (5)!

register Sinatra::Cors # (6)!
set :allow_origin, '*' # (7)!
set :allow_methods, 'POST,OPTIONS'
set :allow_headers, 'content-type'
set :bind, '0.0.0.0' # (8)!
```

1. Import `livekit` library
1. The port where the application will be listening
1. The API key of LiveKit Server
1. The API secret of LiveKit Server
1. Configure the port
1. Enable CORS support
1. Set allowed origin (any), methods and headers
1. Listen in any available network interface of the host

The `app.rb` file imports the required dependencies and loads the necessary environment variables (defined in `env.rb` file):

- `SERVER_PORT`: the port where the application will be listening.
- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Finally the application configures the port, sets the CORS configuration for Sinatra and binds the application to all available network interfaces (0.0.0.0).

______________________________________________________________________

#### Create token endpoint

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```ruby
post '/token' do
  body = JSON.parse(request.body.read)
  room_name = body['roomName']
  participant_name = body['participantName']

  if room_name.nil? || participant_name.nil?
    status 400
    return json({errorMessage: 'roomName and participantName are required'})
  end

  token = LiveKit::AccessToken.new(api_key: LIVEKIT_API_KEY, api_secret: LIVEKIT_API_SECRET) # (1)!
  token.identity = participant_name # (2)!
  token.add_grant(roomJoin: true, room: room_name) # (3)!

  return json({token: token.to_jwt}) # (4)!
end
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
1. We set participant's identity in the AccessToken.
1. We set the video grants in the AccessToken. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant) .
1. Finally, we convert the AccessToken to a JWT token and send it back to the client.

The endpoint first obtains the `roomName` and `participantName` parameters from the request body. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby) :

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
1. We set participant's identity in the AccessToken.
1. We set the video grants in the AccessToken. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant) .
1. Finally, we convert the AccessToken to a JWT token and send it back to the client.

______________________________________________________________________

#### Receive webhook

The endpoint `/livekit/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/home/server/webhooks/#Events) .

```ruby
post '/livekit/webhook' do
  auth_header = request.env['HTTP_AUTHORIZATION'] # (1)!
  token_verifier = LiveKit::TokenVerifier.new(api_key: LIVEKIT_API_KEY, api_secret: LIVEKIT_API_SECRET) # (2)!
  begin
    token_verifier.verify(auth_header) # (3)!
    body = JSON.parse(request.body.read) # (4)!
    puts "LiveKit Webhook: #{body}" # (5)!
    return
  rescue => e
    puts "Authorization header is not valid: #{e}"
  end
end
```

1. Get the `Authorization` header from the HTTP request.
1. Create a new `TokenVerifier` instance providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. This will validate the webhook event to confirm it is actually coming from our LiveKit Server.
1. Verify the `Authorization` header with the `TokenVerifier`.
1. Now that we are sure the event is valid, we can parse the request JSON body to get the actual webhook event.
1. Consume the event as you whish.

We need to verify that the event is coming from our LiveKit Server. For that we need the `Authorization` header from the HTTP request and a `TokenVerifier` instance built with the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.

If the verification is successful, we can parse the request JSON body and consume the event (in this case, we just log it).

Remember to return a `200` OK response at the end to let LiveKit Server know that the webhook was received correctly.

Configure Webhooks

If you are using a [production deployment](#deploy-openvidu), remember to configure the webhook URL to point to your local application server as explained in the [Send Webhooks to a Local Application Server](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/enable-webhooks/#send-webhooks-to-a-local-application-server) section.
