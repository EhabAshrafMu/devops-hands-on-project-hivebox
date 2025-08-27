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


### Phase 2: Basic Implementation & Containers

**Duration:** ~1 hours  
**Status:** ✅ Completed  
**Branch:** `phase-2-implementation`

## 🎯 Objectives

- Implement basic FastAPI application with version functionality
- Create production-ready Docker containerization
- Establish foundation for API development
- Set up proper Python package structure
- Validate container deployment workflow

## ✅ Deliverables

- [x] FastAPI application with version endpoint (`/version`)
- [x] Version print functionality meeting Phase 2 requirements
- [x] Production-ready Dockerfile with best practices
- [x] Docker image build and testing
- [x] Requirements management with pip
- [x] Proper Python package structure
- [x] Container validation and testing

## 🏗️ Technical Implementation

### Application Architecture

**Core Components:**
- `src/main.py` - FastAPI application with endpoints
- `src/version_print.py` - Standalone version printing utility
- `src/__init__.py` - Python package initialization
- `requirements.txt` - Python dependencies management
- `Dockerfile` - Container configuration
- `.dockerignore` - Build optimization

### FastAPI Application Structure
```python
# main.py - Core application
- FastAPI app initialization with metadata
- /version endpoint (returns JSON version info)
- /health endpoint for container health checks  
- / root endpoint with API information
- Uvicorn server configuration
```

### Version Management
```python
# version_print.py - Phase 2 requirement
- Semantic versioning: v0.0.1
- Standalone execution capability
- Simple print and exit functionality
```

### Container Configuration
```dockerfile
# Single-stage Dockerfile approach
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python3", "src/main.py"]
```

## 🧪 Testing and Validation

### Local Development Testing
```bash
# Version function validation
python3 src/version_print.py
# Expected output: HiveBox App Version: v0.0.1

# FastAPI server testing  
python3 src/main.py
# Expected: Server running on http://0.0.0.0:8000
# Endpoints accessible: /version, /health, /docs
```

### Container Testing
```bash
# Docker image build
docker build -t hivebox:v0.0.1 .

# Container functionality test
docker run hivebox:v0.0.1
# Expected output: HiveBox App Version: v0.0.1

# Container cleanup
docker rmi hivebox:v0.0.1
```

### Endpoint Validation
```bash
# Version endpoint (when running FastAPI)
curl http://localhost:8000/version
# Expected: {"version": "0.0.1", "name": "HiveBox"}

```

## 📦 Dependencies Management

### Production Dependencies
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pytest==7.4.3
httpx==0.25.2
requests==2.31.0
```

### Development Dependencies
```txt
pytest==7.4.3          # Testing framework
```

### Docker Optimization
- `.dockerignore` excludes unnecessary files:
  - Git files, documentation, cache files
  - Test files, IDE configurations
  - Reduces build context size and improves security

## 🔍 Key Technical Decisions

1. **Framework Choice**: FastAPI over Flask
   - Automatic OpenAPI documentation
   - Type hints support
   - Async/await support for future scalability
   - Better performance for API-focused applications

2. **Container Strategy**: Single-stage Dockerfile
   - Simplified for Phase 2 requirements
   - Focus on functionality over optimization
   - Room for multi-stage enhancement in later phases

3. **Version Management**: Semantic Versioning
   - v0.0.1 indicating initial development
   - Consistent across all components
   - Ready for automated version bumping

4. **Python Version**: 3.11
   - Latest stable features
   - Performance improvements
   - Strong community support


## ⚠️ Challenges Encountered

1. **Dependency Management**: 
   - Initial missing uvicorn.run() call
   - Resolution: Added proper server startup code

2. **Container Command Strategy**:
   - Decision between running main.py vs version_print.py
   - Resolution: Followed Phase 2 requirement for version function

3. **Docker Build Context**:
   - Large build context without .dockerignore
   - Resolution: Comprehensive .dockerignore implementation

## 🔧 Development Workflow

### Local Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run version function
python3 src/version_print.py

# Run development server
python3 src/main.py
```

