# openvidu-ios

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-client/openvidu-ios){ .md-button target=\_blank }

This tutorial is a simple video-call application built for **iOS**, using **Swift**, that allows:

- Joining a video call room by requesting a token from any [application server](../application-server/index.md).
- Publishing your camera and microphone.
- Subscribing to all other participants' video and audio tracks automatically.
- Leaving the video call room at any time.

It uses the [LiveKit Swift SDK](https://docs.livekit.io/client-sdk-swift/documentation/livekit/){:target="\_blank"} to connect to the LiveKit server and interact with the video call room.

## Running this tutorial

### 1. Run OpenVidu Server

--8<-- "docs/docs/tutorials/shared/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b v3.0.0-beta3
```

### 3. Run a server application

--8<-- "docs/docs/tutorials/shared/application-server-tabs.md"

### 4. Run the client application

To run the client application tutorial, you need [Xcode](https://apps.apple.com/es/app/xcode/id497799835?mt=12){:target="\_blank"} installed on your MacOS.

1. Launch Xcode and open the `OpenViduIOS.xcodeproj` that you can find under `openvidu-livekit-tutorials/application-client/openvidu-ios`.

2. Run the application in an emulator or a physical device by clicking on the menu Product > Run or by ⌘R.

!!! warning "Emulator limitations"
    Publishing the camera track is not supported by iOS Simulator.

If you encounter code signing issues, make sure you change the **Team** and **bundle id** from the previous step.

The application will initiate as a native iOS application. Once the app is opened, you should see a screen like this:

<div class="grid-container">

<div class="grid-100"><p style="text-align: center;"><a class="glightbox" href="/assets/images/application-clients/configure-urls-ios.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/configure-urls-ios.png" loading="lazy" style="width: 25%;"/></a></p></div>

</div>

This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

!!! info "Connecting real iOS device to application server running in you local network"

    One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client in a real iOS device and be able to reach the application server very easily without worrying about SSL certificates if they are both running in the same local network. For more information, see section [Accessing your app from other devices in your network](/openvidu-vs-livekit/#accessing-your-app-from-other-devices-in-your-network){target="_blank"}.

Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

<div class="grid-container">

<div class="grid-50"><p style="text-align: center;"><a class="glightbox" href="/assets/images/application-clients/join-ios.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/join-ios.png" loading="lazy" style="width: 50%;"/></a></p></div>

<div class="grid-50"><p style="text-align: center;"><a class="glightbox" href="/assets/images/application-clients/room-ios.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/room-ios.png" loading="lazy" style="width: 50%;"/></a></p></div>

</div>

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
2. Add LiveKit to the `dependencies` array.
3. Include LiveKit in the `targets` array.

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
2. Go to **Project Settings**.
3. Select the **Swift Packages** tab.
4. Click the **+** button to add a new package.
5. Enter the URL: `https://github.com/livekit/client-sdk-swift`.
6. Choose the version you want, such as "Up to Next Major Version" with `2.0.12`.


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

2. **Automatic Permission Requests**

    The app will automatically request these permissions when it runs.

3. **Check Permissions**

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

You should configure these URLs according to your deployment settings. If you are [running OpenVidu locally](#run-openvidu-locally), you can set `applicationServerUrl` to [`https://xxx-yyy-zzz-www.openvidu-local.dev:6443`](https://xxx-yyy-zzz-www.openvidu-local.dev:6443) and `livekitUrl` to [`wss://xxx-yyy-zzz-www.openvidu-local.dev:7443`](wss://xxx-yyy-zzz-www.openvidu-local.dev:7443), where `xxx-yyy-zzz-www` represents the LAN private IP address of the machine running OpenVidu, with dashes (-) instead of dots (.).

If these URLs are left empty, the user will be prompted to enter them when the application starts. This configuration is managed in the `ConfigureUrlsView.swift` file:

<div class="grid-container">

<div class="grid-100"><p style="text-align: center;"><a class="glightbox" href="/assets/images/application-clients/configure-urls-ios.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/configure-urls-ios.png" loading="lazy" style="width: 25%;"/></a></p></div>

</div>

When the user clicks the `Save` button, the `LKButton` action triggers the validation and saves the URLs into the `AppContext` and `RoomContext`. The `ConfigureUrlsView` handles this logic:

```swift title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ios/Shared/Views/ConfigureUrlsView.swift#L50-L64' target='_blank'>ConfigureUrlsView.swift</a>" linenums="28"
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

---


### Joining a room

Before joining a room, the `ConnectView.swift` defines the view for the connection screen. It includes a logo, text fields for participant name and room name, and buttons for joining the room and resetting URLs.

<div class="grid-container">

<div class="grid-100"><p style="text-align: center;"><a class="glightbox" href="/assets/images/application-clients/join-ios.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/application-clients/join-ios.png" loading="lazy" style="width: 25%;"/></a></p></div>

</div>

After define the participant and room name, the user can click the `Join` button to connect to the room. This action triggers the `connectToRoom` method asynchronously:

```swift title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/82d64332150b5c4204ba0d065d40c411175dee51/application-client/openvidu-ios/Shared/Views/ConnectView.swift#L96-L123' target='_blank'>ConnectView.swift</a>" linenums="96"
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
2. The `connect` method is called to connect to the room using the LiveKit URL and the token.
3. The `enableCameraAndMicrophone` method is called to enable the camera and microphone for the local participant.
4. The `setCamera` method is called to enable the camera for the local participant.
5. The `setMicrophone` method is called to enable the microphone for the local participant.

The `OpenViduApp.swift` handle the navigation page. When room status is `connected`, the user is redirected to the `RoomView`:

```swift title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ios/Shared/OpenViduApp.swift' target='_blank'>OpenViduApp.swift</a>"
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
2. If the URLs are not configured, the user is redirected to the `ConfigureUrlsView`.
3. If the room is not connected and the URLs are configured, the user is redirected to the `ConnectView`.

---


### Displaying Video Tracks

To display the video tracks of participants in the room, the `RoomView.swift` uses various SwiftUI views and custom components. This approach allows the application to dynamically load and display the video tracks as they are received.


```swift title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ios/Shared/Views/RoomView.swift' target='_blank'>RoomView.swift</a>"
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
2. The `ParticipantView` component is used to display the video track of a participant.

The `ParticipantView` component is responsible for rendering the video track of a participant. It uses the `SwiftUIVideoView` component to display the video track and the `VideoView.LayoutMode` enum to define the layout mode.

The **LiveKit Swift SDK** includes a VideoView class, based on UIKit, specifically designed for rendering video tracks. Additionally, subscribed audio tracks are automatically played by default.

```swift title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-ios/Shared/Views/ParticipantView.swift' target='_blank'>ParticipantView.swift</a>"
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


---

### Leaving the room

To leave the room, the user can click the `Leave` button in the `RoomView`. This action triggers the `leaveRoom` method asynchronously:


```swift title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/55d303d7b5f57edcaadd5d7864734fe6fa062067/application-client/openvidu-ios/Shared/Views/RoomView.swift#L111-L127' target='_blank'>RoomView.swift</a>" linenums="111"
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

