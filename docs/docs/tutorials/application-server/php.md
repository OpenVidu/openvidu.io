# PHP

[Source code :simple-github:](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-server/php){ .md-button target=\_blank }

This is a minimal server application built for PHP  that allows:

- Generating LiveKit tokens on demand for any [application client](../application-client/index.md).
- Receiving LiveKit [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.

It internally uses [LiveKit PHP SDK](https://github.com/agence104/livekit-server-sdk-php){:target="\_blank"}.

## Running this application

Download the tutorial code:

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

--8<-- "docs/docs/tutorials/shared/php.md"

!!! info

    You can run any [Application Client](../application-client/index.md) to test against this server right away.

!!! warning

    LiveKit PHP SDK requires library [BCMath](https://www.php.net/manual/en/book.bc.php){:target="\_blank"}. This is available out-of-the-box in PHP for Windows, but a manual installation might be necessary in other OS. Run **`sudo apt install php-bcmath`** or **`sudo yum install php-bcmath`**

## Understanding the code

The application is a simple PHP app with a single file `index.php` that exports two endpoints:

- `/token` : generate a token for a given Room name and Participant name.
- `/webhook` : receive LiveKit webhook events.

Let's see the code of the `index.php` file:

```php title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/php/index.php#L1-L17' target='_blank'>index.php</a>" linenums="1"
<?php
require __DIR__ . "/vendor/autoload.php";

use Agence104\LiveKit\AccessToken; // (1)!
use Agence104\LiveKit\AccessTokenOptions;
use Agence104\LiveKit\VideoGrant;
use Agence104\LiveKit\WebhookReceiver;
use Dotenv\Dotenv;

Dotenv::createImmutable(__DIR__)->safeLoad();

header("Access-Control-Allow-Origin: *"); // (2)!
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Content-type: application/json");

$LIVEKIT_API_KEY = $_ENV["LIVEKIT_API_KEY"] ?? "devkey"; // (3)!
$LIVEKIT_API_SECRET = $_ENV["LIVEKIT_API_SECRET"] ?? "secret"; // (4)!
```

1. Import all necessary dependencies from the PHP LiveKit library.
2. Configure HTTP headers for the web server: enable CORS support, allow the `Content-Type` and `Authorization` headers and set the response content type to `application/json`.
3. The API key of LiveKit Server.
4. The API secret of LiveKit Server.

The `index.php` file imports the required dependencies, sets the HTTP headers for the web server and loads the necessary environment variables:

- `LIVEKIT_API_KEY`: the API key of LiveKit Server.
- `LIVEKIT_API_SECRET`: the API secret of LiveKit Server.

---

#### Create token

The endpoint `/token` accepts `POST` requests with a payload of type `application/json`, containing the following fields:

- `roomName`: the name of the Room where the user wants to connect.
- `participantName`: the name of the participant that wants to connect to the Room.

```php title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/php/index.php#L19-L43' target='_blank'>index.php</a>" linenums="18"
<?php
if (isset($_SERVER["REQUEST_METHOD"]) && $_SERVER["REQUEST_METHOD"] === "POST" && $_SERVER["PATH_INFO"] === "/token") {
    $data = json_decode(file_get_contents("php://input"), true);

    $roomName = $data["roomName"] ?? null;
    $participantName = $data["participantName"] ?? null;

    if (!$roomName || !$participantName) {
        http_response_code(400);
        echo json_encode(["errorMessage" => "roomName and participantName are required"]);
        exit();
    }

    $tokenOptions = (new AccessTokenOptions()) // (1)!
        ->setIdentity($participantName);
    $videoGrant = (new VideoGrant()) // (2)!
        ->setRoomJoin()
        ->setRoomName($roomName);
    $token = (new AccessToken($LIVEKIT_API_KEY, $LIVEKIT_API_SECRET)) // (3)!
        ->init($tokenOptions)
        ->setGrant($videoGrant)
        ->toJwt();

    echo json_encode(["token" => $token]); // (4)!
    exit();
}
```

1. Create an `AccessTokenOptions` object with the participant's identity.
2. Create a `VideoGrant` object setting the necessary video grants options. `setRoomJoin` allows the user to join a room and `setRoomName` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. We create the `AccessToken` providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, initialize it with the token options, set the video grants and generate the JWT token.
4. Finally, the token is sent back to the client.

The endpoint first obtains the `roomName` and `participantName` parameters from the request body. If they are not available, it returns a `400` error.

If required fields are available, a new JWT token is created. For that we use the [LiveKit PHP SDK](https://github.com/agence104/livekit-server-sdk-php){:target="\_blank"}:

1. Create an `AccessTokenOptions` object with the participant's identity.
2. Create a `VideoGrant` object setting the necessary video grants options. `setRoomJoin` allows the user to join a room and `setRoomName` determines the specific room. Check out all [Video Grants](https://docs.livekit.io/realtime/concepts/authentication/#Video-grant){:target="\_blank"}.
3. We create the `AccessToken` providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, initialize it with the token options, set the video grants and generate the JWT token.
4. Finally, the token is sent back to the client.

---

#### Receive webhook

The endpoint `/webhook` accepts `POST` requests with a payload of type `application/webhook+json`. This is the endpoint where LiveKit Server will send [webhook events](https://docs.livekit.io/realtime/server/webhooks/#Events){:target="\_blank"}.

```php title="<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/php/index.php#L45-L62' target='_blank'>index.php</a>" linenums="44"
<?php
$webhookReceiver = (new WebhookReceiver($LIVEKIT_API_KEY, $LIVEKIT_API_SECRET)); // (1)!

if (isset($_SERVER["REQUEST_METHOD"]) && $_SERVER["REQUEST_METHOD"] === "POST" && $_SERVER["PATH_INFO"] === "/webhook") {
    $headers = getallheaders();
    $authHeader = $headers["Authorization"]; // (2)!
    $body = file_get_contents("php://input"); // (3)!
    try {
        $event = $webhookReceiver->receive($body, $authHeader); // (4)!
        error_log("LiveKit Webhook:");
        error_log(print_r($event->getEvent(), true)); // (5)!
        exit();
    } catch (Exception $e) {
        http_response_code(401);
        echo "Error validating webhook event";
        echo json_encode($e->getMessage());
        exit();
    }
}
```

1. Create a new `WebhookReceiver` object providing the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. It will help validating and decoding incoming [webhook events](https://docs.livekit.io/realtime/server/webhooks/){target=\_blank}.
2. The `Authorization` header of the HTTP request.
3. The raw body of the HTTP request as a string.
4. Obtain the `WebhookEvent` object using the `WebhookReceiver#receive` method. It takes the raw body as a String and the Authorization header of the request.
5. Consume the event as you wish.

We first create a `WebhookReceiver` object using the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`. Then we must retrieve the `Authorization` header and the raw body of the HTTP request. We need both of them to validate and decode the incoming webhook event.

Finally, we obtain the `WebhookEvent` object using the `WebhookReceiver#receive` method. It takes the raw body as a String and the Authorization header of the request. We can consume the event as we wish (in this case, we just log it using the error output).

<br>
