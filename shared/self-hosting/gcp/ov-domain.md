By default the stack answers on an `sslip.io` name derived from its public IP, which is fine for testing. For anything real, use **your own domain**. No Google Cloud template points a domain for you, so you create one DNS record; `ov` prints it as soon as the machine has a public IP, so you can create it while OpenVidu installs.

Pass `--domain-name` and the certificate you want: `--certificate-type letsencrypt` issues one automatically once the record resolves, or `owncert` carries your own (the [`--owncert-public-key` / `--owncert-private-key` flags](/docs/self-hosting/ha/gcp/install.md#deploy), base64-encoded).

```bash
ov stack deploy openvidu --cloud gcp --gcp-project my-project \
  --edition pro --openvidu-pro-license <your-license> \
  --domain-name openvidu.example.com --certificate-type letsencrypt --mode auto
```

As soon as the machine has its public IP, the deploy prints the `A` record to create (`<domain> A <public_ip>`) and goes on installing OpenVidu meanwhile. What happens at the end depends on the edition:

- An **OpenVidu PRO**{ .openvidu-tag .openvidu-pro-tag } deploy does not wait for the record. If the domain does not point at the stack when OpenVidu is up, it ends with one step left instead of `is up`, and prints the record again:

    ```text
    ! OpenVidu Pro (single node) is deployed on Google Cloud, with one step left: openvidu.example.com does not point at it yet.
      Create this DNS record where its zone is hosted, and it is up:
        openvidu.example.com.                    A      203.0.113.10
      URL:          https://openvidu.example.com/ (once the record resolves)
      Meanwhile `ov stack status` works (it reaches the stack by its address), and
      `ov stack status --wait` waits for the record too.
    ```

- An **OpenVidu COMMUNITY**{ .openvidu-tag .openvidu-community-tag } Single Node deploy reaches the stack by its URL, so its wait blocks on the record (up to `--wait-timeout`) and ends with the stack up once the name resolves.

Create the record as soon as `ov` prints it. With `letsencrypt`, the certificate is issued the moment the name resolves to the stack; `ov stack status --wait` reports `URL not answering yet` until then.
