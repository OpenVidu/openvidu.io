The deploy prints the URL of the deployment. OpenVidu Meet is served at `/meet` (`/` redirects there unless you serve your own application) and OpenVidu Dashboard at `/dashboard/`. In the Single Node example, both use the Let's Encrypt certificate:

```console
$ D=openvidu-zclupo-40-112-77-3.sslip.io
$ curl -s -o /dev/null -w "meet %{http_code}\n" https://$D/
meet 302
$ curl -s -o /dev/null -w "dashboard %{http_code}\n" https://$D/dashboard/
dashboard 200
```

The credentials are secrets in the stack's Key Vault; the `credentials:` line prints the command that reads them. These are the keys of a Single Node COMMUNITY stack (values replaced by their length; the storage account key is masked too):

```text
vault openvidu-ce12a-keyvault
AZURE-STORAGE-ACCOUNT-KEY      <set, 88 chars>
AZURE-STORAGE-ACCOUNT-NAME     ovdatammuudi34y26y2
AZURE-STORAGE-CONTAINER-NAME   openvidu-appdata
DASHBOARD-ADMIN-PASSWORD       <set, 44 chars>
DASHBOARD-ADMIN-USERNAME       dashboardadmin
DASHBOARD-URL                  https://openvidu-zclupo-40-112-77-3.sslip.io/dashboard/
DOMAIN-NAME                    openvidu-zclupo-40-112-77-3.sslip.io
ENABLED-MODULES                egress,ingress,dashboard,meet,observability
LIVEKIT-API-KEY                <set, 15 chars>
LIVEKIT-API-SECRET             <set, 44 chars>
LIVEKIT-URL                    wss://openvidu-zclupo-40-112-77-3.sslip.io/
OPENVIDU-URL                   https://openvidu-zclupo-40-112-77-3.sslip.io/
…
```

`ov stack config get <key>` reads any of them from the running stack. The secret is a copy made at deploy time: after a later `ov stack config set`, the running stack's configuration is the source of truth, not the copy.

Your applications connect with the values of `LIVEKIT-URL`, `LIVEKIT-API-KEY` and `LIVEKIT-API-SECRET` (`LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` in your application's environment), as with any other OpenVidu deployment. Key Vault does not allow `_` in a secret name, so the keys use `-`.

To look inside a machine, use the key pair the deploy generated, which `ov` keeps in `.openvidu/azure/` as `<stack>-key.pem` (a Community deploy also prints it on the `SSH:` line; on PRO, log in to a master's public address). The login user is `ubuntu`, and the node has `ov` too, so `sudo ov stack …` there operates the same stack:

```bash
ssh -i .openvidu/azure/openvidu-ce12a-key.pem ubuntu@40.112.77.3
```
