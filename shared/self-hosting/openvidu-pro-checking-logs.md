## Checking logs

If any of the services are not working as expected, you can check the logs of the services using the following command:

```bash
cd /opt/openvidu/
docker compose logs <service-name>
```

Replace `<service-name>` with the name of the service you want to check. For example, to check the logs of the OpenVidu Server, use the following command:

```bash
cd /opt/openvidu/
docker compose logs openvidu
```

To check the logs of all services, use the following command:

```bash
cd /opt/openvidu/
docker compose logs
```

You can also review your logs using the Grafana dashboard provided with OpenVidu. To access it, go to [https://<your-domain.com\>/grafana](https://<your-domain.com>/grafana){:target=\_blank} and use the credentials located in `/opt/openvidu/.env` to log in. Once inside, navigate to the _"Home"_ section, select _"Dashboard"_, and then click on:

- _"OpenVidu > OpenVidu Cluster Nodes Logs"_: To check the logs of the OpenVidu services organized per node.
- _"OpenVidu > OpenVidu Cluster Services Logs"_: To check the logs of the OpenVidu services organized per service.
