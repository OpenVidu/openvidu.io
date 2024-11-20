# Configuring External S3 for OpenVidu Recordings

By default, OpenVidu uses MinIO for recording storage. However, it can be configured to use an external S3 provider. This guide outlines the steps to configure OpenVidu with an external S3 provider for your deployment.

## Configuration

Configuring an external S3 bucket in OpenVidu is straightforward. Update the following parameters in the `openvidu.env` file on one of the Master Nodes or your Single Node deployment. Depending on your deployment type, the location of the `openvidu.env` file is as follows:

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

### Basic Configuration

```bash
EXTERNAL_S3_ENDPOINT=<YOUR_S3_HTTP_ENDPOINT>
EXTERNAL_S3_ACCESS_KEY=<YOUR_S3_ACCESS_KEY>
EXTERNAL_S3_SECRET_KEY=<YOUR_S3_SECRET_KEY>
EXTERNAL_S3_REGION=<YOUR_S3_REGION>
EXTERNAL_S3_PATH_STYLE_ACCESS=<YOUR_S3_PATH_STYLE_ACCESS>
```

**Parameter Details:**

- `EXTERNAL_S3_ENDPOINT`: HTTP endpoint of your S3 provider.
- `EXTERNAL_S3_ACCESS_KEY`: Access key for your S3 provider.
- `EXTERNAL_S3_SECRET_KEY`: Secret key for your S3 provider.
- `EXTERNAL_S3_REGION`: Region of your S3 provider.
- `EXTERNAL_S3_PATH_STYLE_ACCESS`: Use path-style access for the S3 bucket (`true` or `false` based on provider requirements).

### Buckets Configuration

Before proceeding, ensure you have access to the S3 provider and create the following bucket:

- **App Data Bucket**: Stores OpenVidu recordings and data related to the Default Application (OpenVidu Call).

If you are deploying a High Availability cluster, you will need an additional bucket:

- **Cluster Data Bucket** (High Availability only): Stores observability data and other data specific to a High Availability deployment.

Configure these buckets in the `openvidu.env` file:

```bash
# For all deployments
EXTERNAL_S3_BUCKET_APP_DATA=<YOUR_APP_DATA_BUCKET>
# For High Availability deployments only
EXTERNAL_S3_BUCKET_CLUSTER_DATA=<YOUR_CLUSTER_DATA_BUCKET>
```

## Restart

After updating the `openvidu.env` file, restart the service on the Master Node or your Single Node deployment:

```bash
systemctl restart openvidu
```

## Example Configuration with AWS S3

Assume your region is `eu-west-1` and you have an S3 bucket named `my-openvidu-bucket`. Your configuration should be:

```bash
EXTERNAL_S3_ENDPOINT=https://s3.eu-west-1.amazonaws.com
EXTERNAL_S3_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
EXTERNAL_S3_SECRET_KEY=<YOUR_AWS_SECRET_KEY>
EXTERNAL_S3_REGION=eu-west-1
EXTERNAL_S3_PATH_STYLE_ACCESS=false
EXTERNAL_S3_BUCKET_APP_DATA=my-openvidu-bucket
```

!!! warning
    Note that the region must be specified in the `EXTERNAL_S3_ENDPOINT` parameter for AWS S3. This may not be required for other S3 providers.

For High Availability deployments, you will also need an additional bucket for cluster data, e.g., `my-openvidu-cluster-bucket`:

```bash
EXTERNAL_S3_BUCKET_CLUSTER_DATA=my-openvidu-cluster-bucket
```

After updating the `openvidu.env` file, restart the service on one of the Master Nodes or your Single Node deployment:

```bash
systemctl restart openvidu
```

## Configuring S3 Bucket Directories

Both the Default Application (OpenVidu Call) and the V2 Compatibility Service use the `EXTERNAL_S3_BUCKET_APP_DATA` for storing data. Configure the directories for each service using the following environment variables.

### `app.env` Configuration for OpenVidu Call

Locate the following variables in the `app.env` file:

```bash
CALL_S3_PARENT_DIRECTORY=openvidu-call
CALL_S3_RECORDING_DIRECTORY=recordings
```

**Parameter Details:**

- `CALL_S3_PARENT_DIRECTORY`: Parent directory for application data.
- `CALL_S3_RECORDING_DIRECTORY`: Directory for recordings within the parent directory.

### `v2compatibility.env` Configuration for V2 Compatibility Service

Locate the following variables in the `v2compatibility.env` file:

```bash
V2COMPAT_OPENVIDU_PRO_AWS_S3_PARENT_DIRECTORY=openvidu-server-v2compatibility
V2COMPAT_OPENVIDU_PRO_AWS_S3_RECORDING_DIRECTORY=recordings
```

**Parameter Details:**

- `V2COMPAT_OPENVIDU_PRO_AWS_S3_PARENT_DIRECTORY`: Parent directory for application data.
- `V2COMPAT_OPENVIDU_PRO_AWS_S3_RECORDING_DIRECTORY`: Directory for recordings within the parent directory.

## Troubleshooting

On any problem, check these sections:

- [Config Troubleshooting](../configuration/changing-config.md#troubleshooting-configuration){:target="_blank"}
- Status and Checking Logs sections of Administration sections of each deployment type:
    - [Single Node](../single-node/on-premises/admin.md#checking-the-status-of-services){:target="_blank"}
    - [Elastic](../elastic/on-premises/admin.md#checking-the-status-of-services){:target="_blank"}
    - [High Availability](../ha/on-premises/admin.md#checking-the-status-of-services){:target="_blank"}
