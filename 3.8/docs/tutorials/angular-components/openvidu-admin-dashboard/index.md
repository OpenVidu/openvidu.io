# Create admin dashboard using Angular Components

[Source code](https://github.com/OpenVidu/openvidu-tutorials/tree/3.8.0/openvidu-components-angular/openvidu-admin-dashboard)

The **openvidu-admin-dashboard** tutorial demonstrates how to create an admin dashboard to manage the recordings of a videoconference using the OpenVidu Components Angular library.

OpenVidu Components Angular

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

#### 4. Run the openvidu-admin-dashboard tutorial

To run the client application tutorial, you need [Node.js](https://nodejs.org/en/download) installed on your development computer.

1. Navigate into the application client directory:

   ```bash
     cd openvidu-tutorials/openvidu-components-angular/openvidu-admin-dashboard
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

Use the `ov-admin-login` component to create a login form and the `ov-admin-dashboard` component to create the admin dashboard.

```typescript
import { OpenViduComponentsModule } from 'openvidu-components-angular';

@Component({
  selector: 'app-root',
  template:`
    @if (logged) {
    <ov-admin-dashboard
      [recordingsList]="recordings()"
      (onLogoutRequested)="onLogoutRequested()"
      (onRefreshRecordingsRequested)="onRefreshRecordingsRequested()"
      (onLoadMoreRecordingsRequested)="onLoadMoreRecordingsRequested()"
      (onRecordingDeleteRequested)="onRecordingDeleteRequested($event)"
    ></ov-admin-dashboard>
    } @else {
    <ov-admin-login (onLoginRequested)="onLoginRequested($event)">
    </ov-admin-login>
    }
  `,
  styles: [''],
  standalone: true,
  imports: [OpenViduComponentsModule],
})
export class AppComponent {

  roomName = 'openvidu-admin-dashboard'; // (1)!

  logged: boolean = false; // (2)!

  // Recordings list to show in the dashboard
  // This is a dummy list, you should replace it with your own list from the server
  recordings: WritableSignal<RecordingInfo[]> = signal([ // (3)!
    {
      id: 'recording1',
      roomName: this.roomName,
      roomId: 'roomId1',
      outputMode: RecordingOutputMode.COMPOSED,
      status: RecordingStatus.READY,
      filename: 'sampleRecording.mp4',
      startedAt: new Date().getTime(),
      endedAt: new Date().getTime(),
      duration: 0,
      size: 100,
      location: 'http://localhost:8080/recordings/recording1',
    }
  ]);

  constructor() 

  onLoginRequested(credentials: { username: string; password: string }) { // (4)!
    console.log(`Login button clicked ${credentials}`);
    /**
     * WARNING! This code is developed for didactic purposes only.
     * The authentication process should be done in the server side.
     **/
    this.logged = true;
  }

  onLogoutRequested() { // (5)!
    console.log('Logout button clicked');
    /**
     * WARNING! This code is developed for didactic purposes only.
     * The authentication process should be done in the server side.
     **/
    this.logged = false;
  }

  onRefreshRecordingsRequested() { // (6)!
    console.log('Refresh recording clicked');
    /**
     * WARNING! This code is developed for didactic purposes only.
     * The authentication process should be done in the server side.
     **/
    // Getting the recordings from the server
    this.recordings.update(() => [
      {
        id: 'recording1',
        roomName: this.title,
        roomId: 'roomId1',
        outputMode: RecordingOutputMode.COMPOSED,
        status: RecordingStatus.READY,
        filename: 'sampleRecording1.mp4',
        startedAt: new Date().getTime(),
        endedAt: new Date().getTime(),
        duration: 0,
        size: 100,
        location: 'http://localhost:8080/recordings/recording1',
      },
    ]);
  }

  onLoadMoreRecordingsRequested() { // (7)!
    console.log('Load more recordings clicked');
  }

  onRecordingDeleteRequested(recording: RecordingDeleteRequestedEvent) { // (8)!
    console.log(`Delete recording clicked ${recording.recordingId}`);
    /**
     * WARNING! This code is developed for didactic purposes only.
     * The authentication process should be done in the server side.
     **/
    // Deleting the recording from the server
    this.recordings.update((recordings) =>
      recordings.filter((rec) => rec.id !== recording.recordingId)
    );

    console.log(this.recordings());
  }
}
```

1. `roomName`: OpenVidu Room name.
1. `logged`: Boolean that indicates if the user is logged in.
1. `recordings`: Dummy list of recordings to show in the dashboard. You should replace it with your own list from the server from the server.
1. `onLoginRequested` method that fires when the login button is clicked.
1. `onLogoutRequested` method that fires when the logout button is clicked.
1. `onRefreshRecordingsRequested` method that fires when the refresh recordings button is clicked.
1. `onLoadMoreRecordingsRequested` method that fires when the load more recordings button is clicked.
1. `onRecordingDeleteRequested` method that fires when the delete recording button is clicked.

The `app.component.ts` file declares the following properties and methods:

- `roomName`: OpenVidu Room name.
- `logged`: Boolean that indicates if the user is logged in.
- `recordings`: Dummy list of recordings to show in the dashboard. You should replace it with your own list from the server from the server.
- `onLoginRequested` method that fires when the login button is clicked.
- `onLogoutRequested` method that fires when the logout button is clicked.
- `onRefreshRecordingsRequested` method that fires when the refresh recordings button is clicked.
- `onLoadMoreRecordingsRequested` method that fires when the load more recordings button is clicked.
- `onRecordingDeleteRequested` method that fires when the delete recording button is clicked.

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
