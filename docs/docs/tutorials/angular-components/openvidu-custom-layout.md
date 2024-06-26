# openvidu-custom-layout

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-tutorials/tree/master/openvidu-components-angular/openvidu-custom-layout){ .md-button target=\_blank }

The **openvidu-custom-layout** tutorial demonstrates how to replace the default layout of the OpenVidu Components Angular library with a custom layout.

Replacing the default layout is made simple with the **LayoutDirective**, which offers a straightforward way to customize the **LayoutComponent**.

<figure markdown>
  ![OpenVidu Components Angular](../../../assets/images/components/openvidu-components-layout.svg){ loading=lazy .svg-img  .mkdocs-img}
  <figcaption>OpenVidu Components - Custom Layout</figcaption>
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

#### 4. Run the openvidu-custom-layout tutorial

To run the client application tutorial, you need [Node](https://nodejs.org/en/download){:target="\_blank"} installed on your development computer.

1.  Navigate into the application client directory:

    ```bash
      cd openvidu-tutorials/openvidu-components/openvidu-custom-layout
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
    import { OpenViduComponentsModule, ParticipantModel, ParticipantService } from 'openvidu-components-angular';

    @Component({
      selector: 'app-root',
      template:`
          <!-- OpenVidu Video Conference Component -->
          <ov-videoconference
            [token]="token"
            [livekitUrl]="LIVEKIT_URL"
            (onTokenRequested)="onTokenRequested($event)"
          >
            <!-- Custom Layout for Video Streams -->
            <div *ovLayout>
              <div class="container">
                <!-- Local Participant's Tracks -->
                @for (track of localParticipant.tracks; track track) {
                <div
                  class="item"
                  [ngClass]="{
                    hidden:
                      track.isAudioTrack && !track.participant.onlyHasAudioTracks
                  }"
                >
                  <ov-stream [track]="track"></ov-stream>
                </div>
                }

                <!-- Remote Participants' Tracks -->
                @for (track of remoteParticipants | tracks; track track) {
                <div
                  class="item"
                  [ngClass]="{
                    hidden:
                      track.isAudioTrack && !track.participant.onlyHasAudioTracks
                  }"
                >
                  <ov-stream [track]="track"></ov-stream>
                </div>
                }
              </div>
            </div>
          </ov-videoconference>
      `,
      styles: `
        /* css styles */
      `,
      standalone: true,
        imports: [OpenViduComponentsModule, NgClass],
    })
    export class AppComponent implements OnInit, OnDestroy {
      // For local development, leave these variables empty
      // For production, configure them with correct URLs depending on your deployment

      APPLICATION_SERVER_URL = '';  // (1)!
      LIVEKIT_URL = ''; // (2)!

      // The name of the room to join.
      roomName = 'openvidu-custom-layout';  // (3)!

      // The token used to join the room.
      token!: string; // (4)!

      // Participant-related properties
      localParticipant!: ParticipantModel; // (5)!
      remoteParticipants!: ParticipantModel[]; // (6)!
      localParticipantSubs!: Subscription; // (7)!
      remoteParticipantsSubs!: Subscription; // (8)!

      constructor(private httpClient: HttpClient,	private participantService: ParticipantService) {
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

      ngOnInit() {
        // Subscribe to participants' updates
        this.subscribeToParticipants();
      }

      ngOnDestroy() {
        // Unsubscribe from participant updates to prevent memory leaks
        this.localParticipantSubs?.unsubscribe();
        this.remoteParticipantsSubs?.unsubscribe();
      }

      // Requests a token to join the room with the given participant name.
      async onTokenRequested(participantName: string) { // (9)!
        const { token } = await this.getToken(this.roomName, participantName);
        this.token = token;
      }

      // Subscribe to updates for local and remote participants
      private subscribeToParticipants() { // (10)!
        this.localParticipantSubs = this.participantService.localParticipant$.subscribe((p) => {
          if (p) this.localParticipant = p;
        });

        this.remoteParticipantsSubs = this.participantService.remoteParticipants$.subscribe((participants) => {
          this.remoteParticipants = participants;
        });
      }

      // Retrieves a token to join the room with the given name and participant name.
      getToken(roomName: string, participantName: string): Promise<any> { // (11)!
        // Requesting token to the server application
      }
    }
    ```

    1. `APPLICATION_SERVER_URL`: URL to communicate the client application with the server application to request OpenVidu tokens.
    2. `LIVEKIT_URL`: URL to communicate the client application with the LiveKit server.
    3. `roomName`: OpenVidu Room identifier. This is the room where the VideoconferenceComponent will connect.
    4. `token`: OpenVidu Token used to connect to the OpenVidu Room.
    5. `localParticipant`: Local participant model.
    6. `remoteParticipants`: Remote participants model.
    7. `localParticipantSubs`: Subscription to the local participant updates.
    8. `remoteParticipantsSubs`: Subscription to the remote participants updates.
    9. `onTokenRequested` method that fires when the VideoconferenceComponent requests a token to connect to the OpenVidu Room.
    10. `subscribeToParticipants` method that subscribes to updates for local and remote participants.
    11. `getToken` method that requests a token to the server application.


    The `app.component.ts` file declares the following properties and methods:

    - `APPLICATION_SERVER_URL`: URL to communicate the client application with the server application to request OpenVidu tokens.
    - `LIVEKIT_URL`: URL to communicate the client application with the LiveKit server.
    - `roomName`: OpenVidu Room identifier. This is the room where the VideoconferenceComponent will connect.
    - `token`: OpenVidu Token used to connect to the OpenVidu Room.
    - `localParticipant`: Local participant model.
    - `remoteParticipants`: Remote participants model.
    - `localParticipantSubs`: Subscription to the local participant updates.
    - `remoteParticipantsSubs`: Subscription to the remote participants updates.
    - `onTokenRequested` method that fires when the VideoconferenceComponent requests a token to connect to the OpenVidu Room.
    - `subscribeToParticipants` method that subscribes to updates for local and remote participants.
    - `getToken` method that requests a token to the server application.

    --8<-- "docs/docs/tutorials/shared/configure-urls.md"

