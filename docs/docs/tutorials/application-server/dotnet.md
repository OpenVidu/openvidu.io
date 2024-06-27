# .NET

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-server/dotnet){ .md-button target=\_blank }

This is a minimal server application built for .NET with [ASP.NET Core Minimal APIs](https://docs.microsoft.com/aspnet/core/tutorials/min-web-api?view=aspnetcore-6.0&tabs=visual-studio){:target="\_blank"} that allows:

- Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

Unfortunately there is no .NET SDK for LiveKit available, so the application has to manually build LiveKit compatible JWT tokens using the .NET library `System.IdentityModel.Tokens.Jwt`, and check the validity of webhook events on its own. It is a fairly easy process.

## Running this application

Download the tutorial code:

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

--8<-- "docs/docs/tutorials/shared/dotnet.md"

!!! info

    You can run any [Application Client](../application-client/index.md) to test against this server right away.

## Understanding the code

The application is a simple ASP.NET Core Minimal APIs app with a single file `Program.cs` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/webhook` : receive LiveKit webhook events.

Let's see the code `Program.cs` file:

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/dotnet/Program.cs#L8-L37' target='_blank'>Program.cs</a>" linenums="8"
var builder = WebApplication.CreateBuilder(args); // (1)!
var MyAllowSpecificOrigins = "_myAllowSpecificOrigins"; // (2)!

IConfiguration config = new ConfigurationBuilder() // (3)!
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json")
                .AddEnvironmentVariables().Build();

// Load env variables
var SERVER_PORT = config.GetValue<int>("SERVER_PORT"); // (4)!
var LIVEKIT_API_KEY = config.GetValue<string>("LIVEKIT_API_KEY"); // (5)!
var LIVEKIT_API_SECRET = config.GetValue<string>("LIVEKIT_API_SECRET"); // (6)!

// Enable CORS support
builder.Services.AddCors(options => // (7)!
{
    options.AddPolicy(name: MyAllowSpecificOrigins,
                      builder =>
                      {
                          builder.WithOrigins("*").AllowAnyHeader();
                      });
});

builder.WebHost.UseKestrel(serverOptions => // (8)!
{
    serverOptions.ListenAnyIP(SERVER_PORT);
});

var app = builder.Build(); // (9)!
app.UseCors(MyAllowSpecificOrigins);
```

1. A `WebApplicationBuilder` instance to build the application.
2. The name of the CORS policy to be used in the application.
3. A `IConfiguration` instance to load the configuration from the `appsettings.json` file, including the required environment variables.
4. The port where the application will be listening.
5. The API key of LiveKit Server.
6. The API secret of LiveKit Server.
7. Configure CORS support.
8. Configure the port.
9. Build the application and enable CORS support.

The `Program.cs` file imports the required dependencies and loads the necessary environment variables (defined in `appsettings.json` file):

- `SERVER_PORT`: the port where the application will be listening.
- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

Finally the application enables CORS support and the port where the application will be listening.

---

#### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/dotnet/Program.cs#L39-L54' target='_blank'>Program.cs</a>" linenums="39"
app.MapPost("/token", async (HttpRequest request) =>
{
    var body = new StreamReader(request.Body); // (1)!
    string postData = await body.ReadToEndAsync();
    Dictionary<string, dynamic> bodyParams = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(postData) ?? new Dictionary<string, dynamic>();

    if (bodyParams.TryGetValue("roomName", out var roomName) && bodyParams.TryGetValue("participantName", out var participantName))
    {
        var token = CreateLiveKitJWT(roomName.ToString(), participantName.ToString()); // (2)!
        return Results.Json(new { token }); // (3)!
    }
    else
    {
        return Results.BadRequest(new { errorMessage = "roomName and participantName are required" }); // (4)!
    }
});
```

1. The endpoint obtains a Dictionary from the body request, and check if fields `roomName` and `participantName` are available.
2. Create a new JWT token with the room and participant name.
3. Return the token to the client.
4. Return a `400` error if required fields are not available.

The endpoint obtains a Dictionary from the body request, and check if fields `roomName` and `participantName` are available. If not, it returns a `400` error.

If required fields are available, a new JWT token is created. Unfortunately there is no .NET SDK for LiveKit, so we need to create the JWT token manually. The `CreateLiveKitJWT` method is responsible for creating the LiveKit compatible JWT token:

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/dotnet/Program.cs#L80-L100' target='_blank'>Program.cs</a>" linenums="80"
string CreateLiveKitJWT(string roomName, string participantName)
{
    JwtHeader headers = new(new SigningCredentials(new SymmetricSecurityKey(Encoding.UTF8.GetBytes(LIVEKIT_API_SECRET)), "HS256")); // (1)!

    var videoGrants = new Dictionary<string, object>() // (2)!
    {
        { "room", roomName },
        { "roomJoin", true }
    };
    JwtPayload payload = new()
    {
        { "exp", new DateTimeOffset(DateTime.UtcNow.AddHours(6)).ToUnixTimeSeconds() }, // (3)!
        { "iss", LIVEKIT_API_KEY }, // (4)!
        { "nbf", 0 }, // (5)!
        { "sub", participantName }, // (6)!
        { "name", participantName },
        { "video", videoGrants }
    };
    JwtSecurityToken token = new(headers, payload);
    return new JwtSecurityTokenHandler().WriteToken(token); // (7)!
}
```

1. Create a new `JwtHeader` with `LIVEKIT_API_SECRET` as the secret key and HS256 as the encryption algorithm.
2. Create a new Dictionary with the video grants for the participant. `roomJoin` allows the user to join a room and `room` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. Set the expiration time of the token. LiveKit default's is 6 hours.
4. Set the API key of LiveKit Server as the issuer (`iss`) of the token.
5. The `Not before` field (`nbf`) sets when the token becomes valid (0 for immediately valid).
6. Set the participant's name in the claims `sub` and `name`.
7. Finally, the returned token is sent back to the client.

This method uses the native `System.IdentityModel.Tokens.Jwt` library to create a JWT token valid for LiveKit. The most important field in the JwtPayload is `video`, which will determine the [VideoGrant](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"} permissions of the participant in the Room. You can also customize the expiration time of the token by changing the `exp` field, and add a `metadata` field for the participant. Check out all the available [claims](https://docs.livekit.io/realtime/concepts/authentication/#Token-example){:target="\_blank"}.

Finally, the returned token is sent back to the client.

---

#### Receive webhook

The endpoint `/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/realtime/server/webhooks/#Events){:target="\_blank"}.

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/dotnet/Program.cs#L56-L78' target='_blank'>Program.cs</a>" linenums="56"
app.MapPost("/webhook", async (HttpRequest request) =>
{
    var body = new StreamReader(request.Body);
    string postData = await body.ReadToEndAsync(); // (1)!

    var authHeader = request.Headers["Authorization"]; // (2)!
    if (authHeader.Count == 0)
    {
        return Results.BadRequest("Authorization header is required");
    }
    try
    {
        VerifyWebhookEvent(authHeader.First(), postData); // (3)!
    }
    catch (Exception e)
    {
        Console.Error.WriteLine("Error validating webhook event: " + e.Message);
        return Results.Unauthorized();
    }

    Console.Out.WriteLine(postData); // (4)!
    return Results.Ok(); // (5)!
});
```

1. The raw string body of the request contains the webhook event.
2. The `Authorization` header is required to validate the webhook event.
3. Verify the webhook event.
4. Consume the event as you whish.
5. Return a response to LiveKit Server to let it know that the webhook was received correctly.

The endpoint receives the incoming webhook event and validates it to ensure it is coming from our LiveKit Server. For that we need the raw string body and the `Authorization` header of the request. After validating it, we can consume the event (in this case, we just log it), and we must also return a `200` OK response to LiveKit Server to let it know that the webhook was received correctly.

Unfortunately there is no .NET SDK for LiveKit, so we need to manually validate the webhook event. The `VerifyWebhookEvent` method does that:

```cs title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/dotnet/Program.cs#L102-L125' target='_blank'>Program.cs</a>" linenums="102"
void VerifyWebhookEvent(string authHeader, string body)
{
    var utf8Encoding = new UTF8Encoding();
    var tokenValidationParameters = new TokenValidationParameters()
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(utf8Encoding.GetBytes(LIVEKIT_API_SECRET)), // (1)!
        ValidateIssuer = true,
        ValidIssuer = LIVEKIT_API_KEY, // (2)!
        ValidateAudience = false
    };

    var jwtValidator = new JwtSecurityTokenHandler();
    var claimsPrincipal = jwtValidator.ValidateToken(authHeader, tokenValidationParameters, out SecurityToken validatedToken); // (3)!

    var sha256 = SHA256.Create();
    var hashBytes = sha256.ComputeHash(utf8Encoding.GetBytes(body));
    var hash = Convert.ToBase64String(hashBytes); // (4)!

    if (claimsPrincipal.HasClaim(c => c.Type == "sha256") && claimsPrincipal.FindFirstValue("sha256") != hash)
    {
        throw new ArgumentException("sha256 checksum of body does not match!");
    }
}
```

1. Use the `LIVEKIT_API_SECRET` as the secret key to validate the token.
2. Set the `LIVEKIT_API_KEY` as the issuer of the token.
3. Validate the `Authorization` header with the recently created `TokenValidationParameters`. If the `LIVEKIT_API_SECRET` or `LIVEKIT_API_KEY` of the LiveKit Server that sent the event do not match the ones in the application, this will throw an exception.
4. Calculate the SHA256 hash of the body and compare it with the `sha256` claim in the token. If they match, it means the webhook event was not tampered and we can trust it.

We need a `TokenValidationParameters` object from the `Microsoft.IdentityModel.Tokens` namespace. We use the `LIVEKIT_API_SECRET` as the symmetric key, and the `LIVEKIT_API_KEY` as the issuer of the token.

If method `JwtSecurityTokenHandler#ValidateToken` does rise an exception when validating the `Authorization` header, it means the webhook event was sent by a LiveKit Server with different credentials.

Finally, we calculate the SHA256 hash of the body and compare it with the `sha256` claim in the token. If they match, it means the webhook event was not tampered and we can definitely trust it.

<br>
