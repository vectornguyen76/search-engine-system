# Kubernetes Development

## Table of Contents

1. [Architecture](#architecture)
2. [Development Environment Setup](#development-environment-setup)
3. [Production Environment Setup](#production-environment-setup)
4. [Kubernetes Cluster Deployment](#kubernetes-cluster-deployment)
   - [Deploy Ingress Nginx](#deploy-ingress-nginx)
     - [Installation](#installation)
     - [Configuration](#configuration)
     - [Verification](#verification)
     - [Uninstallation](#uninstallation)
   - [Deploy Postgres](#deploy-postgres)
     - [Local Installation](#local-installation)
     - [EKS Installation](#eks-installation)
     - [Local Uninstallation](#local-uninstallation)
     - [EKS Uninstallation](#eks-uninstallation)
   - [Deploy Backend](#deploy-backend)
   - [Deploy Frontend](#deploy-frontend)
   - [Deploy Qdrant](#deploy-qdrant)
   - [Deploy Triton Inference Server](#deploy-triton-inference-server)
   - [Deploy Image Search](#deploy-image-search)
   - [Deploy Text Search](#deploy-text-search)
5. [References](#references)

## Architecture

<p align="center">
  <img src="./assets/kubernetes-architecture.png" alt="Kubernetes Architecture Diagram" />
  <br>
  <em>Fig: Kubernetes Architecture</em>
</p>

## Development Environment Setup

This section covers the steps to set up a Kubernetes development environment.

### Start Kubernetes with Docker Desktop

Initiate Kubernetes within Docker Desktop for local development.

### Show Node Status

Check the status of Kubernetes nodes.

```
kubectl get nodes
```

### Build and Push Docker Images

Commands to build Docker images and push them to Docker Hub.

```
docker compose build
docker compose push
```

## Production Environment Setup

Guidelines for setting up a Kubernetes environment suitable for production.

### Create and Manage Cluster and NodeGroup

- **Creating a Cluster and Node Group**

  ```
  eksctl create cluster -f cluster-config-eksctl.yaml
  ```

   <p align="center">
   <img src="./assets/create-cluster.png" alt="Creating a Cluster and Node Group" />
   <br>
   <em>Fig: Creating a Cluster and Node Group</em>
   </p>

- **Deleting a Cluster and Node Group**

  ```
  eksctl delete cluster -f cluster-config-eksctl.yaml --disable-nodegroup-eviction
  ```

   <p align="center">
   <img src="./assets/delete-cluster.png" alt="Deleting a Cluster and Node Group" />
   <br>
   <em>Fig: Deleting a Cluster and Node Group</em>
   </p>

- **Creating only Node Group**
  ```
  eksctl create nodegroup -f cluster-config-eksctl.yaml
  ```
- **Deleting only Node Group**
  ```
  eksctl delete nodegroup -f cluster-config-eksctl.yaml
  ```

### Node Status Verification

Same as in the development environment setup.

### Install aws-ebs-csi-driver

```
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.25"
```

Instructions to install the AWS EBS CSI driver in the production environment.

## Kubernetes Cluster Deployment

### Deploy Ingress Nginx

#### Installation

1. **Install Ingress Nginx Controller**
   ```
   helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx
   ```
   This command installs the Ingress Nginx controller using Helm.

#### Configuration

1. **Configure Ingress Nginx Service**
   ```
   kubectl apply -f ingress-nginx-service.yaml
   ```
   Apply the configuration defined in `ingress-nginx-service.yaml`.

#### Verification

1. **Check Ingress Nginx**
   ```
   kubectl get ingress
   ```
   Verify the ingress setup by listing all ingress resources.

#### Uninstallation

1. **Remove Ingress Nginx**
   ```
   helm uninstall ingress-nginx
   kubectl delete -f ingress-nginx-service.yaml
   ```
   Uninstall the Ingress Nginx controller and delete its service configuration.

### Deploy Postgres

#### Local Installation

1. **Apply Postgres Configuration for Local**
   ```
   kubectl apply -f postgres-deployment.yaml,postgres-service.yaml,postgres-pvc.yaml,postgres-pv.yaml
   ```
   Set `storageClassName: standard` in `postgres-pvc.yaml` for local deployment.

#### EKS Installation

1. **Apply Postgres Configuration for EKS**
   ```
   kubectl apply -f postgres-deployment.yaml,postgres-service.yaml,postgres-pvc.yaml
   ```
   Set `storageClassName: gp3` in `postgres-pvc.yaml` for EKS deployment.

#### Local Uninstallation

1. **Remove Postgres in Local**
   ```
   kubectl delete -f postgres-deployment.yaml,postgres-service.yaml,postgres-pvc.yaml,postgres-pv.yaml
   ```

#### EKS Uninstallation

1. **Remove Postgres in EKS**
   ```
   kubectl delete -f postgres-deployment.yaml,postgres-service.yaml,postgres-pvc.yaml
   ```

### Deploy Backend

1. **Install Backend Service**

   ```
   kubectl apply -f backend-deployment.yaml,backend-service.yaml
   ```

   Deploy the backend service using the specified Kubernetes configurations.

2. **Uninstall Backend Service**
   ```
   kubectl delete -f backend-deployment.yaml,backend-service.yaml
   ```
   Remove the backend service from the cluster.

### Deploy Frontend

1. **Set Up Environment Variables**

   - For local deployment: `NEXT_PUBLIC_API_URL=http://localhost/api`
   - For production: Retrieve the IP address of the load balancer from `kubectl get ingress` and set `NEXT_PUBLIC_API_URL=http://{ip-address-loadbalancer}/api`.

2. **Deploy Frontend Service**

   ```
   kubectl apply -f frontend-deployment.yaml,frontend-service.yaml
   ```

   Apply the frontend deployment and service configurations.

3. **Uninstall Frontend Service**
   ```
   kubectl delete -f frontend-deployment.yaml,frontend-service.yaml
   ```

### Deploy Qdrant

1. **Install Qdrant Database**

   ```
   helm upgrade --install qdrant-db qdrant --repo https://qdrant.github.io/qdrant-helm
   ```

   Install Qdrant using the Helm chart.

2. **Uninstall Qdrant Database**
   ```
   helm uninstall qdrant-db
   kubectl delete pvc -l app.kubernetes.io/instance=qdrant-db
   ```

### Deploy Triton Inference Server

1.  **Model Repository**

- Create s3
  ```
  aws s3api create-bucket --bucket qai-triton-repository --region us-east-1
  ```
- Copy model repository from local to s3
  ```
  aws s3 cp ./../image-search-engine/model_repository s3://qai-triton-repository/model_repository --recursive
  ```
- To load the model from the AWS S3, you need to convert the following AWS credentials in the base64 format and add it to the values.yaml

  ```
  echo -n 'REGION' | base64
  ```

  ```
  echo -n 'SECRECT_KEY_ID' | base64
  ```

  ```
  echo -n 'SECRET_ACCESS_KEY' | base64
  ```

- Update path model repository in values.yaml
  ```
  modelRepositoryPath: s3://qai-triton-repository/model_repository
  ```

2. **Deploy Prometheus and Grafana**

   The inference server metrics are collected by Prometheus and viewable by Grafana. The inference server helm chart assumes that Prometheus
   and Grafana are available so this step must be followed even if you don't want to use Grafana.

   ```
   helm install search-engine-metrics --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false prometheus-community/kube-prometheus-stack
   ```

   Then port-forward to the Prometheus and Grafana service so you can access it from
   your local browser.

   ```
   kubectl port-forward service/search-engine-metrics-grafana 8080:80
   kubectl port-forward service/search-engine-metrics-kube-prometheus 9090:9090
   ```

3. **Deploy the Inference Server**
   Deploy the inference server using the default configuration with the
   following commands.

   ```
   cd helm-charts/triton-inference-server

   helm install search-engine-serving .
   ```

4. **Clean up**

   Once you've finished using the inference server you should use helm to
   delete the deployment.

   ```
   helm uninstall search-engine-metrics
   helm uninstall search-engine-serving
   ```

   For the Prometheus and Grafana services, you should [explicitly delete
   CRDs](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack#uninstall-helm-chart):

   ```
   kubectl delete crd alertmanagerconfigs.monitoring.coreos.com alertmanagers.monitoring.coreos.com podmonitors.monitoring.coreos.com probes.monitoring.coreos.com prometheuses.monitoring.coreos.com prometheusrules.monitoring.coreos.com servicemonitors.monitoring.coreos.com thanosrulers.monitoring.coreos.com
   ```

   You may also want to delete the AWS bucket you created to hold the
   model repository.

   ```
   aws s3 rm -r gs://qai-triton-repository
   ```

### Deploy Image Search

1. **Install Image Search Service**

   ```
   kubectl apply -f image-search-deployment.yaml,image-search-service.yaml
   ```

2. **Uninstall Image Search Service**
   ```
   kubectl delete -f image-search-deployment.yaml,image-search-service.yaml
   ```

### Deploy Text Search

1. **Install Text Search Service**

   ```
   kubectl apply -f text-search-deployment.yaml,text-search-service.yaml
   ```

2. **Uninstall Text Search Service**
   ```
   kubectl delete -f text-search-deployment.yaml,text-search-service.yaml
   ```

## References

Useful links for additional information and external resources.

- [EKSCTL Getting Started](https://eksctl.io/getting-started/)
- [AWS EBS CSI Driver Installation Guide](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/install.md)
- [Qdrant Helm Charts](https://github.com/qdrant/qdrant-helm/tree/main/charts/qdrant)
- [Elastic Cloud on Kubernetes Documentation](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html)
- [Elastic Cloud Kubernetes Deployment](https://github.com/elastic/cloud-on-k8s/tree/main/deploy/eck-stack)
