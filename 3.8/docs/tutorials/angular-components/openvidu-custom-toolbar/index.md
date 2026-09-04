# Custom toolbar using Angular Components

[Source code](https://github.com/OpenVidu/openvidu-tutorials/tree/3.8.0/openvidu-components-angular/openvidu-custom-toolbar)

The **openvidu-custom-toolbar** tutorial demonstrates how to replace the default toolbar with a custom one, providing a more tailored user experience.

Customizing the toolbar is made simple with the **ToolbarDirective**, which offers a straightforward way to replace and adapt the **ToolbarComponent** to your needs.

OpenVidu Components Angular

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

To use a production-ready OpenVidu deployment, visit the official [deployment guide](https://openvidu.io/3.8/docs/self-hosting/deployment-types/index.md).

Configure Webhooks

All [application servers](https://openvidu.io/3.8/docs/tutorials/application-server/index.md) have an endpoint to receive webhooks from OpenVidu. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/enable-webhooks/#send-webhooks-to-a-local-application-server) section for more information.

#### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.8.0
git clone https://github.com/OpenVidu/openvidu-tutorials.git -b 3.8.0
```

#### 3. Run a server application

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

To run this server application, you need [Rust](https://rust-lang.org/tools/install/) installed on your device.

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

#### 4. Run the openvidu-custom-toolbar tutorial

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
     cd openvidu-tutorials/openvidu-components/openvidu-custom-toolbar
   ```

1. Install the required dependencies:

   ```bash
     npm install
   ```

1. Serve the application:

   ```bash
     npm start
   ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080).

Accessing your application client from other devices in your local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client with other devices in your local network very easily without worrying about SSL certificates.

Access your application client through `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`, where `xxx-yyy-zzz-www` part of the domain is your LAN private IP address with dashes (-) instead of dots (.). For more information, see section [Accessing your local deployment from other devices on your network](https://openvidu.io/3.8/docs/self-hosting/local/#accessing-your-local-deployment-from-other-devices-on-your-network) .

## Understanding the code

This tutorial is an Angular project generated with Angular CLI tool. Therefore, you will see many configuration files and other components that are not the primary focus of this tutorial. We will concentrate on the following files in the `src` directory:

- `main.ts`: This file defines the root application component. It imports the `OpenViduComponentsModule`, where we configure the [OpenVidu Components Angular](https://openvidu.io/3.8/docs/reference-docs/openvidu-components-angular/index.md) library.
- `app/app.component.ts`: This file defines the **AppComponent**, the primary and sole component of the application. It is responsible for requesting the OpenVidu token and passing it to the videoconference component, facilitating the connection to the OpenVidu Room.
- `styles.scss`: This file defines the global styles of the application. Here, you can customize the UI of the OpenVidu Components Angular library.

______________________________________________________________________

To use OpenVidu Components Angular in your application, you need to install the library and import the `OpenViduComponentsModule` in your Angular module. Let's see how to do this:

1. Create an Angular Project (version 17 or higher)

   To begin, you will need to create a new Angular project if you haven't already. Ensure you have Node.js and the Angular CLI installed. Then, run the following command to create a new Angular project:

   ```bash
   ng new your-project-name
   ```

   Replace `your-project-name` with the desired name for your project.

1. Add Angular Material to your project

   OpenVidu Components Angular needs Angular Material, which provides a range of UI components. To add Angular Material to your project, navigate to your project directory and run:

   ```bash
   ng add @angular/material
   ```

1. Install OpenVidu Components Angular

   With your Angular project set up, it's time to add videoconferencing capabilities with OpenVidu Components Angular. Install the library using npm:

   ```bash
   npm install openvidu-components-angular
   ```

1. Import and use OpenVidu Components Angular

   To use OpenVidu Components Angular in your application, you need to:

   1. Import the `OpenViduComponentsModule` in your Angular application.
   1. Configure the module with the `OpenViduComponentsConfig` object.
   1. Add the component to your template file.
   1. Assign the OpenVidu token and LiveKit URL to the component.
   1. Customize the appearance of the components using CSS variables.

**main.ts**

In your `main.ts` application file, import the it and configure it as follows:

```typescript
// Other imports ...

import { OpenViduComponentsModule, OpenViduComponentsConfig } from 'openvidu-components-angular';

const config: OpenViduComponentsConfig = {
    production: true,
};

bootstrapApplication(AppComponent, {
    providers: [
        importProvidersFrom(
            OpenViduComponentsModule.forRoot(config)
            // Other imports ...
        ),
        provideAnimations(),
    ],
}).catch((err) => console.error(err));
```

**app.component.ts**

Use the `ov-videoconference` component to create a videoconference. This component requires a token to connect to the OpenVidu Room. The `AppComponent` class is responsible for requesting the token and passing it to the `ov-videoconference` component.

```typescript
import { OpenViduComponentsModule, ParticipantService } from 'openvidu-components-angular';

@Component({
  selector: 'app-root',
  template:`
    <ov-videoconference
      [token]="token"
      [livekitUrl]="LIVEKIT_URL"
      (onTokenRequested)="onTokenRequested($event)"
    >
      <div *ovToolbar style="text-align: center;">
        <button (click)="toggleVideo()">Toggle Video</button>
        <button (click)="toggleAudio()">Toggle Audio</button>
      </div>
    </ov-videoconference>
  `,
  styles: [''],
  standalone: true,
  imports: [OpenViduComponentsModule],
})
export class AppComponent {
  // For local development, leave these variables empty
  // For production, configure them with correct URLs depending on your deployment

  APPLICATION_SERVER_URL = '';  // (1)!
  LIVEKIT_URL = ''; // (2)!

  // The name of the room to join.
  roomName = 'openvidu-custom-toolbar';  // (3)!

  // The token used to join the room.
  token!: string; // (4)!

  constructor(private httpClient: HttpClient, private participantService: ParticipantService) {
    this.configureUrls();
  }

  private configureUrls() {
    // If APPLICATION_SERVER_URL is not configured, use default value from local development
    if (!this.APPLICATION_SERVER_URL) {
      if (window.location.hostname === 'localhost') {
        this.APPLICATION_SERVER_URL = 'http://localhost:6080/';
      } else {
        this.APPLICATION_SERVER_URL =
          'https://' + window.location.hostname + ':6443/';
      }
    }

    // If LIVEKIT_URL is not configured, use default value from local development
    if (!this.LIVEKIT_URL) {
      if (window.location.hostname === 'localhost') {
        this.LIVEKIT_URL = 'ws://localhost:7880/';
      } else {
        this.LIVEKIT_URL = 'wss://' + window.location.hostname + ':7443/';
      }
    }
  }

  // Requests a token to join the room with the given participant name.
  async onTokenRequested(participantName: string) { // (5)!
    const { token } = await this.getToken(this.roomName, participantName);
    this.token = token;
  }

  // Toggles the camera on and off.
  async toggleVideo() { // (6)!
    const isCameraEnabled = this.participantService.isMyCameraEnabled();
    await this.participantService.setCameraEnabled(!isCameraEnabled);
  }

  // Toggles the microphone on and off.
  async toggleAudio() { // (7)!
    const isMicrophoneEnabled = this.participantService.isMyMicrophoneEnabled();
    await this.participantService.setMicrophoneEnabled(!isMicrophoneEnabled);
  }

  // Retrieves a token to join the room with the given name and participant name.
  getToken(roomName: string, participantName: string): Promise<any> { // (8)!
    // Requesting token to the server application
  }
}
```

1. `APPLICATION_SERVER_URL`: URL to communicate the client application with the server application to request OpenVidu tokens.
1. `LIVEKIT_URL`: URL to communicate the client application with the LiveKit server.
1. `roomName`: OpenVidu Room identifier. This is the room where the VideoconferenceComponent will connect.
1. `token`: OpenVidu Token used to connect to the OpenVidu Room.
1. `onTokenRequested` method that fires when the VideoconferenceComponent requests a token to connect to the OpenVidu Room.
1. `toggleVideo` method that toggles the camera on and off.
1. `toggleAudio` method that toggles the microphone on and off.
1. `getToken` method that requests a token to the server application.

The `app.component.ts` file declares the following properties and methods:

- `APPLICATION_SERVER_URL`: URL to communicate the client application with the server application to request OpenVidu tokens.
- `LIVEKIT_URL`: URL to communicate the client application with the LiveKit server.
- `roomName`: OpenVidu Room identifier. This is the room where the VideoconferenceComponent will connect.
- `token`: OpenVidu Token used to connect to the OpenVidu Room.
- `onTokenRequested` method that fires when the VideoconferenceComponent requests a token to connect to the OpenVidu Room.
- `toggleVideo` method that toggles the camera on and off.
- `toggleAudio` method that toggles the microphone on and off.
- `getToken` method that requests a token to the server application.

Configure the URLs

When [running OpenVidu locally](#run-openvidu-locally), leave `APPLICATION_SERVER_URL` and `LIVEKIT_URL` variables empty. The function `configureUrls()` will automatically configure them with default values. However, for other deployment type, you should configure these variables with the correct URLs depending on your deployment.

**styles.scss**

The OpenVidu Components Angular library provides a set of CSS variables that you can use to customize the appearance of the components. You can define these variables in your application's global styles file (e.g. `styles.scss`).

```css
:root {
    /* Basic colors */
    --ov-background-color: #303030; // Background color
    --ov-surface-color: #ffffff; // Surfaces colors (panels, dialogs)

    /* Text colors */
    --ov-text-primary-color: #ffffff; // Text color over primary background
    --ov-text-surface-color: #1d1d1d; // Text color over surface background

    /* Action colors */
    --ov-primary-action-color: #273235; // Primary color for buttons, etc.
    --ov-secondary-action-color: #f1f1f1; // Secondary color for buttons, etc.
    --ov-accent-action-color: #0089ab; // Color for highlighted elements

    /* Status colors */
    --ov-error-color: #eb5144; // Error color
    --ov-warn-color: #ffba53; // Warning color

    /* Radius */
    --ov-toolbar-buttons-radius: 50%; // Radius for toolbar buttons
    --ov-leave-button-radius: 10px; // Radius for leave button
    --ov-video-radius: 5px; // Radius for videos
    --ov-surface-radius: 5px; // Radius for surfaces
}
```

### Customizing the toolbar

The `*ov-toolbar` directive allows you to replace the default toolbar with a custom one. This directive is applied to a `div` element that contains the custom toolbar elements.

In the `app.component.ts` file, you can see the following code snippet:

```typescript
@Component({
  selector: 'app-root',
  template:`
    <ov-videoconference
      [token]="token"
      [livekitUrl]="LIVEKIT_URL"
      (onTokenRequested)="onTokenRequested($event)"
    >
      <div *ovToolbar style="text-align: center;">
        <button (click)="toggleVideo()">Toggle Video</button>
        <button (click)="toggleAudio()">Toggle Audio</button>
      </div>

    </ov-videoconference>
  `,
  styles: [''],
  standalone: true,
  imports: [OpenViduComponentsModule],
})
export class AppComponent {
  // ...
}
```

In this code snippet, the `*ov-toolbar` directive is applied to a `div` element that contains two buttons. These buttons are used to toggle the camera and microphone on and off.
