---
title: OpenVidu Elastic administration on-premises
description: Learn how to perform administrative tasks on an on-premises OpenVidu Elastic deployment
---

# <span span class="openvidu-tag openvidu-pro-tag" style="font-size: .5em">PRO</span> OpenVidu Elastic Administration: On-premises

The OpenVidu installer offers an easy way to deploy OpenVidu Elastic on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

This section provides details on configuration parameters and common administrative tasks for on-premises OpenVidu Elastic deployments.

## Starting, stopping, and restarting OpenVidu

To start, stop, or restart any Node in your OpenVidu Elastic deployment, you can use the following commands:

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

=== "Master Node"

    The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

    ```bash
    NAME                       IMAGE                                              COMMAND                  SERVICE                    CREATED          STATUS
    app                        docker.io/openvidu/openvidu-call                   "docker-entrypoint.s…"   app                        12 seconds ago   Up 10 seconds
    caddy                      docker.io/openvidu/openvidu-pro-caddy              "/bin/caddy run --co…"   caddy                      12 seconds ago   Up 10 seconds
    dashboard                  docker.io/openvidu/openvidu-pro-dashboard          "./openvidu-dashboard"   dashboard                  12 seconds ago   Up 10 seconds
    grafana                    docker.io/grafana/grafana                          "/run.sh"                grafana                    11 seconds ago   Up 8 seconds
    loki                       docker.io/grafana/loki                             "/usr/bin/loki -conf…"   loki                       11 seconds ago   Up 9 seconds
    mimir                      docker.io/grafana/mimir                            "/bin/mimir -config.…"   mimir                      11 seconds ago   Up 9 seconds
    minio                      docker.io/bitnami/minio                            "/opt/bitnami/script…"   minio                      11 seconds ago   Up 9 seconds
    mongo                      docker.io/mongo                                    "docker-entrypoint.s…"   mongo                      11 seconds ago   Up 9 seconds
    openvidu-v2compatibility   docker.io/openvidu/openvidu-v2compatibility        "/bin/server"            openvidu-v2compatibility   12 seconds ago   Up 10 seconds
    operator                   docker.io/openvidu/openvidu-operator               "/bin/operator"          operator                   12 seconds ago   Up 10 seconds
    promtail                   docker.io/grafana/promtail                         "/usr/bin/promtail -…"   promtail                   11 seconds ago   Up 9 seconds
    redis                      docker.io/redis                                    "docker-entrypoint.s…"   redis                      12 seconds ago   Up 10 seconds
    ```

=== "Media Node"

    The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

    ```bash
    NAME         IMAGE                                          COMMAND                  SERVICE      CREATED          STATUS
    egress       docker.io/livekit/egress                       "/entrypoint.sh"         egress       53 seconds ago   Up 51 seconds
    ingress      docker.io/livekit/ingress                      "ingress"                ingress      53 seconds ago   Up 52 seconds
    openvidu     docker.io/openvidu/openvidu-server-pro         "/livekit-server --c…"   openvidu     53 seconds ago   Up 52 seconds
    prometheus   docker.io/prom/prometheus                      "/bin/prometheus --c…"   prometheus   53 seconds ago   Up 51 seconds
    promtail     docker.io/grafana/promtail                     "/usr/bin/promtail -…"   promtail     53 seconds ago   Up 52 seconds
    ```

--8<-- "shared/self-hosting/openvidu-pro-checking-logs.md"

## Adding Media Nodes

To add a new Media Node, simply spin up a new VM and run the OpenVidu installer script to integrate it into the existing cluster. Run the [installation command](install.md#media-node) on the new Media Node.

--8<-- "shared/self-hosting/openvidu-pro-removing-media-nodes.md"

## Changing the configuration

You can check how to change the configuration in the [Changing Configuration](../../configuration/changing-config.md) section. Also, there are multiple guides in the [How to Guides](../../how-to-guides/index.md) section that can help you with specific configuration changes.

## Uninstalling OpenVidu

To uninstall any OpenVidu Node, just execute the following commands:

```bash
sudo su
systemctl stop openvidu
rm -rf /opt/openvidu/
rm /etc/systemd/system/openvidu.service
rm /etc/sysctl.d/50-openvidu.conf
```
