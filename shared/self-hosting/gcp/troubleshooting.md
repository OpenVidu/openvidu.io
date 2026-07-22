
If something goes wrong during the initial GCP deployment creation, your stack may reach some failed status for multiple reasons. It could be due to a misconfiguration in the parameters, a lack of permissions, or a problem with GCP services. When this happens, the following steps can help you troubleshoot the issue and identify what went wrong:

1. Check if the instance or instances are running. If they are not, check the GCP cloud build logs for any error messages.
2. If the instance or instances are running, SSH into the instance and check the logs by running this command:

    - `journalctl -u google-startup-scripts | cat`

    These logs will give you more information about the GCP deployment creation process.
