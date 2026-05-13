# Application Server Tutorials

Every application server below has two specific purposes:

- Generate LiveKit tokens on demand for any [application client](https://openvidu.io/3.4.1/docs/tutorials/application-client/index.md).
- Receive LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/) .

To do so they all define two REST endpoints:

- `/token`: takes a room and participant name and returns a token.
- `/webhook`: for receiving webhook events from LiveKit Server.

They use the proper [LiveKit Server SDK](https://docs.livekit.io/reference/) for their language, if available.

[**Node.js**](https://openvidu.io/3.4.1/docs/tutorials/application-server/node/index.md)

[**Go**](https://openvidu.io/3.4.1/docs/tutorials/application-server/go/index.md)

[**Ruby**](https://openvidu.io/3.4.1/docs/tutorials/application-server/ruby/index.md)

[**Java**](https://openvidu.io/3.4.1/docs/tutorials/application-server/java/index.md)

[**Python**](https://openvidu.io/3.4.1/docs/tutorials/application-server/python/index.md)

[**Rust**](https://openvidu.io/3.4.1/docs/tutorials/application-server/rust/index.md)

[**PHP**](https://openvidu.io/3.4.1/docs/tutorials/application-server/php/index.md)

[**.NET**](https://openvidu.io/3.4.1/docs/tutorials/application-server/dotnet/index.md)
