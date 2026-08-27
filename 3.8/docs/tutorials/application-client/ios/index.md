# iOS Tutorial

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.8.0/application-client/openvidu-ios)

This tutorial is a simple video-call application built for **iOS**, using **Swift**, that allows:

- Joining a video call room by requesting a token from any [application server](https://openvidu.io/3.8/docs/tutorials/application-server/index.md).
- Publishing your camera and microphone.
- Subscribing to all other participants' video and audio tracks automatically.
- Leaving the video call room at any time.

It uses the [LiveKit Swift SDK](https://docs.livekit.io/client-sdk-swift/documentation/livekit/) to connect to the LiveKit server and interact with the video call room.

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

For more information, check the [Node.js tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/node/index.md) .

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

For more information, check the [Go tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/go/index.md) .

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

For more information, check the [Ruby tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/ruby/index.md) .

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

For more information, check the [Java tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/java/index.md) .

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

For more information, check the [Python tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/python/index.md) .

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

For more information, check the [Rust tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/rust/index.md) .

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

For more information, check the [PHP tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/php/index.md) .

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

This .NET server application needs the `LIVEKIT_API_SECRET` env variable to be at least 32 characters long. Make sure to update it [here](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/application-server/dotnet/appsettings.json#L11) and in your [OpenVidu Server](#1-run-openvidu-server).

For more information, check the [.NET tutorial](https://openvidu.io/3.8/docs/tutorials/application-server/dotnet/index.md) .

### 4. Run the client application

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

## Understanding the Code

This iOS project, created with Xcode and written in Swift, includes various files and directories. For this tutorial, focus on the following key components within the `openvidu-ios/Shared` directory:

- `OpenViduApp.swift`: Initializes the application and sets up the main view.
- `Support`: Contains files for secure storage, token management, and other support functions.
- `Utils`: Includes utility files like `HttpClient.swift` for HTTP networking.
- `Views`: Houses the user interface components of the application.
- `Contexts`: Manages application state and room contexts for LiveKit interaction.
- `Assets.xcassets`: Stores images and color assets used in the app.

### Integrating LiveKit

To use LiveKit in your iOS app, you need to add the [LiveKit Swift SDK](https://github.com/livekit/client-sdk-swift) as a Swift Package. You can do this using either `Package.swift` or Xcode.

#### Adding LiveKit via `Package.swift`

1. Open your `Package.swift` file.
1. Add LiveKit to the `dependencies` array.
1. Include LiveKit in the `targets` array.

Example `Package.swift`:

```swift
// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [.iOS(.v14)],
    dependencies: [
        .package(name: "LiveKit", url: "https://github.com/livekit/client-sdk-swift.git", .upToNextMajor(from: "2.0.12"))
    ],
    targets: [
        .target(
            name: "MyApp",
            dependencies: ["LiveKit"]
        )
    ]
)
```

#### Adding LiveKit via Xcode

1. Open your Xcode project.
1. Go to **Project Settings**.
1. Select the **Swift Packages** tab.
1. Click the **+** button to add a new package.
1. Enter the URL: `https://github.com/livekit/client-sdk-swift`.
1. Choose the version you want, such as "Up to Next Major Version" with `2.0.12`.

### iOS Specific Requirements

To test the application on an iOS device, you need to ensure it has permission to access the camera and microphone. These configurations are already included in this project. However, if you're starting a new project, follow these steps:

1. **Add Permissions to `Info.plist`**

   Include the following keys in your `Info.plist` file to request access to the camera and microphone:

   ```xml
   <key>NSCameraUsageDescription</key>
   <string>$(PRODUCT_NAME) needs camera access to capture and transmit video</string>
   <key>NSMicrophoneUsageDescription</key>
   <string>$(PRODUCT_NAME) needs microphone access to capture and transmit audio</string>
   ```

1. **Automatic Permission Requests**

   The app will automatically request these permissions when it runs.

1. **Check Permissions**

   To verify if the permissions were granted, use the `AVCaptureDevice.requestAccess(for: .video)` method:

   ```swift
   AVCaptureDevice.requestAccess(for: .video) { granted in
       if granted {
           print("Camera access granted")
       } else {
           print("Camera access denied")
       }
   }
   ```

### Configuring URLs

The `ConfigureUrlsView.swift` file defines a SwiftUI view for configuring the URLs required for the application:

- **`applicationServerUrl`**: The URL of the application server used to obtain tokens for joining the video call room.
- **`livekitUrl`**: The URL of the LiveKit server used to connect to the video call room and handle video communication.

You should configure these URLs according to your deployment settings. If you are [running OpenVidu locally](#run-openvidu-locally), you can set `applicationServerUrl` to `https://xxx-yyy-zzz-www.openvidu-local.dev:6443` and `livekitUrl` to `wss://xxx-yyy-zzz-www.openvidu-local.dev:7443`, where `xxx-yyy-zzz-www` represents the LAN private IP address of the machine running OpenVidu, with dashes (-) instead of dots (.).

If these URLs are left empty, the user will be prompted to enter them when the application starts. This configuration is managed in the `ConfigureUrlsView.swift` file:

URL configuration of the iOS tutorial app

When the user clicks the `Save` button, the `LKButton` action triggers the validation and saves the URLs into the `AppContext` and `RoomContext`. The `ConfigureUrlsView` handles this logic:

```swift
LKButton(title: "Save") {
    Task.detached { @MainActor in
        let isApplicationServerValid = isValidURL(self.applicationServerUrl)
        let isLivekitUrlValid = isValidURL(self.livekitUrl)

        if !isApplicationServerValid || !isLivekitUrlValid {
            print("Invalid URLs")
            errorMessage = "There was an error with the URL values"
            return
        }
        appCtx.applicationServerUrl = self.applicationServerUrl
        roomCtx.livekitUrl = self.livekitUrl
        errorMessage = ""
    }
}
```

In this code snippet, the `isValidURL` function checks the validity of the URLs. If both URLs are valid, they are saved into the `appCtx` and `roomCtx` contexts. If any URL is invalid, an error message is displayed.

______________________________________________________________________

### Joining a room

Before joining a room, the `ConnectView.swift` defines the view for the connection screen. It includes a logo, text fields for participant name and room name, and buttons for joining the room and resetting URLs.

Join screen of the iOS tutorial app

After define the participant and room name, the user can click the `Join` button to connect to the room. This action triggers the `connectToRoom` method asynchronously:

```swift
func connectToRoom() async {
    let livekitUrl = roomCtx.livekitUrl
    let roomName = roomCtx.name
    let participantName = roomCtx.localParticipantName
    let applicationServerUrl = appCtx.applicationServerUrl

    guard !livekitUrl.isEmpty, !roomName.isEmpty else {
        print("LiveKit URL or room name is empty")
        return
    }

    do {
        let token = try await httpService.getToken(
            applicationServerUrl: applicationServerUrl, roomName: roomName,
            participantName: participantName)// (1)!

        if token.isEmpty {
            print("Received empty token")
            return
        }

        roomCtx.token = token
        print("Connecting to room...")
        try await roomCtx.connect() // (2)!
        print("Room connected")
        await enableCameraAndMicrophone() // (3)!

    } catch {
        print("Failed to get token: \(error.localizedDescription)")
    }
}

func enableCameraAndMicrophone() async {
    do {
        try await room.localParticipant.setCamera(enabled: true) // (4)!
        try await room.localParticipant.setMicrophone(enabled: true) // (5)!
    } catch {
        print("Error enabling camera and microphone: \(error.localizedDescription)")
    }
}
```

1. The `getToken` method is called to request a token from the application server.
1. The `connect` method is called to connect to the room using the LiveKit URL and the token.
1. The `enableCameraAndMicrophone` method is called to enable the camera and microphone for the local participant.
1. The `setCamera` method is called to enable the camera for the local participant.
1. The `setMicrophone` method is called to enable the microphone for the local participant.

The `OpenViduApp.swift` handle the navigation page. When room status is `connected`, the user is redirected to the `RoomView`:

[OpenViduApp.swift](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/application-client/openvidu-ios/Shared/OpenViduApp.swift)

```swift
struct RoomSwitchView: View {
    @EnvironmentObject var appCtx: AppContext
    @EnvironmentObject var roomCtx: RoomContext
    @EnvironmentObject var room: Room

    var shouldShowRoomView: Bool {
        room.connectionState == .connected || room.connectionState == .reconnecting
    }

    var shouldShowConfigureUrlsView: Bool {
        appCtx.applicationServerUrl.isEmpty || roomCtx.livekitUrl.isEmpty

    }

    var body: some View {
        ZStack {
            Color.black
                .ignoresSafeArea()

            // Navigation logic
            if shouldShowRoomView {
                RoomView() // (1)!
            } else {
                if shouldShowConfigureUrlsView {
                    ConfigureUrlsView() // (2)!
                } else {
                    ConnectView() // (3)!
                }
            }
        }
        .navigationTitle(computeTitle())
    }
}
```

1. If the room is connected, the user is redirected to the `RoomView`.
1. If the URLs are not configured, the user is redirected to the `ConfigureUrlsView`.
1. If the room is not connected and the URLs are configured, the user is redirected to the `ConnectView`.

______________________________________________________________________

### Displaying Video Tracks

To display the video tracks of participants in the room, the `RoomView.swift` uses various SwiftUI views and custom components. This approach allows the application to dynamically load and display the video tracks as they are received.

[RoomView.swift](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/application-client/openvidu-ios/Shared/Views/RoomView.swift)

```swift
struct RoomView: View {
    @EnvironmentObject var appCtx: AppContext
    @EnvironmentObject var roomCtx: RoomContext
    @EnvironmentObject var room: Room

    @State var isCameraPublishingBusy = false
    @State var isMicrophonePublishingBusy = false

    // ...

    func content(geometry: GeometryProxy) -> some View {
        VStack {
            // ...

            // Display Participant layout
            HorVStack(axis: geometry.isTall ? .vertical : .horizontal, spacing: 5) {
                Group {
                    ParticipantLayout(sortedParticipants(), spacing: 5) { participant in // (1)!
                        ParticipantView(participant: participant, videoViewMode: .fill) // (2)!
                    }
                }
                .frame(
                    minWidth: 0,
                    maxWidth: .infinity,
                    minHeight: 0,
                    maxHeight: .infinity
                )
            }
            .padding(5)
        }
    }
}
```

1. The `ParticipantLayout` component is used to display the video tracks of all participants in the room. It receives the sorted list of participants and a closure that returns a `ParticipantView` for each participant.
1. The `ParticipantView` component is used to display the video track of a participant.

The `ParticipantView` component is responsible for rendering the video track of a participant. It uses the `SwiftUIVideoView` component to display the video track and the `VideoView.LayoutMode` enum to define the layout mode.

The **LiveKit Swift SDK** includes a VideoView class, based on UIKit, specifically designed for rendering video tracks. Additionally, subscribed audio tracks are automatically played by default.

[ParticipantView.swift](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.8.0/application-client/openvidu-ios/Shared/Views/ParticipantView.swift)

```swift
struct ParticipantView: View {
    @ObservedObject var participant: Participant
    @EnvironmentObject var appCtx: AppContext

    var videoViewMode: VideoView.LayoutMode = .fill


    // ...

     var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .bottom) {

                // ...

                // VideoView for the Participant
                if let publication = participant.mainVideoPublication,
                    !publication.isMuted,
                    let track = publication.track as? VideoTrack
                {
                    ZStack(alignment: .topLeading) {
                        SwiftUIVideoView(track, // (1)!
                                            layoutMode: videoViewMode,
                                            isRendering: $isRendering)
                    }
                }
            }
        }
     }

}
```

1. The `SwiftUIVideoView` component renders the participant's video track.

______________________________________________________________________

### Leaving the room

To leave the room, the user can click the `Leave` button in the `RoomView`. This action triggers the `leaveRoom` method asynchronously:

```swift
func content(geometry: GeometryProxy) -> some View {

    // ...

    Button(action: {
        Task {
            await roomCtx.disconnect()
        }
    }, label: {
        HStack {
            Image(systemSymbol: .xmarkCircleFill)
                .renderingMode(.original)
            Text("Leave Room")
                .font(.headline)
                .fontWeight(.semibold)
        }
        .padding(8)
        .background(Color.red.opacity(0.8)) // Background color for the button
        .foregroundColor(.white) // Text color
        .cornerRadius(8)
    })
}
```

After rome is disconnected, the room status is updated to `disconnected` and the `OpenViduApp.swift` handle this update to redirect the user to the `ConnectView`.
