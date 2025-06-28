from kubernetes import client, config

def get_containers(namespaces):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    services = []
    
    for namespace in namespaces:
        try:
            pods = v1.list_namespaced_pod(namespace).items
            for pod in pods:
                for container in pod.spec.containers:
                    services.append({
                        'namespace': namespace,
                        'containerName': pod.metadata.name
                    })
        except client.exceptions.ApiException as e:
            print(f"Error accessing namespace {namespace}: {e}")
    
    return services

# Example usage:
namespaces = ['web-prod', 'api-prod']
containers = get_containers(namespaces)
print(containers)
