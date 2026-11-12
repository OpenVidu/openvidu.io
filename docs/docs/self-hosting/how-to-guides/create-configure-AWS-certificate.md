---
title: "Create an AWS certificate for OpenVidu HA"
description: "Issue an AWS certificate for an OpenVidu High Availability deployment: request it, add the CNAME record and attach it to the load balancer."
---

# Create AWS certificate for OpenVidu HA deployment

An OpenVidu High Availability stack on AWS terminates TLS at a Network Load Balancer with an AWS Certificate Manager (ACM) certificate.

!!! info "When your domain is in Route 53, you do not need this guide"

    If the domain is in a public Route 53 hosted zone of the same account, `ov stack deploy` requests the ACM certificate and creates the DNS records for you, with nothing to do by hand. See [Install OpenVidu High Availability on AWS](../ha/aws/install.md).

Follow this guide only when the domain's DNS is **outside Route 53** (another provider or another account), or when you keep the DNS in your own hands with `--param HostedZoneId=`. Then you request the certificate yourself and pass its ARN to the deploy with `--param OpenViduCertificateARN=…`.

## Prerequisites

It is important to note that you will need access to the Certificate Manager in your AWS account, as well as access to a domain provider.
You will need a domain to be able to create and associate the certificate.


## Creation

=== "AWS Certificate creation"

    These are the steps you need to follow to create the AWS certificate; keep in mind that you need a domain.

    First, go to AWS Certificate Manager and request a new public certificate. The following parameter is the most important.

    ![AWS Certificate Manager view](../../../assets/images/platform/self-hosting/how-to-guides/create-configure-cert/domain-name-for-certificate.png){ .round-corners loading=lazy }

    /// caption
    Domain configuration
    ///

    You need to replace **`yourdesiredname`** for whatever name you want and **`yourdomain`** for the name of the domain that you own.

    Next, leave the rest of the parameters as they are and click request.



The next page will display the certificate status. Here you will need to create a record in your domain provider to validate the status; initially it will show as pending.

=== "Create record in your domain provider"

    Here you will need to create a new CNAME record in the domain you own by using the CNAME name (up to the domain name portion) as the subdomain and the CNAME value as the record value.

    In AWS Certificate Manager, you can check the CNAME name and value by clicking on the certificate you want.

=== "Create record in Route 53"

    ![Create record in Route 53](../../../assets/images/platform/self-hosting/how-to-guides/create-configure-cert/create-record-route53.png){ .round-corners loading=lazy }

    You need to click the button called **`Create records in Route 53`**. This will lead you to the next page, where you just click Create records and that's it.

    ![Create record page](../../../assets/images/platform/self-hosting/how-to-guides/create-configure-cert/create-record-page.png){ .round-corners loading=lazy }
    /// caption
    Create record for certificate
    ///

    Please verify that you have a new entry in the records table of the specified Hosted Zone in Route 53 with the CNAME of the certificate you just created.

    Try refreshing until the status changes to Issued (shown in green).


## Deploy the HA stack with the certificate

The High Availability template terminates TLS at a Network Load Balancer with the certificate you just created, so you pass its ARN to the deploy. Copy the **ARN** of the certificate (shown at the top of the certificate's page in AWS Certificate Manager) and give it to `ov stack deploy` as `--param OpenViduCertificateARN=…`, along with your domain:

```bash
ov stack deploy ha --cloud aws --aws-region <region> \
  --edition pro --openvidu-pro-license <your-license> \
  --deployment-type ha \
  --domain-name yourdesiredname.yourdomain \
  --param OpenViduCertificateARN=arn:aws:acm:<region>:<account>:certificate/<id> \
  --mode auto
```

Because the load balancer terminates TLS with this ACM certificate, `--certificate-type` does not apply to an HA stack on AWS (if you pass one, the deploy warns and goes on). For the full AWS deploy options (VPC, subnets and the rest), see [Install OpenVidu High Availability on AWS](../ha/aws/install.md).

## Point the domain at the load balancer

As soon as the stack exists, the deploy prints the record to create, so you can create it while the machines deploy; until the domain points at the load balancer, nothing serves it. The `NLBDNS` output is the load balancer's DNS name:

- **At your DNS provider** (the domain is outside Route 53): create a **CNAME** record from `yourdesiredname.yourdomain` to the stack's `NLBDNS` output.
- **In a Route 53 zone you kept with `--param HostedZoneId=`:** create an **alias** record instead.

To create the alias in Route 53:

![Create Load Balancer record](../../../assets/images/platform/self-hosting/how-to-guides/create-configure-cert/create-lbrecord.png){ .round-corners loading=lazy }

- Enable **Alias**.
- In **subdomain**, enter the same value you used for `yourdesiredname` when creating the AWS certificate.
- In **Choose endpoint**, select *Alias to Network Load Balancer*, and in **Choose Region** select the region where the stack is deployed.
- In the field that appears, select the load balancer that belongs to the stack you deployed (its DNS name is the stack's `NLBDNS` output).

For the other fields, leave them as they are.