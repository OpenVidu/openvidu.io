Without `--domain-name` the stack answers at an `sslip.io` name derived from its public IP (on Elastic, the master's), which Let's Encrypt certifies without a domain of yours. For anything beyond testing, use your own domain: add `--domain-name` to the deploy command.

```bash
ov stack deploy <name> --cloud digitalocean … \
  --domain-name openvidu.example.com --certificate-type letsencrypt --mode auto
```

No DigitalOcean template touches DNS, so you create the record yourself. As soon as the machines exist the deploy prints the `A` record to create (`openvidu.example.com. A <the stack's address>`), and the two editions wait differently:

- **OpenVidu PRO** reaches the stack by its address, so it does not wait for the record: the deploy ends with `! OpenVidu Pro (…) is deployed on DigitalOcean, with one step left: openvidu.example.com does not point at it yet.` and the record again. Create it, and the Let's Encrypt certificate is issued once the name resolves; `ov stack status` already works.
- **OpenVidu COMMUNITY** (Single Node) waits for the record, because its health check goes through the URL. Create the printed record while `ov` waits, and the deploy finishes once the name resolves and the certificate is issued.

For your own certificate instead of Let's Encrypt, use `--certificate-type owncert` with the two halves base64-encoded (`--owncert-public-key "$(base64 -w0 fullchain.pem)"`, `--owncert-private-key "$(base64 -w0 privkey.pem)"`).
