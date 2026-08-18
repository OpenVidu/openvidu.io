---
title: "Grafana stack for OpenVidu metrics and logs"
description: "The Grafana, Prometheus, Mimir and Loki stack bundled with OpenVidu, and the dashboards it ships for deployment metrics and cluster logs."
page_features:
  - setupcustomgallery
---

# Grafana Stack

OpenVidu also provides different **Grafana dashboards** to monitor **metrics** from **OpenVidu Server** and **logs** from your **cluster**.

<div>
<a class="glightbox" href="/assets/videos/platform/self-hosting/production-ready/observability/grafana_trailer.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/platform/self-hosting/production-ready/observability/grafana_trailer-preview.mp4" poster="/assets/videos/platform/self-hosting/production-ready/observability/grafana_trailer-poster.jpg" muted playsinline autoplay loop></video></a>
</div>

Grafana is available at `https://your.domain/grafana/` and can be accessed using your **Grafana admin credentials**.

  ![Grafana login](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/login.png){ .mkdocs-img loading=lazy }

Dashboards can be found in the **OpenVidu** folder at `https://your.domain/grafana/dashboards/f/openvidu-dashboards/openvidu`.

  ![Grafana dashboards folder](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/dashboards_folder.png){ .mkdocs-img loading=lazy }

### Services

The **Grafana stack** that comes with OpenVidu is composed of the following services:

- **Grafana** :simple-grafana:: Tool for **querying**, **visualizing**, **alerting on** and **exploring** **metrics**, **logs** and **traces**. It queries different **data sources** to show data in beautiful **dashboards**. In OpenVidu, contains all [dashboards](#dashboards) built from **Mimir**/**Prometheus** and **Loki** data sources to monitor **OpenVidu Server** and **logs** from your **cluster**.
- **Prometheus** :simple-prometheus:: System **monitoring** and **alerting** toolkit. It collects and stores **metrics** from different targets as **time series data**. In OpenVidu, it collects metrics from **OpenVidu Server** of each **Media Node** and sends them to **Mimir**.
- **Mimir**: Grafana software project that provides **multi-tenant**, **long-term storage** for **Prometheus** metrics. In **OpenVidu**, it is used to store metrics collected by **Prometheus**.
- **Promtail**: Agent that ships the contents of **local logs** to a **Loki** instance. In OpenVidu, it is used to collect logs from all **services** in your **cluster** and send them to **Loki**.
- **Loki**: **Horizontally-scalable**, **highly-available**, **multi-tenant** **log aggregation** system inspired by **Prometheus**. In OpenVidu, it is used to store logs collected by **Promtail**.

### Dashboards

#### OpenVidu Server Metrics

This dashboard provides **metrics** about **OpenVidu Server**. It includes charts about **active rooms**, **active participants**, **published tracks**, **subscribed tracks**, **send/receive bytes**, **packet loss percentage** and **quality score**.

In case you are using **OpenVidu** <a href="/pricing/#openvidu-pro">**PRO**{ .openvidu-tag .openvidu-pro-tag }</a> and you have more than one **Media Node** deployed, you will see all metrics from all nodes combined in the same chart.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Grafana dashboard with OpenVidu server metrics](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/metrics1.png){ loading=lazy }
</div>

<div class="grid-50" markdown>
![Further panels of the OpenVidu server metrics dashboard in Grafana](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/metrics2.png){ loading=lazy }
</div>

</div>

#### OpenVidu Media Nodes Server Metrics

!!! info "This dashboard is part of <span>OpenVidu <a href="/pricing/#openvidu-pro">**PRO**{ .openvidu-tag .openvidu-pro-tag }</a></span> edition."

This dashboard provides the same **metrics** as the [OpenVidu Server Metrics](#openvidu-server-metrics) dashboard, but grouped by **Media Node**.

You can select the **Media Node** you want to see metrics from in the **media_node** dropdown. You will see different charts in the same panel according to the selected **Media Nodes**.

  ![Media Node dropdown](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_metrics2.png){ .mkdocs-img loading=lazy }

!!! info
    
    If you add new Media Nodes to your OpenVidu deployment, you will have to refresh the page in order to see the new Media Nodes in the dropdown.

  ![Media Node metrics](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_metrics1.png){ .mkdocs-img loading=lazy }

#### OpenVidu Logs

In case you are using **OpenVidu** <a href="/pricing/#openvidu-community">**COMMUNITY**{ .openvidu-tag .openvidu-community-tag }</a>, this dashboard provides different visualizations for **logs** from your **OpenVidu Single Node deployment**.

There is a panel showing **all containers** logs,

  ![Single Node logs](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/single_node_logs1.png){ .mkdocs-img loading=lazy }

another panel to **filter** logs by **room_id** and **participant_id**,

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Grafana logs dashboard with filters by room and participant](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/single_node_logs3.png){ loading=lazy }
</div>

