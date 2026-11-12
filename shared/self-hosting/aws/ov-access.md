The deploy prints the URL of the deployment. OpenVidu Meet is served at `/` and OpenVidu Dashboard at `/dashboard/`. In the Single Node example, both use the Let's Encrypt certificate:

```console
$ D=openvidu-40mfas-54-82-78-43.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are in the stack's Secrets Manager secret, the command printed on the `credentials:` line. These are the keys of a Single Node COMMUNITY stack (values replaced by their length):

```text
DASHBOARD_ADMIN_PASSWORD       <set, 44 chars>
DASHBOARD_ADMIN_USERNAME       dashboardadmin
DASHBOARD_URL                  https://openvidu-40mfas-54-82-78-43.sslip.io/dashboard/
DOMAIN_NAME                    openvidu-40mfas-54-82-78-43.sslip.io
ENABLED_MODULES                egress,ingress,dashboard,meet,observability
GRAFANA_ADMIN_PASSWORD         <set, 44 chars>
GRAFANA_ADMIN_USERNAME         grafanaadmin
GRAFANA_URL                    https://openvidu-40mfas-54-82-78-43.sslip.io/grafana/
LIVEKIT_API_KEY                <set, 15 chars>
LIVEKIT_API_SECRET             <set, 44 chars>
LIVEKIT_URL                    wss://openvidu-40mfas-54-82-78-43.sslip.io/
MEET_INITIAL_ADMIN_PASSWORD    <set, 44 chars>
MEET_INITIAL_ADMIN_USER        admin
MEET_INITIAL_API_KEY           <set, 44 chars>
MEET_URL                       https://openvidu-40mfas-54-82-78-43.sslip.io/
OPENVIDU_URL                   https://openvidu-40mfas-54-82-78-43.sslip.io/
S3_APP_DATA_BUCKET             openvidu-appdata-d56324d0
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at deploy time: after a later `ov stack config set`, the stack's configuration is the source of truth (the node's files on Community, `openvidu.yaml` in the cluster on PRO), not the copy.

Your applications connect with `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`, as with any other OpenVidu deployment.

To look inside a machine, use the key pair the deploy generated (the `SSH:` line). The node has `ov` too, so `sudo ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/aws/openvidu-ce10-key.pem ubuntu@54.82.78.43
```
