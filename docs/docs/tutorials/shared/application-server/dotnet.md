To run this server application, you need [.NET](https://dotnet.microsoft.com/en-us/download){:target="\_blank"} installed on your device.

1. Navigate into the server directory
```bash
cd openvidu-livekit-tutorials/application-server/dotnet
```
2. Run the application
```bash
dotnet run
```

!!! warning

    This .NET server application needs the `LIVEKIT_API_SECRET` env variable to be at least 32 characters long. Make sure to update it [here](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/b97db7278227470fd386337ffde49b2458315c6f/application-server/dotnet/appsettings.json#L11){:target="\_blank"} and in your [OpenVidu Server](#1-run-openvidu-server).
