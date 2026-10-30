# Configuring external S3 for OpenVidu recordings

OpenVidu, by default, utilizes MinIO for recording storage, but it can be configured to use an external S3 provider instead. This guide provides the necessary steps to configure OpenVidu with an external S3 provider for your deployment.

> **Info**
>
> If you are deploying using AWS CloudFormation, the S3 bucket is configured automatically to use the AWS S3 service. **In this case there is no need to follow this guide**.

## Configuration

Configuring an external S3 bucket in OpenVidu is straightforward. Update the following parameters in the `openvidu.env` file on one of the Master Nodes or your Single Node deployment. Depending on your deployment type, the location of the `openvidu.env` file is as follows:

- **Single Node**: `/opt/openvidu/config/openvidu.env`
- **Elastic / High Availability**: `/opt/openvidu/config/cluster/openvidu.env`

```bash
EXTERNAL_S3_ENDPOINT=<YOUR_S3_HTTP_ENDPOINT>
EXTERNAL_S3_ACCESS_KEY=<YOUR_S3_ACCESS_KEY>
EXTERNAL_S3_SECRET_KEY=<YOUR_S3_SECRET_KEY>
EXTERNAL_S3_REGION=<YOUR_S3_REGION>
EXTERNAL_S3_PATH_STYLE_ACCESS=<YOUR_S3_PATH_STYLE_ACCESS>
EXTERNAL_S3_BUCKET_APP_DATA=<YOUR_APP_DATA_BUCKET>
# For High Availability deployments only
EXTERNAL_S3_BUCKET_CLUSTER_DATA=<YOUR_CLUSTER_DATA_BUCKET>
```

**Parameter Details:**

- `EXTERNAL_S3_ENDPOINT`: HTTP endpoint of your S3 provider.
- `EXTERNAL_S3_ACCESS_KEY`: Access key for your S3 provider.
- `EXTERNAL_S3_SECRET_KEY`: Secret key for your S3 provider.
- `EXTERNAL_S3_REGION`: Region of your S3 provider.
- `EXTERNAL_S3_PATH_STYLE_ACCESS`: Use path-style access for the S3 bucket (`true` or `false` based on provider requirements).
- `EXTERNAL_S3_BUCKET_APP_DATA`: Bucket for storing OpenVidu recordings and data related to the OpenVidu Meet service.
- `EXTERNAL_S3_BUCKET_CLUSTER_DATA` (High Availability only): Bucket for storing observability data and other data specific to a High Availability deployment.

After updating the `openvidu.env` file, restart the Master Node or your Single Node deployment:

```bash
systemctl restart openvidu
```

> **Info**
>
> Take into account that when using an external S3 bucket, the MinIO service will not be started, and will appear as `Exited (0)` when checking the status of the services.

## Example with AWS S3

Assume the region of your bucket is `eu-west-1` and you have an S3 bucket named `my-openvidu-bucket`. Your configuration should be:

```bash
EXTERNAL_S3_ENDPOINT=https://s3.eu-west-1.amazonaws.com
EXTERNAL_S3_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
EXTERNAL_S3_SECRET_KEY=<YOUR_AWS_SECRET_KEY>
EXTERNAL_S3_REGION=eu-west-1
EXTERNAL_S3_PATH_STYLE_ACCESS=true
EXTERNAL_S3_BUCKET_APP_DATA=my-openvidu-bucket

# For High Availability deployments only
EXTERNAL_S3_BUCKET_CLUSTER_DATA=my-openvidu-cluster-bucket
```

> **Warning**
>
> Note that the region must be specified in the `EXTERNAL_S3_ENDPOINT` parameter for AWS S3. This may not be required for other S3 providers but is necessary for AWS S3.

## About the Path-Style parameter

The `EXTERNAL_S3_PATH_STYLE_ACCESS` parameter is used to specify whether to use path-style access if `true` or virtual-hosted-style access if `false`. Check this documentation for more information: [Amazon S3 Path Style Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html)

This parameter requires a specific value depending on the S3 provider. Here is a table with some examples:

| S3 Provider         | `EXTERNAL_S3_PATH_STYLE_ACCESS` Value |
| ------------------- | ------------------------------------- |
| AWS S3              | `true` or `false` Recommend `true`    |
| MinIO               | `false`                               |
| DigitalOcean Spaces | `false`                               |

Usually the value `false` is compatible with all S3 providers, but some providers may require `true`, so check the documentation of your S3 provider to confirm the correct value.

## Troubleshooting

On any problem, check these sections:

- [Config Troubleshooting](https://openvidu.io/3.5/docs/self-hosting/configuration/changing-config/#troubleshooting-configuration)
- Status and Checking Logs sections of Administration sections of each deployment type:
  - [Single Node](https://openvidu.io/3.5/docs/self-hosting/single-node/on-premises/admin/#checking-the-status-of-services)
  - [Elastic](https://openvidu.io/3.5/docs/self-hosting/elastic/on-premises/admin/#checking-the-status-of-services)
  - [High Availability](https://openvidu.io/3.5/docs/self-hosting/ha/on-premises/admin/#checking-the-status-of-services)
