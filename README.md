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

## Conceptual Guide

On a high level, **vector-db** can be summarized by the following diagram:
![high_level](./docs/assets/highlevel_diagram.png)

The vector database is made up of:

- **Database**: The top-level object that holds a collection of libraries. It serves as the central structure for organizing and storing all content.
- **Library**: A library is a group of related documents. It acts as a controller for both documents and their corresponding chunks.
- **Document**: A document represents a single piece of text (e.g., an article or report). To enable more efficient retrieval, documents are split into smaller segments called chunks. This allows the system to return only the most relevant parts, avoiding the limitations of an LLM's context window.
- **Chunk**: Chunks are the smaller text segments derived from a document. In vector-db, each chunk is embedded individually and is the core unit returned in a retrieval query.
- **API**: The API provides an interface for users to interact with the database, enabling operations such as storing, querying, and retrieving documents or chunks.