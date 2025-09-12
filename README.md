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

## 🚀 Development Roadmap (Client RFP Requirements)

### **✅ Phase 1: Foundation & Multi-Layered Access System** *(Deadline: December 2025)*
- [x] Backend Dockerfile (Django) 
- [x] Database container configuration (PostgreSQL)
- [x] Docker Compose for local development
- [x] Basic Django REST API foundation
- [ ] **Multi-Layered RBAC Implementation:**
  - [ ] Super Admin - Full control (assign policies, manage data, users)
  - [ ] Admin - Data input capabilities (no policy assignment)
  - [ ] Registered Viewer - View authorized materials only
  - [ ] General Viewer - Public content access (no registration)
- [ ] Email notification service (SMTP integration)
- [ ] User authentication & permission system enhancement

### **Phase 2: AI-Powered Crisis Management Dashboards** *(Deadline: January 2026)*
- [ ] **Dynamic Crisis Dashboard:**
  - [ ] AI-based data scraping (twice daily automation)
  - [ ] Geo-tagged crisis events display (10-15 attributes)
  - [ ] Admin validation workflow
  - [ ] Visual alert indicators (3-day blinking alerts)
  - [ ] Real-time data ingestion pipeline
- [ ] **Dynamic Tracking Dashboard:**
  - [ ] Early action plans tracking
  - [ ] Fund utilization monitoring
  - [ ] Activity status pipeline (planned → in-progress → completed)
  - [ ] Advanced filtering (year, type, sector)
  - [ ] Central data repository

### **Phase 3: Cyclone Predictive Models Integration** *(Deadline: November 2025)*
- [ ] **Cyclone Track Predictive Tool:**
  - [ ] Web-enabled track forecasting
  - [ ] Impact calculation engine
  - [ ] Guideline generation system
  - [ ] Input/output workflow automation
  - [ ] Downloadable results (maps, reports)
- [ ] **Cyclone Classifier Model:**
  - [ ] Fully automated web execution
  - [ ] Simplified input interface
  - [ ] Real-time impact calculation
  - [ ] GIS map generation & visualization
  - [ ] Multi-format downloads (Excel, PDF, Maps)
  - [ ] IWFM BUET collaboration integration

### **Phase 4: Infrastructure & Performance** *(Ongoing)*
- [ ] **Scalability & Performance:**
  - [ ] Standard-2X Heroku equivalent compute power
  - [ ] High-availability architecture design
  - [ ] Real-time model execution optimization
  - [ ] Cost-efficient hosting migration
- [ ] **Data Management:**
  - [ ] Automated online backup system
  - [ ] Offline backup capabilities
  - [ ] Manual save options
  - [ ] Disaster recovery procedures

### **Phase 5: User Experience & Accessibility** *(Deadline: January 2026)*
- [ ] **Mobile-First Design:**
  - [ ] Responsive, low-bandwidth optimized UI
  - [ ] Progressive Web App (PWA) capabilities
  - [ ] Offline functionality for critical features
- [ ] **Multi-Language Support:**
  - [ ] i18n framework implementation
  - [ ] Bengali and English language support
  - [ ] RTL text support preparation
- [ ] **AI Chatbot Integration:**
  - [ ] Location-specific guidance system
  - [ ] Natural language processing
  - [ ] Crisis response recommendations
- [ ] **Report Generation:**
  - [ ] Automated map generation
  - [ ] Data table exports
  - [ ] PDF report compilation
  - [ ] Batch download capabilities

### **Phase 6: Final Integration & Handover** *(Deadline: February 2026)*
- [ ] **System Integration:**
  - [ ] End-to-end testing of all components
  - [ ] Performance optimization
  - [ ] Security hardening & vulnerability assessment
  - [ ] Load testing for concurrent users
- [ ] **Documentation & Handover:**
  - [ ] Complete source code documentation
  - [ ] Database schema documentation
  - [ ] API documentation (OpenAPI/Swagger)
  - [ ] Deployment & maintenance guides
  - [ ] Admin user training materials
  - [ ] Access credentials transfer to Start Bangladesh CARF
- [ ] **Quality Assurance:**
  - [ ] User acceptance testing
  - [ ] Performance benchmarking
  - [ ] Security audit completion
  - [ ] Maintainability assessment

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
