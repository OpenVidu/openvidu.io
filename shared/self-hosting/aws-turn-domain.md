
### (Optional) TURN server configuration with TLS

This section is optional. It is useful when your users are behind a restrictive firewall that blocks UDP traffic. This parameter will only work if you are using `letsencrypt` or `owncert` as the **CertificateType** parameter.

Note that if you are not using any Domain Name in the [Domain and SSL Certificate Configuration](#domain-and-ssl-certificate-configuration) section, this section will be ignored and a generated domain based on the public IP and [sslip.io](https://sslip.io/){:target="_blank"} will be used instead.

=== "TURN server configuration with TLS"

    Parameters in this section look like this:

    ![TURN server configuration with TLS](../../../../assets/images/self-hosting/shared/aws-turn-tls.png)

    Set the **TurnDomainName** parameter to the domain name you intend to use for your TURN server. It should be pointing to the `PublicElasticIP` specified in the previous section.

    If you are using `letsencrypt` as the **CertificateType** parameter, you can leave the **TurnOwnPublicCertificate** and **TurnOwnPrivateCertificate** parameters empty. If you are using `owncert`, you need to specify the base64 encoded certificates for the TURN server in these parameters.
