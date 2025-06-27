---
title: Changing configuration
description: Learn how to modify OpenVidu configuration files across different deployment types, including single node, elastic and high availability setups.
---

# How to change OpenVidu configuration

The following steps are valid to change any configuration file in any deployment type. Simply just go to one of your Master Nodes, or the only Node in your deployment, and follow these steps:

=== "Steps to change OpenVidu configuration"

    1. Go to one of your Master Nodes (or the only node in your deployment).
    2. Go to `/opt/openvidu/config` directory.
    3. Find and change the configuration parameter you want to modify, it could be any file: `openvidu.env`, `master_node.env`, `livekit.yaml`, `egress.yaml`, etc.
    4. Restart OpenVidu just by executing:

        ```
        systemctl restart openvidu
        ```

Notice that you only need to restart OpenVidu in one of the Master Nodes (or the only node in your deployment) to apply the changes to all the nodes.

## Types of configuration files

Configuration files can be divided into three types:

1. **`openvidu.env`**: This file defines configuration parameters used by other services. Such as the domain name, credentials, etc.
2. **`master_node.env`** and **`media_node.env`** *(Only in Elastic and High Availability)*: These files define specific configuration parameters of the node they are placed in. It is very useful when you want to have different parameter values in different nodes.
3. **`<service>.yaml`** or **`<service>.env`**: These files define the configuration of each service. For example, `livekit.yaml` defines the configuration of the OpenVidu Server, `egress.yaml` defines the configuration of the Egress Service, etc. 

    These files make use of the parameters defined in the `openvidu.env`, `master_node.env`, and `media_node.env` files. For example, any service configuration file can access the `DOMAIN_NAME` parameter defined in the `openvidu.env` file by using this syntax:

    ```
    ${openvidu.DOMAIN_NAME}
    ```

    You can check the [OpenVidu Configuration In depth](./in-depth.md){:target="_blank"} section to learn more about how the configuration system works.

## Config files

These are the configuration files for each kind of deployment:

=== "Single Node"

    The single node has all configuration files in the same directory `/opt/openvidu/config/`:

    ```
    |-- /opt/openvidu/config/
        |-- openvidu.env
        |-- livekit.yaml
        |-- egress.yaml
        |-- ingress.yaml
        |-- caddy.yaml
        |-- redis.env
        |-- minio.env
        |-- mongo.env
        |-- dashboard.env
        |-- loki.yaml
        |-- prometheus.yaml
        |-- promtail.yaml
        |-- app.env
        |-- agent-speech-processing.yaml
        `-- grafana/
    ```

=== "Elastic"

    OpenVidu Elastic has all the cluster configuration at `/opt/openvidu/config/cluster/` with each configuration file separated depending on the node they are placed in: `master_node` or `media_node`. The file `openvidu.env` is placed at `/opt/openvidu/config/cluster/` because it is used by services of both types of nodes.

    Specific parameter values of each Master Node are placed at `/opt/openvidu/config/node/master_node.env`.

    **Master Node**

    ```
    |-- /opt/openvidu/config/
        |-- cluster/
        |   |-- openvidu.env
        |   |-- master_node/
        |   |   |-- grafana/
        |   |   |-- app.env
        |   |   |-- caddy.yaml
        |   |   |-- dashboard.env
        |   |   |-- loki.yaml
        |   |   |-- mimir.yaml
        |   |   |-- minio.env
        |   |   |-- mongo.env
        |   |   |-- operator.env
        |   |   |-- promtail.yaml
        |   |   |-- redis.env
        |   |   `-- v2compatibility.env
        |   `-- media_node/
        |       |-- egress.yaml
        |       |-- ingress.yaml
        |       |-- livekit.yaml
        |       |-- prometheus.yaml
        |       |-- promtail.yaml
        |       `-- agent-speech-processing.yaml
        `-- node/
        `-- master_node.env
    ```


    **Media Node**

    The Media Node in contrast has only the `media_node.env` file, because the configuration is centralized in the Master Node.

    ```
    |-- /opt/openvidu/config/
        `-- node/
            `-- media_node.env
    ```

