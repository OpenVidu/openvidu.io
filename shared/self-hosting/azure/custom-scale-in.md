We use a custom scale-in strategy to allow the graceful shutdown of Media Nodes. In this way we ensure no disruption of active Rooms when the cluster tries to remove a Media Node.

=== "Custom scale-in strategy"

    - All instances in the Media Node Virtual Machine Scale Set (VMSS) are protected to prevent their automatic shutdown.
    - We receive and use the shutdown event to execute a custom Automation runbook.
    - The Automation runbook determines the instance that has to be terminated and executes the appropriate commands in all internal services to prevent them from accepting new jobs (new Rooms, new Egresses, new Ingresses, new Agents...).
    - Only when all the jobs hosted by the selected instance finish, it is automatically terminated.