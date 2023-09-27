## Deploy a Kubernetes cluster in Local
1. Start cluster use minikube and docker
    ```
    minikube start --driver=docker
    ```
2. Show node ready
    ```
    kubectl get nodes
    ```
3. Build and push image to docker hub
    ```
    docker compose build
    docker compose push
    ```
4. Install Qdrant Helm Chart
    - Add repo
        ```
        helm repo add qdrant https://qdrant.github.io/qdrant-helm
        ```
    - Update repo
        ```
        helm repo update
        ```
    - Install repo
        ```
        helm upgrade -i qdrant-vector-database qdrant/qdrant
        ```
    - Check repo
        ```
        helm list
        ```

5. Deploy kubenetes template
    ```
    kubectl apply -f image-search-deployment.yaml,image-search-service.yaml
    ```
6. Show dashboard
    ```
    minikube dashboard
    ```
7. Get service
    ```
    minikube service image-search-service
    ```
8. Destroy kubenetes template
    - Delete app
        ```
        kubectl delete -f image-search-deployment.yaml,image-search-service.yaml
        ```
    - Uninstall repo
        ```
        helm uninstall qdrant-vector-database
        ```
    - Delete the qdrant volume 
        ```
        kubectl delete pvc -l app.kubernetes.io/instance=qdrant-vector-database
        ```
    - Delete cluster
        ```
        minikube delete
        ```
### Refrence
- https://github.com/qdrant/qdrant-helm/tree/main/charts/qdrant
- https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html
- https://github.com/elastic/cloud-on-k8s/tree/main/deploy/eck-stack
