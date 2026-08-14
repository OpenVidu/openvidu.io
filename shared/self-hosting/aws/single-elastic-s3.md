
### S3 bucket for application data and recordings

You can specify an S3 bucket to store the recordings and application data. If this parameter is not specified, a new S3 bucket will be created by the CloudFormation stack.

!!! info
    Port `9000` is MinIO's port. This deployment stores recordings and application data in Amazon S3 instead of MinIO, so MinIO is not deployed and port `9000` does not need to be open.

=== "S3 bucket for application data and recordings"

    Parameters in this section look like this:

    ![S3 bucket for application data and recordings](/assets/images/platform/self-hosting/shared/aws/s3-bucket.png){ loading=lazy }

    You can specify an existing S3 bucket or leave it empty to create a new one.
