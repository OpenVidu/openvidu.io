The deploy prints the URL of the deployment. OpenVidu Meet is served at `/` and OpenVidu Dashboard at `/dashboard/`. In the Single Node example, both use the Let's Encrypt certificate:

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

`ov stack config get <key>` reads any of them from the running stack. `secrets.env` is a copy made at deploy time: after a later `ov stack config set`, the stack's configuration is the source of truth (the node's files on Community, `openvidu.yaml` in the cluster on PRO), not the copy.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment (`ov stack config get livekit-api-key` and `livekit-api-secret` print them).

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The login user is `root`, and the node has `ov` too, so `ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/digitalocean/openvidu-ce12d2-key.pem root@164.92.159.209
```