=== "High Availability"

    OpenVidu High Availability has all the cluster configuration at `/opt/openvidu/config/cluster/` with each configuration file separated depending on the node they are placed in: `master_node` or `media_node`. The file `openvidu.env` is placed at `/opt/openvidu/config/cluster/` because it is used by services of both types of nodes.

    Specific parameter values of each Master Node are placed at `/opt/openvidu/config/node/master_node.env`.

    **Master Node**

    ```
    |-- /opt/openvidu/config/
        |-- cluster/
        |   |-- openvidu.env
        |   |-- master_node/
        |   |   |-- grafana/
        |   |   |-- app.env
        |   |   |-- caddy.yaml
        |   |   |-- dashboard.env
        |   |   |-- loki.yaml
        |   |   |-- mimir.yaml
        |   |   |-- minio.env
        |   |   |-- mongo.env
        |   |   |-- operator.env
        |   |   |-- promtail.yaml
        |   |   |-- redis.env
        |   |   `-- v2compatibility.env
        |   `-- media_node/
        |       |-- caddy.yaml
        |       |-- egress.yaml
        |       |-- ingress.yaml
        |       |-- livekit.yaml
        |       |-- prometheus.yaml
        |       |-- promtail.yaml
        |       `-- agent-speech-processing.yaml
        `-- node/
        `-- master_node.env
    ```

    **Media Node**

    The Media Node in contrast has only the `media_node.env` file, because the configuration is centralized in the Master Node.

    ```
    |-- /opt/openvidu/config/
        `-- node/
            `-- media_node.env
    ```

## Troubleshooting configuration

After changing the configuration and restarting, you need to make sure that the changes have been applied correctly. Here are some tips to check if something is wrong. All the following commands must be executed in one of the Master Nodes (or the only node in your deployment):

1. Execute a `docker ps`. If you see an `openvidu-init` container constantly restarting, it means that the configuration file you modified has a syntax error. Check the logs of this container to see the error with:

    ```bash
    docker logs openvidu-init
    ```

    The log is self-explanatory and will tell you what is wrong with the configuration file:

    ```bash
    service 'openvidu': Failed to process config file '/opt/openvidu/config/livekit.yaml': Errors found:

        *  Error at line 18: Unmatched opening brace at position 7
    ```

    Once fixed, restart OpenVidu again:

    ```bash
    systemctl restart openvidu
    ```

2. Execute a `docker ps`. If you don't see the `openvidu-init` container, but you see some containers restarting, check the logs of those restarting containers to see what is wrong:

    ```bash
    docker logs <container_id>
    ```

3. If all the containers are running correctly, execute the following command:

    ```bash
    tail -f /var/log/openvidu/nodes_errors.log
    ```

    If you have an error like: *'No such file or directory'* or simply the file is empty, the configuration is correct. If the file exists with content, some nodes may be malfunctioning. Check this file and failing container logs for errors.

    This is how the log file looks when there are Media Nodes with errors:

    ```
    [2024-10-09T05:54:29Z] [ERROR] Error in Media Node - 10.5.0.5: Container 'openvidu' error:
    could not parse config: yaml: unmarshal errors:
      line 17: cannot unmarshal !!str `trueee` into bool

    [2024-10-09T05:54:29Z] [ERROR] Error in Media Node - 10.5.0.4: Container 'openvidu' error:
    could not parse config: yaml: unmarshal errors:
      line 17: cannot unmarshal !!str `trueee` into bool
    ```

    As you can see, the log informs you about which Media Node is failing and the error that is causing the failure, so in this way you can fix the file which is causing the error. Once fixed, restart OpenVidu again:

    ```bash
    systemctl restart openvidu
    ```

    And again, check the logs until no errors appear.
