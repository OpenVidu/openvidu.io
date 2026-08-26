# OpenVidu Single Node **PRO** administration: On-premises

On-premises

The OpenVidu installer offers an easy way to deploy OpenVidu Single Node **PRO** on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

This section provides details on configuration parameters and common administrative tasks for this deployment.

## Starting, stopping, and restarting OpenVidu

You can start, stop, and restart the OpenVidu services using the following commands:

**Start OpenVidu**

```bash
sudo systemctl start openvidu
```

**Stop OpenVidu**

```bash
sudo systemctl stop openvidu
```

**Restart OpenVidu**

```bash
sudo systemctl restart openvidu
```

## Checking the status of services

You can check the status of the OpenVidu services using the following command:

```bash
cd /opt/openvidu/
docker compose ps
```

The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

```bash
NAME                       IMAGE                                              COMMAND                   SERVICE                    CREATED          STATUS
app                        docker.io/openvidu/openvidu-call:main              "docker-entrypoint.s…"    app                        18 seconds ago   Up 7 seconds
caddy                      docker.io/openvidu/openvidu-pro-caddy:main         "/bin/caddy run --co…"    caddy                      18 seconds ago   Up 8 seconds
dashboard                  docker.io/openvidu/openvidu-pro-dashboard:main     "./openvidu-dashboard"    dashboard                  18 seconds ago   Up 8 seconds
egress                     docker.io/livekit/egress:v1.9.0                    "/entrypoint.sh"          egress                     18 seconds ago   Up 5 seconds
grafana                    docker.io/grafana/grafana:11.5.1                   "/bin/sh -c '\n  if !…"   grafana                    17 seconds ago   Up 4 seconds
ingress                    docker.io/openvidu/ingress:main                    "ingress"                 ingress                    18 seconds ago   Up 6 seconds
loki                       docker.io/grafana/loki:3.3.2                       "/bin/sh -c '\n  if !…"   loki                       18 seconds ago   Up 6 seconds
minio                      docker.io/bitnami/minio:2025.2.7-debian-12-r0      "/bin/sh -c '\n  . /c…"   minio                      18 seconds ago   Up 8 seconds
mongo                      docker.io/mongo:8.0.4                              "/bin/sh -c '\n  . /c…"   mongo                      18 seconds ago   Up 15 seconds
openvidu                   docker.io/openvidu/openvidu-server-pro:main        "/livekit-server --c…"    openvidu                   18 seconds ago   Up 5 seconds
openvidu-v2compatibility   docker.io/openvidu/openvidu-v2compatibility:main   "/bin/entrypoint.sh"      openvidu-v2compatibility   18 seconds ago   Up 6 seconds
operator                   docker.io/openvidu/openvidu-operator:main          "/bin/operator"           operator                   18 seconds ago   Up 5 seconds
prometheus                 docker.io/prom/prometheus:v3.1.0                   "/bin/sh -c '\n  if !…"   prometheus                 17 seconds ago   Up 5 seconds
alloy                      docker.io/grafana/alloy:v1.17.0                    "/bin/sh -c '\n  if !…"   alloy                      18 seconds ago   Up 5 seconds
redis                      docker.io/redis:7.4.2-alpine                       "/bin/sh -c '\n  . /c…"   redis                      18 seconds ago   Up 6 seconds
```

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

Or use journalctl:

```bash
journalctl -f -u openvidu
```

You can also review your logs using the Grafana dashboard provided with OpenVidu. To access it, go to `https://<your-domain.com>/grafana` and use the credentials located in `/opt/openvidu/.env` to log in. Once inside, navigate to the *"Home"* section, select *"Dashboard"*, and then click on *"OpenVidu > OpenVidu Logs"*. All the logs will be displayed there.

## Changing the configuration

You can check how to change the configuration in the [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md) section. Also, there are multiple guides in the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) section that can help you with specific configuration changes.

## Uninstalling OpenVidu

To uninstall OpenVidu, just execute the following commands:

```bash
sudo su
systemctl stop openvidu
rm -rf /opt/openvidu/
rm /etc/systemd/system/openvidu.service
rm /etc/sysctl.d/50-openvidu.conf
```

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
