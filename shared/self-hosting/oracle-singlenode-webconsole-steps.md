### Prerequisites

- An OCI account with permission to create Compute instances and networking resources.

---

### 1. Create the Compute instance

1. Log in to your [**Oracle Cloud Infrastructure** :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.oracle.com/){:target=_blank} account.
2. Search for **Instances**, open it, and click _"Create instance"_.

    <figure markdown>
    ![OCI create instance](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/create-instance.png){ .svg-img .dark-img }
    </figure>

3. Set a name for the instance (for example, `openvidu-singlenode`), or keep the default.
4. Change the image to _"Canonical Ubuntu 24.04"_.

    <figure markdown>
    ![Instance select image](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/select-image.png){ .svg-img .dark-img }
    </figure>

5. Select the shape for your OpenVidu server. We recommend **at least 1 OCPU and 4 GB of RAM** for OpenVidu to run correctly. Then click _"Next"_.

    !!! note
        ARM-based instances are also supported. OpenVidu supports ARM, and the [**Always Free-eligible**](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm){:target="_blank"} tier includes an ARM instance at no cost.

6. In the **Security** tab, keep the default options and click _"Next"_.
7. Create a new `VNIC` with a new `virtual cloud network` and a new `public subnet`.

    <figure markdown>
    ![Network configuration](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/network-config.png){ .svg-img .dark-img }
    </figure>

8. Scroll down and download the private key for the instance so you can connect via SSH. Then click _"Next"_.

    <figure markdown>
    ![Download SSH key](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/download-ssh-key.png){ .svg-img .dark-img }
    </figure>

9.  In the **Storage** tab, select _"Specify a custom boot volume size"_ and set it to **100 GB** instead of the default 50 GB. You can keep 50 GB, but OpenVidu may fail due to insufficient disk space. Then click _"Next"_.

    <figure markdown>
    ![Volume size configuration](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/volume-size-config.png){ .svg-img .dark-img }
    </figure>

10. Review the configuration and click _"Create"_.

---

### 2. Attach a public IP address to the instance

1. Open the instance details, navigate to the **VNIC** resource, and go to the _"Networking"_ tab.

    <figure markdown>
    ![VNIC location](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/vnic-location.png){ .svg-img .dark-img }
    </figure>

2. Open the _"IP administration"_ tab. In the row of the existing IPv4 address, click the three-dots menu and select _"Edit"_.

    <figure markdown>
    ![Edit IPv4](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/edit-ipv4.png){ .svg-img .dark-img }
    </figure>

3. Select _"Ephemeral public IP"_ and click _"Update"_.

    <figure markdown>
    ![Create Ephemeral Public IPv4](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ipv4-ephemeral-public-address.png){ .svg-img .dark-img }
    </figure>

---

### 3. Port rules in the network security lists

OpenVidu and WebRTC require specific inbound rules on both the instance network security (OCI NSG or subnet security list) and the instance firewall (configured later).

The [minimum inbound ports to allow](../on-premises/install.md#port-rules) must be included in the security list rules.

1. From the instance _"Details"_ page, click the _"Virtual cloud network"_ resource.

    <figure markdown>
    ![VCN location](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/vcn-location.png){ .svg-img .dark-img }
    </figure>

2. Go to the _"Security"_ tab and click the default security list.

    <figure markdown>
    ![Security tab](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/security-tab.png){ .svg-img .dark-img }
    </figure>

3. In the _"Security Rules"_ tab, add the following **Ingress rules**.

??? "Ingress Rules"
    <figure markdown>
    ![Ingress rule 1](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule1.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 2](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule2.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 3](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule3.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 4](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule4.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 5](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule5.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 6](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule6.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 7](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule7.png){ .svg-img .dark-img }
    </figure>
    <figure markdown>
    ![Ingress rule 8](../../../../assets/images/self-hosting/single-node/oracle/install-tutorial/ingress-rule8.png){ .svg-img .dark-img }
    </figure>

---

### 4. SSH access, OpenVidu installation, and firewall rules

!!! warning
    Open the required ports in the OS firewall before installing OpenVidu to avoid connectivity issues.

1. SSH into the instance:

    ```bash
    ssh -i private_key_downloaded.key ubuntu@PUBLIC_IP
    sudo apt update && sudo apt upgrade -y
    ```

2. Install and start the `firewalld` tool:

    ```bash
    sudo apt install firewalld -y
    sudo systemctl enable firewalld
    sudo systemctl start firewalld
    ```

3. Clear the existing `iptables` rules, set the default input policy to ACCEPT, disable `iptables` persistence at startup, and restart the network service if required:

    ```bash
    sudo iptables -F
    sudo iptables -P INPUT ACCEPT
    sudo systemctl disable netfilter-persistent
    ```

4. Add the required firewall rules:

    ```bash
    firewall-cmd --add-port=80/tcp
    firewall-cmd --permanent --add-port=80/tcp

    firewall-cmd --add-port=443/tcp
    firewall-cmd --permanent --add-port=443/tcp

    firewall-cmd --add-port=443/udp
    firewall-cmd --permanent --add-port=443/udp

    firewall-cmd --add-port=1935/tcp
    firewall-cmd --permanent --add-port=1935/tcp

    firewall-cmd --add-port=7881/tcp
    firewall-cmd --permanent --add-port=7881/tcp

    firewall-cmd --add-port=7885/udp
    firewall-cmd --permanent --add-port=7885/udp

    firewall-cmd --add-port=9000/tcp
    firewall-cmd --permanent --add-port=9000/tcp

    firewall-cmd --add-port=50000-60000/udp
    firewall-cmd --permanent --add-port=50000-60000/udp
    ```

5. Apply the rules and verify they are correctly configured:

    ```bash
    firewall-cmd --reload
    firewall-cmd --runtime-to-permanent

    firewall-cmd --list-all
    ```
