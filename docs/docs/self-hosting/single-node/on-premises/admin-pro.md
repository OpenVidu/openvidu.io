---
title: OpenVidu Single Node PRO administration on-premises
description: Learn how to perform administrative tasks on an on-premises OpenVidu Single Node PRO deployment
---

# <span class="openvidu-tag openvidu-pro-tag" style="font-size: .5em">PRO</span> OpenVidu Single Node PRO Administration: On-premises

The OpenVidu installer offers an easy way to deploy OpenVidu Single Node <span class="openvidu-tag openvidu-pro-tag" style="font-size: .5em">PRO</span> on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

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
promtail                   docker.io/grafana/promtail:3.3.2                   "/bin/sh -c '\n  if !…"   promtail                   18 seconds ago   Up 5 seconds
redis                      docker.io/redis:7.4.2-alpine                       "/bin/sh -c '\n  . /c…"   redis                      18 seconds ago   Up 6 seconds
```

--8<-- "shared/self-hosting/single-node/admin-checking-logs.md"

--8<-- "shared/self-hosting/single-node/admin-change-config.md"
