---
title: Ruby Server Tutorial
description: Learn how to build a minimal Ruby application server with Sinatra to generate LiveKit tokens and receive webhook events using the LiveKit Ruby SDK.
---

# Ruby Server Tutorial

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.3.0/application-server/ruby){ .md-button target=\_blank }

This is a minimal server application built for Ruby with [Sinatra](https://sinatrarb.com/){:target="\_blank"} that allows:

-   Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
-   Receiving LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/){target=\_blank}.

It internally uses [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby){:target="\_blank"}.

## Running this tutorial

### 1. Run OpenVidu Server

--8<-- "shared/tutorials/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.3.0
```

### 3. Run the server application

--8<-- "shared/tutorials/application-server/ruby.md"

### 4. Run a client application to test against this server

--8<-- "shared/tutorials/application-client/application-client-tabs.md"

## Understanding the code

The application is a simple Ruby app using the popular Sinatra web library. It has a single file `app.rb` that exports two endpoints:

-   `/token` : generate a token for a given Room name and Participant name.
-   `/livekit/webhook` : receive LiveKit webhook events.

Let's see the code of the `app.rb` file:

```ruby title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/application-server/ruby/app.rb#L1-L17' target='_blank'>app.rb</a>" linenums="1"
require 'sinatra'
require 'sinatra/cors'
require 'sinatra/json'
require 'livekit' # (1)!
require './env.rb'

SERVER_PORT = ENV['SERVER_PORT'] || 6080 # (2)!
LIVEKIT_API_KEY = ENV['LIVEKIT_API_KEY'] || 'devkey' # (3)!
LIVEKIT_API_SECRET = ENV['LIVEKIT_API_SECRET'] || 'secret' # (4)!

set :port, SERVER_PORT # (5)!

register Sinatra::Cors # (6)!
set :allow_origin, '*' # (7)!
set :allow_methods, 'POST,OPTIONS'
set :allow_headers, 'content-type'
set :bind, '0.0.0.0' # (8)!
```

1. Import `livekit` library
2. The port where the application will be listening
3. The API key of LiveKit Server
4. The API secret of LiveKit Server
5. Configure the port
6. Enable CORS support
7. Set allowed origin (any), methods and headers
8. Listen in any available network interface of the host

The `app.rb` file imports the required dependencies and loads the necessary environment variables (defined in `env.rb` file):

-   `SERVER_PORT`: the port where the application will be listening.
-   `LIVEKIT_API_KEY`: the API key of LiveKit Server.
-   `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Finally the application configures the port, sets the CORS configuration for Sinatra and binds the application to all available network interfaces (0.0.0.0).

---

#### Create token endpoint

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

-   `roomName`: the name of the Room where the user wants to connect.
-   `participantName`: the name of the participant that wants to connect to the Room.

```ruby title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/application-server/ruby/app.rb#L19-L34' target='_blank'>app.rb</a>" linenums="19"
post '/token' do
  body = JSON.parse(request.body.read)
  room_name = body['roomName']
  participant_name = body['participantName']

  if room_name.nil? || participant_name.nil?
    status 400
    return json({errorMessage: 'roomName and participantName are required'})
  end

  token = LiveKit::AccessToken.new(api_key: LIVEKIT_API_KEY, api_secret: LIVEKIT_API_SECRET) # (1)!
  token.identity = participant_name # (2)!
  token.add_grant(roomJoin: true, room: room_name) # (3)!

  return json({token: token.to_jwt}) # (4)!
end
```

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set participant's identity in the AccessToken.
3. We set the video grants in the AccessToken. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant){:target="\_blank"}.
4. Finally, we convert the AccessToken to a JWT token and send it back to the client.

The endpoint first obtains the `roomName` and `participantName` parameters from the request body. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit Ruby SDK](https://github.com/livekit/server-sdk-ruby){:target="\_blank"}:

1. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
2. We set participant's identity in the AccessToken.
3. We set the video grants in the AccessToken. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/home/get-started/authentication/#Video-grant){:target="\_blank"}.
4. Finally, we convert the AccessToken to a JWT token and send it back to the client.

---

#### Receive webhook

The endpoint `/livekit/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/home/server/webhooks/#Events){:target="\_blank"}.

```ruby title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.3.0/application-server/ruby/app.rb#L36-L47' target='_blank'>app.rb</a>" linenums="36"
post '/livekit/webhook' do
  auth_header = request.env['HTTP_AUTHORIZATION'] # (1)!
  token_verifier = LiveKit::TokenVerifier.new(api_key: LIVEKIT_API_KEY, api_secret: LIVEKIT_API_SECRET) # (2)!
  begin
    token_verifier.verify(auth_header) # (3)!
    body = JSON.parse(request.body.read) # (4)!
    puts "LiveKit Webhook: #{body}" # (5)!
    return
  rescue => e
    puts "Authorization header is not valid: #{e}"
  end
end
```

1. Get the `Authorization` header from the HTTP request.
2. Create a new `TokenVerifier` instance providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. This will validate the webhook event to confirm it is actually coming from our LiveKit Server.
3. Verify the `Authorization` header with the `TokenVerifier`.
4. Now that we are sure the event is valid, we can parse the request JSON body to get the actual webhook event.
5. Consume the event as you whish.

<span></span>

We need to verify that the event is coming from our LiveKit Server. For that we need the `Authorization` header from the HTTP request and a `TokenVerifier` instance built with the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.

If the verification is successful, we can parse the request JSON body and consume the event (in this case, we just log it).

Remember to return a `200` OK response at the end to let LiveKit Server know that the webhook was received correctly.

--8<-- "shared/tutorials/webhook-local-server.md"

<br>
