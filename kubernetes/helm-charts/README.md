# Helm Charts for Kubernetes

## Overview
Helm is a package manager for Kubernetes, simplifying the process of defining, installing, and upgrading Kubernetes applications. This document provides guidelines and references for using Helm Charts with various Kubernetes services and tools.

## Table of Contents
1. [Model Repository S3](#model-repository-s3)
2. [Install aws-ebs-csi-driver](#install-aws-ebs-csi-driver)
3. [Install the Charts](#install-the-charts)
4. [Upgrade Charts](#upgrade-charts)
5. [Uninstall Charts](#uninstall-charts)
6. [Clean up PVC](#clean-up-pvc)
7. [References](#references)

## Model Repository S3
Instructions to create an S3 bucket and copy a model repository from local to S3.

- **Create S3 Bucket**
  ```bash
  aws s3api create-bucket --bucket qai-triton-repository --region us-east-1
  ```
- **Copy Model Repository**
  ```bash
  aws s3 cp ./../image-search-engine/model_repository s3://qai-triton-repository/model_repository --recursive
  ```

## Install aws-ebs-csi-driver
You may deploy the EBS CSI driver via Kustomize, Helm, or as an [Amazon EKS managed add-on](https://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html).

1. **Kustomize**
```sh
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.25"
```

2. **Helm**
- Add the `aws-ebs-csi-driver` Helm repository.
   ```sh
   helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
   helm repo update
   ```

- Install the latest release of the driver.
   ```sh
   helm upgrade --install aws-ebs-csi-driver \
      --namespace kube-system \
      aws-ebs-csi-driver/aws-ebs-csi-driver
   ```

   Review the [configuration values](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/charts/aws-ebs-csi-driver/values.yaml) for the Helm chart.

## Install the Charts
Step-by-step instructions to create namespaces and install various Helm charts like Ingress Nginx Controller, Postgresql, Elastic Search, Qdrant, Prometheus, Grafana, and others.

- **Create Namespaces**
  ```bash
  kubectl create namespace ingress-nginx
  kubectl create namespace application
  kubectl create namespace database
  kubectl create namespace model-serving
  kubectl create namespace monitoring
  ```

1. **Ingress Nginx Controller**
   Installs the Ingress Nginx controller using Helm.
   ```bash
   helm install ingress-nginx ./ingress-nginx --namespace ingress-nginx
   ```

2. **Postgresql**
   Build dependencies and then install Postgresql Helm Chart.
   ```bash
   helm dependency build ./postgresql
   helm install database ./postgresql --namespace database --set auth.username=db_user,auth.password=db_password,auth.database=db_dev
   ```

3. **Elastic Search**
   Build dependencies and then install Elastic Search Helm Chart.
   ```bash
   helm dependency build ./elasticsearch
   helm install elasticsearch ./elasticsearch --namespace database --set master.masterOnly=false,master.replicaCount=1,data.replicaCount=0,coordinating.replicaCount=0,ingest.replicaCount=0,master.nodeSelector.nodegroup-type=cpu-nodegroup
   ```

4. **Qdrant**
   Install Qdrant Helm Chart for vector search engine.
   ```bash
   helm install qdrant ./qdrant --namespace database --set nodeSelector.nodegroup-type=cpu-nodegroup
   ```

5. **Prometheus and Grafana**
   Install Prometheus and Grafana for monitoring. Assumes availability of Prometheus and Grafana.
   ```bash
   helm dependency build ./kube-prometheus-stack
   helm install monitoring ./kube-prometheus-stack --namespace monitoring --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
   ```
   Port-forward to Prometheus and Grafana services for local access.
   ```bash
   kubectl port-forward service/monitoring-grafana 8080:80 --namespace monitoring
   kubectl port-forward service/monitoring-kube-prometheus 9090:9090 --namespace monitoring
   ```

6. **Inference Server**
   Load models from AWS S3 and deploy the inference server using Helm.
   Convert AWS credentials to base64 and update `values.yaml`.
   ```bash
   echo -n 'REGION' | base64
   echo -n 'SECRECT_KEY_ID' | base64
   echo -n 'SECRET_ACCESS_KEY' | base64
   ```
   Update model repository path in `values.yaml`.
   ```yaml
   modelRepositoryPath: s3://qai-triton-repository/model_repository
   ```
   Deploy the inference server.
   ```bash
   helm install model-serving ./triton-inference-server --namespace model-serving --set nodeSelector.nodegroup-type=gpu-nodegroup
   ```

7. **Image Search Application**
   Install Image Search Application Helm Chart.
   ```bash
   helm install image-search-app ./image-search --namespace application --set nodeSelector.nodegroup-type=cpu-nodegroup
   ```

8. **Text Search Application**
   Install Text Search Application Helm Chart.
   ```bash
   helm install text-search-app ./text-search --namespace application --set nodeSelector.nodegroup-type=cpu-nodegroup
   ```

9. **Backend Application**
   Install Backend Application Helm Chart.
   ```bash
   helm install backend-app ./backend --namespace application --set nodeSelector.nodegroup-type=cpu-nodegroup
   ```

10. **Frontend Application**
   Install Frontend Application Helm Chart.
   ```bash
   helm install frontend-app ./frontend --namespace application --set nodeSelector.nodegroup-type=cpu-nodegroup
   ```

## Upgrade Charts
Instructions on how to upgrade existing Helm Chart releases.

```bash
helm upgrade [RELEASE_NAME] [CHART_NAME] --version [NEW_VERSION] -f [VALUES_FILE]
```

## Uninstall Charts
Guidelines to list and uninstall Helm Chart releases.

```bash
helm list
helm uninstall [RELEASE_NAME]
```

## Clean up PVC

Deleting PVCs is irreversible and can lead to data loss. Ensure backups are in place before proceeding.

1. **List All PVCs**
   To view all PVCs across all namespaces:
   ```bash
   kubectl get pvc --all-namespaces
   ```

2. **Delete All PVCs**
   To remove all PVCs in the cluster:
   ```bash
   kubectl delete pvc --all --all-namespaces
   ```

3. **Delete PVCs in a Specific Namespace**
   To delete PVCs in a particular namespace:
   ```bash
   kubectl delete pvc --all -n <namespace>
   ```
   Replace `<namespace>` with the desired namespace name.

4. **Verify Deletion**
   To confirm the PVCs have been removed:
   ```bash
   kubectl get pvc --all-namespaces
   ```

## Testing


## References
- [Bitnami Charts](https://github.com/bitnami/charts)
- [NetApp Postgres Helm Chart](https://docs.netapp.com/us-en/astra-control-center-2204/solutions/postgres-deploy-from-helm-chart.html#requirements)
- [Helm Official Install Guide](https://helm.sh/docs/intro/install/)
- [Ingress Nginx GitHub Repository](https://github.com/kubernetes/ingress-nginx)
- [Triton Inference Server AWS Deployment Guide](https://github.com/triton-inference-server/server/tree/main/deploy/aws)
- [Prometheus Community Helm Charts](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [Qdrant Helm Charts](https://github.com/qdrant/qdrant-helm/tree/main/charts/qdrant)
- [Elastic Cloud on Kubernetes Documentation](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html)
- [CSI driver for Amazon EBS](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)