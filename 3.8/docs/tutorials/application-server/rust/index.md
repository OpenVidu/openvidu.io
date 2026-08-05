# Rust Server Tutorial

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/application-server/rust)

This is a minimal server application built for Rust with [Axum](https://github.com/tokio-rs/axum) that allows:

- Generating LiveKit tokens on demand for any [application client](https://openvidu.io/3.8/docs/tutorials/application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/) .

It internally uses the [LiveKit Rust SDK](https://github.com/livekit/rust-sdks) .

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

To run this server application, you need [Rust](https://www.rust-lang.org/tools/install) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/rust
   ```

1. Run the application

   ```bash
   cargo run
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

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

For more information, check the [JavaScript tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/javascript/index.md).

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

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

For more information, check the [React tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/react/index.md).

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

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

For more information, check the [Angular tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/angular/index.md).

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

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

For more information, check the [Vue tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/vue/index.md).

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

Running your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

For more information, check the [Electron tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/electron/index.md).

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

   Accessing your application client from other devices in your local network

   One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

   Access your application client through [`https://xxx-yyy-zzz-www.openvidu-local.dev:5443`](https://xxx-yyy-zzz-www.openvidu-local.dev:5443), where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

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

   This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

   Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

For more information, check the [Ionic tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/ionic/index.md).

**Android**

To run the client application tutorial, you need [Android Studio](https://developer.android.com/studio) installed on your development computer.

1. Open Android Studio and import the project located at `openvidu-livekit-tutorials/application-client/openvidu-android`.
1. Run the application in an emulator or a physical device by clicking the "Run" button in Android Studio. Check out the [official documentation](https://developer.android.com/studio/run) for further information.

The application will initiate as a native Android program. Once the application is opened, you should see a screen like this:

This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

Connecting real Android device to application server running in you local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client in a real Android device and be able to reach the application server very easily without worrying about SSL certificates if they are both running in the same local network. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

For more information, check the [Android tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/android/index.md).

**iOS**

To run the client application tutorial, you need [Xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12) installed on your MacOS.

1. Launch Xcode and open the `OpenViduIOS.xcodeproj` that you can find under `openvidu-livekit-tutorials/application-client/openvidu-ios`.
1. Run the application in an emulator or a physical device by clicking on the menu Product > Run or by ⌘R.

Emulator limitations

Publishing the camera track is not supported by iOS Simulator.

If you encounter code signing issues, make sure you change the **Team** and **bundle id** from the previous step.

The application will initiate as a native iOS application. Once the app is opened, you should see a screen like this:

This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

Connecting real iOS device to application server running in you local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client in a real iOS device and be able to reach the application server very easily without worrying about SSL certificates if they are both running in the same local network. For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network).

Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

For more information, check the [iOS tutorial](https://openvidu.io/3.8/docs/tutorials/application-client/ios/index.md).

## Understanding the code

The application is a simple Rust app with a single file `main.rs` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/livekit/webhook` : receive LiveKit webhook events.

Let's see the code of the `main.rs` file:

```rust
use axum::http::HeaderMap;
use axum::{
    extract::Json, http::header::CONTENT_TYPE, http::Method, http::StatusCode, routing::post,
    Router,
};
use dotenv::dotenv;
use livekit_api::access_token::AccessToken; // (1)!
use livekit_api::access_token::TokenVerifier;
use livekit_api::access_token::VideoGrants;
use livekit_api::webhooks::WebhookReceiver;
use serde_json::{json, Value};
use std::env;
use tokio::net::TcpListener;
use tower_http::cors::{Any, CorsLayer};

#[tokio::main]
async fn main() {
    dotenv().ok(); // (2)!

    let server_port = env::var("SERVER_PORT").unwrap_or("6081".to_string());

    let cors = CorsLayer::new() // (3)!
        .allow_methods([Method::POST])
        .allow_origin(Any)
        .allow_headers([CONTENT_TYPE]);

    let app = Router::new() // (4)!
        .route("/token", post(create_token))
        .route("/livekit/webhook", post(receive_webhook))
        .layer(cors);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:".to_string() + &server_port)
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap(); // (5)!
}
```

1. Import all necessary dependencies from the Rust LiveKit library.
1. Load environment variables from `.env` file.
1. Enable CORS support.
1. Define `/token` and `/livekit/webhook` endpoints.
1. Start the server listening on the specified port.

The `main.rs` file imports the required dependencies and loads the necessary environment variables:

- `SERVER_PORT`: the port where the application will be listening.
- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Then CORS support is enabled and the endpoints are defined. Finally the `axum` application is initialized on the specified port.

______________________________________________________________________

#### Create token endpoint

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```rust
async fn create_token(payload: Option<Json<Value>>) -> (StatusCode, Json<Value>) {
    if let Some(payload) = payload {
        let livekit_api_key = env::var("LIVEKIT_API_KEY").unwrap_or("devkey".to_string());
        let livekit_api_secret = env::var("LIVEKIT_API_SECRET").unwrap_or("secret".to_string());

        let room_name = match payload.get("roomName") {
            Some(value) => value,
            None => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({ "errorMessage": "roomName is required" })),
                );
            }
        };
        let participant_name = match payload.get("participantName") {
            Some(value) => value,
            None => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({ "errorMessage": "participantName is required" })),
                );
            }
        };

        let token = match AccessToken::with_api_key(&livekit_api_key, &livekit_api_secret) // (1)!
            .with_identity(&participant_name.to_string()) // (2)!
            .with_name(&participant_name.to_string())
            .with_grants(VideoGrants { // (3)!
                room_join: true,
                room: room_name.to_string(),
                ..Default::default()
            })
            .to_jwt() // (4)!
        {
            Ok(token) => token,
            Err(_) => {
                return (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    Json(json!({ "errorMessage": "Error creating token" })),
                );
            }
        };

        return (StatusCode::OK, Json(json!({ "token": token }))); // (5)!
    } else {
        return (
            StatusCode::BAD_REQUEST,
            Json(json!({ "errorMessage": "roomName and participantName are required" })),
        );
    }
}
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
1. We set participant's name and identity in the AccessToken.
1. We set the video grants in the AccessToken. `room_join` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant) .
1. We convert the AccessToken to a JWT token.
1. Finally, the token is sent back to the client.