=== "styles.scss"

    --8<-- "docs/docs/tutorials/shared/openvidu-components-styles.md"

### Adding custom buttons to the toolbar

OpenVidu Components Angular provides a directive called `*ovLayout` that allows you to customize the default layout of the videoconference.
In this tutorial, we are creating a very basic layout just for demonstration purposes.

```typescript
@Component({
	selector: 'app-root',
	template: `
		<!-- OpenVidu Video Conference Component -->
		<ov-videoconference
			[token]="token"
			[livekitUrl]="LIVEKIT_URL"
			(onTokenRequested)="onTokenRequested($event)"
		>
			<!-- Custom Layout for Video Streams -->
			<div *ovLayout>
				<div class="container">
					<!-- Local Participant's Tracks -->
					@for (track of localParticipant.tracks; track track) {
					<div
						class="item"
						[ngClass]="{
							hidden:
								track.isAudioTrack && !track.participant.onlyHasAudioTracks
						}"
					>
						<ov-stream [track]="track"></ov-stream>
					</div>
					}

					<!-- Remote Participants' Tracks -->
					@for (track of remoteParticipants | tracks; track track) {
					<div
						class="item"
						[ngClass]="{
							hidden:
								track.isAudioTrack && !track.participant.onlyHasAudioTracks
						}"
					>
						<ov-stream [track]="track"></ov-stream>
					</div>
					}
				</div>
			</div>
		</ov-videoconference>
	`,
	styles: [''],
	standalone: true,
	imports: [OpenViduComponentsModule, MatIconButton, MatIcon],
})
export class AppComponent implements OnInit, OnDestroy {
	// ...
}
```

In this code snippet, the `*ovLayout` directive is used to customize the layout of the videoconference. The layout is divided into two sections: one for the local participant's tracks and another for the remote participants' tracks.

The repeater directive `@for` is used to iterate over the tracks of the local participant and the remote participants and display them in the layout using the `ov-stream` component.

<!-- ## Deploying openvidu-custom-layout

#### 1) Build the docker image

Under the root project folder, you can see the `openvidu-components/docker/` directory. Here it is included all the required files yo make it possible the deployment with OpenVidu.

First of all, you will need to create the **openvidu-custom-layout** docker image. Under `openvidu-components/docker/` directory you will find the `create_image.sh` script. This script will create the docker image with the [openvidu-basic-node](application-server/openvidu-basic-node/) as application server and the static files.

```bash
./create_image.sh openvidu/openvidu-custom-layout-demo:X.Y.Z openvidu-custom-layout
```

The script needs two parameters:

1. The name of the docker image to create.
2. The name of the tutorial folder.

This script will create an image named `openvidu/openvidu-custom-layout-demo:X.Y.Z`. This name will be used in the next step.

#### 2) Deploy the docker image

Time to deploy the docker image. You can follow the [Deploy OpenVidu based application with Docker](/deployment/deploying-openvidu-apps/#with-docker) guide for doing this. -->
