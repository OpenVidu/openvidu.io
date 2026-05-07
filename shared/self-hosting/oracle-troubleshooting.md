
If something goes wrong during the initial Oracle Cloud Infrastructure deployment, you will not be able to reach the **OPENVIDU_URL**. This can happen due to a misconfiguration in the parameters, insufficient permissions, or a problem with OCI services. The steps below will help you troubleshoot the issue and identify the root cause:

1. Check whether the instance is running. If it is not, review the output of the `terraform apply` command for any errors.
2. If the instance is running, SSH into it and inspect the logs by running the following command:

    ```
    cat /var/log/cloud-init-output.log
    ```

    These logs contain detailed information about the Oracle Cloud Infrastructure deployment process.
