### Scale In

Google Cloud Platform instances may only wait at most 90 seconds to execute the shutdown script when the MIG terminates them after detecting a surplus of CPU capacity. This is a problem for those active Rooms hosted by the instance that can last longer than that. To avoid the disruption of active Rooms, we have implemented a custom scale-in strategy that uses a lambda function (Cloud Run Function) to gracefully shut down instances only after all active jobs have finished.

Due to GCP limitations, this strategy has the minor drawback that it can take up to 6 minutes from the time that the recommended size changes until the shutdown process is gracefully initiated.