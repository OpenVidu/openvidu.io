# .NET

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/3.0.0/application-server/dotnet){ .md-button target=\_blank }

This is a minimal server application built for .NET with [ASP.NET Core Minimal APIs](https://docs.microsoft.com/aspnet/core/tutorials/min-web-api?view=aspnetcore-6.0&tabs=visual-studio){:target="\_blank"} that allows:

-   Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
-   Receiving LiveKit [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

It internally uses the [LiveKit .NET SDK](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="\_blank"}.

## Running this tutorial

### 1. Run OpenVidu Server

--8<-- "shared/tutorials/run-openvidu-server.md"

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git -b 3.0.0
```

### 3. Run the server application

--8<-- "shared/tutorials/application-server/dotnet.md"

### 4. Run a client application to test against this server

--8<-- "shared/tutorials/application-client/application-client-tabs.md"

## Understanding the code

The application is a simple [ASP.NET Core Minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/tutorials/min-web-api?view=aspnetcore-6.0&tabs=visual-studio){target=\_blank} app with a single file `Program.cs` that exports two endpoints:

-   `/token` : generate a token for a given Room name and Participant name.
-   `/livekit/webhook` : receive LiveKit webhook events.

Let's see the code `Program.cs` file:

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.0.0/application-server/dotnet/Program.cs#L1-L36' target='_blank'>Program.cs</a>" linenums="1"
using System.Text.Json;
using Livekit.Server.Sdk.Dotnet; // (1)!

var builder = WebApplication.CreateBuilder(args); // (2)!
var MyAllowSpecificOrigins = "_myAllowSpecificOrigins"; // (3)!

IConfiguration config = new ConfigurationBuilder() // (4)!
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();

// Load env variables
var SERVER_PORT = config.GetValue<int>("SERVER_PORT"); // (5)!
var LIVEKIT_API_KEY = config.GetValue<string>("LIVEKIT_API_KEY"); // (6)!
var LIVEKIT_API_SECRET = config.GetValue<string>("LIVEKIT_API_SECRET"); // (7)!

// Enable CORS support
builder.Services.AddCors(options => // (8)!
{
    options.AddPolicy(
        name: MyAllowSpecificOrigins,
        builder =>
        {
            builder.WithOrigins("*").AllowAnyHeader();
        }
    );
});

builder.WebHost.UseKestrel(serverOptions => // (9)!
{
    serverOptions.ListenAnyIP(SERVER_PORT);
});

var app = builder.Build(); // (10)!
app.UseCors(MyAllowSpecificOrigins);
```

1. Import the [LiveKit .NET SDK](https://github.com/pabloFuente/livekit-server-sdk-dotnet){:target="\_blank"}.
2. A `WebApplicationBuilder` instance to build the application.
3. The name of the CORS policy to be used in the application.
4. A `IConfiguration` instance to load the configuration from the `appsettings.json` file, including the required environment variables.
5. The port where the application will be listening.
6. The API key of LiveKit Server.
7. The API secret of LiveKit Server.
8. Configure CORS support.
9. Configure the port.
10. Build the application and enable CORS support.

The `Program.cs` file imports the required dependencies and loads the necessary environment variables (defined in `appsettings.json` file):

-   `SERVER_PORT`: the port where the application will be listening.
-   `LIVEKIT_API_KEY`: the API key of LiveKit Server.
-   `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Finally the application enables CORS support and the port where the application will be listening.

---

#### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

-   `roomName`: the name of the Room where the user wants to connect.
-   `participantName`: the name of the participant that wants to connect to the Room.

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.0.0/application-server/dotnet/Program.cs#L38-L68' target='_blank'>Program.cs</a>" linenums="38"
app.MapPost(
    "/token",
    async (HttpRequest request) =>
    {
        var body = new StreamReader(request.Body); // (1)!
        string postData = await body.ReadToEndAsync();
        Dictionary<string, dynamic> bodyParams =
            JsonSerializer.Deserialize<Dictionary<string, dynamic>>(postData)
            ?? new Dictionary<string, dynamic>();

        if (
            bodyParams.TryGetValue("roomName", out var roomName)
            && bodyParams.TryGetValue("participantName", out var participantName)
        )
        {
            var token = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) // (2)!
                .WithIdentity(participantName.ToString()) // (3)!
                .WithName(participantName.ToString())
                .WithGrants(new VideoGrants{ RoomJoin = true, Room = roomName.ToString() }); // (4)!

            var jwt = token.ToJwt(); // (5)!
            return Results.Json(new { token = jwt }); // (6)!
        }
        else
        {
            return Results.BadRequest(
                new { errorMessage = "roomName and participantName are required" } // (7)!
            );
        }
    }
);
```

1. The endpoint obtains a Dictionary from the body request, and check if fields `roomName` and `participantName` are available.
2. A new `AccessToken` is created providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.
3. We set participant's name and identity in the AccessToken.
4. We set the video grants in the AccessToken. `RoomJoin` allows the user to join a room and `RoomName` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
5. Obtain the JWT string from the AccessToken.
6. Return the token to the client.
7. Return a `400` error if required fields are not available.

The endpoint obtains a Dictionary from the body request, and check if fields `roomName` and `participantName` are available. If not, it returns a `400` error. If required fields are available, a new `AccessToken` is created with the proper participant's identity, name and video grants. The `RoomJoin` grant allows the user to join a room and the `Room` grant determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.

Finally, the returned token is sent back to the client.

---

#### Receive webhook

The endpoint `/livekit/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/realtime/server/webhooks/#Events){:target="\_blank"}.

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/3.0.0/application-server/dotnet/Program.cs#L70-L95' target='_blank'>Program.cs</a>" linenums="70"
app.MapPost(
    "/livekit/webhook",
    async (HttpRequest request) =>
    {
        var webhookReceiver = new WebhookReceiver(LIVEKIT_API_KEY, LIVEKIT_API_SECRET); // (1)!
        try
        {
            StreamReader body = new StreamReader(request.Body); // (2)!
            string postData = await body.ReadToEndAsync();
            string authHeader =
                request.Headers["Authorization"].FirstOrDefault() // (3)!
                ?? throw new Exception("Authorization header is missing");

            WebhookEvent webhookEvent = webhookReceiver.Receive(postData, authHeader); // (4)!

            Console.Out.WriteLine(webhookEvent); // (5)!

            return Results.Ok(); // (6)!
        }
        catch (Exception e)
        {
            Console.Error.WriteLine("Error validating webhook event: " + e.Message); // (7)!
            return Results.Unauthorized();
        }
    }
);
```

1. Initialize the WebhookReceiver using the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. It will help validating and decoding incoming [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.
2. The raw string body of the request contains the webhook event.
3. The `Authorization` header is required to validate the webhook event.
4. Obtain the `WebhookEvent` object using the `WebhookReceiver#Receive` method. It takes the raw body as a String and the Authorization header of the request.
5. Consume the event as you whish.
6. Return a response to LiveKit Server to let it know that the webhook was received correctly.
7. You can handle any exception triggered by the validation process.

We first initialize a `WebhookReceiver` object using the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.

Then we need the raw body as a String and the `Authorization` header of the request. With them we obtain a `WebhookEvent` object calling method `WebhookReceiver#Receive`. If everything is correct, you can do whatever you want with the event (in this case, we just log it).

Remember to return a `200` OK response at the end to let LiveKit Server know that the webhook was received correctly.

--8<-- "shared/tutorials/webhook-local-server.md"

<br>
