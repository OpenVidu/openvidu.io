The deploy commands above derive an `sslip.io` name from the machine's public IP and certify it with Let's Encrypt, so they work without a domain of yours. That is meant for testing. For anything else, use your own domain: add `--domain-name openvidu.example.com` to the deploy, and choose a certificate for it.

- **`--certificate-type letsencrypt`** (the default) issues a Let's Encrypt certificate once the domain resolves.
- **`--certificate-type owncert`** serves a certificate of yours instead. On a cloud the certificate travels as a template parameter, so pass its content, base64-encoded, not the path to the file:

    ```bash
    --domain-name openvidu.example.com --certificate-type owncert \
      --owncert-public-key "$(base64 -w0 fullchain.pem)" \
      --owncert-private-key "$(base64 -w0 privkey.pem)"
    ```

Caddy serves the certificate from the machine, as in any other Single Node or Elastic deployment. With `--domain-name`, the deploy reads the domain's DNS in your account (read-only calls, in both modes) while it builds the plan, and the plan says which of two paths applies:

- **The domain is in a Route 53 hosted zone of this account**, and the public DNS delegates it there. `ov` finds the zone and the stack creates an **A record** from the domain to the machine's Elastic IP (the master's, on Elastic), deleted with the stack. The deploy then waits until the domain resolves and OpenVidu answers on it, and only then says the stack is up. If the zone already has an `A`, `AAAA` or `CNAME` record for the domain, the deploy stops before creating anything (exit `2`): delete that record first, or pass `--param HostedZoneId=` to keep the DNS in your hands.

- **The domain is somewhere else** (another DNS provider or another account), or you pass `--param HostedZoneId=`. You create the record. As soon as the machine exists, the deploy prints it, so you can create it while the machine installs:

    ```text
    openvidu.example.com has to point at the stack. Unless it already does, create this DNS record where its
    zone is hosted (the deploy goes on meanwhile):
        openvidu.example.com.                    A      89.60.28.34
    ```

    What happens at the end depends on the edition. A **COMMUNITY** deploy reaches OpenVidu at its URL, so it **waits for the record** (up to `--wait-timeout`): create it as soon as the deploy prints it, or the wait times out. A **PRO** deploy does not wait for it: if the domain does not resolve to the stack by the time the machine is ready, the deploy does not say the stack is up. It ends with the step left instead:

    ```text
    ! OpenVidu Pro (single node) is deployed on AWS, with one step left: openvidu.example.com does not point at it yet.
      Create this DNS record where its zone is hosted, and it is up:
          openvidu.example.com.                    A      89.60.28.34
      URL:          https://openvidu.example.com/ (once the record resolves)
    ```

For two Route 53 zones with the same name, where `ov` refuses to guess, pass `--param HostedZoneId=<id>` to name the one to use.