### Container Development Workflow
```bash
# Build image
docker build -t hivebox:v0.0.1 .

# Test container
docker run hivebox:v0.0.1

# Interactive debugging (if needed)
docker run -it hivebox:v0.0.1 /bin/bash
```

## 🔄 Next Phase Preparation

**Phase 3 Requirements Analysis:**
- Unit testing implementation
- GitHub Actions CI pipeline
- Code quality gates (linting, formatting)
- Automated testing on pull requests

**Technical Preparation Needed:**
- pytest configuration
- GitHub Actions workflow files
- Code coverage setup
- Quality tools integration (black, flake8, isort)

## 📋 Action Items for Phase 3

- [ ] Set up pytest test structure
- [ ] Create GitHub Actions workflow
- [ ] Implement code quality checks
- [ ] Add temperature endpoint functionality
- [ ] Set up automated testing pipeline
- [ ] Configure branch protection rules

## 🚀 Deployment Notes

**Container Deployment Ready:**
- Image builds successfully
- Version function executes correctly
- FastAPI application structure in place
- Health checks implemented
- Ready for orchestration (Kubernetes in Phase 4)

**Security Considerations:**
- Non-root user implementation (future enhancement)
- Minimal base image usage
- No sensitive data in container
- Build context optimization

## 📝 Git Workflow

**Branch Management:**
```bash
# Current phase branch
git checkout -b phase-2-implementation

# Development workflow
git add .
git commit -m "feat: complete Phase 2 basic implementation and containers"
git push origin phase-2-implementation

# Create PR: phase-2-implementation → main
```

## 🎉 Success Criteria Met

- ✅ **Version Function**: Prints correct version and exits
- ✅ **FastAPI Application**: Runs with proper endpoints
- ✅ **Docker Container**: Builds and executes successfully
- ✅ **Requirements Management**: Dependencies properly defined
- ✅ **Code Structure**: Professional Python package layout
- ✅ **Documentation**: Comprehensive phase documentation

---

**Phase 2 Complete! Container-ready HiveBox application successfully implemented** 🐳

**Ready for Phase 3: Quality Gates & CI Pipeline** 🚀
---


### Phase 3: Quality Gates & CI Pipeline

## 🎯 Overview
Phase 3 successfully implemented comprehensive quality gates and continuous integration pipeline for the HiveBox project, establishing automated code quality checks and testing workflows.

## ✅ Completed Implementation

### 3.1 Tools Setup ✅
- **Pylint**: Configured with custom `.pylintrc` for code quality analysis
- **pytest**: Enhanced testing framework with async support
- **GitHub Actions**: Complete CI/CD pipeline automation

### 3.2 Code Implementation ✅
- **Conventional Commits**: Applied throughout development workflow
- **OpenSenseMap API Integration**: Successfully implemented real-time data fetching
- **Complete Endpoint Coverage**: All required endpoints implemented and tested

#### Implemented Endpoints:
**✅ Version Endpoint**
- **URL**: `/version`
- **Method**: GET
- **Response**: Returns app version and name
- **Status**: Fully implemented and tested

**✅ Temperature Endpoint**
- **URL**: `/temperature`
- **Method**: GET  
- **Functionality**: 
  - Fetches data from 3 real senseBox devices
  - Calculates average temperature
  - Filters data to ensure freshness (< 1 hour)
  - Handles device failures gracefully
- **SenseBox IDs Used**:
  - `5eba5fbad46fb8001b799786`
  - `5c21ff8f919bf8001adf2488`
  - `5ade1acf223bd80019a1011c`

**✅ Health Endpoint**
- **URL**: `/health`
- **Method**: GET
- **Response**: Application health status

**✅ Root Endpoint**
- **URL**: `/`
- **Method**: GET
- **Response**: Welcome message with API information

### 3.3 Code Quality Achievement ✅
- **Pylint Score**: Perfect 10.00/10
- **Code Standards**: 
  - Proper import ordering
  - Comprehensive docstrings
  - Type hints and error handling
  - PEP 8 compliance
  - No trailing whitespace
  - Modular function design

