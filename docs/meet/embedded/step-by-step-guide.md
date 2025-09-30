---
title: Step by step guide
tags:
  - setupcustomgallery
---

## 1. Run OpenVidu Meet

--8<-- "shared/tutorials/run-openvidu-meet.md"

## 2. Create a room

You can create a room from the **"Rooms"** page in OpenVidu Meet:

<a class="glightbox" href="../../../assets/videos/meet/meet-rooms-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../assets/videos/meet/meet-rooms-dark.mp4#only-dark" loading="lazy" defer muted playsinline autoplay loop async></video></a>
<a class="glightbox" href="../../../assets/videos/meet/meet-rooms-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="../../../assets/videos/meet/meet-rooms-light.mp4#only-light" loading="lazy" defer muted playsinline autoplay loop async></video></a>

### Automating room creation

You can automate the room creation process by using the [OpenVidu Meet REST API](../embedded/reference/rest-api.md). This allows you to create rooms programmatically from your application's backend, without manual intervention.

Check out the [API reference for creating rooms :fontawesome-solid-external-link:{.external-link-icon}](../../assets/htmls/rest-api.html#/operations/createRoom){:target="_blank"}. Below you have copy-paste snippets for most common languages.

!!! info
    Remember to replace **`YOUR_OPENVIDU_DEPLOYMENT_DOMAIN`** and **`YOUR_API_KEY`** in the snippets below.

=== ":material-bash:{.icon .lg-icon .tab-icon} curl"

    ```bash
    curl --request POST \
        --url https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms \
        --header 'Accept: application/json' \
        --header 'Content-Type: application/json' \
        --header 'X-API-KEY: YOUR_API_KEY' \
        --data '{"roomIdPrefix": "my-room"}'
    ```

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    ```javascript
    const https = require('https');

    const options = {
        method: 'POST',
        hostname: 'YOUR_OPENVIDU_DEPLOYMENT_DOMAIN',
        port: 443,
        path: '/api/v1/rooms',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-API-KEY': 'YOUR_API_KEY'
        }
    };

    const req = https.request(options, function (res) {
        const chunks = [];
        res.on('data', function (chunk) {
            chunks.push(chunk);
        });
        res.on('end', function () {
            const body = Buffer.concat(chunks);
            console.log(body.toString());
        });
    });

    req.write(JSON.stringify({
        roomIdPrefix: 'my-room',
    }));

    req.end();
    ```

=== ":simple-goland:{.icon .lg-icon .tab-icon} Go"

    ```go
    package main

    import (
        "fmt"
        "strings"
        "net/http"
        "io"
    )

    func main() {

        url := "https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms"

        payload := strings.NewReader("{\"roomIdPrefix\":\"my-room\"}")

        req, _ := http.NewRequest("POST", url, payload)

        req.Header.Add("Content-Type", "application/json")
        req.Header.Add("Accept", "application/json")
        req.Header.Add("X-API-KEY", "YOUR_API_KEY")

        res, _ := http.DefaultClient.Do(req)

        defer res.Body.Close()
        body, _ := io.ReadAll(res.Body)

        fmt.Println(res)
        fmt.Println(string(body))

    }
    ```

=== ":simple-ruby:{.icon .lg-icon .tab-icon} Ruby"

    ```ruby
    require 'uri'
    require 'net/http'
    require 'openssl'

    url = URI("https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms")

    http = Net::HTTP.new(url.host, url.port)
    http.use_ssl = true

    request = Net::HTTP::Post.new(url)
    request["Content-Type"] = 'application/json'
    request["Accept"] = 'application/json'
    request["X-API-KEY"] = 'YOUR_API_KEY'
    request.body = "{\"roomIdPrefix\": \"my-room\"}"

    response = http.request(request)
    puts response.read_body
    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    ```java
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms"))
        .header("Content-Type", "application/json")
        .header("Accept", "application/json")
        .header("X-API-KEY", "YOUR_API_KEY")
        .method("POST", HttpRequest.BodyPublishers.ofString("{\"roomIdPrefix\": \"my-room\"}"))
        .build();
    HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
    System.out.println(response.body());
    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    ```python
    import http.client

    conn = http.client.HTTPSConnection("YOUR_OPENVIDU_DEPLOYMENT_DOMAIN")

    payload = "{\"roomIdPrefix\": \"my-room\"}"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'X-API-KEY': "YOUR_API_KEY"
    }

    conn.request("POST", "/api/v1/rooms", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    ```rust
    // Cargo.toml:
    // reqwest = { version = "0.12", features = ["blocking", "rustls-tls"] }

    use reqwest::blocking::Client;
    use reqwest::header::{ACCEPT, CONTENT_TYPE};

    fn main() -> Result<(), Box<dyn std::error::Error>> {
        let client = Client::new();
        let url = "https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms";
        let payload = r#"{"roomIdPrefix": "my-room"}"#;

        let resp = client
            .post(url)
            .header(ACCEPT, "application/json")
            .header(CONTENT_TYPE, "application/json")
            .header("X-API-KEY", "YOUR_API_KEY")
            .body(payload)
            .send()?;

        println!("Status: {}", resp.status());
        println!("{}", resp.text()?);
        Ok(())
    }
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    ```php
    <?php

    $curl = curl_init();

    curl_setopt_array($curl, [
        CURLOPT_URL => "https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode(['roomIdPrefix' => 'my-room']),
        CURLOPT_HTTPHEADER => [
            "Accept: application/json",
            "Content-Type: application/json",
            "X-API-KEY: YOUR_API_KEY"
        ],
    ]);

    $response = curl_exec($curl);
    $err = curl_error($curl);

    curl_close($curl);

    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    ```csharp
    using System.Net.Http.Headers;
    var client = new HttpClient();
    var request = new HttpRequestMessage
    {
        Method = HttpMethod.Post,
        RequestUri = new Uri("https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms"),
        Headers =
        {
            { "Accept", "application/json" },
            { "X-API-KEY", "YOUR_API_KEY" },
        },
        Content = new StringContent("{\"roomIdPrefix\": \"my-room\"}")
        {
            Headers =
            {
                ContentType = new MediaTypeHeaderValue("application/json")
            }
        }
    };
    using (var response = await client.SendAsync(request))
    {
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadAsStringAsync();
        Console.WriteLine(body);
    }
    ```

The response to this request will be a JSON object as below. The required properties for the next step are `moderatorUrl` and `publisherUrl`, needed to embed the room into your application as explained in step 3.

```json hl_lines="18-19"
{
    "roomId": "my-room-123",
    "roomIdPrefix": "my-room",
    "creationDate": 1620000000000,
    "autoDeletionDate": 1900000000000,
    "preferences": {
        "chatPreferences": {
            "enabled": true
        },
        "recordingPreferences": {
            "enabled": true,
            "allowAccessTo": "admin-moderator-publisher"
        },
        "virtualBackgroundPreferences": {
            "enabled": true
        }
    },
    "moderatorUrl": "http://localhost:6080/room/my-room-123?secret=123456",
    "publisherUrl": "http://localhost:6080/room/my-room-123?secret=654321"
}
```

## 3. Get the room URL

To embed a room into your application's frontend you need the **room URL**. You can copy the room URL for each participant role from the "Rooms" page in OpenVidu Meet console:

<a class="glightbox" href="../../../assets/images/meet/embedded/share-room-link.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/embedded/share-room-link.png" loading="lazy" class="round-corners"/></a>

### Automating room URL retrieval

You can get the room URLs programmatically using the [OpenVidu Meet REST API](../embedded/reference/rest-api.md). They are available in properties `moderatorUrl` and `speakerUrl` of object [MeetRoom :fontawesome-solid-external-link:{.external-link-icon}](../../assets/htmls/rest-api.html#/schemas/MeetRoom){:target="_blank"}. This object is returned as a JSON response from methods:

- [Create a room :fontawesome-solid-external-link:{.external-link-icon}](../../assets/htmls/rest-api.html#/operations/createRoom){:target="_blank"}
- [Get a room :fontawesome-solid-external-link:{.external-link-icon}](../../assets/htmls/rest-api.html#/operations/getRoom){:target="_blank"}
- [Get all rooms :fontawesome-solid-external-link:{.external-link-icon}](../../assets/htmls/rest-api.html#/operations/getRooms){:target="_blank"}

## 4. Embed the room into your application

Once you got the desired room URL, there are 3 alternatives to embed the OpenVidu Meet room into your application's interface:

### Use a direct link

This is the simplest and easiest way to embed an OpenVidu Meet room into your application. It's a perfect fit if your frontend is a web application, and you don't need any custom elements in the video meeting UI: the polished UI of OpenVidu Meet will be displayed in its own browser tab.

Just link to the room URL from any element in your frontend. For example, with a simple `<a>` tag:

```html
<a href="{{ your-room-url }}">Join Room</a>
```

After clicking on the element, the user will be redirected to OpenVidu Meet, ready to join the room.

<a class="glightbox" href="../../../assets/videos/meet/embed-url.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery4"><video class="round-corners" src="../../../assets/videos/meet/embed-url.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>

!!! info
    You can customize the room by simply appending query parameters to the room URL. For example, you can redirect back to your application after the user leaves the room by appending this query param: <code class="no-break">https://{{ your-room-url }}<strong class="accent-code">&leave-redirect-url=https://myapp.com</strong></code>

    See [Passing attributes to a direct link](./reference/direct-link.md#attributes) for more information.

### Use the Web Component

The OpenVidu Meet Web Component is the best option if you want to integrate the OpenVidu Meet UI along your own custom UI. OpenVidu Meet will simply become another component of your UI, blending seamlessly with your application's design and logic.

Include a `<script>` tag to load the OpenVidu Meet Web Component definition from your OpenVidu deployment. Then, you can use the `<openvidu-meet>` custom element in your HTML, setting the `room-url` attribute.

!!! info
    Check out the [Web Component reference](./reference/webcomponent.md) for the complete list of attributes, commands and events offered by it.

```html
<html>
    <head>
        <title>My meeting</title>
        <script src="https://{{ your-openvidu-deployment-domain }}/v1/openvidu-meet.js"></script>
    </head>
    <body>
        <div>
            <openvidu-meet room-url="{{ your-room-url }}"></openvidu-meet>
        </div>
    </body>
</html>
```

<a class="glightbox" href="../../../assets/images/meet/embedded/webcomponent-meeting.png" data-type="image" data-desc-position="bottom" data-gallery="gallery5"><img src="../../../assets/images/meet/embedded/webcomponent-meeting.png" loading="lazy" class="round-corners"/></a>

### Use an iframe

Some applications may not allow including a Web Component. For these cases OpenVidu Meet can be embedded using a traditional iframe.

```html
<html>
    <head>
        <title>My meeting</title>
    </head>
    <body>
        <div>
            <iframe
                src="{{ your-room-url }}"
                allow="camera; microphone; display-capture; fullscreen; autoplay; compute-pressure;"
                width="100%" height="100%">
            </iframe>
        </div>
    </body>
</html>
```

The required iframe attributes are:

- `src`: the room URL.
- `allow`: the minimum permissions required by the iframe for the room to work fine. These are:
    - `camera`: allow access to the camera.
    - `microphone`: allow access to the microphone.
    - `display-capture`: allow screen sharing.
    - `fullscreen`: allow full screen mode.
    - `autoplay`: allow autoplay of media.
    - `compute-pressure`: allow access to the device's compute pressure API.

!!! info
    The same **attributes**, **commands** and **events** available for the Web Component may also be used in an iframe. Check out these sections to learn how:

    - [Pass attributes to an OpenVidu Meet iframe](./reference/iframe.md#attributes)
    - [Send commands to an OpenVidu Meet iframe](./reference/iframe.md#commands)
    - [Receive events from an OpenVidu Meet iframe](./reference/iframe.md#events)

## 5. Embed recordings into your application

If your use case includes recording your rooms, you can also embed them right into your app. You can embed the list of recordings of a room or directly show the player for a specific recording.

### Embed the list of recordings of a room

To show the list of recordings of a room, declare attribute **`show-recordings`** in the embedding element:

```html
<openvidu-meet room-url="{{ your-room-url }}" show-only-recordings="true"></openvidu-meet>
```

!!! info
    Checkout the Web Component's [attributes](./reference/webcomponent.md#attributes) section for more information.

This will show the list of recordings for the specified room:

<a class="glightbox" href="../../../assets/images/meet/embedded/webcomponent-recording-list.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/embedded/webcomponent-recording-list.png" loading="lazy" class="round-corners"/></a>

### Embed the player for a specific recording

To show the player for a specific recording, replace attribute `room-url` with **`recording-url`** in the embedding element. The recording URL can be obtained from:

- [OpenVidu Meet console](../../features/recordings/#sharing-recordings-via-link)
- [Programmatically via REST API :fontawesome-solid-external-link:{.external-link-icon}](../../assets/htmls/rest-api.html#/operations/getRecordingUrl){:target="_blank"}

```html
<openvidu-meet recording-url="{{ your-recording-url }}"></openvidu-meet>
```

!!! info
    Checkout the Web Component's [attributes](./reference/webcomponent.md#attributes) section for more information.

This will show the player for the specified recording:

<a class="glightbox" href="../../../assets/images/meet/embedded/webcomponent-recording-player.png" data-type="image" data-desc-position="bottom" data-gallery="gallery3"><img src="../../../assets/images/meet/embedded/webcomponent-recording-player.png" loading="lazy" class="round-corners"/></a>

## 6. REST API and Webhooks

Up to this point everything has been focused on the client-side integration of OpenVidu Meet. To integrate OpenVidu Meet into your application's backend you have available:

- [REST API](./reference/rest-api.md): manage rooms and recordings programmatically.
- [Webhooks](./reference/webhooks.md): listen to events happening in real time.