## 1. Run OpenVidu Meet

--8<-- "shared/tutorials/run-openvidu-server.md"

## 2. Generate an API key

1. Connect to OpenVidu Meet at `https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/`.
2. Navigate to "Embedded" page.
3. Click on ":material-key: Generate API Key" button.

## 3. Create a room

> Remember to replace `YOUR_OPENVIDU_DEPLOYMENT_DOMAIN` and `YOUR_API_KEY` in the snippets below.

=== ":material-bash:{.icon .lg-icon .tab-icon} curl"

    ```bash
    curl --request POST \
        --url https://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms \
        --header 'Accept: application/json' \
        --header 'Content-Type: application/json' \
        --header 'X-API-KEY: YOUR_API_KEY' \
        --data '{"roomIdPrefix": "quickstart-room"}'
    ```

=== ":simple-nodedotjs:{.icon .lg-icon .tab-icon} Node.js"

    ```javascript
    const http = require('http');

    const options = {
        method: 'POST',
        hostname: 'YOUR_OPENVIDU_DEPLOYMENT_DOMAIN',
        port: '443',
        path: '/api/v1/rooms',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-API-KEY': 'YOUR_API_KEY'
        }
    };

    const req = http.request(options, function (res) {
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
        roomIdPrefix: 'quickstart-room',
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

        url := "http://YOUR_OPENVIDU_DEPLOYMENT_DOMAIN/api/v1/rooms"

        payload := strings.NewReader("{\"roomIdPrefix\":\"quickstart-room\"}")

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

    ```

=== ":fontawesome-brands-java:{.icon .lg-icon .tab-icon} Java"

    ```java

    ```

=== ":fontawesome-brands-python:{.icon .lg-icon .tab-icon} Python"

    ```python
    
    ```

=== ":simple-rust:{.icon .lg-icon .tab-icon} Rust"

    ```rust
    
    ```

=== ":simple-php:{.icon .lg-icon .tab-icon} PHP"

    ```php

    ```

=== ":simple-dotnet:{.icon .lg-icon .tab-icon} .NET"

    ```csharp

    ```

## 3. Embed the OpenVidu Meet component into your application

You can use a **Web Component** or an **iframe**.

=== ":simple-webcomponentsdotorg:{.icon .tab-icon} Web Component"

    ```html
    <html>
        <head>
            <script src="https://{{ your-openvidu-deployment-domain }}/v1/openvidu-meet.js"></script>
        </head>
        <body>
            <div>
                <openvidu-meet room-url="{{ my-room-url }}"></openvidu-meet>
            </div>
        </body>
    </html>
    ```

=== ":material-code-tags:{.icon .tab-icon} iframe"

    ```html
    <html>
        <head>
            <script src="https://{{ your-openvidu-deployment-domain }}/v1/openvidu-meet.js"></script>
        </head>
        <body>
            <div>
                <iframe
                    src="https://{{ your-openvidu-deployment-domain }}/v1/openvidu-meet?room={{ my-room-url }}"
                    width="100%"
                    height="100%"
                    frameborder="0"
                    allowfullscreen>
                </iframe>
            </div>
        </body>
    </html>
    ```
