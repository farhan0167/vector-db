# vector-db

This project is an implementation of a vector database written from scratch. 

## Getting Started

To install this project, simply clone the repository:

```bash
git clone https://github.com/farhan0167/vector-db.git
cd vector-db/src/
```

Once cloned, and within `src/`, you will have two options to spin up the database:
- via Docker, or
- through a standalone Kubernetes cluster.

### Running as a standalone Docker container
1. Build the container:
    ```bash
    docker build -t vector-db-image:latest .
    ```
2. Spin a container
   ```bash
   docker run --name vector-db -p 8000:8000 vector-db-image:latest 
   ```

### Launching a Kubernetes Cluster

#### Prerequisite
Make sure you have the following installed in your system:
- [Minikube](https://minikube.sigs.k8s.io/docs/): Helps you spin up a local k8 cluster
- [Helm](https://helm.sh/): A package manager for Kubernetes

#### Running `vector-db` on k8
1. Spin up minikube
   ```bash
   minikube start
   ```
2. Build the docker image
   ```bash
    eval $(minikube docker-env)
    docker build -t vector-db-image .  
   ```
3. Deploy using Helm
   ```bash
   helm install vector-db ./vector_db-chart/
   ```
   **Note**: If you previously installed `vector-db`, you'll need to uninstall it:

   ```bash
   helm uninstall vector-db
   ```

4. Check if the service is available
   ```bash
   kubectl get svc
   ```
5. Launch the service
   ```bash
   minikube service vector-db
   ```
