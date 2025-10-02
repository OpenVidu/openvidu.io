# Scalability

Scalability is a very broad term with implications on many levels. In the case of real-time applications, it usually refers to the number of simultaneous Rooms you can host and the maximum number of participants in each Room, or more accurately, the number of media tracks sent and received in each Room.

OpenVidu offers scalability out-of-the-box for typical **videoconferencing** use cases, but also for large low-latency **live streams** with hundreds of viewers. With **OpenVidu Elastic** and **OpenVidu High Availability** you can easily scale your deployment to host many simultaneous videoconferences and live streams. And it is also possible to scale automatically with our **autoscaling** feature, so you can truly adapt your resources to the demand.

## Scalability depending on the use case

### Small and medium videoconferences

OpenVidu allows you to host multiple small and medium videoconferences (up to 10 participants). The number of simultaneous rooms depends on the deployment used and the power of machines.

- **Single Node deployment** (OpenVidu Community): In this deployment, OpenVidu can manage up to **50** simultaneous videoconferences of 8 participants in a 4 CPU server. If you need more videoconferences at the same time, you can use more powerful server. This is known as **vertical scalability**. The limit here is usually the maximum computational power available for a single server and the maximum network bandwidth for it. You can read more about this benchmark scenario in the [Performance benchmarks](../performance/#benchmarking) page.
- **Elastic and High Availability deployments** (OpenVidu Pro): In these deployments, OpenVidu is able to distribute the videoconferences in multiple media servers. This is known as **horizontal scalability**. In this case, the maximum number of simultaneous videoconferences depends on the number of media server used and the computational power of each of them. Also, other services used to coordinate and monitor the media servers (caches, data bases, proxies) can themselves become bottlenecks and limit the capacity of the system. In High Availability deployments, these services are distributed in 4 master nodes, so it is able to handle more load than in the Elastic deployment (with only 1 master node).

### Big live streams

Live streaming is different from a video conference. In a videoconference, usually all participants can publish audio and video. Instead, in a live stream, only one participant can publish audio and video (known as the publisher) and others can view it (known as viewers).

OpenVidu is able to manage live streams with up to **1000** viewers (1 publisher and **1000** subscribers) in a single Room hosted in a server with 4 CPUs. To manage more than one live stream simultaneously, an Elastic or High Availability deployment is needed with several media servers.

### Big videoconferences and massive live streams (Working on it! )

For big videoconferences with many participants (in the order of 100- or even 1000-) and massive live streams with few publishers and thousands of viewers, OpenVidu will offer in the near future two distinct strategies:

- **Distributing participants of one Room in multiple servers**: By connecting multiple media servers between them, OpenVidu will be able to manage Rooms with unlimited number of participants and live streams with unlimited number of viewers.
- **Only show last speakers**: A browser or mobile app is able to show a limited number of participants. A powerful computer can visualize up to 10 simultaneous videoconference participants at the same time with high video quality. To allow big videoconferences, OpenVidu will provide features on its frontend SDKs to show only last speakers in the videoconference.

## Load balancing strategies across Media Nodes

In **OpenVidu Elastic** and **OpenVidu High Availability**, work is distributed across multiple Media Nodes. The distribution strategy varies depending on the type of job.

### Rooms

The Room allocation strategy can be configured in the [**`livekit.yaml`** configuration file](../../configuration/changing-config/#config-files). Specifically, property `node_selector` defines the strategy to select the Media Node where a new Room will be hosted:

livekit.yaml

```yaml
node_selector:
    kind: any # [any, cpuload, sysload]
    sort_by: sysload # [random, sysload, cpuload, rooms, clients, tracks, bytespersec]
    cpu_load_limit: 0.9 # used with kind cpuload
    sysload_limit: 0.9 # used with kind sysload
```

Upon a new Room creation request:

1. First, property `kind` acts as a filter to remove non-eligible nodes:

   | `kind`  | Description                                                                                                                                                                         |
   | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | any     | All nodes are eligible.                                                                                                                                                             |
   | cpuload | Only nodes with CPU load below `cpu_load_limit` are eligible. cpuload states the current CPU load of the node. This is the **default** option.                                      |
   | sysload | Only nodes with system load below `sysload_limit` are eligible. sysload smooths CPU spikes in comparison to cpuload, as it takes the average load of the system in the last minute. |

1. Then, property `sort_by` defines how to sort the eligible nodes. The first node in the sorted list will be chosen to host the new Room:

   | `sort_by`   | Description                                                                             |
   | ----------- | --------------------------------------------------------------------------------------- |
   | random      | A random node will be selected.                                                         |
   | cpuload     | The node with the lowest CPU load will be selected. This is the **default** option.     |
   | sysload     | The node with the lowest system load will be selected.                                  |
   | rooms       | The node with the lowest total number of Rooms hosted will be selected.                 |
   | clients     | The node with the lowest total number of clients connected will be selected.            |
   | tracks      | The node with the lowest total number of media tracks being processed will be selected. |
   | bytespersec | The node with the lowest bandwidth will be selected.                                    |

   Room allocation never fails, as long as there is at least one Media Node connected to the cluster. Limits `cpu_load_limit` and `sysload_limit` will simply be ignored if no node is eligible.

### Egress

Info

Check out the official Egress documentation of LiveKit [here](https://docs.livekit.io/home/egress/overview/) .

The Egress allocation strategy can be configured in the [**`egress.yaml`** configuration file](../../configuration/changing-config/#config-files).

egress.yaml

```yaml
cpu_cost:
    max_cpu_utilization: 0.8
    room_composite_cpu_cost: 2.0
    audio_room_composite_cpu_cost: 1.0
    web_cpu_cost: 2.0
    audio_web_cpu_cost: 0.5
    participant_cpu_cost: 1.0
    track_composite_cpu_cost: 1.0
    track_cpu_cost: 0.5

openvidu:
    allocation_strategy: cpuload # [cpuload, binpack]
```

Upon a new Egress request:

1. First, OpenVidu filters eligible Media Nodes. A Media Node is eligible to host a new Egress request if:

   1. Its **CPU load is below a certain threshold** (by default 80%).
   1. It has enough **free CPUs** to handle the new Egress. The amount of free CPUs required depends on the type of Egress (room composite egress, web egress, participant egress, track composite egress, track egress).

   Sane defaults are provided by OpenVidu, but you can configure both the CPU load threshold and the amount of free CPUs required for each type of Egress in the `cpu_cost`:

   egress.yaml

   ```yaml
   cpu_cost:
       max_cpu_utilization: 0.8
       room_composite_cpu_cost: 2.0
       audio_room_composite_cpu_cost: 1.0
       web_cpu_cost: 2.0
       audio_web_cpu_cost: 0.5
       participant_cpu_cost: 1.0
       track_composite_cpu_cost: 1.0
       track_cpu_cost: 0.5
   ```

1. Then, OpenVidu chooses from the pool of eligible nodes the best one according to property `openvidu.allocation_strategy`:

   egress.yaml

   ```yaml
   openvidu:
       allocation_strategy: cpuload # [cpuload, binpack]
   ```

   | `sort_by` | Description                                                                                                                                                                                          |
   | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | cpuload   | The node with the lowest CPU load will be selected. This strategy helps distributing the CPU load evenly across all available nodes. This is the **default** option.                                 |
   | binpack   | Some node already hosting at least one Egress will be selected. If all eligible nodes are idle, a random one will be chosen. This strategy helps filling up nodes before assigning work to new ones. |

1. If no Media Node is eligible, the Egress request fails with a **`503 Service Unavailable`** error.

#### Egress CPU overload killer

By default the Egress service has the ability to **automatically kill active egresses under high CPU load**. If a >95% CPU load is sustained over 10 seconds, the Egress service will automatically terminate the most CPU-intensive active egress.

This helps preventing an egress process from overloading the entire Media Node. Nonetheless, this feature can be disabled by setting property `openvidu.disable_cpu_overload_killer` to `true` in the [**`egress.yaml`** configuration file](../../configuration/changing-config/#config-files):

egress.yaml

```yaml
openvidu:
    disable_cpu_overload_killer: true
```

### Ingress

Info

Check out the official Ingress documentation of LiveKit [here](https://docs.livekit.io/home/ingress/overview/) .

The Ingress allocation strategy is fixed and cannot be changed. Upon a new Ingress request:

1. First, OpenVidu filters eligible Media Nodes. A Media Node is eligible to host a new Ingress request if it has enough **free CPUs** to handle it. The amount of free CPUs required depends on the type of Ingress (RTMP, WHIP, URL). Sane defaults are provided by OpenVidu, but you can tweak these values by modifying the following properties in the [**`ingress.yaml`** configuration file](../../configuration/changing-config/#config-files):

   ingress.yaml

   ```yaml
   cpu_cost:
       rtmp_cpu_cost: 2.0
       whip_cpu_cost: 2.0
       whip_bypass_transcoding_cpu_cost: 0.1
       url_cpu_cost: 2.0
       min_idle_ratio: 0.3
   ```

1. Then, OpenVidu chooses a **random** Media Node among the eligible ones. If no Media Node is eligible, the Ingress request fails with a **`503 Service Unavailable`** error.

### Agents

For AI agents the allocation strategy varies depending if the Agent is an [**OpenVidu agent**](../../../ai/openvidu-agents/overview/) or a [**custom agent**](../../../ai/custom-agents/).

- For [**OpenVidu agents**](../../../ai/openvidu-agents/overview/): the agent will be available to process a new request if the CPU load of its Media Node is below a threshold. The default threshold is 70%, but you can change it in the agent's YAML configuration file. For example, for the **Speech Processing Agent**, you can change it in [**`agent-speech-processing.yaml`**](../../../ai/openvidu-agents/speech-processing-agent/#configuration-reference):

  agent-speech-processing.yaml

  ```yaml
  # Maximum CPU load threshold for the agent to accept new jobs. Value between 0 and 1.
  load_threshold: 0.7
  ```

- When developing a [**custom agent**](../../../ai/custom-agents/): the agent will be available to process a new request if its load does not exceed a specific threshold. Both the load metric and its threshold have the same defaults as for OpenVidu agents (average CPU load must be below 70%), but you can customize them in the `WorkerOptions` when developing your agent:

  ```python
  # Called to determine the current load of the worker. Must return a value between 0 and 1
  def custom_load_function(worker: Worker) -> float:
      ...
      return load_value

  worker_options = WorkerOptions(
      ...
      load_fnc=custom_load_function,
      load_threshold=0.7,  # Maximum load to consider the worker available
      ...
  )
  ```

  ```javascript
  // Called to determine the current load of the worker. Must return a value between 0 and 1
  const customLoadFunction = (worker: Worker): Promise<number> => {
      ...
      return loadValue;
  };

  const workerOptions = {
      ...
      loadFunc: customLoadFunction,
      loadThreshold: 0.7,  // Maximum load to consider the worker available
      ...
  };
  ```

In both cases, OpenVidu will assign the request to a random available agent. If no agent is available, the request will be ignored. The log of the [OpenVidu Server service](../../deployment-types/#media-node-services) will show an INFO message stating `not dispatching agent job since no worker is available`.

## Autoscaling

**OpenVidu Elastic** and **OpenVidu High Availability** have multiple Media Nodes to handle the load.

- Rooms, Egress, Ingress and Agents are distributed across the Media Nodes according to different allocation strategies. Some strategies are configurable, others are fixed, but all of them have sane defaults (see [Load balancing strategies across Media Nodes](#load-balancing-strategies-across-media-nodes)).
- It is possible to dynamically add new Media Nodes to the cluster when the load increases. New nodes will automatically start accepting new jobs according to the allocation strategies.
- It is possible to dynamically remove Media Nodes from the cluster when the load decreases. If the Media Node is hosting ongoing jobs (Rooms, Egresses, Ingresses or Agents), it will enter in a draining state in which it will not accept new jobs, but will continue processing the ongoing ones until they finish. At that point, the Media Node will be removed from the cluster.

The deployment environment determines how the autoscaling is managed:

### Autoscaling in cloud providers

When deploying in a supported **cloud provider** using our official templates, OpenVidu will automatically add and remove Media Nodes according to load. Depending on the cloud provider:

Deploy OpenVidu using our official **CloudFormation** template:

- [OpenVidu Elastic in AWS](../../elastic/aws/install/)
- [OpenVidu High Availability in AWS](../../ha/aws/install/)

The cluster scales automatically thanks to [AWS Auto Scaling Groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html) . You can configure the Auto Scaling Group parameters when deploying the CloudFormation stack, in section **Media Nodes Autoscaling Group Configuration**.

Parameters in this section look like this:

The **InitialNumberOfMediaNodes** parameter specifies the initial number of Media Nodes to deploy. The **MinNumberOfMediaNodes** and **MaxNumberOfMediaNodes** parameters specify the minimum and maximum number of Media Nodes that you want to be deployed.

The **ScaleTargetCPU** parameter specifies the target CPU utilization to trigger the scaling up or down. The goal is to keep the CPU utilization of the Media Nodes close to this value. The autoscaling policy is based on [Target Tracking Scaling Policy](https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html) .

Deploy OpenVidu using our official **ARM** template:

- [OpenVidu Elastic in Azure](../../elastic/azure/install/)
- [OpenVidu High Availability in Azure](../../ha/azure/install/)

The cluster scales automatically thanks to [Azure Virtual Machine Scale Sets](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/) . You can configure the Scale Set parameters when deploying the ARM template, in section **Media Nodes Scaling Set Configuration**.

Parameters in this section look like this:

The **Initial Number Of Media Nodes** parameter specifies the initial number of Media Nodes to deploy. The **Min Number Of Media Nodes** and **Max Number Of Media Nodes** parameters specify the minimum and maximum number of Media Nodes that you want to be deployed.

The **Scale Target CPU** parameter specifies the target CPU utilization to trigger the scaling up or down. The goal is to keep the CPU utilization of the Media Nodes close to this value. The autoscaling policy is based on [Azure Monitor autoscale metrics](https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling#use-the-azure-monitor-autoscale-feature) .

### Autoscaling On Premises

When deploying an OpenVidu cluster **On Premises** you are responsible of monitoring the load of your Media Nodes and triggering the addition of new Media Nodes or removal of existing Media Nodes. Depending on your OpenVidu deployment type, you can do so like this:

- For **OpenVidu Elastic On Premises**:
  - [Add a new Media Node](../../elastic/on-premises/admin/#adding-media-nodes)
  - [Removing Media Nodes gracefully](../../elastic/on-premises/admin/#removing-media-nodes-gracefully)
  - [Removing Media Nodes forcefully](../../elastic/on-premises/admin/#removing-media-nodes-forcefully)
- For **OpenVidu High Availability On Premises**:
  - [Adding Media Nodes](../../ha/on-premises/admin/#adding-media-nodes)
  - [Removing Media Nodes gracefully](../../ha/on-premises/admin/#removing-media-nodes-gracefully)
  - [Removing Media Nodes forcefully](../../ha/on-premises/admin/#removing-media-nodes-forcefully)
