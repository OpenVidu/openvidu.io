=== "Media Nodes Scaling Set Configuration"

    Parameters in this section look like this:

    <figure markdown>
    ![Media Nodes Scaling Set Configuration](../../../../assets/images/self-hosting/elastic/azure/media-nodes-asg-config.png){ .svg-img .dark-img }
    </figure>

    The **Initial Number Of Media Nodes** parameter specifies the initial number of Media Nodes to deploy. The **Min Number Of Media Nodes** and **Max Number Of Media Nodes** parameters specify the minimum and maximum number of Media Nodes that you want to be deployed.

    The **Scale Target CPU** parameter specifies the target CPU utilization to trigger the scaling up or down. The goal is to keep the CPU utilization of the Media Nodes close to this value. The autoscaling policy is based on [Azure Monitor autoscale metrics :fontawesome-solid-external-link:{.external-link-icon}](https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling#use-the-azure-monitor-autoscale-feature){:target=_blank}.