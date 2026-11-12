Without `--domain-name`, the stack answers on an `sslip.io` name derived from its public IP, and Let's Encrypt certifies that name. That is enough to try it out. For anything else, use a domain of your own: pass `--domain-name` on the deploy and point the domain at the machine. You can keep Let's Encrypt, or bring your own certificate.

=== "Let's Encrypt on your domain"

    Add `--domain-name openvidu.example.com` to the deploy command and keep `--certificate-type letsencrypt`. `ov` creates the machine first (`az` returns in about four minutes), then waits for OpenVidu while Let's Encrypt issues the certificate, so create the DNS record during that wait: an `A` record from your domain to the machine's public IP. The IP is the deployment's `publicIp` output (on Elastic the machine is the master node):

    ```bash
    az deployment group show --resource-group <group> --name <deployment> \
      --query properties.outputs.publicIp.value -o tsv
    ```

    Let's Encrypt issues the certificate as soon as the name resolves to that address, and the deploy finishes. Until the record exists, `ov` keeps waiting and reports `URL not answering yet`.

=== "Your own certificate (`owncert`)"

    Bring your own certificate for your domain, base64-encoded, instead of Let's Encrypt. Add these flags to the deploy command:

    ```bash
    --domain-name openvidu.example.com --certificate-type owncert \
      --owncert-public-key "$(base64 -w0 fullchain.pem)" \
      --owncert-private-key "$(base64 -w0 privkey.pem)"
    ```

    On a cloud the certificate travels as a template parameter, so pass its content, base64-encoded as above, not the path to the file. Point your domain at the machine's public IP (the `publicIp` output above) the same way.
