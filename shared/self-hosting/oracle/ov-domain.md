Without `--domain-name` the stack answers at an `sslip.io` name derived from its public address, certified by Let's Encrypt (or self-signed with `--certificate-type selfsigned`). That is enough to try OpenVidu out. For anything else, use your own domain.

No Oracle template touches DNS, so you create the record yourself. Add `--domain-name` to your deploy command, with `letsencrypt` or with `owncert` and your own certificate (base64-encoded, since on a cloud it travels as a template parameter). On a Single Node COMMUNITY deploy:

```bash
ov stack deploy openvidu --cloud oracle --oci-region eu-madrid-1 \
  --domain-name openvidu.example.com --certificate-type letsencrypt --mode auto
```

As soon as the machines exist, the deploy prints the `A` record to create: `<domain> A <public_ip>`, the instance's public IP (the master's, on Elastic). Create it where your domain's zone is hosted. What happens next depends on the edition:

- **PRO** reaches the stack at the master's public address, so `ov` registers it before the record exists. If the name does not point at the stack yet when OpenVidu is up, the deploy ends with that one step left instead of `is up` (the topology named in the first line is the one you deployed):

    ```text
    ! OpenVidu Pro (single node) is deployed on Oracle Cloud, with one step left: openvidu.example.com does not point at it yet.
      Create this DNS record where its zone is hosted, and it is up:
        openvidu.example.com.                    A      <public_ip>
      URL:          https://openvidu.example.com/ (once the record resolves)
      Meanwhile `ov stack status` works (it reaches the stack by its address), and
      `ov stack status --wait` waits for the record too.
    ```

- **COMMUNITY** (Single Node) reaches OpenVidu at its URL, so the deploy **waits for the record**: create it as soon as the deploy prints it, or the wait times out. With Let's Encrypt the certificate is issued once the name resolves.

To move a running stack to a domain afterwards, run `ov stack config set domain-name=openvidu.example.com` (with the certificate settings it needs), or redeploy with `--domain-name` and the certificate flags, which applies them the same way. The change is made in the running stack: the instance is not recreated and keeps its public IP, so point the `A` record at that same address. The vault keeps the `DOMAIN_NAME` and `OPENVIDU_URL` of the first boot.
