# Application Server Tutorials

Every application server below has two specific purposes:

- Generate LiveKit tokens on demand for any [application client](../application-client/).
- Receive LiveKit [webhook events](https://docs.livekit.io/home/server/webhooks/) .

To do so they all define two REST endpoints:

- `/token`: takes a room and participant name and returns a token.
- `/webhook`: for receiving webhook events from LiveKit Server.

They use the proper [LiveKit Server SDK](https://docs.livekit.io/reference/) for their language, if available.

[**Node.js**](node/)

[**Go**](go/)

[**Ruby**](ruby/)

[**Java**](java/)

[**Python**](python/)

[**Rust**](rust/)

[**PHP**](php/)

[**.NET**](dotnet/)
