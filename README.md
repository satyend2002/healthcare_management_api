# Healthcare Management API

A production-oriented **Healthcare Management REST API** built with **Python, Flask, MySQL, SQLAlchemy, JWT authentication, Role-Based Access Control (RBAC), Docker, and Gunicorn**.

The system is designed to manage core healthcare operations such as patients, doctors, departments, appointments, prescriptions, medicines, medical records, laboratory tests, invoices, payments, and inventory.

The project is being developed from a local development environment through a complete **production deployment workflow**.

---

## Project Overview

The Healthcare Management API provides a centralized backend for managing healthcare-related data and operations through RESTful APIs.

The project focuses on:

* Clean backend architecture
* RESTful API development
* Database relationships
* Authentication and authorization
* Role-based access control
* Secure API design
* Database migrations
* API validation
* Standardized API responses
* Error handling and logging
* Automated testing
* API documentation
* Docker containerization
* Production configuration
* Production database deployment
* Gunicorn application serving
* Nginx reverse proxy
* HTTPS/SSL
* Cloud/VPS deployment

---

# Features

## Patient Management

* Create patients
* Retrieve patients
* Retrieve patient by ID
* Update patient information
* Delete patients
* Search and filter patients
* Pagination
* Standard API responses

## Doctor Management

* Create doctors
* Retrieve doctors
* Retrieve doctor by ID
* Update doctor information
* Delete doctors
* Associate doctors with departments

## Department Management

* Create departments
* Retrieve departments
* Retrieve department details
* Update departments
* Delete departments

## Appointment Management

* Create appointments
* Retrieve appointments
* Update appointments
* Cancel/delete appointments
* Associate patients with doctors
* Appointment status management

## Prescription Management

* Create prescriptions
* Retrieve prescriptions
* Associate prescriptions with patients and doctors
* Prescription items
* Medicine association

## Medicine Management

* Medicine catalogue
* Medicine details
* Stock management
* Reorder level
* Active/inactive medicines
* Inventory transactions

## Medical Records

* Patient medical records
* Medical history
* Diagnosis information
* Treatment information

## Laboratory Tests

* Lab test management
* Patient test records
* Test status and results

## Billing

* Invoice management
* Payment management
* Invoice/payment relationships

---

# Authentication & Security

The API uses JWT-based authentication.

Current/Planned security features include:

* User registration
* User login
* Password hashing
* JWT access tokens
* JWT refresh tokens
* Protected APIs
* Role-Based Access Control
* Token expiration
* Token revocation/blocklist
* Active/inactive users

### Roles

The application supports role-based permissions such as:

```text
Admin
Doctor
Receptionist
User
```

Different roles can access different API operations.

---

# Advanced Authentication Roadmap

The security layer will be extended with:

* Refresh token rotation
* Password reset
* Password reset email
* Email verification
* Two-factor authentication
* Advanced permission tables
* Fine-grained permissions
* OAuth/social login

---

# API Features

The API is being developed with:

* RESTful endpoints
* CRUD operations
* Pagination
* Search
* Filtering
* Sorting
* Standardized responses
* Input validation
* HTTP status codes
* Centralized error handling

Example standardized response:

```json
{
    "message": "Patients retrieved successfully",
    "data": []
}
```

---

# Technology Stack

## Backend

* Python
* Flask
* Flask-RESTful
* SQLAlchemy
* Marshmallow

## Database

* MySQL

## Database Migration

* Flask-Migrate
* Alembic

## Authentication

* Flask-JWT-Extended
* JWT
* Password hashing

## API Testing

* Postman
* Pytest

## Development Tools

* VS Code
* Git
* GitHub

## Deployment

* Docker
* Docker Compose
* Gunicorn
* Nginx
* HTTPS/SSL
* Cloud/VPS

---

# Project Architecture

The project follows a layered backend architecture.

```text
Client
   │
   ▼
API / Resources
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
SQLAlchemy Models
   │
   ▼
MySQL Database
```

Supporting components:

```text
Authentication
Authorization / RBAC
Validation
Error Handling
Logging
Database Migrations
Configuration
```

---

# Project Structure

The project is organized into separate responsibilities.

```text
healthcare_management_api/
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── extensions/
│
├── models/
│
├── resources/
│
├── services/
│
├── repositories/
│
├── schemas/
│
├── routes/
│
├── utils/
│
├── tests/
│
└── migrations/
```

The exact structure may evolve as the project moves toward production.

---

# Database

The application uses MySQL as its relational database.

Major entities include:

```text
Users
Patients
Doctors
Departments
Appointments
Prescriptions
Prescription Items
Medicines
Medical Records
Patient Medical History
Lab Tests
Invoices
Payments
Inventory Transactions
Token Blocklist
```

