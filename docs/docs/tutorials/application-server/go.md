---
title: Go Server Tutorial
description: Learn how to build a minimal Go application server with Gin to generate LiveKit tokens and receive webhook events using the LiveKit Go SDK.
---

# Go Server Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.1.0/application-server/go){ .md-button target=\_blank }

This is a minimal server application built for Go with [Gin](https://gin-gonic.com/){:target="\_blank"} that allows:

-   Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
-   Receiving LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/){target=\_blank}.

It internally uses the [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go){:target="\_blank"}.

## Running this tutorial

### 1. Run OpenVidu Server

--8<-- "shared/tutorials/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.1.0
```

### 3. Run the server application

--8<-- "shared/tutorials/application-server/go.md"

### 4. Run a client application to test against this server

--8<-- "shared/tutorials/application-client/application-client-tabs.md"

## Understanding the code

The application is a simple Go app with a single file `main.go` that exports two endpoints:

-   `/token` : generate a token for a given Room name and Participant name.
-   `/livekit/webhook` : receive LiveKit webhook events.

Let's see the code of the `main.go` file:

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.1.0/application-server/go/main.go/#L15-L17' target='_blank'>main.go</a>" linenums="15"
var SERVER_PORT string // (1)!
var LIVEKIT_API_KEY string // (2)!
var LIVEKIT_API_SECRET string // (3)!
```

1. The port where the application will be listening
2. The API key of LiveKit Server
3. The API secret of LiveKit Server

The `main.go` file first declares the necessary global variables:

-   `SERVER_PORT`: the port where the application will be listening.
-   `LIVEKIT_API_KEY`: the API key of LiveKit Server.
-   `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

The server launch takes place in the `main` function at the end of the file, where we first load the environment variables, then set the REST endpoints and finally start the server on `SERVER_PORT`:

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.1.0/application-server/go/main.go#L63-L70' target='_blank'>main.go</a>" linenums="63"
func main() {
	loadEnv() // (1)!
	router := gin.Default() // (2)!
	router.Use(cors.Default()) // (3)!
	router.POST("/token", createToken) // (4)!
	router.POST("/livekit/webhook", receiveWebhook) // (5)!
	router.Run(":" + SERVER_PORT) // (6)!
}
```

1. Load environment variables
2. Create a new Gin router
3. Enable CORS support
4. Create the `/token` endpoint
5. Create the `/livekit/webhook` endpoint
6. Start the server on the `SERVER_PORT`

---

### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

-   `roomName`: the name of the Room where the user wants to connect.
-   `participantName`: the name of the participant that wants to connect to the Room.

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.1.0/application-server/go/main.go#L19-L49' target='_blank'>main.go</a>" linenums="19"
func createToken(context *gin.Context) {
	var body struct {
		RoomName        string `json:"roomName"`
		ParticipantName string `json:"participantName"`
	}

	if err := context.BindJSON(&body); err != nil {
		context.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if body.RoomName == "" || body.ParticipantName == "" {
		context.JSON(http.StatusBadRequest, gin.H{"errorMessage": "roomName and participantName are required"})
		return
	}

	at := auth.NewAccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) // (1)!
	grant := &auth.VideoGrant{
		RoomJoin: true,
		Room:     body.RoomName,
	}
	at.SetVideoGrant(grant).SetIdentity(body.ParticipantName) // (2)!

	token, err := at.ToJWT() // (3)!
	if err != nil {
		context.JSON(http.StatusInternalServerError, err.Error())
		return
	}

	context.JSON(http.StatusOK, gin.H{"token": token}) // (4)!
}
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set the video grants and identity of the participant in the AccessToken. `RoomJoin` allows the user to join a room and `Room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant){:target="\_blank"}.
3. We convert the AccessToken to a JWT token.
4. Finally, the token is sent back to the client.

We first load the request body into a struct with `roomName` and `participantName` string fields. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go){:target="\_blank"}:

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set the video grants and identity of the participant in the AccessToken. `RoomJoin` allows the user to join a room and `Room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant){:target="\_blank"}.
3. We convert the AccessToken to a JWT token and return it to the client.
4. Finally, the token is sent back to the client.

---

### Receive webhook

The endpoint `/livekit/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/home/server/webhooks/#Events){:target="\_blank"}.

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.1.0/application-server/go/main.go#L51-L61' target='_blank'>main.go</a>" linenums="51"
func receiveWebhook(context *gin.Context) {
	authProvider := auth.NewSimpleKeyProvider( // (1)!
		LIVEKIT_API_KEY, LIVEKIT_API_SECRET,
	)
	event, err := webhook.ReceiveWebhookEvent(context.Request, authProvider) // (2)!
	if err != nil {
		fmt.Fprintf(os.Stderr, "error validating webhook event: %v", err)
		return
	}
	fmt.Println("LiveKit Webhook", event) // (3)!
}
```

1. Create a `SimpleKeyProvider` with the `LIVEKIT_API_KEY` and `LIVEKIT_API`.
2. Receive the webhook event providing the `http.Request` in the Gin context and the `SimpleKeyProvider` we just created. This will validate and decode the incoming [webhook event](https://docs.livekit.io/home/server/webhooks/){:target="\_blank"}.
3. Consume the event as you whish.

<span></span>

1. Create a `SimpleKeyProvider` with the `LIVEKIT_API_KEY` and `LIVEKIT_API`.
2. Receive the webhook event providing the `http.Request` in the Gin context and the `SimpleKeyProvider` we just created. This will validate and decode the incoming [webhook event](https://docs.livekit.io/home/server/webhooks/){:target="\_blank"}.
3. Consume the event as you whish.

--8<-- "shared/tutorials/webhook-local-server.md"

<br>
