The deploy prints the URL of the deployment. OpenVidu Meet is served at `/meet` (`/` redirects there unless you serve your own application) and OpenVidu Dashboard at `/dashboard/`. In the Single Node example, both use the Let's Encrypt certificate:

```console
$ D=openvidu-u57z2l-51-170-56-241.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The passwords and keys are in the stack's configuration, which `ov stack config get` reads from the running stack:

```bash
ov stack config get meet-initial-admin-password
ov stack config get dashboard-admin-password
ov stack config get livekit-api-key
ov stack config get livekit-api-secret
```

The deploy also published them, base64-encoded, to the stack's vault, with the command printed on the `credentials:` line of the deploy. These are the keys of a Single Node COMMUNITY stack (values replaced by their length):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-u57z2l-51-170-56-241.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-u57z2l-51-170-56-241.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
EXTERNAL_S3_ACCESS_KEY         <set, 40 chars>
EXTERNAL_S3_ENDPOINT           https://<namespace>.compat.objectstorage.eu-madrid-1.oraclecloud.com
EXTERNAL_S3_SECRET_KEY         <set, 44 chars>
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-u57z2l-51-170-56-241.sslip.io/
OPENVIDU_URL                   https://openvidu-u57z2l-51-170-56-241.sslip.io/
S3_APP_DATA_BUCKET             openvidu-ce12o-appdata-9f79dd
…
```

That vault copy is made at deploy time and is not updated afterwards: after a later `ov stack config set`, the stack's configuration is the source of truth (the node's files on Community, `openvidu.yaml` in the cluster on PRO), not the copy.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, the login user is `ubuntu` and the node has `ov` too, so `sudo ov stack …` there operates the same stack. Where the private key is depends on the edition:

=== "OpenVidu **COMMUNITY**{ .openvidu-tag .openvidu-community-tag }"

    Use the key the template generated, which `ov` saves in the stack directory (the `SSH:` line of the summary):

    ```bash
    ssh -i .openvidu/oracle/openvidu-ce12o-key.pem ubuntu@51.170.56.241
    ```

=== "OpenVidu **PRO**{ .openvidu-tag .openvidu-pro-tag }"

    The template generated the machines' key (master and media nodes share it) and keeps its private half in Object Storage, not in the stack directory. The `ssh_private_key_object` output names the object as `<bucket>/<object>`; download it and log in to a master's public address:

    ```bash
    terraform -chdir=.openvidu/oracle output -raw ssh_private_key_object
    oci os object get --bucket-name <bucket> --name <object> --file openvidu-key.pem
    chmod 600 openvidu-key.pem
    ssh -i openvidu-key.pem ubuntu@<master's public address>
    ```