Relationships between entities are handled through SQLAlchemy models and foreign keys.

---

# Database Migrations

Database schema changes are managed using:

```text
Flask-Migrate
       ↓
Alembic
       ↓
MySQL
```

Example commands:

```bash
flask db migrate -m "Add new table"
flask db upgrade
```

This allows database changes to be tracked and deployed safely instead of manually modifying production tables.

---

# Environment Configuration

Application configuration will be separated from source code.

Sensitive values such as:

* Database username
* Database password
* JWT secret
* Email credentials
* Production credentials

will be stored using environment variables.

Example:

```env
FLASK_ENV=production

DB_HOST=mysql
DB_PORT=3306
DB_NAME=healthcare_db
DB_USER=healthcare_user
DB_PASSWORD=********

JWT_SECRET_KEY=********
```

Sensitive `.env` files will not be committed to GitHub.

An `.env.example` file will be provided for configuration reference.

---

# Docker

The application will be containerized using Docker.

The Docker workflow:

```text
Dockerfile
     │
     ▼
Docker Image
     │
     ▼
Docker Container
```

The Flask application will run inside a container using Gunicorn.

MySQL can run as a separate container during the containerized deployment setup.

---

# Docker Compose

Docker Compose will be used to manage multiple services.

Planned architecture:

```text
Docker Compose
│
├── healthcare_api
│      └── Flask + Gunicorn
│
└── healthcare_mysql
       └── MySQL
```

Services can communicate through the Docker network.

---

# Gunicorn

The Flask development server is intended for development only.

For production, the application will run using **Gunicorn**, a production WSGI application server.

Example:

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

Architecture:

```text
Gunicorn
    ↓
Flask Application
    ↓
Healthcare API
```

---

# Nginx

Nginx will be used as a reverse proxy in production.

Production request flow:

```text
Client
   ↓
HTTPS
   ↓
Nginx
   ↓
Gunicorn
   ↓
Flask
   ↓
MySQL
```

Nginx will handle responsibilities such as:

* Reverse proxy
* HTTPS termination
* Static content handling where required
* Request forwarding
* Basic connection management

---

# HTTPS / SSL

The production API will be secured using HTTPS.

The goal is:

```text
http://example.com
```

to redirect to:

```text
https://example.com
```

SSL/TLS certificates will be configured on the production server.

---

# CORS

Cross-Origin Resource Sharing (CORS) will be configured according to the application's frontend/client requirements.

Development may allow broader origins, while production will use restricted trusted origins.

---

# Production Database

Development and production databases will be treated separately.

### Development

```text
Local machine
     ↓
Development MySQL
     ↓
Test data
```

### Production

```text
Cloud/VPS
     ↓
Production MySQL
     ↓
Real application data
```

Production database responsibilities will include:

* Secure credentials
* Restricted access
* Backups
* Database migrations
* Recovery planning
* Monitoring
* Controlled access

Development data will not be treated as production data.

---

# Health Checks

A health-check endpoint will be used to determine whether the application is running correctly.

Example:

```text
GET /health
```

A successful response can indicate that the API is available.

Production health checks can be used by monitoring or deployment infrastructure.

---

# Logging

Application logging will be implemented for production.

Logging will help track:

* API requests
* Errors
* Authentication events
* Database failures
* Application failures
* Important system events

Sensitive information such as passwords and secrets will not be logged.

---

# Centralized Error Handling

The API will use centralized error handling for consistent responses.

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Internal Server Error
```

Responses will follow a consistent structure.

---

# Automated Testing

Automated testing will be implemented using Pytest.

Testing areas will include:

* Authentication
* Authorization
* CRUD operations
* Validation
* Database operations
* API responses
* Error handling
* Role-based access
* Important business logic

Example:

```bash
pytest
```

---

# API Documentation

Swagger / OpenAPI documentation will be added.

The documentation will provide:

* Available endpoints
* HTTP methods
* Request parameters
* Request bodies
* Authentication requirements
* Response examples
* Error responses

This will make the API easier for developers and recruiters to understand and test.

---

# Git & GitHub

Git will be used for source-code version control.

The project will be maintained in GitHub.

Typical workflow:

```text
Local Development
       ↓
Git
       ↓
GitHub Repository
       ↓
Production Deployment
```

Example commands:

```bash
git add .
git commit -m "Add healthcare API feature"
git push origin main
```

---

# Production Deployment

The final deployment architecture will be:

```text
                    Internet
                       │
                       ▼
                  HTTPS / SSL
                       │
                       ▼
                     Nginx
                       │
                       ▼
              Gunicorn / WSGI
                       │
                       ▼
                Flask Application
                       │
                       ▼
                  MySQL Database
