# Custom Alert Rules ConfigMap

This ConfigMap defines a custom set of Prometheus alerting rules under the key `custom_rules.yaml`. 

The rules are in Prometheus alert rule syntax. They define one alert rule called `NodeNotReady` which will fire if any Kubernetes node is in the `NotReady` state for over 5 seconds.

The alert has annotations providing a summary and description. Labels provide metadata like the instance, cluster, and cluster ID. The severity is set to `critical`.

This ConfigMap provides a way to dynamically configure custom alert rules for Prometheus in Kubernetes. The rules can be mounted into Prometheus and reloaded.

```
apiVersion: v1
data:
 custom_rules.yaml: |
   groups:
     - name: kube-node-health
       rules:
       - alert: NodeNotReady
         annotations:
           summary: Notify when any node on a cluster is in NotReady state
           description: "One of the node of the cluster is down: Cluster {{ $labels.cluster }} {{ $labels.clusterID }}."
         expr: kube_node_status_condition{condition="Ready",job="kube-state-metrics",status="true"} != 1
         for: 5s
         labels:
           instance: "{{ $labels.instance }}"
           cluster: "{{ $labels.cluster }}"
           clusterID: "{{ $labels.clusterID }}"
           tag: kubenode
           severity: critical
kind: ConfigMap
metadata:
  name: thanos-ruler-custom-rules
  namespace: open-cluster-management-observability
```

# Alertmanager ServiceNow Receiver 

This example defines a `service-now` receiver in Alertmanager to send alerts to a ServiceNow webhook. 

The `webhook_configs` section defines the endpoint URL to send alerts to. This should be the external route URL to the alert processing application.

The `routes` section sends all alerts to the ServiceNow receiver, except `Watchdog` alerts which go to `null` (dropped).

This provides a way for Alertmanager to take alerts generated based on the custom rules, and forward them to ServiceNow for incident management.

```
global:
  resolve_timeout: "5m"

receivers:
- name: "null"
- name: "service-now"
  webhook_configs:
    - url: "https://alert-manager-to-service-now-alert-manager-to-service-now.apps.cluster-nvpdr.nvpdr.sandbox2232.opentlc.com/alerts"

route:
  group_by:
  - "namespace"
  group_interval: "5m"
  group_wait: "30s"
  receiver: "null"
  repeat_interval: "12h"
  routes:
  - match:
      alertname: "Watchdog"
    receiver: "null"
  - match:
    receiver: "service-now"
```