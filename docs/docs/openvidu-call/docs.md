# openvidu-call

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-call){ .md-button target=\_blank }

Introducing **OpenVidu Call**, the premier videoconference application that showcases the full potential of the OpenVidu platform. OpenVidu Call is not just any videoconferencing tool; it’s the default and flagship app built with the robust and versatile [OpenVidu Components](../ui-components/angular-components.md).

<figure markdown>
  ![OpenVidu Call](../../assets/images/openvidu-call/openvidu-call.jpg){ loading=lazy .ov-call-docs-img .round-corners .mkdocs-img}
  <figcaption>OpenVidu Call</figcaption>
</figure>

## Run OpenVidu Call

#### 1. Run OpenVidu Server

--8<-- "docs/docs/tutorials/shared/run-openvidu-server.md"

!!! info "Accessible via openvidu-local-deployment"

    A pre-built OpenVidu Call application is launched as part of the **openvidu-local-deployment** and it can be accessible  by visiting [`http://localhost:7880/openvidu-call/`](http://localhost:7880/openvidu-call/){:target="\_blank"}.

    If you want to explore and run the OpenVidu Call code locally, follow the instructions below.


#### 2. Download OpenVidu Call code

```bash
git clone https://github.com/OpenVidu/openvidu-call.git
```

#### 3. Run the OpenVidu Call backend


1. Navigate to the `openvidu-call-back` directory:

    ```bash
    cd openvidu-call/openvidu-call-back
    ```

2. Install the dependencies:

    ```bash
    npm install
    ```

3. Start the application:

    ```bash
    npm run dev:start
    ```

#### 4. Run the OpenVidu Call frontend

Launching another terminal, under the `openvidu-call` directory:

1. Navigate to the `openvidu-call-front` directory:

    ```bash
    cd openvidu-call/openvidu-call-front
    ```

2. Install the dependencies:

    ```bash
    npm install
    ```

3. Start the application:

    ```bash
    npm run dev:start
    ```

The application will be available at [`http://localhost:5080`](http://localhost:5080){:target="\_blank"}.


## Architecture

The OpenVidu Call architecture is divided into two main components:

* **OpenVidu Call frontend** which is the client-side application built with Angular and OpenVidu Components.
* **OpenVidu Call backend** which is the server-side application built with Node.js and Express and uses the LiveKit Server SDK library to interact with the OpenVidu Server.

<figure markdown>
  ![OpenVidu Call Architecture](../../assets/images/openvidu-call/openvidu-call-achitecture.png){ loading=lazy .svg-img .mkdocs-img}
  <figcaption>OpenVidu Call Architecture</figcaption>
</figure>

=== ":simple-angular:{.icon .lg-icon .tab-icon} OpenVidu Call frontend"

    The client-side application built with Angular that provides the user interface for the videoconference. It uses the OpenVidu Components library to create the videoconference layout with ease.

    The project architecture is divided into the following directories:

    - `components`: Contains the components that define the UI elements.
    - `services`: Contains the services that interact with the OpenVidu Call backend in a RESTful manner.

    Additionally, the project hosts the following files:

    - `app.component.ts`: The main file that initializes the Angular application.
    - `app-routing.module.ts`: Contains the routes that define the application navigation.

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} OpenVidu Call backend"

    The server-side application built with Node.js and Express that manages the communication between the OpenVidu Server and the OpenVidu Call Frontend.

    It uses the LiveKit Server SDK library to interact with the OpenVidu Server and handle the authentication, videoconference rooms, recordings, broadcasts, and other features.

    The project architecture is divided into the following directories:

    - `controllers`: Contains the controllers that handle the HTTP requests.
    - `services`: Contains the services that interact with the OpenVidu Server.
    - `models`: Contains the models that define the data structures.
    - `helpers`: Contains the helper functions.

    Additionally, the project hosts the following files:

    - `server.ts`: The main file that initializes the Express application.
    - `routes.ts`: Contains the routes that define the API endpoints.
    - `config.ts`: Contains the configuration settings for the application.

## Features

### Authentication

OpenVidu Call provides user authentication to ensure that only authorized users can access the videoconference rooms. The authentication process is handled by the OpenVidu Call backend, which uses **Basic Authentication** to verify the user credentials.

### Video conferencing

#### Essential Features

OpenVidu Call offers essential features that make video conferencing simple and intuitive for users. These features include:

<div class="grid cards" markdown>

-   :material-translate-variant:{ .ov-call-docs-icon .middle } __Multilingual__

    ---

    Supports for multiple languages, allowing users to select their preferred language for the interface

-   :material-microphone:{ .ov-call-docs-icon .middle } :material-video:{ .ov-call-docs-icon .middle } __Device Selection__

    ---

    Users can choose their preferred audio and video devices before and during the call

-   :material-fullscreen:{ .ov-call-docs-icon .middle } __Fullscreen Mode__

    ---

	Offers a fullscreen mode for users to **focus on the videoconference without any distractions**


-   :material-monitor-share:{ .ov-call-docs-icon .middle } __Screen Sharing__

    ---

    Allow users to **share their screen and their camera at the same time** with other participants in the call


-   :material-view-grid-plus:{ .ov-call-docs-icon  .middle } __Powerful Layout__

    ---

    Offers a powerful layout where users can **view multiple participants simultaneously** in a **grid layout** or **focus on a single participant**

-   :material-chat:{ .ov-call-docs-icon .middle } __Chat Integration__

    ---

    Built-in chat functionality enabling participants to send text messages to the group

</div>

<br>

#### Advanced Features

The advanced features of OpenVidu Call enhance the video conferencing experience by providing additional functionalities that improve collaboration and productivity.


<div class="grid cards" markdown>

-   :material-account-voice:{ .ov-call-docs-icon .middle } __Speaker Detection__

    ---

    **Highlights the active speaker automatically**, making it easier for participants to follow the conversation

-   :material-connection:{ .ov-call-docs-icon .middle } __Automatic Reconnection__

    ---

    Ensures that **users are automatically reconnected** to the call in case of temporary network issues


-   :material-record-circle-outline:{ .ov-call-docs-icon .middle } __Recording__

    ---

    Supports recording of video conferences for later playback

-   :material-broadcast:{ .ov-call-docs-icon .middle } __Broadcasting (Live Streaming)__

    ---

    Allows **live streaming** of the video conference to platforms like **YouTube**, **Twitch**, and others **for a wider audience**

-   :material-blur:{ .ov-call-docs-icon .middle } __Virtual Backgrounds__

    ---

    Enables users to use **virtual backgrounds** during the call, **enhancing privacy and professionalism**

</div>

### Admin Dashboard

An admin dashboard is integrated into OpenVidu Call to provide additional functionalities for the admin user.

<div class="grid cards" markdown>

-   :material-lock:{ .ov-call-docs-icon .middle } __Admin Authentication__

    ---

    Provides admin authentication to ensure that only authorized users can access the admin dashboard

-   :material-note-search:{ .ov-call-docs-icon .middle } __Recording Management__

    ---

    Allows the admin user to view, download, and delete the recordings stored in the OpenVidu Server

</div>


## Build and Deployment

### Docker Image

The process to build a Docker image of OpenVidu call is really easy, you just need to run the following instructions:

1. Build the Docker image:

	```bash
	cd docker
	./create_image.sh openvidu-call
	```

	This script will create a Docker image with the name `openvidu-call`.

2. Run the Docker container:

	```bash
	docker run -p 5000:5000 \
	-e LIVEKIT_URL=wss://your-livekit-server-url \
	-e LIVEKIT_API_KEY=your-livekit-api-key \
	-e LIVEKIT_API_SECRET=your-livekit-api-secret \
	openvidu-call
	```

	Once the container is running, you can access the OpenVidu Call application by visiting [`http://localhost:5000`](http://localhost:5000){:target="\_blank"}.

### Package bundle

To build the OpenVidu Call application without using Docker, you can follow the instructions:

1. Build the frontend application:

	```bash
	cd openvidu-call-front
	npm install
	npm run prod:build
	```

2. Build the backend application:

	```bash
	cd openvidu-call-back
	npm install
	npm run build
	```

3. Start the backend application:

	```bash
	cd dist
	node server.js
	```