```

Containerized version:

```text
Cloud / VPS Server
│
└── Docker
    │
    ├── Nginx
    │
    ├── Healthcare API
    │     └── Gunicorn + Flask
    │
    └── MySQL
```

---

# Cloud / VPS Deployment

The application will eventually be deployed to a cloud/VPS server.

Deployment steps will include:

1. Provision server
2. Install Docker
3. Configure firewall
4. Clone GitHub repository
5. Configure production environment variables
6. Configure production database
7. Build Docker images
8. Start containers
9. Run database migrations
10. Configure Gunicorn
11. Configure Nginx
12. Configure domain
13. Configure HTTPS/SSL
14. Configure health checks
15. Verify API
16. Monitor logs

---

# Production Deployment Checklist

The project will be completed through the following production workflow:

* [ ] Production configuration
* [ ] Environment variables
* [ ] Secure secrets
* [ ] Production MySQL
* [ ] Database migrations
* [ ] Dockerfile
* [ ] Docker image
* [ ] Docker Compose
* [ ] Gunicorn
* [ ] Nginx
* [ ] HTTPS/SSL
* [ ] CORS configuration
* [ ] Health checks
* [ ] Logging
* [ ] Error handling
* [ ] Automated testing
* [ ] Swagger/OpenAPI
* [ ] GitHub deployment workflow
* [ ] Cloud/VPS deployment
* [ ] Production verification
* [ ] Backup strategy

---

# Future Enhancements

After completing the single-organization production deployment, the project can be extended with advanced features such as:

## Multi-Tenancy

Allow multiple independent healthcare organizations to use the same application while keeping their data isolated.

Example:

```text
Healthcare Platform
│
├── Hospital A
│    ├── Users
│    ├── Patients
│    └── Doctors
│
├── Hospital B
│    ├── Users
│    ├── Patients
│    └── Doctors
│
└── Hospital C
     ├── Users
     ├── Patients
     └── Doctors
```

## Additional Future Features

* Advanced permission management
* Email notifications
* SMS notifications
* Appointment reminders
* File/document uploads
* Prescription PDF generation
* Reports and analytics
* Audit logs
* Advanced inventory management
* Payment gateway integration
* Background jobs
* Redis caching
* Celery
* CI/CD pipeline
* Monitoring
* Cloud-managed database

---

# Development Roadmap

The project roadmap is:

```text
Phase 1
Core Healthcare API
        ↓
Phase 2
Authentication & RBAC
        ↓
Phase 3
Advanced API Features
        ↓
Phase 4
Database & Relationships
        ↓
Phase 5
Testing
        ↓
Phase 6
Swagger / OpenAPI
        ↓
Phase 7
Logging & Error Handling
        ↓
Phase 8
Docker
        ↓
Phase 9
Production Configuration
        ↓
Phase 10
Production MySQL
        ↓
Phase 11
Gunicorn
        ↓
Phase 12
Nginx
        ↓
Phase 13
HTTPS / SSL
        ↓
Phase 14
Cloud / VPS Deployment
        ↓
Phase 15
Health Checks & Monitoring
        ↓
Phase 16
Production Verification
        ↓
Future
Multi-Tenancy & Advanced Features
```

---

# Current Project Status

The project is actively being developed.

### Completed / Implemented

* Flask REST API
* MySQL database
* SQLAlchemy
* Database migrations
* Patient management
* Doctor management
* Department management
* Appointment management
* Prescription management
* Prescription items
* Medicine catalogue
* Medical records
* Laboratory tests
* Patient medical history
* Invoice management
* Payment management
* Inventory transactions
* JWT authentication
* Role-Based Access Control
* Token blocklist/revocation
* Standard API responses
* Pagination/search/filtering development

### In Progress / Planned

* Advanced authentication features
* Automated testing
* Swagger/OpenAPI
* Centralized error handling
* Production logging
* Docker production setup
* Production configuration
* Production database
* Gunicorn
* Nginx
* HTTPS/SSL
* CORS hardening
* Health checks
* Cloud/VPS deployment
* Production monitoring
* CI/CD

---

# Project Goal

The goal of this project is to build a complete, production-oriented healthcare backend that demonstrates practical experience in:

```text
Python
   +
Flask
   +
REST APIs
   +
MySQL
   +
SQLAlchemy
   +
Authentication
   +
RBAC
   +
Testing
   +
Docker
   +
Gunicorn
   +
Nginx
   +
HTTPS
   +
Cloud/VPS Deployment
```

The project is intended as a portfolio project demonstrating the complete journey from **local backend development to production deployment**.

---

# Author

**Satyendra Dwivedi**

GitHub:
https://github.com/satyend2002
