## Custom scale-in strategy

We use a custom scale-in strategy to allow the graceful shutdown of Media Nodes. In this way we ensure no disruption of active Rooms when the cluster tries to remove a Media Node.

=== "Custom scale-in strategy"

    - A lambda function is deployed scheduled every four minutes to manage the scale out and scale in of the media nodes by checking the variables of **minNumberOfMediaNodes** and **maxNumberOfMediaNodes** and by polling the average CPU usage and comparing it with the **scaleTargetCPU**.    
    When a decision is made, the main tag is removed from the media node and a ‘draining’ tag is added to mark it as complete.
    - The instances have a cron job that checks every two minute if they have the ‘draining’ tag and if that is true they start the graceful shutdown script waiting for the meetings in that node to stop.