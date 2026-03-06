
If something goes wrong during the initial DigitalOcean deployment creation, you won't be able to reach the **OPENVIDU_URL**. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check whether the instance or instances are running. If they are not, check whether the `terraform apply` command logged an error.
2. If the instance or instances are running, SSH into the instance and check the logs by running this command:

    ```
    cat /var/log/cloud-init-output.log
    ```

    These logs will give you more information about the DigitalOcean deployment creation process.
