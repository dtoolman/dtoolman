from string import Template

yaml_template = """apiVersion: "autoscaling.k8s.io/v1"
kind: VerticalPodAutoscaler
metadata:
  name: ${SERVICE_NAME}
  namespace: ${SERVICE_NAMESPACE}
  annotations:
    k8s-cloud-system/user: jenkins
    k8s-cloud-system/pushed: Mon Jun 18 20:45:56 UTC 2025
    datasite-k8s-manifests/template: generic/deployment
    meta.helm.sh/release-name: ${SERVICE_NAME}
    meta.helm.sh/release-namespace: ${SERVICE_NAMESPACE}
  labels:
    app.kubernetes.io/managed-by: Helm
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: ${SERVICE_NAME}
  updatePolicy:
    updateMode: Off
  resourcePolicy:
    containerPolicies:
      - containerName: ${CONTAINER_NAME}
        minAllowed:
          cpu: 100m
          memory: 50Mi
        controlledResources: ["cpu", "memory"]
        controlledValues: RequestsOnly
"""

services = [
    {
        'name': 'frontend',
        'namespace': 'web-prod',
        'containerName': 'nginx'
    },
    {
        'name': 'backend',
        'namespace': 'api-prod',
        'containerName': 'gunicorn'
    }
]

output = []
template = Template(yaml_template)

for service in services:
    substituted = template.substitute(
        SERVICE_NAME=service['name'],
        SERVICE_NAMESPACE=service['namespace'],
        CONTAINER_NAME=service['containerName']
    )
    output.append(substituted)

with open('vpa-manifests.yaml', 'w') as f:
    f.write("\n---\n".join(output))
