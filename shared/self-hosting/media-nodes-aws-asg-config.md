=== "Media Nodes Autoscaling Group Configuration"

    Parameters in this section look like this:

    ![Media Nodes Autoscaling Group Configuration](../../../../assets/images/self-hosting/elastic/aws/media-nodes-asg-config.png)

    The **InitialNumberOfMediaNodes** parameter specifies the initial number of Media Nodes to deploy. The **MinNumberOfMediaNodes** and **MaxNumberOfMediaNodes** parameters specify the minimum and maximum number of Media Nodes that you want to be deployed.

    The **ScaleTargetCPU** parameter specifies the target CPU utilization to trigger the scaling up or down. The goal is to keep the CPU utilization of the Media Nodes close to this value. The autoscaling policy is based on [Target Tracking Scaling Policy :fontawesome-solid-external-link:{.external-link-icon}](https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html){:target=_blank}.