The endpoint first obtains the `roomName` and `participantName` parameters from the request body. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit Rust SDK](https://github.com/livekit/rust-sdks) :

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
1. We set participant's name and identity in the AccessToken.
1. We set the video grants in the AccessToken. `room_join` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant) .
1. We convert the AccessToken to a JWT token.
1. Finally, the token is sent back to the client.

______________________________________________________________________

#### Receive webhook

The endpoint `/livekit/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/home/server/webhooks/#Events) .

```rust
async fn receive_webhook(headers: HeaderMap, body: String) -> (StatusCode, String) {
    let livekit_api_key = env::var("LIVEKIT_API_KEY").unwrap_or("devkey".to_string());
    let livekit_api_secret = env::var("LIVEKIT_API_SECRET").unwrap_or("secret".to_string());
    let token_verifier = TokenVerifier::with_api_key(&livekit_api_key, &livekit_api_secret); // (1)!
    let webhook_receiver = WebhookReceiver::new(token_verifier); // (2)!

    let auth_header = match headers.get("Authorization") { // (3)!
        Some(header_value) => match header_value.to_str() {
            Ok(header_str) => header_str,
            Err(_) => {
                return (
                    StatusCode::BAD_REQUEST,
                    "Invalid Authorization header format".to_string(),
                );
            }
        },
        None => {
            return (
                StatusCode::BAD_REQUEST,
                "Authorization header is required".to_string(),
            );
        }
    };

    match webhook_receiver.receive(&body, auth_header) { // (4)!
        Ok(event) => {
            println!("LiveKit WebHook: {:?}", event); // (5)!
            return (StatusCode::OK, "ok".to_string());
        }
        Err(_) => {
            return (
                StatusCode::UNAUTHORIZED,
                "Error validating webhook event".to_string(),
            );
        }
    }
}
```

1. Create a `TokenVerifier` with the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. This will validate the webhook event to confirm it is actually coming from our LiveKit Server.
1. Create a `WebhookReceiver` with the `TokenVerifier`.
1. Get the `Authorization` header from the HTTP request.
1. Obtain the webhook event using the `WebhookReceiver#receive` method. It expects the raw string body of the request and the `Authorization` header.
1. Consume the event as you wish.

We declare as function parameters the map of headers (`headers: HeaderMap`) and the raw body (`body: String`) of the HTTP request. We will need both of them to validate and decode the incoming webhook event. We then:

1. Create a `TokenVerifier` with the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. This will validate the webhook event to confirm it is actually coming from our LiveKit Server.
1. Create a `WebhookReceiver` with the `TokenVerifier`.
1. Get the `Authorization` header from the HTTP request.
1. Obtain the webhook event using the `WebhookReceiver#receive` method. It expects the raw string body of the request and the `Authorization` header.
1. Consume the event as you wish (in this case, we just log it).

Remember to return a `200` OK response at the end to let LiveKit Server know that the webhook was received correctly.

Configure Webhooks

If you are using a [production deployment](#deploy-openvidu), remember to configure the webhook URL to point to your local application server as explained in the [Send Webhooks to a Local Application Server](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/enable-webhooks/#send-webhooks-to-a-local-application-server) section.
