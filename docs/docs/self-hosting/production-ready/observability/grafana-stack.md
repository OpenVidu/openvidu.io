## Grafana Stack

OpenVidu also provides different **Grafana dashboards** to monitor **metrics** from **OpenVidu Server** and **logs** from your **cluster**.

<video controls>
<source src="/assets/videos/grafana_trailer.mp4" type="video/mp4">
</video>

Grafana is available at [https://your.domain/grafana/]() and can be accessed using your **Grafana admin credentials**.

<figure markdown>
  ![Grafana login](../../../../assets/images/grafana/login.png){ .mkdocs-img }
</figure>

Dashboards can be found in the **OpenVidu** folder at [https://your.domain/grafana/dashboards/f/openvidu-dashboards/openvidu]().

<figure markdown>
  ![Grafana dashboards folder](../../../../assets/images/grafana/dashboards_folder.png){ .mkdocs-img }
</figure>

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

In case you are using **OpenVidu** <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a> and you have more than one **Media Node** deployed, you will see all metrics from all nodes combined in the same chart.

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/metrics1.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/metrics1.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/metrics2.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/metrics2.png" loading="lazy"/></a></p></div>

</div>

#### OpenVidu Media Nodes Server Metrics

!!! info "This dashboard is part of <span>OpenVidu <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

This dashboard provides the same **metrics** as the [OpenVidu Server Metrics](#openvidu-server-metrics) dashboard, but grouped by **Media Node**.

You can select the **Media Node** you want to see metrics from in the **media_node** dropdown. You will see different charts in the same panel according to the selected **Media Nodes**.

<figure markdown>
  ![Media Node dropdown](../../../../assets/images/grafana/nodes_metrics2.png){ .mkdocs-img }
</figure>

!!! info
    If you add new Media Nodes to your OpenVidu deployment, you will have to refresh the page in order to see the new Media Nodes in the dropdown.

<figure markdown>
  ![Media Node metrics](../../../../assets/images/grafana/nodes_metrics1.png){ .mkdocs-img }
</figure>

#### OpenVidu Logs

In case you are using **OpenVidu** <a href="/pricing#openvidu-community"><span class="openvidu-tag openvidu-community-tag">COMMUNITY</span></a>, this dashboard provides different visualizations for **logs** from your **OpenVidu Single Node deployment**.

There is a panel showing **all containers** logs,

<figure markdown>
  ![Single Node logs](../../../../assets/images/grafana/single_node_logs1.png){ .mkdocs-img }
</figure>

another panel to **filter** logs by **room_id** and **participant_id**,

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/single_node_logs3.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/single_node_logs3.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/single_node_logs4.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/single_node_logs4.png" loading="lazy"/></a></p></div>

</div>

and one row for each selected **service**, containing **all logs**, **warnings** and **errors** from that service.

<figure markdown>
  ![Single Node select services](../../../../assets/images/grafana/single_node_logs2.png){ .mkdocs-img }
</figure>

<figure markdown>
  ![Single Node service logs](../../../../assets/images/grafana/single_node_logs6.png){ .mkdocs-img }
</figure>

You can also filter logs containing a specific **text** by using the **filter search box**.

<figure markdown>
  ![Single Node filter logs](../../../../assets/images/grafana/single_node_logs5.png){ .mkdocs-img }
</figure>

#### OpenVidu Cluster Nodes Logs

!!! info "This dashboard is part of <span>OpenVidu <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

In case you are using **OpenVidu** <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a>, this dashboard provides different visualizations for **logs** from your **OpenVidu Elastic** or **OpenVidu High Availability** cluster, grouped by **node**.

First of all, there is a panel showing **all containers** logs from all nodes.

<figure markdown>
  ![Cluster logs](../../../../assets/images/grafana/nodes_logs1.png){ .mkdocs-img }
</figure>

Then, there is a row for each selected **node**, containing **all logs**, **warnings** and **errors** from that node. Besides, each row contains a panel for each selected container, showing all its logs.

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/nodes_logs2.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/nodes_logs2.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/nodes_logs3.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/nodes_logs3.png" loading="lazy"/></a></p></div>

</div>

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/nodes_logs4.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/nodes_logs4.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/nodes_logs5.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/nodes_logs5.png" loading="lazy"/></a></p></div>

</div>

!!! info
    Note that some panels have no data. This is because some containers are running in **Master Nodes** and others in **Media Nodes**.

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/nodes_logs6.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/nodes_logs6.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/nodes_logs7.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/nodes_logs7.png" loading="lazy"/></a></p></div>

</div>

You can also filter logs containing a specific **text** by using the **filter search box**.

<figure markdown>
  ![Cluter filter logs](../../../../assets/images/grafana/nodes_logs8.png){ .mkdocs-img }
</figure>

#### OpenVidu Cluster Services Logs

!!! info "This dashboard is part of <span>OpenVidu <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a></span> edition."

In case you are using **OpenVidu** <a href="/pricing#openvidu-pro"><span class="openvidu-tag openvidu-pro-tag">PRO</span></a>, this dashboard provides different visualizations for **logs** from your **OpenVidu Elastic** or **OpenVidu High Availability** cluster, grouped by **service**.

First of all, there is a panel to **filter** logs by **room_id** and **participant_id**.

<div class="grid-container">

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/services_logs3.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/services_logs3.png" loading="lazy"/></a></p></div>

<div class="grid-50"><p><a class="glightbox" href="/assets/images/grafana/services_logs4.png" data-type="image" data-width="100%" data-height="auto" data-desc-position="bottom"><img src="/assets/images/grafana/services_logs4.png" loading="lazy"/></a></p></div>

</div>

Then, there is a row for each selected **service**, containing **all logs**, **warnings** and **errors** from that service.

<figure markdown>
  ![Cluster select services](../../../../assets/images/grafana/services_logs1.png){ .mkdocs-img }
</figure>

<figure markdown>
  ![Cluster service logs](../../../../assets/images/grafana/services_logs2.png){ .mkdocs-img }
</figure>

### Limitations

For now, in [**OpenVidu High Availability deployments**](../../deployment-types.md#openvidu-high-availability), we have decided to **not** implement Grafana in High Availability (HA) mode. This decision is based on the fact that Grafana needs a configured HA MySQL or PostgreSQL database to work in HA mode, and we want to keep the deployment as simple as possible.

There are 4 instances of Grafana in an OpenVidu High Availability deployment, one for each Master Node, but they are not synchronized between them. Therefore, if you make any change (change your admin password, create a new dashboard...) in one Grafana instance and the Master Node suddenly goes down, you will be redirected to another Grafana instance where the changes will not be reflected. That is the reason why we disable user signups and saving dashboard or datasource modifications in Grafana.

However, all metrics and logs from all nodes are available in all Grafana instances, so you can monitor your OpenVidu cluster without any problem.

<script>window.setupGallery()</script>