
# How to configure an external S3 bucket for recordings instead of the default MinIO

By default, OpenVidu uses MinIO to store recordings. However, you can configure OpenVidu to use an external S3 bucket to store recordings.

In this example we will use AWS S3 with an S3 bucket named `openvidu-recordings` in region `us-east-1`.

## Single Node deployment

1. SSH into your Server and edit the file `/opt/openvidu/config/egress.yml` to add the following configuration:

    ```yaml
    s3:
        access_key: <YOUR_AWS_ACCESS_KEY>
        secret: <YOUR_AWS_ACCESS_SECRET>
        region: us-east-1
        endpoint: https://s3.amazonaws.com
        bucket: openvidu-recordings
        force_path_style: true
    ```

2. Restart OpenVidu Server:

    ```bash
    systemctl restart openvidu
    ```

## Elastic and High Availability deployment

1. SSH into all your Media Nodes and edit the file `/opt/openvidu/config/egress.yaml` to add the following configuration:

    ```yaml
    s3:
        access_key: <YOUR_AWS_ACCESS_KEY>
        secret: <YOUR_AWS_ACCESS_SECRET>
        region: us-east-1
        endpoint: https://s3.amazonaws.com
        bucket: openvidu-recordings
        force_path_style: true
    ```

2. Restart your Media Nodes:

    ```bash
    systemctl restart openvidu
    ```

If you are using `v2compatibility` module, you also need to configure the `openvidu-v2compatibility` service in your Master Node/s:

1. SSH into your Master Node/s and edit the file `/opt/openvidu/.env` to add the following configuration:

    ```bash
    V2COMPAT_OPENVIDU_PRO_RECORDING_STORAGE=s3
    V2COMPAT_OPENVIDU_PRO_AWS_S3_BUCKET=openvidu-elastic-s3-recordings/test-path/recordings
    V2COMPAT_OPENVIDU_PRO_AWS_S3_SERVICE_ENDPOINT=https://s3.amazonaws.com
    V2COMPAT_OPENVIDU_PRO_AWS_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
    V2COMPAT_OPENVIDU_PRO_AWS_SECRET_KEY=<YOUR_AWS_ACCESS_SECRET>
    V2COMPAT_OPENVIDU_PRO_AWS_REGION=us-east-1
    ```

2. Restart your Master Node/s:

    ```bash
    systemctl restart openvidu
    ```
