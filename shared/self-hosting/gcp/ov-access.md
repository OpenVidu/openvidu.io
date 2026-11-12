The deploy prints the URL of the deployment. OpenVidu Meet is served at `/meet` (`/` redirects there unless you serve your own application) and OpenVidu Dashboard at `/dashboard/`. In the Single Node example below, both use the Let's Encrypt certificate:

```console
$ D=openvidu-uj9zj7-34-105-214-170.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are stored as one Secret Manager secret per key, each id prefixed with the stack name; the `credentials:` line prints the command that reads them. These are the keys of a Single Node COMMUNITY stack (values replaced by their length; the service-account key is masked entirely):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-uj9zj7-34-105-214-170.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-uj9zj7-34-105-214-170.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
GCP_CREDENTIALS_JSON           <set>
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-uj9zj7-34-105-214-170.sslip.io/
OPENVIDU_URL                   https://openvidu-uj9zj7-34-105-214-170.sslip.io/
S3_APP_DATA_BUCKET             my-project-openvidu-ce12g-1300d7
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at deploy time: after a later `ov stack config set`, the stack's configuration is the source of truth (the node's files on Community, `openvidu.yaml` in the cluster on PRO), not the copy. `GCP_CREDENTIALS_JSON` is the exception Terraform writes itself: the one input only Google Cloud knows.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, the login user is `ubuntu` and the node has `ov` too, so `sudo ov stack …` there operates the same stack. How you reach it depends on the edition:

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    Use the key pair the deploy generated (the `SSH:` line of the summary):

    ```bash
    ssh -i .openvidu/gcp/openvidu-ce12g-key.pem ubuntu@34.105.214.170
    ```

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    A PRO stack keeps no key pair. Reach the node with `gcloud compute ssh`, as the deploy's `ssh_command` output prints (`terraform -chdir=.openvidu/gcp output -raw ssh_command`):

    ```bash
    gcloud compute ssh <instance-name> --zone <zone> --project my-project
    ```
