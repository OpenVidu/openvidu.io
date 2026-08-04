# OpenVidu High Availability administration: On-premises

On-premises

The OpenVidu installer offers an easy way to deploy OpenVidu High Availability on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

This section provides details on configuration parameters and common administrative tasks for on-premises OpenVidu High Availability deployments.

## Starting, stopping, and restarting OpenVidu

To start, stop, or restart any Node in your OpenVidu High Availability deployment, you can use the following commands:

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

Depending on the node type, you will see different services running.

**Master Node**

The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

```bash
NAME                       IMAGE                                              COMMAND                  SERVICE                    CREATED          STATUS
openvidu-meet              docker.io/openvidu/openvidu-call                   "docker-entrypoint.s…"   openvidu-meet              12 seconds ago   Up 10 seconds
caddy                      docker.io/openvidu/openvidu-pro-caddy              "/bin/caddy run --co…"   caddy                      12 seconds ago   Up 10 seconds
dashboard                  docker.io/openvidu/openvidu-pro-dashboard          "./openvidu-dashboard"   dashboard                  12 seconds ago   Up 10 seconds
grafana                    docker.io/grafana/grafana                          "/run.sh"                grafana                    11 seconds ago   Up 8 seconds
loki                       docker.io/grafana/loki                             "/usr/bin/loki -conf…"   loki                       11 seconds ago   Up 9 seconds
mimir                      docker.io/grafana/mimir                            "/bin/mimir -config.…"   mimir                      11 seconds ago   Up 9 seconds
minio                      docker.io/bitnami/minio                            "/opt/bitnami/script…"   minio                      11 seconds ago   Up 9 seconds
mongo                      docker.io/mongo                                    "docker-entrypoint.s…"   mongo                      11 seconds ago   Up 9 seconds
openvidu-v2compatibility   docker.io/openvidu/openvidu-v2compatibility        "/bin/server"            openvidu-v2compatibility   12 seconds ago   Up 10 seconds
operator                   docker.io/openvidu/openvidu-operator               "/bin/operator"          operator                   12 seconds ago   Up 10 seconds
alloy                      docker.io/grafana/alloy                            "/usr/bin/alloy -…"      alloy                      11 seconds ago   Up 9 seconds
redis-sentinel             docker.io/redis                                    "docker-entrypoint.s…"   redis-sentinel             10 seconds ago   Up 10 seconds
redis-server               docker.io/redis                                    "docker-entrypoint.s…"   redis-server               10 seconds ago   Up 10 seconds
```

**Media Node**

The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

```bash
NAME         IMAGE                                          COMMAND                  SERVICE      CREATED          STATUS
caddy        docker.io/openvidu/openvidu-caddy:main         "/bin/caddy run --co…"   caddy        53 seconds ago   Up 53 seconds
egress       docker.io/livekit/egress                       "/entrypoint.sh"         egress       53 seconds ago   Up 51 seconds
ingress      docker.io/livekit/ingress                      "ingress"                ingress      53 seconds ago   Up 52 seconds
openvidu     docker.io/openvidu/openvidu-server-pro         "/livekit-server --c…"   openvidu     53 seconds ago   Up 52 seconds
prometheus   docker.io/prom/prometheus                      "/bin/prometheus --c…"   prometheus   53 seconds ago   Up 51 seconds
alloy        docker.io/grafana/alloy                        "/usr/bin/alloy -…"      alloy        53 seconds ago   Up 52 seconds
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

You can also review your logs using the Grafana dashboard provided with OpenVidu. To access it, go to https://\<your-domain.com>/grafana and use the credentials located in `/opt/openvidu/.env` to log in. Once inside, navigate to the *"Home"* section, select *"Dashboard"*, and then click on:

- *"OpenVidu > OpenVidu Cluster Nodes Logs"*: To check the logs of the OpenVidu services organized per node.
- *"OpenVidu > OpenVidu Cluster Services Logs"*: To check the logs of the OpenVidu services organized per service.

## Adding Media Nodes

To add a new Media Node, simply spin up a new VM and run the OpenVidu installer script to integrate it into the existing cluster. Run the [installation command](https://openvidu.io/3.8/docs/self-hosting/ha/on-premises/install-nlb/#media-node) on the new Media Node.

## Removing Media Nodes Gracefully

To stop a Media Node gracefully, you need to stop the containers `openvidu`, `ingress`, and `egress` with a `SIGQUIT` signal. Here is a simple script that you can use to stop all these containers gracefully:

```bash
#!/bin/bash
# Stop OpenVidu, Ingress, and Egress containers gracefully (1)
docker container kill --signal=SIGQUIT openvidu || true
docker container kill --signal=SIGQUIT ingress || true
docker container kill --signal=SIGQUIT egress || true
for agent_container in $(docker ps --filter "label=openvidu-agent=true" --format '{{.Names}}'); do
    docker container kill --signal=SIGQUIT "$agent_container"
done

# Wait for the containers to stop (2)
while [ $(docker ps --filter "label=openvidu-agent=true" -q | wc -l) -gt 0 ] || \
    [ $(docker inspect -f '{{.State.Running}}' openvidu 2>/dev/null) == "true" ] || \
    [ $(docker inspect -f '{{.State.Running}}' ingress 2>/dev/null) == "true" ] || \
    [ $(docker inspect -f '{{.State.Running}}' egress 2>/dev/null) == "true" ]; do
    echo "Waiting for containers to stop..."
    sleep 5
done
```

1. This script stops the OpenVidu, Ingress, Egress and AI Agents containers gracefully. The `true` at the end of each command is to avoid the script from stopping if the container is not running.
1. This script waits for the containers to stop before exiting.

When all the containers are stopped, you can then stop the systemd service and remove the VM:

```text
sudo systemctl stop openvidu
```

## Removing Media Nodes Forcefully

To remove a Media Node forcefully, without considering the rooms, ingress, egress and agents hosted by the node, you can simply stop the OpenVidu service in the Media Node and delete the VM.

```bash
sudo systemctl stop openvidu
```

## Changing the configuration

You can check how to change the configuration in the [Changing Configuration](https://openvidu.io/3.8/docs/self-hosting/configuration/changing-config/index.md) section. Also, there are multiple guides in the [How to Guides](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/index.md) section that can help you with specific configuration changes.

## Uninstalling OpenVidu

To uninstall any OpenVidu Node, just execute the following commands:

```bash
sudo su
systemctl stop openvidu
rm -rf /opt/openvidu/
rm /etc/systemd/system/openvidu.service
rm /etc/sysctl.d/50-openvidu.conf
```

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](https://openvidu.io/3.8/docs/self-hosting/how-to-guides/backup-and-restore/index.md) guide for recommended backup workflows.
