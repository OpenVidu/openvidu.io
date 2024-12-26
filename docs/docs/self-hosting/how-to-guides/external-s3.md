# Configuring External S3 for OpenVidu Recordings

By default, OpenVidu uses MinIO for storing recordings. You can configure it to use an external S3 bucket instead. This guide uses AWS S3, but can be adapted for other S3-compatible services.

## Global Configuration with `openvidu.env`

The `openvidu.env` file defines global parameters used in service configurations. So we can use it to define our S3 configuration details and afterwards use them in the services that need them.

1. SSH into one of your Master Nodes (or Single Node).
2. Add these variables to `openvidu.env`:

    ```bash
    RECORDINGS_S3_BUCKET=openvidu-recordings
    RECORDINGS_S3_ENDPOINT=https://s3.us-east-2.amazonaws.com
    RECORDINGS_AWS_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
    RECORDINGS_AWS_SECRET_KEY=<YOUR_AWS_ACCESS_SECRET>
    RECORDINGS_AWS_REGION=us-east-2
    RECORDINGS_S3_FORCE_PATH_STYLE=false
    ```

    The location of the file depends on the type of deployment:

    - **Single Node**: `/opt/openvidu/config/openvidu.env`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

    !!! warning
        In AWS it is necessary to specify the region in the endpoint URL as you can see in `RECORDINGS_S3_ENDPOINT`. Check the [AWS S3 endpoints documentation](https://docs.aws.amazon.com/general/latest/gr/s3.html){:target="_blank"} for more information.
    !!! info
        The parameters defined at `openvidu.env` can be used in other configuration files by using the `${openvidu.VARIABLE_NAME}` syntax. If you want to know more about the configuration system of OpenVidu, check the [Configuration In-depth](../configuration/in-depth.md){:target="_blank} section.



3. Update `egress.yaml` to use these variables:

    ```yaml
    s3:
        access_key: ${openvidu.RECORDINGS_AWS_ACCESS_KEY}
        secret: ${openvidu.RECORDINGS_AWS_SECRET_KEY}
        region: ${openvidu.RECORDINGS_AWS_REGION}
        endpoint: ${openvidu.RECORDINGS_S3_ENDPOINT}
        bucket: ${openvidu.RECORDINGS_S3_BUCKET}
        force_path_style: ${openvidu.RECORDINGS_S3_FORCE_PATH_STYLE}
    ```
    The location of the file depends on the type of deployment:

    - **Single Node**: `/opt/openvidu/config/egress.yaml`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/media_node/egress.yaml`

4. Restart the Master Node (or Single Node) to apply the changes:

    ```bash
    systemctl restart openvidu
    ```

    This command will restart the services which changed their configuration files in your entire OpenVidu deployment.

## Additional Configuration for Default App and V2 Compatibility

If using the Default App (OpenVidu Call) or V2 Compatibility, additional configurations are required.

### OpenVidu Default App (OpenVidu Call)

1. Update `app.env` with:

    ```bash
    CALL_S3_BUCKET=${openvidu.RECORDINGS_S3_BUCKET}
    CALL_S3_SERVICE_ENDPOINT=${openvidu.RECORDINGS_S3_ENDPOINT}
    CALL_S3_ACCESS_KEY=${openvidu.RECORDINGS_AWS_ACCESS_KEY}
    CALL_S3_SECRET_KEY=${openvidu.RECORDINGS_AWS_SECRET_KEY}
    CALL_AWS_REGION=${openvidu.RECORDINGS_AWS_REGION}
    CALL_S3_WITH_PATH_STYLE_ACCESS=${openvidu.RECORDINGS_S3_FORCE_PATH_STYLE}
    ```

    The location of the file depends on the type of deployment:

    - **Single Node**: `/opt/openvidu/config/app.env`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/master_node/app.env`

### <span class="openvidu-tag openvidu-pro-tag">PRO</span> V2 Compatibility

1. Update `v2compatibility.env` with:

    ```bash
    V2COMPAT_OPENVIDU_PRO_RECORDING_STORAGE=s3
    V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET=${openvidu.RECORDINGS_S3_BUCKET}
    V2COMPAT_OPENVIDU_PRO_AWS_S3_SERVICE_ENDPOINT=${openvidu.RECORDINGS_S3_ENDPOINT}
    V2COMPAT_OPENVIDU_PRO_AWS_ACCESS_KEY=${openvidu.RECORDINGS_AWS_ACCESS_KEY}
    V2COMPAT_OPENVIDU_PRO_AWS_SECRET_KEY=${openvidu.RECORDINGS_AWS_SECRET_KEY}
    V2COMPAT_OPENVIDU_PRO_AWS_REGION=${openvidu.RECORDINGS_AWS_REGION}
    V2COMPAT_OPENVIDU_PRO_AWS_S3_WITH_PATH_STYLE_ACCESS=${openvidu.RECORDINGS_S3_FORCE_PATH_STYLE}
    ```

    The location of the file depends on the type of deployment:

    - **Single Node**: `/opt/openvidu/config/v2compatibility.env`
    - **Elastic / High Availability**: `/opt/openvidu/config/cluster/master_node/v2compatibility.env`
