# Phase 4: Kubernetes & CD Pipeline

## Overview

**Objective:** Transform the containerized FastAPI application into a production-ready Kubernetes deployment with enhanced CI/CD pipeline featuring comprehensive security scanning and quality gates.

This phase establishes the foundation for container orchestration and implements DevOps best practices for continuous integration with security-first approach.

## What We Built

### 4.1 Enhanced FastAPI Application

**Code Requirements:**
- `/metrics` endpoint with Prometheus instrumentation
- `/temperature` endpoint with status logic (Too Cold/Good/Too Hot)
- `/readyz` endpoint for Kubernetes readiness probes
- Environment-configurable senseBox IDs via `SENSEBOX_IDS`

**Implementation:**
```python
# Added Prometheus metrics support
from prometheus_fastapi_instrumentator import Instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Temperature status logic
def get_temperature_status(temperature):
    if temperature < 10:
        return "Too Cold"
    if 11 <= temperature <= 36:
        return "Good"
    return "Too Hot"
```

**Key Features:**
- Configurable via environment variables
- Production-ready health checks
- Automatic metrics collection
- Status-based temperature monitoring

### 4.2 Integration Testing

**Three Testing Approaches:**

1. **FastAPI TestClient** (Unit-style testing)
```python
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/version")
assert response.status_code == 200
```

2. **httpx AsyncClient** (Async testing)
```python
async with httpx.AsyncClient(app=app, base_url="http://test") as client:
    response = await client.get("/")
    assert response.status_code == 200
```

3. **requests Library** (Live server testing)
```python
response = requests.get("http://localhost:8000/version")
assert response.status_code == 200
```

### 4.3 Kubernetes Manifests

**Production-Ready Configuration:**

**Deployment Manifest (`k8s_manifests/deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hivebox-api
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: hivebox-api
        image: ehabashrafmu/hivebox:0.0.2
        ports:
        - containerPort: 8000
        env:
        - name: SENSEBOX_IDS
          value: "5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8000
```

**Service Manifest (`k8s_manifests/service.yaml`):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: hivebox-api-service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: hivebox-api
```

**Ingress Manifest (`k8s_manifests/ingress.yaml`):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hivebox-api-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - host: hivebox.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hivebox-api-service
            port:
              number: 80
```

### 4.4 Enhanced CI Pipeline

**Comprehensive Quality Gates:**

**Pipeline Structure:**
1. **Test Stage**: Linting, unit tests, integration tests, API validation
2. **Security Analysis** (Parallel):
   - SonarCloud code quality and security analysis
   - Terrascan Kubernetes manifest security scanning
   - Semgrep security analysis for Python, Docker, and K8s
3. **Build Stage**: Docker build, container testing, Trivy security scan
4. **Registry Push**: Automated Docker Hub publishing

**Key Features:**
- Professional job dependencies and error handling
- Comprehensive endpoint testing for both local and containerized apps
- Coverage reporting integration with SonarCloud
- SARIF security results uploaded to GitHub Security tab
- Pipeline fails fast if critical quality gates fail

**Security Scanning Integration:**
- **SonarCloud**: Code quality, security vulnerabilities, test coverage
- **Terrascan**: Kubernetes manifest misconfigurations and security issues
- **Semgrep**: Static analysis for Python, Docker, and Kubernetes
- **Trivy**: Container image vulnerability scanning

## Local Development Setup

### Prerequisites

```bash
# Required tools
- Docker and Docker Compose
- Minikube or KIND
- kubectl
- Python 3.11+
```

### Minikube Cluster Setup

**Start Minikube with Ingress:**
```bash
# Start cluster with specific profile
minikube start --profile=hivebox --memory=4096 --cpus=2

# Enable required addons
minikube addons enable ingress --profile=hivebox
minikube addons enable metrics-server --profile=hivebox
```

**Configure Local DNS:**
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip --profile=hivebox)

