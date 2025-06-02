---
title: OpenVidu Single Node administration on-premises
description: Learn how to perform administrative tasks on an on-premises OpenVidu Single Node deployment
---

# <span class="openvidu-tag openvidu-community-tag" style="font-size: .5em">COMMUNITY</span> OpenVidu Single Node Administration: On-premises

The OpenVidu installer offers an easy way to deploy OpenVidu Single Node <span class="openvidu-tag openvidu-community-tag" style="font-size: .5em">COMMUNITY</span> on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

This section provides details on configuration parameters and common administrative tasks for this deployment.

--8<-- "shared/self-hosting/single-node/admin-start-stop.md"

## Checking the status of services

You can check the status of the OpenVidu services using the following command:

```bash
cd /opt/openvidu/
docker compose ps
```

The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

```bash
NAME         IMAGE                                        COMMAND                  SERVICE      CREATED          STATUS
app          docker.io/openvidu/openvidu-call             "docker-entrypoint.s…"   app          19 seconds ago   Up 16 seconds
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
promtail     docker.io/grafana/promtail                   "/usr/bin/promtail -…"   promtail     18 seconds ago   Up 14 seconds
redis        docker.io/redis                              "docker-entrypoint.s…"   redis        19 seconds ago   Up 15 seconds
```

--8<-- "shared/self-hosting/single-node/admin-checking-logs.md"

--8<-- "shared/self-hosting/single-node/admin-change-config.md"

--8<-- "shared/self-hosting/single-node/admin-uninstall.md"
