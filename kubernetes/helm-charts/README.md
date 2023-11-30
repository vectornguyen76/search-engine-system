# Helm Charts

Helm is a package manager for Kubernetes, which simplifies the process of defining, installing, and upgrading even the most complex Kubernetes applications. Below are references to Helm Charts and documentation for various Kubernetes services and tools.

### Install aws-ebs-csi-driver

```
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.25"
```

Instructions to install the AWS EBS CSI driver in the production environment.

### Install the Charts

Create namespace
```
kubectl create namespace ingress-nginx
kubectl create namespace application
kubectl create namespace database
kubectl create namespace model-serving
kubectl create namespace monitoring
```

1. **Ingress Nginx Controller**
   ```
   helm install ingress-nginx ./ingress-nginx --namespace ingress-nginx
   ```
   This command installs the Ingress Nginx controller using Helm.

2. **Postgresql**
   ```
   helm dependency build ./postgresql
   ```
   ```
   helm install database ./postgresql --namespace database --set auth.username=db_user,auth.password=db_password,auth.database=db_dev
   ```

3. **Elastic Seach**
   ```
   helm dependency build ./postgresql
   ```
   ```
   helm install elasticsearch ./elasticsearch --namespace database --set master.masterOnly=false,master.replicaCount=1,data.replicaCount=0,coordinating.replicaCount=0,ingest.replicaCount=0,master.nodeSelector.nodegroup-type=cpu-nodegroup
   ```

4. **Qdrant**
   ```
   helm install qdrant ./qdrant --namespace database --set nodeSelector.nodegroup-type=cpu-nodegroup
   ```

2. **Deploy Prometheus and Grafana**
   ```
   helm install search-engine-metrics --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false prometheus-community/kube-prometheus-stack
   ```

3. **Deploy the Inference Server**
   ```
   helm install search-engine-metrics --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false prometheus-community/kube-prometheus-stack
   ```

5. **Image Search**
   ```
   helm install image-search-app ./image-search --namespace application
   ```

6. **Text Search**
   ```
   helm install text-search-app ./text-search --namespace application
   ```

7. **Backend**
   ```
   helm install backend-app ./backend --namespace application
   ```

8. **Frontend**
   ```
   helm install frontend-app ./frontend --namespace application
   ```

helm install elasticsearch elasticsearch

2. **Frontend**
   ```
   helm install frontend-app ./frontend --namespace application
   ```



2. **Backend**

```
helm install backend-app backend
```

```
helm upgrade backend-app backend
```

```
helm uninstall backend-app backend
```

2. **Backend**

```
helm install backend-app backend
```

```
helm upgrade backend-app backend
```

```
helm uninstall backend-app backend
```

3. **Image Search**

```
helm install image-search-app image-search
```

```
helm upgrade image-search-app image-search
```

```
helm uninstall image-search-app image-search

```

```
helm install text-search-app text-search
helm upgrade text-search-app text-search
helm uninstall text-search-app
```
kubectl port-forward service/text-search-app 8000:8000

### Postgresql 
```
helm install postgres-app --set auth.username=db_user,auth.password=db_password,auth.database=db_dev oci://registry-1.docker.io/bitnamicharts/postgresql
```

helm uninstall postgres-app 

helm install postgres-app ./postgresql --set auth.username=db_user,auth.password=db_password,auth.database=db_dev 

helm dependency build postgresql

helm install elasticsearch elasticsearch
helm install elasticsearch oci://registry-1.docker.io/bitnamicharts/elasticsearch
helm uninstall elasticsearch

kubectl create clusterrolebinding tiller-cluster-admin --clusterrole=cluster-admin --serviceaccount=kube-system:tiller

helm install --name elasticsearch elastic/elasticsearch --set service.type=LoadBalancer

### Upgrade charts
```bash
helm uninstall elasticsearch
```


### Clean up
To delete all Persistent Volume Claims (PVCs) in a Kubernetes cluster, you can use the `kubectl` command. However, be cautious with this operation, as deleting PVCs can result in data loss if the volumes are not backed up or replicated elsewhere.

Here's a step-by-step guide on how to do this:

1. **List All PVCs**
First, it's a good practice to list all PVCs to review what will be deleted:

```bash
kubectl get pvc --all-namespaces
```

2. **Deleting All PVCs**
To delete all PVCs in the cluster, you can use the following command:

```bash
kubectl delete pvc --all --all-namespaces
```

- `--all` deletes all resources of the specified type (PVCs in this case).
- `--all-namespaces` ensures the command runs across every namespace in the cluster.

3. **Specific Namespace**
If you want to delete PVCs in a specific namespace, omit the `--all-namespaces` flag and specify the namespace:

```bash
kubectl delete pvc --all -n <namespace>
```

Replace `<namespace>` with the name of the namespace.


Remember, this action cannot be undone, so proceed with caution and ensure that this operation aligns with your data management policies.
## References
- https://github.com/bitnami/charts
- https://docs.netapp.com/us-en/astra-control-center-2204/solutions/postgres-deploy-from-helm-chart.html#requirements
- **Helm Installation**: [Helm Official Install Guide](https://helm.sh/docs/intro/install/)
- **Ingress Nginx**: [GitHub Repository](https://github.com/kubernetes/ingress-nginx) | [Quick Start Guide](https://kubernetes.github.io/ingress-nginx/deploy/#quick-start)
- **Triton Inference Server on AWS**: [Deployment Guide](https://github.com/triton-inference-server/server/tree/main/deploy/aws)
- **Prometheus Community Helm Charts**: [GitHub Repository](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- **Qdrant Helm Charts**: [GitHub Repository](https://github.com/qdrant/qdrant-helm/tree/main/charts/qdrant)
- **Elastic Cloud on Kubernetes**: [Documentation](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html) | [Kubernetes Deployment](https://github.com/elastic/cloud-on-k8s/tree/main/deploy/eck-stack)
- **Grafana Dashboards**: [Explore Dashboards](https://grafana.com/grafana/dashboards)