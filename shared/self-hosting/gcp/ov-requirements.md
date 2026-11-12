- The [OpenVidu CLI](/docs/self-hosting/openvidu-cli.md#install-the-openvidu-cli).
- A Google Cloud project and [**Terraform** :fontawesome-solid-external-link:{.external-link-icon}](https://developer.hashicorp.com/terraform/install){:target="_blank"} on your PATH: `ov` drives your own Terraform, so the provider plugins, the state and the audit trail are the ones that apply.
- The [`gcloud` CLI :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.google.com/sdk/docs/install){:target="_blank"} with **application-default credentials** (`gcloud auth application-default login`), which Terraform and the secret reads use.
- A project id: `--gcp-project`, otherwise `$GCP_PROJECT_ID`, otherwise what `gcloud` has configured. `--gcp-region` / `--gcp-zone` default to the template's `europe-west2` / `europe-west2-b`.
- Permission to create Compute Engine instances, a static address, firewall rules, a Cloud Storage bucket, service accounts and Secret Manager secrets. The template also **mints a service-account key** that egress uses to upload recordings.

For OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }, you also need your **license** (`--openvidu-pro-license`): [create an OpenVidu account :fontawesome-solid-external-link:{.external-link-icon}](/account.md){:target="_blank"} to get one, there is a 15-day free trial. The deploy checks that it is present before it touches your project.

You need neither a key pair nor a domain: the template generates an SSH key pair for the stack, and without `--domain-name` the stack derives an `sslip.io` name from its public IP (on High Availability, from the load balancer's), so Let's Encrypt has a name to certify on Single Node and Elastic. Use your own domain for anything beyond testing.

!!! warning "Service-account key creation"

    The template mints a Cloud Storage service-account key that egress uses to upload recordings. An organization policy that blocks key creation (`iam.disableServiceAccountKeyCreation`) stops the apply. Allow key creation in the project, or the deploy cannot finish.
