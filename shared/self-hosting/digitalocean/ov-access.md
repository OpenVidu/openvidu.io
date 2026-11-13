The deploy prints the URL of the deployment. OpenVidu Meet is served at `/meet` (`/` redirects there unless you serve your own application) and OpenVidu Dashboard at `/dashboard/`. In the Single Node example, both use the Let's Encrypt certificate:

```console
$ D=openvidu-324jl8-164-92-159-209.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are in `secrets.env` in the stack's Space, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-324jl8-164-92-159-209.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-324jl8-164-92-159-209.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
EXTERNAL_S3_ACCESS_KEY         <set, 20 chars>
EXTERNAL_S3_ENDPOINT           https://ams3.digitaloceanspaces.com
EXTERNAL_S3_SECRET_KEY         <set, 43 chars>
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-324jl8-164-92-159-209.sslip.io/
OPENVIDU_URL                   https://openvidu-324jl8-164-92-159-209.sslip.io/
S3_APP_DATA_BUCKET             openvidu-ce12d2-space-dae2e06c8c
…
```

`ov stack config get <key>` reads any of them from the running stack. `secrets.env` is a copy made at deploy time: after a later `ov stack config set`, the stack's configuration is the source of truth, not the copy.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment (`ov stack config get livekit-api-key` and `livekit-api-secret` print them).

To look inside a machine, the login user is `root` and the node has `ov` too, so `ov stack …` there operates the same stack. Where the private key is depends on the edition:

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    Use the key the template generated, which `ov` saves in the stack directory (the `SSH:` line of the summary):

    ```bash
    ssh -i .openvidu/digitalocean/openvidu-ce12d2-key.pem root@164.92.159.209
    ```

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The template generated the machines' key and keeps it in its state, not as a file in the stack directory. The `sshPrivateKey` output prints its private half:

    ```bash
    terraform -chdir=.openvidu/digitalocean output -raw sshPrivateKey > openvidu-key.pem
    chmod 600 openvidu-key.pem
    ssh -i openvidu-key.pem root@<master's public address>
    ```
