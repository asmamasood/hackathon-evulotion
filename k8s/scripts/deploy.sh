#!/bin/bash

# Deployment script for Todo Application to Kubernetes

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment of Todo Application to Kubernetes..."

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl first."
    echo "Follow instructions at: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "Helm is not installed. Please install Helm first."
    echo "Follow instructions at: https://helm.sh/docs/intro/install/"
    exit 1
fi

if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install Minikube first."
    echo "Follow instructions at: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "Minikube is not running. Starting Minikube..."
    minikube start --cpus=4 --memory=8192 --disk-size=40g
    minikube addons enable ingress
    minikube addons enable metrics-server
fi

echo "Prerequisites check passed."

# Build Docker images
echo "Building Docker images..."
eval $(minikube docker-env)

# Build frontend image
echo "Building frontend image..."
cd ../frontend
docker build -t todo-frontend:latest .
cd ..

# Build backend image
echo "Building backend image..."
cd backend
docker build -t todo-backend:latest .
cd ..

echo "Docker images built successfully."

# Navigate to Helm chart directory
cd k8s/helm

# Add any required Helm repositories
echo "Adding Helm repositories..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install or upgrade the release
echo "Installing/upgrading Helm release..."
helm upgrade --install todo-app . \
    --namespace todo-app \
    --create-namespace \
    --set global.betterAuthSecret="$(openssl rand -base64 32)" \
    --set global.openaiApiKey="${OPENAI_API_KEY:-sk-your-openai-key-here}" \
    --set postgresql.auth.postgresPassword="${POSTGRES_PASSWORD:-postgres}" \
    --set postgresql.auth.database="todo_app" \
    --wait \
    --timeout=10m

echo "Application deployed successfully!"

# Wait a moment for services to be ready
sleep 10

# Show deployment status
echo "Deployment status:"
helm status todo-app -n todo-app

# Show services
echo "Services:"
kubectl get svc -n todo-app

# Show pods
echo "Pods:"
kubectl get pods -n todo-app

# Show ingress
echo "Ingress:"
kubectl get ingress -n todo-app

echo ""
echo "Deployment completed successfully!"
echo "Access the application at the Minikube IP:"
echo "  Minikube IP: $(minikube ip)"
echo ""
echo "To access services directly:"
echo "  Frontend: $(minikube service todo-app-frontend --url -n todo-app)"
echo "  Backend: $(minikube service todo-app-backend --url -n todo-app)"
echo ""
echo "To access the Kubernetes dashboard:"
echo "  $(minikube dashboard --url)"