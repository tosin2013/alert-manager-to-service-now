# Deployment Notes

This set of YAML files defines Kubernetes resources to deploy an application called `alert-manager-to-service-now` on OpenShift. The main components are:

- Namespace: Creates a namespace called `alert-manager-to-service-now` to deploy resources into.

- Service: Exposes the application via a ClusterIP service on port 5000.

- Deployment: Deploys the `alert-manager-to-service-now` container image built from the Git repository.

- BuildConfig: Defines a build config to build the container image from the Git repository source code.

- ImageStream: Tracks built container images.

- Route: Creates a route to expose the service externally via a hostname.

# Configuration

The Deployment defines a few key environment variables:

- `SERVICENOW_INSTANCE_URL`: The ServiceNow instance URL to connect to.
- `SERVICE_NOW_USERNAME`: Username for authenticating to ServiceNow. 
- `SERVICE_NOW_PASSWORD`: Password for the ServiceNow user.

These should be configured with the appropriate values for your ServiceNow instance.

The container image is built from the Git repository at `https://github.com/tosin2013/alert-manager-to-service-now.git`. The BuildConfig watches this repository for changes to trigger new builds.

The Route exposes the service externally via the generated hostname. Traffic is secured with edge TLS termination.