# OpenVidu Configuration In depth

OpenVidu utilizes a powerful and flexible system for configuring services by expanding global parameters defined in the configuration files. This mechanism ensures consistency and simplifies management by allowing global settings to be referenced across multiple service configurations. The variable expansion follows the same interpolation rules as Docker Compose, providing a familiar syntax for those accustomed to Docker.

### How Variable Interpolation Works

To understand how variable interpolation works in OpenVidu, it is important to consider two main types of configuration files: global configuration files and service configuration files.

1. **Global Configuration Files**:

    - Global parameters are defined in the global configuration files such as `openvidu.env`, `master_node.env`, and `media_node.env`.
    - These files contain key-value pairs that define parameters than can be used in service configuration files.

2. **Service Configuration Files**:

    - Each service configuration file can reference these global parameters using a specific syntax.
    - The syntax `${openvidu.ENV_VAR}` is used to access and interpolate those values from the global configuration files.
    - If you are configuring a service of the Master Node which needs a specific variable of the Master Node, you can use `${master_node.ENV_VAR}`.
    - If you are configuring a service of the Media Node which needs a specific variable of the Media Node, you can use `${media_node.ENV_VAR}`.

3. **Interpolation Rules**:

    - The interpolation follows the Docker Compose specification, which provides robust handling of global variables.
    - If a variable is mandatory and not set, the syntax `${VAR:?mandatory}` can be used to throw an error if the parameter is not defined, ensuring required configurations are not missed. For more detailed information about the interpolation rules, you can refer to the Docker Compose documentation on [variable interpolation](https://docs.docker.com/compose/compose-file/12-interpolation/).

4. **Example**:

    Look at this part of the `/opt/openvidu/config/media_node/livekit.yaml` configuration file in the Master Node of an Elastic deployment:

    ```yaml
    openvidu:
        license: ${openvidu.OPENVIDU_PRO_LICENSE:?mandatory}
        cluster_id: ${openvidu.DOMAIN_NAME:?mandatory}
        node:
            private_ip: ${media_node.MEDIA_NODE_PRIVATE_IP:?mandatory}
    ```

    This file uses global variables from the `openvidu.env` and `media_node.env` files to set up the license, cluster ID, and private IP address for the LiveKit service. The `:?mandatory` part means these variables must be defined; otherwise, an error will occur. Since this file is for a Media Node, it uses the `media_node` variables, allowing each Media Node to have different values for the same variable.

    To use a variable from the `media_node.env` file, write it as `${media_node.ENV_VAR}`. Similarly, to use a variable from the `openvidu.env` or `master_node.env` file, write it as `${openvidu.ENV_VAR}` or `${master_node.ENV_VAR}` respectively.

### Config Files Replication

In Elastic and High Availability deployments, the configuration files are replicated across all the Master Nodes in the cluster.

This ensures that all nodes have the same configuration, making it easier to manage and maintain the cluster. The global configuration files are placed in the `/opt/openvidu/config/cluster/` directory, while the node-specific configuration files are placed in the `/opt/openvidu/config/node/` directory.
