
### (Optional) TURN server configuration with TLS

This section is optional. It is useful when your users are behind a restrictive firewall that blocks UDP traffic. This parameter will only work if you are using `letsencrypt` or `owncert` as the **Certificate Type** parameter.

=== "TURN server configuration with TLS"

    Parameters in this section look like this:

    <figure markdown>
    ![TURN server configuration with TLS](../../../../assets/images/self-hosting/shared/azure-turn-tls.png){ .svg-img .dark-img }
    </figure>

    Set the **Turn Domain Name** parameter to the domain name you intend to use for your TURN server. It should be pointing to the `Public Ip Address` specified in the previous section.

    If you are using `letsencrypt` as the **Certificate Type** parameter, you can leave the **Turn Own Public Certificate** and **Turn Own Private Certificate** parameters empty. If you are using `owncert`, you need to specify the base64 encoded certificates for the TURN server in these parameters.
