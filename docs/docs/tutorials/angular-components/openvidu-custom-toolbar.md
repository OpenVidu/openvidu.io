# openvidu-custom-toolbar

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-tutorials/tree/master/openvidu-components-angular/openvidu-custom-toolbar){ .md-button target=\_blank }

The **openvidu-custom-toolbar** tutorial demonstrates how to replace the default toolbar with a custom one, providing a more tailored user experience.

Customizing the toolbar is made simple with the **ToolbarDirective**, which offers a straightforward way to replace and adapt the **ToolbarComponent** to your needs.


<figure markdown>
  ![OpenVidu Components Angular](../../../assets/images/components/openvidu-components-toolbar.svg){ loading=lazy .svg-img  .mkdocs-img}
  <figcaption>OpenVidu Components - Custom Toolbar</figcaption>
</figure>

## Running this tutorial

#### 1. Run OpenVidu Server

--8<-- "docs/docs/tutorials/shared/run-openvidu-server.md"

#### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
git clone https://github.com/OpenVidu/openvidu-tutorials.git
```

#### 3. Run the server application

--8<-- "docs/docs/tutorials/shared/run-application-server.md"

#### 4. Run the openvidu-custom-toolbar tutorial

To run the client application tutorial, you need [Node](https://nodejs.org/en/download){:target="\_blank"} installed on your development computer.

1.  Navigate into the application client directory:

    ```bash
      cd openvidu-tutorials/openvidu-components/openvidu-custom-toolbar
    ```

2.  Install the required dependencies:

    ```bash
      npm install
    ```

3.  Serve the application:

    ```bash
      npm start
    ```

Once the server is up and running, you can test the application by visiting [`http://localhost:5080`](http://localhost:5080){:target="\_blank"}.

<!-- ![OpenVidu Angular Components - Custom Toolbar](../../../assets/images/components/custom-toolbar.png){ loading=lazy } -->

--8<-- "docs/docs/tutorials/shared/testing-other-devices.md"

## Understanding the code


--8<-- "docs/docs/tutorials/shared/openvidu-components-files.md"

---


--8<-- "docs/docs/tutorials/shared/openvidu-components-install.md"

=== "main.ts"

    --8<-- "docs/docs/tutorials/shared/openvidu-components-import.md"

=== "app.component.ts"

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
    2. `LIVEKIT_URL`: URL to communicate the client application with the LiveKit server.
    3. `roomName`: OpenVidu Room identifier. This is the room where the VideoconferenceComponent will connect.
    4. `token`: OpenVidu Token used to connect to the OpenVidu Room.
    5. `onTokenRequested` method that fires when the VideoconferenceComponent requests a token to connect to the OpenVidu Room.
    6. `toggleVideo` method that toggles the camera on and off.
    7. `toggleAudio` method that toggles the microphone on and off.
    8. `getToken` method that requests a token to the server application.

    The `app.component.ts` file declares the following properties and methods:

    - `APPLICATION_SERVER_URL`: URL to communicate the client application with the server application to request OpenVidu tokens.
    - `LIVEKIT_URL`: URL to communicate the client application with the LiveKit server.
    - `roomName`: OpenVidu Room identifier. This is the room where the VideoconferenceComponent will connect.
    - `token`: OpenVidu Token used to connect to the OpenVidu Room.
    - `onTokenRequested` method that fires when the VideoconferenceComponent requests a token to connect to the OpenVidu Room.
    - `toggleVideo` method that toggles the camera on and off.
    - `toggleAudio` method that toggles the microphone on and off.
    - `getToken` method that requests a token to the server application.

    --8<-- "docs/docs/tutorials/shared/configure-urls.md"

=== "styles.scss"

    --8<-- "docs/docs/tutorials/shared/openvidu-components-styles.md"


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

<!-- ## Deploying openvidu-custom-toolbar

#### 1) Build the docker image

Under the root project folder, you can see the `openvidu-components/docker/` directory. Here it is included all the required files yo make it possible the deployment with OpenVidu.

First of all, you will need to create the **openvidu-custom-toolbar** docker image. Under `openvidu-components/docker/` directory you will find the `create_image.sh` script. This script will create the docker image with the [openvidu-basic-node](application-server/openvidu-basic-node/) as application server and the static files.

```bash
./create_image.sh openvidu/openvidu-custom-toolbar-demo:X.Y.Z openvidu-custom-toolbar
```

The script needs two parameters:

1. The name of the docker image to create.
2. The name of the tutorial folder.

This script will create an image named `openvidu/openvidu-custom-toolbar-demo:X.Y.Z`. This name will be used in the next step.

#### 2) Deploy the docker image

Time to deploy the docker image. You can follow the [Deploy OpenVidu based application with Docker](/deployment/deploying-openvidu-apps/#with-docker) guide for doing this. -->
