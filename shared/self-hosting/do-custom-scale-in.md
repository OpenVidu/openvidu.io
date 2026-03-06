## Custom scale-in strategy

Currently DigitalOcean does not support autoscaling. OpenVidu Elastic and OpenVidu High Availability Autoscale Pool of Media Nodes is fixed in number.

!!! info
    Autoscaling of Media Nodes in DigitalOcean is a work in progress and will be available in a future release.

<!-- We use a custom scale-in strategy to allow the graceful shutdown of Media Nodes. In this way we ensure no disruption of active Rooms when the cluster tries to remove a Media Node.

=== "Custom scale-in strategy"

    - The Managed Instance Group (MIG) is set to Scale OUT only.
    - We use a lambda function to check if the MIG current size is more than the recommended size that it targets.
    - If the current size is more than the recommended size we calculate the number of instances that should scale in and we remove them from the MIG.
    - The instances have a cron job that checks every minute if they are out of the MIG and runs the graceful shutdown script if they are out of the MIG. -->