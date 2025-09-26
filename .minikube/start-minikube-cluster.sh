#!/bin/bash

# HiveBox Minikube Cluster Setup Script
# This script ensures consistent cluster configuration across team members

echo "🚀 Starting HiveBox Minikube cluster..."

# Start Minikube with specific configuration
minikube start \
  --profile=hivebox \
  --memory=4096 \
  --cpus=2 \
  --disk-size=5g \


echo "📦 Enabling required addons..."

# Enable Ingress addon (equivalent to Ingress-Nginx)
minikube addons enable ingress --profile=hivebox

# Enable metrics server for resource monitoring
minikube addons enable metrics-server --profile=hivebox

# Enable dashboard for web UI (optional but useful)
minikube addons enable dashboard --profile=hivebox

echo "✅ HiveBox Minikube cluster is ready!"
