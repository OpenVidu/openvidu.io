# Go

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-server/go){ .md-button target=\_blank }

This is a minimal server application built for Go with [Gin](https://gin-gonic.com/){:target="\_blank"}  that allows:

- Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

It internally uses the [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go){:target="\_blank"}.

## Running this application

Download the tutorial code:

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

--8<-- "docs/docs/tutorials/shared/go.md"

!!! info

    You can run any [Application Client](../application-client/index.md) to test against this server right away.

## Understanding the code

The application is a simple Go app with a single file `main.go` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/webhook` : receive LiveKit webhook events.

Let's see the code of the `main.go` file:

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/go/main.go/#L14-L25' target='_blank'>main.go</a>" linenums="14"
var (
	SERVER_PORT        = getEnv("SERVER_PORT", "6080") // (1)!
	LIVEKIT_API_KEY    = getEnv("LIVEKIT_API_KEY", "devkey") // (2)!
	LIVEKIT_API_SECRET = getEnv("LIVEKIT_API_SECRET", "secret") // (3)!
)

func getEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}
```

1. The port where the application will be listening
2. The API key of LiveKit Server
3. The API secret of LiveKit Server

The `main.go` file first loads the necessary environment variables:

- `SERVER_PORT`: the port where the application will be listening.
- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Method `getEnv` simply load each environment variable, giving a default value if not found.

The server launch takes place in the `main` function at the end of the file, where we set the REST endpoints and start the server on `SERVER_PORT`:

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/go/main.go#L71-L77' target='_blank'>main.go</a>" linenums="71"
func main() {
	router := gin.Default() // (1)!
	router.Use(cors.Default()) // (2)!
	router.POST("/token", createToken) // (3)!
	router.POST("/webhook", receiveWebhook) // (4)!
	router.Run(":" + SERVER_PORT) // (5)!
}
```

1. Create a new Gin router
2. Enable CORS support
3. Create the `/token` endpoint
4. Create the `/webhook` endpoint
5. Start the server on the `SERVER_PORT`

---

### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/go/main.go#L27-L57' target='_blank'>main.go</a>" linenums="27"
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
	at.AddGrant(grant).SetIdentity(body.ParticipantName) // (2)!

	token, err := at.ToJWT() // (3)!
	if err != nil {
		context.JSON(http.StatusInternalServerError, err.Error())
		return
	}

	context.JSON(http.StatusOK, gin.H{"token": token}) // (4)!
}
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set the video grants and identity of the participant in the AccessToken. `RoomJoin` allows the user to join a room and `Room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. We convert the AccessToken to a JWT token.
4. Finally, the token is sent back to the client.

We first load the request body into a struct with `roomName` and `participantName` string fields. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit Go SDK](https://pkg.go.dev/github.com/livekit/server-sdk-go){:target="\_blank"}:

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set the video grants and identity of the participant in the AccessToken. `RoomJoin` allows the user to join a room and `Room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. We convert the AccessToken to a JWT token and return it to the client.
4. Finally, the token is sent back to the client.

---

### Receive webhook

The endpoint `/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/realtime/server/webhooks/#Events){:target="\_blank"}.

```go title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/go/main.go#L59-L69' target='_blank'>main.go</a>" linenums="59"
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
2. Receive the webhook event providing the `http.Request` in the Gin context and the `SimpleKeyProvider` we just created. This will validate and decode the incoming [webhook event](https://docs.livekit.io/realtime/server/webhooks/){:target="\_blank"}.
3. Consume the event as you whish.

<span></span>

1. Create a `SimpleKeyProvider` with the `LIVEKIT_API_KEY` and `LIVEKIT_API`.
2. Receive the webhook event providing the `http.Request` in the Gin context and the `SimpleKeyProvider` we just created. This will validate and decode the incoming [webhook event](https://docs.livekit.io/realtime/server/webhooks/){:target="\_blank"}.
3. Consume the event as you whish.

<br>