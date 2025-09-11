# FOREWARN IBF Portal

A production-ready admin dashboard built with modern microservices architecture, featuring containerized services for scalable deployment on AWS EC2 with CI/CD automation.

## 🎯 Project Overview

A full-stack admin portal dashboard with complete separation of concerns:
- **User Management System**: Registration, Authentication, Role Management
- **Role-Based Authorization**: Dynamic roles (User, Manager, Admin, SuperAdmin)
- **Data Dashboard**: Analytics and reporting with real-time insights
- **Microservices Architecture**: Three independent containerized services
- **Cloud-Native**: Designed for AWS EC2 deployment with auto-scaling

## 🏗️ Three-Container Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Frontend      │    │   Backend       │    │   Database      │
│   Container     │    │   Container     │    │   Container     │
│   (Next.js)     │    │   (Django)      │    │  (PostgreSQL)   │
│                 │    │                 │    │                 │
│  Port: 3000     │    │  Port: 8000     │    │  Port: 5432     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │                 │
                    │  Docker Network │
                    │  (forewarn-net) │
                    │                 │
                    └─────────────────┘
```

## 🛠️ Tech Stack

### **Container 1: Frontend Service**
- **Framework**: Next.js 15 with App Router & TypeScript
- **Styling**: Tailwind CSS v4 + Shadcn/ui components
- **State Management**: Zustand for client state
- **HTTP Client**: Axios for API communication
- **Container**: Node.js Alpine image

### **Container 2: Backend Service**
- **Framework**: Django 5.0 + Django REST Framework
- **Language**: Python 3.11+
- **Authentication**: JWT tokens + Role-based permissions
- **API Documentation**: Django REST Swagger
- **Container**: Python Alpine image

### **Container 3: Database Service**
- **Database**: PostgreSQL 15
- **ORM**: Django ORM with migrations
- **Extensions**: UUID, full-text search
- **Container**: PostgreSQL Alpine image

## 🚀 Deployment Architecture (AWS EC2)

```
┌──────────────────────────────────────────────────────────┐
│                     AWS EC2 Instance                     │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  Frontend   │  │  Backend    │  │  Database   │       │
│  │  Container  │  │  Container  │  │  Container  │       │
│  │  :3000      │  │  :8000      │  │  :5432      │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│           │               │               │              │
│           └───────────────┼───────────────┘              │
│                           │                              │
│  ┌─────────────────────────────────────────────────────┐ │
│  │            Docker Compose Network                   │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Load Balancer │
                    │   (Nginx/ALB)   │
                    └─────────────────┘
                              │
                              ▼
                         Internet
```

## 🔄 API Communication Flow

### **Service-to-Service Communication**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Request Flow Architecture                              │
└─────────────────────────────────────────────────────────────────────────────────┘

User Browser ──► Frontend Container ──► Backend Container ──► Database Container
     │                    │                     │                     │
     │                    │                     │                     │
   HTTP/HTTPS          API Calls           ORM Queries          SQL Queries
  (Port 3000)         (Port 8000)         (Internal)          (Port 5432)
```


### **Deployment Flow**
```
Developer Push → GitHub → CI/CD Pipeline → Docker Registry → AWS EC2 → Live Application
      ↓              ↓            ↓              ↓            ↓           ↓
   git push      Actions     Build Images    ECR/DockerHub   Pull    Auto Restart
```

## 🚀 Development Roadmap

### **Phase 1: Container Setup**
- [ ] Frontend Dockerfile (Next.js)
- [ ] Backend Dockerfile (Django)
- [ ] Database container configuration
- [ ] Docker Compose for local development

### **Phase 2: Service Development**
- [ ] Django REST API development
- [ ] Next.js frontend integration
- [ ] PostgreSQL schema and migrations
- [ ] Inter-container communication

### **Phase 3: AWS Infrastructure**
- [ ] EC2 instance setup and configuration
- [ ] Security groups and networking
- [ ] Domain and SSL certificate setup
- [ ] Load balancer configuration

### **Phase 4: CI/CD Pipeline**
- [ ] GitHub Actions workflow setup
- [ ] Docker image building and pushing
- [ ] Automated deployment to EC2
- [ ] Health checks and rollback mechanisms

### **Phase 5: Production Optimization**
- [ ] Container monitoring and logging
- [ ] Database backup automation
- [ ] Performance optimization
- [ ] Security hardening

## 📁 Project Structure

```
forewarn-ibf-portal/
├── frontend/                   # Next.js Container
│   ├── Dockerfile
│   ├── src/
│   └── package.json
│
├── backend/                    # Django Container  
│   ├── Dockerfile
│   ├── requirements.txt
│   └── manage.py
│
├── database/                   # PostgreSQL Container
│   ├── init-scripts/
│   └── backups/
│
├── docker-compose.dev.yml      # Development environment
├── docker-compose.prod.yml     # Production environment
│
├── .github/                    # CI/CD Pipeline
│   └── workflows/
│       └── deploy.yml
│
├── infrastructure/             # AWS Infrastructure
│   ├── ec2-setup.sh
│   ├── nginx.conf
│   └── security-groups.tf
│
└── docs/                       # Documentation
    ├── deployment.md
    └── architecture.md
```
## �️ Local Development

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.9+ (for backend development)
- Git

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/forewarn-ibf-portal.git
   cd forewarn-ibf-portal
   ```

2. **Start the development environment**
   ```bash
   # Start all containers
   docker-compose -f docker-compose.dev.yml up -d
   
   # View logs
   docker-compose logs -f
   ```

3. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:5433

### Individual Service Development

**Frontend (Next.js)**
```bash
cd frontend
npm install
npm run dev
```

**Backend (Django)**
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

## 🚢 Production Deployment

### AWS EC2 Setup

1. **Launch EC2 instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security groups configured for HTTP/HTTPS

2. **Instance preparation**
   ```bash
   # Install Docker and Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Setup production environment
   git clone https://github.com/your-username/forewarn-ibf-portal.git
   cd forewarn-ibf-portal
   ```

3. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Builds Docker images for all services
2. Pushes images to Docker Hub
3. Deploys to EC2 via SSH
4. Runs health checks
5. Sends deployment notifications
