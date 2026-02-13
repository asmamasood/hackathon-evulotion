#!/bin/bash

# Minikube setup script for Todo Application

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Minikube for Todo Application..."

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install minikube first."
    echo "Follow instructions at: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl first."
    echo "Follow instructions at: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Start minikube with sufficient resources
echo "Starting Minikube with 4 CPUs and 8GB memory..."
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Enable required addons
echo "Enabling required addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Wait for addons to be ready
echo "Waiting for addons to be ready..."
sleep 10

# Verify cluster is running
echo "Verifying cluster status..."
kubectl cluster-info

# Verify ingress controller is running
echo "Verifying ingress controller..."
kubectl get pods -n ingress-nginx

echo "Minikube setup completed successfully!"
echo "Minikube IP: $(minikube ip)"
echo "Dashboard URL: $(minikube dashboard url --format='{{.URL}}')"