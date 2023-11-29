# Helm Charts

Helm is a package manager for Kubernetes, which simplifies the process of defining, installing, and upgrading even the most complex Kubernetes applications. Below are references to Helm Charts and documentation for various Kubernetes services and tools.


### Install the Chart

1. **Frontend**

```bash
helm install frontend-app frontend
```

```bash
helm upgrade frontend-app frontend
```

```bash
helm uninstall frontend-app frontend
```

2. **Backend**

```bash
helm install backend-app backend
```

```bash
helm upgrade backend-app backend
```

```bash
helm uninstall backend-app backend
```

2. **Backend**

```bash
helm install backend-app backend
```

```bash
helm upgrade backend-app backend
```

```bash
helm uninstall backend-app backend
```

3. **Image Search**

```bash
helm install image-search-app image-search
```

```bash
helm upgrade image-search-app image-search
```

```bash
helm uninstall image-search-app image-search
```

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