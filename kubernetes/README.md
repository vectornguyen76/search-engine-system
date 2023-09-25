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
4. Install Qdrant helm chart
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
    - Uninstall repo
        ```
        helm uninstall qdrant-vector-database
        ```
    - Delete the volume
        ```
        kubectl delete pvc -l app.kubernetes.io/instance=qdrant-vector-database
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
    ```
    kubectl delete -f image-search-deployment.yaml,image-search-service.yaml
    ```

### Refrence
- https://github.com/qdrant/qdrant-helm/tree/main/charts/qdrant