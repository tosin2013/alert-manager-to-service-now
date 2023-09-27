![20230927100134](https://i.imgur.com/N3F58Tb.png)

![20230927145958](https://i.imgur.com/hgHhTx5.png)
Example Custom Alert 

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

Example service-now webhook

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


Links: 
* https://shanna-chan.blog/2023/05/01/way-too-many-alerts-which-alerts-are-important/