# Add to /etc/hosts
echo "$MINIKUBE_IP hivebox.local" | sudo tee -a /etc/hosts
```

### Deploy Application

```bash
# Build and load Docker image
docker build -t ehabashrafmu/hivebox:0.0.2 .
minikube image load ehabashrafmu/hivebox:0.0.2 --profile=hivebox

# Deploy to Kubernetes
kubectl apply -f k8s_manifests/

# Verify deployment
kubectl get pods
kubectl get services
kubectl get ingress

# Check rollout status
kubectl rollout status deployment/hivebox-api
```

### Test Deployment

```bash
# Test all endpoints
curl http://hivebox.local/
curl http://hivebox.local/version
curl http://hivebox.local/health
curl http://hivebox.local/readyz
curl http://hivebox.local/temperature
curl http://hivebox.local/metrics | head -10

# Check Swagger documentation
open http://hivebox.local/docs
```

## CI/CD Pipeline Configuration

### GitHub Repository Secrets

Required secrets for full pipeline functionality:

```bash
# SonarCloud Integration
SONAR_TOKEN=your_sonarcloud_token

# Docker Hub Integration (already configured)
DOCKER_HUB_USERNAME=your_username
DOCKER_HUB_ACCESS_TOKEN=your_access_token

# Optional: Enhanced Semgrep features
SEMGREP_APP_TOKEN=your_semgrep_token
```

### Pipeline Triggers

The CI pipeline runs on:
- Push to `main`, `development`, `phase-4-kubernetes` branches
- Pull requests to `main` and `development` branches

### Quality Gates

Pipeline progression requires:
- All tests pass (unit, integration, endpoint validation)
- Code quality meets SonarCloud standards
- No critical security vulnerabilities found
- Kubernetes manifests pass security scanning
- Docker build succeeds with container validation

## Verification Commands

### Application Health
```bash
# Check Kubernetes resources
kubectl get all
kubectl describe deployment hivebox-api
kubectl describe service hivebox-api-service
kubectl describe ingress hivebox-api-ingress

# View application logs
kubectl logs -l app=hivebox-api
kubectl logs -l app=hivebox-api --tail=50 -f

# Port forward for direct testing (alternative to Ingress)
kubectl port-forward service/hivebox-api-service 8080:80
curl http://localhost:8080/version
```

### CI Pipeline Status
```bash
# Check pipeline runs
# Visit: https://github.com/EhabAshrafMu/devops-hands-on-project-hivebox/actions
```

## Troubleshooting

### Common Issues

**Minikube Image Loading:**
```bash
# If image not found
minikube image load ehabashrafmu/hivebox:0.0.2 --profile=hivebox
kubectl delete pods -l app=hivebox-api  # Force pod recreation
```

**Ingress Access Issues:**
```bash
# Check Ingress controller
kubectl get pods -n ingress-nginx

# Verify DNS resolution
ping hivebox.local

# Alternative: Use port forwarding
kubectl port-forward service/hivebox-api-service 8080:80
```

**Pipeline Failures:**
- Check secrets are properly configured in repository settings
- Verify SonarCloud project exists and automatic analysis is disabled
- Ensure Terrascan has access to k8s_manifests directory

## Phase 4 Achievements

- Enhanced FastAPI application with production-ready endpoints
- Comprehensive integration testing with multiple approaches  
- Production-ready Kubernetes manifests with security best practices
- Multi-stage CI pipeline with comprehensive quality gates
- Security-first approach with multiple scanning tools
- Automated container vulnerability scanning
- Professional error handling and pipeline reporting
- Documentation following DevOps best practices

## Next Steps (Phase 5)

- Redis/Valkey caching implementation for improved performance
- MinIO S3-compatible storage for data persistence
- Prometheus and Grafana monitoring setup
- Production-ready observability and alerting
- Enhanced health checks and metrics collection

**Time Investment:** ~6-8 hours
**Difficulty:** Intermediate
**Key Learning:** Kubernetes fundamentals, CI/CD security practices, production-ready deployments