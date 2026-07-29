!!! info
    We recommend to create a new project to deploy OpenVidu there, avoiding possible conflicts between resources. Enable [Secrets Manager Api :fontawesome-solid-external-link:{.external-link-icon}](https://console.cloud.google.com/security/secret-manager){target="_blank"} first in that project and then deploy the stack. You might need to deploy multiple times to let the APIs activate.

!!! info
    Port `9000` is MinIO's port. This deployment stores recordings and application data in Google Cloud Storage instead of MinIO, so MinIO is not deployed and port `9000` does not need to be open.
