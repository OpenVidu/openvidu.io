## Custom scale-in strategy

We use a custom scale-in strategy to enable the graceful shutdown of Media Nodes, ensuring that active Rooms are never disrupted when the cluster removes a Media Node.

=== "Custom scale-in strategy"

    - A Lambda function is deployed on a four-minute schedule to manage the scaling of Media Nodes. It does this by checking the **`minNumberOfMediaNodes`** and **`maxNumberOfMediaNodes`** variables, polling the average CPU usage, and comparing it against **`scaleTargetCPU`**. Once a scale-in decision is made, the main tag is removed from the target Media Node and a "draining" tag is applied to mark it as ready for shutdown.
    - Each instance runs a cron job that checks every two minutes whether the "draining" tag is present. If it is, the graceful shutdown script is triggered, which waits for all active rooms on that node to conclude before shutting down.