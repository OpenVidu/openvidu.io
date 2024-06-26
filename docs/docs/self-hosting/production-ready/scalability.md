# Scalability :material-chart-timeline-variant-shimmer:

Scalability is a very broad term with implications on many levels. In the case of real-time applications, it usually refers to the number of simultaneous Rooms you can host and the maximum number of participants in each Room, or more accurately, the number of media tracks sent and received in each Room.

OpenVidu offers scalability out-of-the-box for typical **videoconferencing** use cases, but also for large low-latency **live streams** with hundreds of viewers. With **OpenVidu Elastic** and **OpenVidu High Availability** you can easily scale your deployment to host many simultaneous videoconferences and live streams. And it is also possible to scale automatically with our **autoscaling** feature, so you can truly adapt your resources to the demand.

## Scalability depending on the use case

### Small and medium videoconferences

OpenVidu allows you to host multiple small and medium videoconferences (up to 10 participants). The number of simultaneous rooms depends on the deployment used and the power of machines.

- **Single Node deployment** (OpenVidu Community): In this deployment, OpenVidu can manage up to **XXX** simultaneous videoconferences of 10 participants in a 4 CPU server. If you need more videoconferences at the same time, you can use more powerful server. This is known as **vertical scalability**. The limit here is usually the maximum computational power available for a single server and the maximum network bandwidth for it.

- **Elastic and High Availability deployments** (OpenVidu Pro): In these deployments, OpenVidu is able to distribute the videoconferences in multiple media servers. This is known as **horizontal scalability**. In this case, the maximum number of simultaneous videoconferences depends on the number of media server used and the computational power of each of them. Also, the service used to coordinate the media servers (Redis) can be the bottleneck and limit the number of videoconferences. In High Availability deployments, Redis is distributed in 4 master nodes, so it is able to handle more load than in the Elastic deployment (with only one master node).

### Big live streams

Live streaming is different from a video conference. In a videoconference, usually all participants can publish audio and video. Instead, in a live stream, only one participant can publish audio and video (known as the publisher) and others can view it (known as viewers).

OpenVidu is able to manage live streams with up to **XXX** viewers (1 publisher and **XXX** subscribers) in a single Room hosted in a server with 4 CPUs. To manage more than one live stream simultaneously, an Elastic or High Availability deployment is needed with several media servers.

### Big videoconferences and massive live streams (Working on it! :hammer:)

For big videoconferences with many participants (in the order of 100- or even 1000-) and massive live streams with few publishers and thousands of viewers, OpenVidu will offer in the near future two distinct strategies:

- **Distributing participants of one Room in multiple servers**: By connecting multiple media servers between them, OpenVidu will be able to manage Rooms with unlimited number of participants and live streams with unlimited number of viewers.
- **Only show last speakers**: A browser or mobile app is able to show a limited number of participants. A powerful computer can visualize up to 10 simultaneous videoconference participants at the same time with high video quality. To allow big videoconferences, OpenVidu will provide features on its frontend SDKs to show only last speakers in the videoconference.

## Autoscaling

**OpenVidu Elastic** and **OpenVidu High Availability** have multiple Media Nodes to handle the load.

- Rooms are distributed among the available nodes prioritizing the less-loaded nodes.
- It is possible to dynamically add new Media Nodes to the cluster when the load increases.
- It is possible to remove Media Nodes from the cluster when the load decreases. If the Media Node is hosting ongoing Rooms, it won't accept new Rooms and will wait until the ongoing Rooms finish before terminating.

When deploying on AWS, OpenVidu will automatically add and remove Media Nodes according to load, thanks to [Auto Scaling Groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html){:target=_blank}. When deploying On Premises you are responsible of monitoring the load of your Media Nodes and triggering the addition of new Media Nodes or removal of existing Media Nodes.
