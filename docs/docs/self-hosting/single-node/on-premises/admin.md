---
title: "Administer OpenVidu Single Node on-premises"
description: "Administer OpenVidu Single Node on your own servers: check the status of every service, and back up and restore its data."
---

# OpenVidu Single Node administration: On-premises

<div class="provider-chip" markdown>

:material-server:{ .provider-chip-icon } On-premises

</div>


The OpenVidu installer offers an easy way to deploy OpenVidu Single Node on-premises. However, once the deployment is complete, you may need to perform administrative tasks based on your specific requirements, such as changing passwords, specifying custom configurations, and starting or stopping services.

This section provides details on configuration parameters and common administrative tasks for this deployment.

--8<-- "self-hosting/on-premises/single-node/admin-start-stop.md"

## Checking the status of services

You can check the status of the OpenVidu services using the following command:

```bash
cd /opt/openvidu/
docker compose ps
```

The services are operating correctly if you see an output similar to the following and there are no restarts from any of the services:

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

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

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

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

--8<-- "self-hosting/on-premises/single-node/admin-checking-logs.md"

--8<-- "self-hosting/on-premises/single-node/admin-change-config.md"

--8<-- "self-hosting/on-premises/single-node/admin-uninstall.md"

## Backup and Restore

Review the [Backup and restore OpenVidu deployments](../../how-to-guides/backup-and-restore.md) guide for recommended backup workflows.
