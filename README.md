# Multi-Model Kubernetes Deployment with User Type Differentiation

This project demonstrates a multi-model Kubernetes deployment where different configurations can be applied based on the intended user type (e.g., cloud users vs. local machine users). It includes two simple models (square and cube) served via FastAPI and accessible through a Kubernetes Ingress.

## Project Structure
                                       ┌───────────────────────────────┐
                                       │       Kubernetes Cluster      │
                                       │───────────────────────────────│
                                       │   Ingress Controller          │
                                       │       (e.g., Nginx)           │
                                       │     /square  → Square Service │
                                       │     /cube    → Cube Service   │
                                       │───────────────────────────────│
                                       │   Square Model Deployment     │
                                       │     - Pod 1                   │
                                       │     - Pod 2                   │
                                       │   Cube Model Deployment       │
                                       │     - Pod 1                   │
                                       │     - Pod 2                   │
                                       │   Square Service (Load Balancer)│
                                       │   Cube Service   (Load Balancer)│
                                       └───────────────────────────────┘
                                          ▲
                                          │ Network Connectivity
                                          │┌───────────────────┐      ┌───────────────────┐      ┌─────────────────────┐
                                           │ Cloud User 1      │──────▶│ Internet          │◀──────│ Local Machine User 1│
                                           │ (e.g., AWS EC2)   │      └───────────────────┘      └─────────────────────┘
                                           └───────────────────┘                                  ▲
                                                                                                  │ Network Connectivity (e.g., VPN, Port Forwarding)
                                                                                                  │
                                                                                               ┌─────────────────────┐
                                                                                               │ Local Machine User 2│
                                                                                               └─────────────────────┘

## Overview

This setup allows you to manage different Kubernetes configurations for your model deployments based on the environment or the type of users accessing them. For example, you might want to have different resource allocations or scaling strategies for cloud deployments compared to local development or internal access.

- **Separate Model Services:** Each model (square and cube) is implemented as a separate FastAPI application.
- **Dockerized Applications:** Each model service is containerized using Docker for easy deployment in Kubernetes.
- **Kubernetes Deployments and Services:** Kubernetes Deployment and Service definitions are provided for each model, organized under `k8s/cloud` and `k8s/local`. You can customize these configurations as needed.
- **Ingress for Routing:** An Ingress resource is configured to route external traffic to the appropriate model service based on the URL path (`/square` and `/cube`).

## Prerequisites

- **Kubernetes Cluster:** You need access to a Kubernetes cluster (e.g., Minikube for local testing, or a cloud-based Kubernetes service like AKS, EKS, or GKE).
- **kubectl:** The Kubernetes command-line tool (`kubectl`) must be configured to interact with your cluster.
- **Docker:** Docker needs to be installed on your local machine to build the container images.
- **Minikube (for local testing):** If you are testing locally, ensure Minikube is installed.

## Getting Started

Follow these steps to deploy the multi-model system on your Kubernetes cluster.

**1. Clone the Repository (if applicable):**

```bash
git clone <repository_url>
cd <repository_directory>

# Build square model image
docker build -t square-model:latest models/square/

# Build cube model image
docker build -t cube-model:latest models/cube/

# Load images into Minikube (if using Minikube)
minikube image load square-model:latest
minikube image load cube-model:latest

kubectl apply -f k8s/cloud/square-deployment.yaml
kubectl apply -f k8s/cloud/square-service.yaml
kubectl apply -f k8s/cloud/cube-deployment.yaml
kubectl apply -f k8s/cloud/cube-service.yaml
kubectl apply -f k8s/ingress.yaml

kubectl apply -f k8s/local/square-deployment.yaml
kubectl apply -f k8s/local/square-service.yaml
kubectl apply -f k8s/local/cube-deployment.yaml
kubectl apply -f k8s/local/cube-service.yaml
kubectl apply -f k8s/ingress.yaml

minikube addons enable ingress


5. Access the Models:

For Cloud Users (assuming your Ingress is exposed via a LoadBalancer or public IP):

Get the external IP or hostname of your Ingress controller. The method varies depending on your cloud provider.

Access the models via HTTP POST requests:

Bash

curl -X POST http://<INGRESS_IP_OR_HOSTNAME>/square/predict -H "Content-Type: application/json" -d '{"input": 10}'
curl -X POST http://<INGRESS_IP_OR_HOSTNAME>/cube/predict -H "Content-Type: application/json" -d '{"input": 10}'
For Local Machine Users (using Minikube):

Get the Minikube IP:

Bash

minikube ip
Access the models via HTTP POST requests:

Bash

curl -X POST http://$(minikube ip)/square/predict -H "Content-Type: application/json" -d '{"input": 15}'
curl -X POST http://$(minikube ip)/cube/predict -H "Content-Type: application/json" -d '{"input": 15}'
Alternatively, you can use port forwarding to access via localhost:

Bash

kubectl port-forward service/ingress-nginx-controller -n ingress-nginx 8080:80 &
curl -X POST http://localhost:8080/square/predict -H "Content-Type: application/json" -d '{"input": 20}'
curl -X POST http://localhost:8080/cube/predict -H "Content-Type: application/json" -d '{"input": 20}'
