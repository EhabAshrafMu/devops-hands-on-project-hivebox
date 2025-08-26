# HiveBox - DevOps End-to-End Project 🐝

A scalable RESTful API for tracking environmental sensor data from openSenseMap, customized to help beekeepers monitor their hives. This project follows DevOps best practices and covers the complete Software Development Life Cycle (SDLC).

## 📋 Project Overview

HiveBox builds a production-ready API that:
- Fetches real sensor data from [openSenseMap](https://opensensemap.org/)
- Provides temperature monitoring for beekeepers
- Scales from basic implementation to handling thousands of requests per second
- Implements complete CI/CD pipeline with monitoring and observability

**Target SenseBox IDs:**
- `5eba5fbad46fb8001b799786`
- `5c21ff8f919bf8001adf2488` 
- `5ade1acf223bd80019a1011c`

## 🗺️ Project Roadmap

| Phase | Status | Description |
|-------|---------|-------------|
| **Phase 1** | ✅ | Project Setup & Planning |
| **Phase 2** | ✅ | Basic Implementation & Containers |
| **Phase 3** | 📋 | Quality Gates & CI Pipeline |
| **Phase 4** | 📋 | Kubernetes & CD Pipeline |
| **Phase 5** | 📋 | Production Features (Cache, Storage, Monitoring) |
| **Phase 6** | 📋 | Optimization & Advanced Features |
## 🚀 Getting Started

### Prerequisites
- Git installed
- GitHub account
- Docker (for Phase 2+)
- Python 3.8+ (for Phase 2+)

---

## 📖 Detailed Implementation Guide

## Phase 1: Kickoff - Setting up the GitHub repo and the project page

**Objective:** Establish project structure, Git workflow, and project management setup.

### 1. Fork the Main Repository

We start by forking the main project repository (It only has a README.md, nothing more):

**Main Project Link:** https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox

1. Go to the repository link above
2. Click "Fork" button in the top right
3. Select your GitHub account as the destination

### 2. Clone the Repository Locally

```bash
# Clone your forked repository
git clone https://github.com/YOUR-USERNAME/devops-hands-on-project-hivebox
cd devops-hands-on-project-hivebox
```

### 3. Add Upstream Remote

We add the original repo as upstream to pull any updates:

```bash
git remote add upstream https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox.git
```

**Verify remote repositories:**
```bash
git remote -v
```

You should see:
- `origin`: Your forked repo (where you push changes)
- `upstream`: Project's original repo (for pulling updates)

### 4. Branching Strategy

We follow **Git Flow best practices** for development projects by creating an integration branch and feature branches for each phase.

**Branch Structure:**
```
main (production-ready code) - Production environment (always deployable)
├── development (integration branch) - Staging/QA environment (integration testing)
    ├── phase-1-kickoff (feature branch)
    ├── phase-2-implementation (feature branch)
    ├── phase-3-ci-cd (feature branch)
    └── etc...
```

**Setup branches:**
```bash
# Create development branch
git checkout -b development

# Create feature branch for Phase 1
git checkout -b phase-1-kickoff
```

**Important Rule:** "Each phase should be presented as a pull request against the main branch. Don't push directly to the main branch!"

**Workflow:**
1. Work on `phase-1-kickoff` branch
2. When done, create PR: `phase-1-kickoff` → `main`
3. Merge the PR
4. Start next phase on new branch from updated `main`

### 5. GitHub Project Board Setup

1. Go to your forked repository on GitHub
2. Click "Projects" tab → "New project"
3. Choose "Table" view → "Kanban" template
4. Create columns: "Backlog", "In Progress", "In Review", "Done"
5. Add cards for each phase and major tasks

### 6. Project Structure Creation

Create the initial project structure:

```bash
# Create directories
mkdir -p docs src tests

# Create initial files
touch requirements.txt
touch src/__init__.py

# Create phase documentation
touch docs/phase-1.md
```

### 7. OpenSenseMap API Research

Test the target senseBox APIs to understand the data structure:

```bash
# Test first senseBox
curl -s "https://api.opensensemap.org/boxes/5eba5fbad46fb8001b799786"

# Check temperature sensor data
curl -s "https://api.opensensemap.org/boxes/5eba5fbad46fb8001b799786" | grep -i temperature
```

### 8. Commit Phase 1 Work

```bash
# Add all changes
git add .

# Commit with conventional commits format
git commit -m "docs: complete Phase 1 project setup and documentation

- Add project structure (src, tests, docs)
- Create branching strategy following Git Flow
- Update README with step-by-step guide
- Research openSenseMap API endpoints"

# Push to your fork
git push origin phase-1-kickoff
```

### 9. Create Pull Request

1. Go to your GitHub repository
2. Click "Compare & pull request" for `phase-1-kickoff` branch
3. Target: `main` branch
4. Add description of Phase 1 completion
5. Create pull request and merge it

---

## 🔮 Upcoming Phases

### Phase 2: Basic Implementation & Containers
- FastAPI/Flask implementation
- Docker containerization
- Version endpoint implementation

### Phase 3: Quality Gates & CI Pipeline
- Unit testing
- GitHub Actions CI
- Code quality checks
- Temperature endpoint with status logic

### Phase 4: Kubernetes & CD Pipeline
- KIND cluster setup
- Kubernetes manifests
- Ingress configuration
- Continuous Delivery pipeline

### Phase 5: Production Features
- Redis caching layer
- MinIO storage integration
- Prometheus metrics
- Health checks and readiness probes

### Phase 6: Optimization & GitOps
- Argo CD for GitOps
- Multi-environment setup
- Performance optimization
- Advanced monitoring

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python |
| **Framework** | FastAPI |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes |
| **CI/CD** | GitHub Actions |
| **Caching** | Valkey (Redis-compatible) |
| **Storage** | MinIO (S3-compatible) |
| **Monitoring** | Prometheus, Grafana |
| **Infrastructure** | Terraform |

## 📚 Learning Outcomes

By completing this project, you will gain hands-on experience with:

- ✅ Agile project management and Git Flow
- 🔄 RESTful API development and testing
- 🐳 Docker containerization best practices
- ☸️ Kubernetes deployment and management
- 🔄 CI/CD pipeline implementation
- 📊 Monitoring and observability
- 🏗️ Infrastructure as Code (IaC)
- 🔒 Security best practices
- 📈 Performance optimization and scaling

## 🤝 Contributing

This is a learning project following DevOps best practices:

1. Each phase should be implemented in a separate branch
2. All changes must go through Pull Request review
3. Follow conventional commit messages
4. Document everything for future reference

## 📄 License

This project is for educational purposes as part of the DevOps learning journey.

---

**Built with ♾️ DevOps best practices and a passion for continuous learning!**