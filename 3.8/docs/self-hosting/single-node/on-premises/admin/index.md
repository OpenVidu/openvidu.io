# OpenVidu Single Node COMMUNITY administration: On-premises

On-premises

The OpenVidu installer offers an easy way to deploy OpenVidu Single Node COMMUNITY on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

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
NAME         IMAGE                                        COMMAND                  SERVICE      CREATED          STATUS
meet         docker.io/openvidu/openvidu-meet             "docker-entrypoint.s…"   meet         19 seconds ago   Up 16 seconds
caddy        docker.io/openvidu/openvidu-caddy            "/bin/caddy run --co…"   caddy        19 seconds ago   Up 16 seconds
dashboard    docker.io/openvidu/openvidu-dashboard        "./openvidu-dashboard"   dashboard    19 seconds ago   Up 16 seconds
egress       docker.io/livekit/egress                     "/entrypoint.sh"         egress       18 seconds ago   Up 14 seconds
grafana      docker.io/grafana/grafana                    "/run.sh"                grafana      18 seconds ago   Up 13 seconds
ingress      docker.io/livekit/ingress                    "ingress"                ingress      19 seconds ago   Up 14 seconds
loki         docker.io/grafana/loki                       "/usr/bin/loki -conf…"   loki         18 seconds ago   Up 14 seconds
minio        docker.io/bitnami/minio                      "/opt/bitnami/script…"   minio        18 seconds ago   Up 14 seconds
mongo        docker.io/mongo                              "docker-entrypoint.s…"   mongo        18 seconds ago   Up 15 seconds
openvidu     docker.io/openvidu/openvidu-server           "/livekit-server --c…"   openvidu     19 seconds ago   Up 14 seconds
prometheus   docker.io/prom/prometheus                    "/bin/prometheus --c…"   prometheus   18 seconds ago   Up 14 seconds
alloy        docker.io/grafana/alloy                      "/usr/bin/alloy -…"      alloy        18 seconds ago   Up 14 seconds
redis        docker.io/redis                              "docker-entrypoint.s…"   redis        19 seconds ago   Up 15 seconds
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

You can also review your logs using the Grafana dashboard provided with OpenVidu. To access it, go to https://\<your-domain.com>/grafana{:target="*blank"} and use the credentials located in `/opt/openvidu/.env` to log in. Once inside, navigate to the* "Home" *section, select* "Dashboard"*, and then click on* "OpenVidu > OpenVidu Logs"\_. All the logs will be displayed there.

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