<div class="grid-50" markdown>
![OpenVidu log entries in the Grafana logs dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/single_node_logs4.png){ loading=lazy }
</div>

</div>

and one row for each selected **service**, containing **all logs**, **warnings** and **errors** from that service.

  ![Single Node select services](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/single_node_logs2.png){ .mkdocs-img loading=lazy }

  ![Single Node service logs](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/single_node_logs6.png){ .mkdocs-img loading=lazy }

You can also filter logs containing a specific **text** by using the **filter search box**.

  ![Single Node filter logs](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/single_node_logs5.png){ .mkdocs-img loading=lazy }

#### OpenVidu Cluster Nodes Logs

!!! info "This dashboard is part of <span>OpenVidu <a href="/pricing/#openvidu-pro">**PRO**{ .openvidu-tag .openvidu-pro-tag }</a></span> edition."

In case you are using **OpenVidu** <a href="/pricing/#openvidu-pro">**PRO**{ .openvidu-tag .openvidu-pro-tag }</a>, this dashboard provides different visualizations for **logs** from your **OpenVidu Elastic** or **OpenVidu High Availability** cluster, grouped by **node**.

First, there is a panel showing **all containers'** logs from all nodes.

  ![Cluster logs](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs1.png){ .mkdocs-img loading=lazy }

Then, there is a row for each selected **node**, containing **all logs**, **warnings** and **errors** from that node. Additionally, each row contains a panel for each selected container, showing all its logs.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Cluster Nodes Logs dashboard with a row of panels per node](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs2.png){ loading=lazy }
</div>

<div class="grid-50" markdown>
![Log panels of a Master Node in the Cluster Nodes Logs dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs3.png){ loading=lazy }
</div>

</div>

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Warnings and errors panels of a node in the Cluster Nodes Logs dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs4.png){ loading=lazy }
</div>

<div class="grid-50" markdown>
![Log panels of a Media Node in the Cluster Nodes Logs dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs5.png){ loading=lazy }
</div>

</div>

!!! info
    
    Note that some panels have no data. This is because some containers are running in **Master Nodes** and others in **Media Nodes**.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Node panels with no data for containers running on other nodes](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs6.png){ loading=lazy }
</div>

<div class="grid-50" markdown>
![Per-container log panels in the Cluster Nodes Logs dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs7.png){ loading=lazy }
</div>

</div>

You can also filter logs containing a specific **text** by using the **filter search box**.

  ![Cluter filter logs](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/nodes_logs8.png){ .mkdocs-img loading=lazy }

#### OpenVidu Cluster Services Logs

!!! info "This dashboard is part of <span>OpenVidu <a href="/pricing/#openvidu-pro">**PRO**{ .openvidu-tag .openvidu-pro-tag }</a></span> edition."

In case you are using **OpenVidu** <a href="/pricing/#openvidu-pro">**PRO**{ .openvidu-tag .openvidu-pro-tag }</a>, this dashboard provides different visualizations for **logs** from your **OpenVidu Elastic** or **OpenVidu High Availability** cluster, grouped by **service**.

First, there is a panel to **filter** logs by **room_id** and **participant_id**.

<div class="grid-container" markdown>

<div class="grid-50" markdown>
![Cluster Services Logs dashboard with filters by room and participant](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/services_logs3.png){ loading=lazy }
</div>

<div class="grid-50" markdown>
![Per-service log panels in the Cluster Services Logs dashboard](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/services_logs4.png){ loading=lazy }
</div>

</div>

Then, there is a row for each selected **service**, containing **all logs**, **warnings** and **errors** from that service.

  ![Cluster select services](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/services_logs1.png){ .mkdocs-img loading=lazy }

  ![Cluster service logs](../../../../assets/images/platform/self-hosting/production-ready/observability/grafana-stack/services_logs2.png){ .mkdocs-img loading=lazy }

### Limitations

For now, in [**OpenVidu High Availability deployments**](../../deployment-types.md#openvidu-high-availability), we have decided to **not** implement Grafana in High Availability (HA) mode. This decision is based on the fact that Grafana needs a configured HA MySQL or PostgreSQL database to work in HA mode, and we want to keep the deployment as simple as possible.

There are 4 instances of Grafana in an OpenVidu High Availability deployment, one for each Master Node, but they are not synchronized with each other. Therefore, if you make any change (change your admin password, create a new dashboard...) in one Grafana instance and the Master Node suddenly goes down, you will be redirected to another Grafana instance where the changes will not be reflected. That is why we disable user signups and saving dashboard or datasource modifications in Grafana.

However, all metrics and logs from all nodes are available in all Grafana instances, so you can monitor your OpenVidu cluster without any problem.
