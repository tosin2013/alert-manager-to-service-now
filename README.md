# Sending Alert Manager alerts to ServiceNow on OpenShift 

## Requirements
* OpenShift 4.12+
* kustomize or oc 
* [ServiceNow](https://developer.servicenow.com/dev.do) instance
  
## Overview
This is a simple Flask application that receives alerts from an alert manager, and creates corresponding incidents in ServiceNow.


![20230927100134](https://i.imgur.com/N3F58Tb.png)

![20230927145958](https://i.imgur.com/hgHhTx5.png)

## Workflow
* Prometheus evaluates alert rules and sends firing alerts to AlertManager
* AlertManager routes the alerts to the webhook endpoint exposed by the Flask app
* The Flask app parses the alert data and calls the ServiceNow API to create an incident
* New incidents are created in ServiceNow for each alert

## Deployment
```
oc apply -k ./app
```
**Quick deployment**
```
oc apply -k https://github.com/tosin2013/alert-manager-to-service-now/app --dry-run=client -o yaml 
```

**Example Custom Alert** 
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

**Example service-now webhook**
```
global:
  resolve_timeout: "5m"

receivers:
- name: "null"
- name: "service-now"
  webhook_configs:
    - url: "https://alert-manager-to-service-now-alert-manager-to-service-now.apps.ocp4.example.com/alerts"

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

## Documentation
See the documentation in the repo for more details on the YAML configs and deployment instructions
* [Python Code](docs/python-code.md)
* [Deployment Notes](docs/deployment.md)
* [Custom Alert Rules ConfigMap](docs/custom-alert-rules-configmap.md)

## Links: 
* https://shanna-chan.blog/2023/05/01/way-too-many-alerts-which-alerts-are-important/
