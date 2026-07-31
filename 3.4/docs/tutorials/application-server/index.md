# Application Server Tutorials

Every application server below has two specific purposes:

- Generate LiveKit tokens on demand for any [application client](https://openvidu.io/3.4/docs/tutorials/application-client/index.md).
- Receive LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/) .

To do so they all define two REST endpoints:

- `/token`: takes a room and participant name and returns a token.
- `/webhook`: for receiving webhook events from LiveKit Server.

They use the proper [LiveKit Server SDK](https://docs.livekit.io/reference/) for their language, if available.

[**Node.js**](https://openvidu.io/3.4/docs/tutorials/application-server/node/)

[**Go**](https://openvidu.io/3.4/docs/tutorials/application-server/go/)

[**Ruby**](https://openvidu.io/3.4/docs/tutorials/application-server/ruby/)

[**Java**](https://openvidu.io/3.4/docs/tutorials/application-server/java/)

[**Python**](https://openvidu.io/3.4/docs/tutorials/application-server/python/)

[**Rust**](https://openvidu.io/3.4/docs/tutorials/application-server/rust/)

[**PHP**](https://openvidu.io/3.4/docs/tutorials/application-server/php/)

[**.NET**](https://openvidu.io/3.4/docs/tutorials/application-server/dotnet/)
