### Domain and SSL Certificate Configuration

There are three possible scenarios for this section:

=== "Let's Encrypt Without Domain Name"

    If you don't have a Domain Name and want to quickly test OpenVidu on Azure, you can use this option, simply selecting the **Certificate Type** as _letsencrypt_ and keep the rest of parameters empty.

    It will deploy OpenVidu with a Let's Encrypt certificate generated using [sslip.io](https://sslip.io/){:target="_blank"} based on the public IP created for the deployment.

    ![Let's Encrypt certificates](../../../../assets/images/self-hosting/shared/azure-letsencrypt-nodomain.png)

=== "Let's Encrypt With Domain Name (recommended)"

    For a production-ready setup, this scenario is ideal when you have an **FQDN (Fully Qualified Domain Name)** and a **Public IP** at your disposal. It leverages the services of Let's Encrypt to automatically generate valid certificates.

    First, you need to have the FQDN pointing to the Public IP you are going to use.

    Then, you need to fill in the following parameters:

    <figure markdown>
    ![Let's Encrypt certificates](../../../../assets/images/self-hosting/shared/azure-letsencrypt.png){ .svg-img .dark-img }
    </figure>

    As you can see, you need to specify the **Public Ip Address** with the Public IP that the domain points to, the **Domain Name** with your FQDN, and the **Lets Encrypt Email** with your email address for Let’s Encrypt notifications. These parameters are mandatory.

=== "Custom Certificates"

    Opt for this method if you possess **your own certificate for an existing FQDN**. It enables you to deploy OpenVidu on Azure using your certificates.

    You need to have your FQDN pointing to a previously created Public Ip.

    The configured parameters would look like this:
    
    <figure markdown>
    ![Custom certificates](../../../../assets/images/self-hosting/shared/azure-owncert.png){ .svg-img .dark-img }
    </figure>

    
    You need to specify at **Own Public Certificate** and **Own Private Certificate** the certificates files in base64. The **Domain Name**, **Public Ip Address** are mandatory parameters.

    Certificates need to be in PEM format and base64 encoded. You can encode them using the following command in a terminal where `fullchain.pem` is your public certificate and `privkey.pem` is your private certificate:

    ```bash
    base64 -w 0 fullchain.pem # OwnPublicCertificate
    base64 -w 0 privkey.pem # OwnPrivateCertificate
    ```

=== "Self-Signed Certificate"

    This is the most straightforward option for deploying OpenVidu on Azure when you do not have a Fully Qualified Domain Name (FQDN). This method allows for the immediate use of OpenVidu with ARM Templates.

    However, this convenience comes with the caveat that users will need to manually accept the certificate in their web browsers. Please be aware that this configuration is solely for developmental and testing purposes and is not suitable for a real production environment.

    These are the parameters needed in this section to use self-signed certificates:
    
    <figure markdown>
    ![Self-signed certificates](../../../../assets/images/self-hosting/shared/azure-selfsigned.png){ .svg-img .dark-img }
    </figure>
    
    You don’t need to specify any parameters; just select the **CertificateType** as _self-signed_. The domain name used will be an Azure-generated one.