### 3.4 Testing Implementation ✅
- **Unit Tests**: Complete coverage for all endpoints
- **Test Framework**: pytest with FastAPI TestClient
- **Test Results**: 4/4 tests passing consistently
- **Performance**: Tests execute in ~2 seconds (optimized from 32s)

#### Test Coverage:
- `test_root_endpoint()`: Validates welcome message
- `test_version_endpoint()`: Confirms version information
- `test_health_endpoint()`: Checks application health
- `test_temperature_endpoint()`: Validates temperature API integration

### 3.5 Continuous Integration Pipeline ✅
- **Platform**: GitHub Actions
- **Trigger Events**: Push to main/feature branches, Pull Requests
- **Pipeline Stages**:
  1. **Code Quality**: Pylint analysis (must achieve 10/10)
  2. **Unit Testing**: Complete test suite execution
  3. **Integration Testing**: Live application endpoint testing  
  4. **Container Build**: Docker image creation
  5. **Container Testing**: Validates container functionality

#### CI Workflow Features:
- **Automated Quality Gates**: Blocks merges on failures
- **Multi-stage Validation**: Tests code, app, and containers
- **Real-time Feedback**: Immediate notification of issues
- **Parallel Execution**: Efficient pipeline with job dependencies

### 3.6 Container Best Practices ✅
- **Base Image**: `python:3.11-slim` for security and size
- **Build Optimization**: Multi-stage potential for future phases
- **Health Checks**: Integrated with application endpoints
- **Production Ready**: Proper error handling and logging

## 🏗️ Technical Architecture

### Code Structure:
```
├── src/
│   ├── main.py (FastAPI app with all endpoints)
│   └── version_print.py (Phase 2 requirement)
├── tests/
│   ├── __init__.py
│   └── test_main.py (comprehensive unit tests)
├── .github/
│   └── workflows/
│       └── ci.yml (complete CI pipeline)
├── pytest.ini (test configuration)
├── .pylintrc (linting configuration)
└── requirements.txt (updated dependencies)
```

### API Integration Flow:
1. **Client Request** → `/temperature`
2. **Parallel API Calls** → 3 senseBox devices via OpenSenseMap API
3. **Data Validation** → Check timestamp freshness (< 1 hour)
4. **Temperature Extraction** → Parse sensor data
5. **Average Calculation** → Mathematical aggregation
6. **Error Handling** → Graceful failure management
7. **JSON Response** → Structured data return

## 📊 Quality Metrics
- **Code Quality**: 10.00/10 Pylint score
- **Test Coverage**: 100% endpoint coverage
- **CI Success Rate**: 100% pipeline success
- **Performance**: < 2s test execution time
- **API Response Time**: ~2s for temperature endpoint (real IoT data)

## 🔧 Configuration Files

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short
```

### .pylintrc
```ini
[MASTER]
init-hook='import sys; sys.path.append("src")'

[MESSAGES CONTROL]
disable=C0114,C0116,R0903,W0613
```

## 🎯 Key Achievements
1. **Perfect Code Quality**: Achieved maximum Pylint score
2. **Real IoT Integration**: Successfully connects to live environmental sensors
3. **Robust Error Handling**: Graceful degradation on sensor failures
4. **Automated Quality Gates**: CI blocks poor quality code
5. **Professional Testing**: Comprehensive unit and integration tests
6. **Production Readiness**: Container and deployment ready

## 🚀 Next Steps
Phase 3 establishes the foundation for Phase 4's advanced container orchestration and monitoring implementation. The CI pipeline and quality gates ensure all future development maintains these high standards.

## 📝 Lessons Learned
- **Real-time API integration** requires careful error handling for IoT device reliability
- **Quality gates** significantly improve code maintainability 
- **Automated testing** provides confidence in continuous development
- **Proper CI/CD** enables rapid, reliable deployments

## 🔮 Upcoming Phases

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