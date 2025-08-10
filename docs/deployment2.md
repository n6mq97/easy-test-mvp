# 🚀 Production Deployment Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Server Setup](#server-setup)
- [GitHub Setup](#github-setup)
- [Deployment Process](#deployment-process)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Security](#security)

## 🎯 Overview

This guide describes the process of automatically deploying the application to a production server using GitHub Actions CI/CD pipeline.

**Key Principles:**
- ✅ Fully automated deployment
- ✅ Security through GitHub Secrets
- ✅ Minimal manual intervention
- ✅ Easy rollback to previous versions

## 🏗️ Architecture

```
Internet → Nginx (80/443) → Static files + Backend (8000)
```

**Components:**
- **Nginx** - web server on host (serving static files + API proxying)
- **Frontend** - static files (React build)
- **Backend** - FastAPI in Docker container (port 8000)
- **PostgreSQL** - database in Docker container (port 5432)

## 🔧 Requirements

### System Requirements
- **OS:** Ubuntu 20.04+ or Debian 11+
- **RAM:** minimum 2GB (recommended 4GB+)
- **Disk:** minimum 20GB free space
- **Network:** static IP or domain

### Software Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Git 2.30+
- Nginx 1.18+
- SSH server

## 🖥️ Server Setup

### Step 1: Connect to Server
```bash
ssh username@your-server-ip
```

### Step 2: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 3: Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Reload session
newgrp docker

# Verify installation
docker --version
```

### Step 4: Install Docker Compose
```bash
# Download latest version
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Set execute permissions
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 5: Install Git
```bash
sudo apt install git -y
git --version
```

### Step 6: Install Nginx
```bash
sudo apt install nginx -y

# Enable autostart
sudo systemctl enable nginx
sudo systemctl start nginx

# Check status
sudo systemctl status nginx
```

### Step 7: Create Working Directory
```bash
# Create project directory
sudo mkdir -p /opt/myapp

# Set ownership
sudo chown $USER:$USER /opt/myapp

# Verify permissions
ls -la /opt/
```

## 🔑 GitHub Setup

### Step 1: Generate SSH Keys
```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "deployment@yourdomain.com"

# View public key
cat ~/.ssh/id_rsa.pub
```

### Step 2: Add Key to Server
```bash
# Copy public key to server
ssh-copy-id username@your-server-ip

# Test connection
ssh username@your-server-ip
```

### Step 3: Configure GitHub Secrets

Go to your repository: `Settings` → `Secrets and variables` → `Actions`

**Add the following secrets:**

| Secret | Description | Example |
|--------|-------------|---------|
| `PROD_SSH_HOST` | Server IP or domain | `192.168.1.100` |
| `PROD_SSH_USER` | SSH username | `ubuntu` |
| `PROD_SSH_KEY` | Private SSH key | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `PROD_DB_USER` | PostgreSQL username | `myapp_user` |
| `PROD_DB_PASSWORD` | PostgreSQL password | `secure_password_123` |
| `PROD_DB_NAME` | Database name | `myapp_prod` |
| `PROD_API_URL` | API URL for frontend | `https://yourdomain.com/api` |
| `PROD_DOMAIN` | Your domain | `yourdomain.com` |

### Step 4: Configure Environment

Create `production` Environment in GitHub:
1. `Settings` → `Environments` → `New environment`
2. Name: `production`
3. Add all secrets from step 3

## 🚀 Deployment Process

### Automatic Deployment

**Trigger:** Push to `main` branch

**Sequence:**
1. **Testing** - run backend and frontend tests
2. **Build** - create production build
3. **Deploy** - automatic deployment to server
4. **Verification** - health checks and validation

### Manual Deployment

```bash
# Connect to server
ssh username@your-server-ip

# Navigate to project directory
cd /opt/myapp/easy-test-mvp

# Update code
git pull origin main

# Run deployment
./scripts/deploy.sh
```

### What Happens During Deployment

1. **Preparation**
   - Check project existence
   - Clone/update code

2. **Configuration**
   - Create `.env.prod` from GitHub Secrets
   - Create `front/.env.prod`

3. **Build**
   - Frontend production build
   - Save to volume

4. **Service Startup**
   - PostgreSQL with health checks
   - Backend with health checks
   - Apply database migrations

5. **Nginx Setup**
   - Create configuration
   - Restart service

6. **Verification**
   - Backend health checks
   - Frontend verification

## 📊 Monitoring

### Health Checks

**Backend API:**
```bash
curl http://localhost:8000/health
```

**Frontend:**
```bash
curl http://localhost/
```

**PostgreSQL:**
```bash
docker exec -it $(docker ps -q -f name=db) pg_isready
```

### Logs

**View all logs:**
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

**Service-specific logs:**
```bash
# Backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Database
docker-compose -f docker-compose.prod.yml logs -f db
```

**Nginx logs:**
```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### Service Status

```bash
# Docker container status
docker-compose -f docker-compose.prod.yml ps

# Nginx status
sudo systemctl status nginx

# Resource usage
docker stats
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check occupied ports
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :5432

# Stop conflicting services
sudo systemctl stop conflicting-service
```

#### 2. Permission Issues
```bash
# Check directory permissions
ls -la /opt/myapp/

# Fix permissions
sudo chown -R $USER:$USER /opt/myapp/
sudo chmod -R 755 /opt/myapp/
```

#### 3. Database Issues
```bash
# Test database connection
docker exec -it $(docker ps -q -f name=db) psql -U $PROD_DB_USER -d $PROD_DB_NAME

# Check database logs
docker-compose -f docker-compose.prod.yml logs db
```

#### 4. Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx
```

### Rollback to Previous Version

```bash
# Navigate to project directory
cd /opt/myapp/easy-test-mvp

# View commit history
git log --oneline -10

# Rollback to previous commit
git reset --hard HEAD~1

# Restart deployment
./scripts/deploy.sh
```

### Complete Reinstallation

```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Remove volumes
docker volume prune -f

# Remove project
rm -rf /opt/myapp/easy-test-mvp

# Re-clone
cd /opt/myapp
git clone git@github.com:username/repo.git easy-test-mvp
cd easy-test-mvp

# Start deployment
./scripts/deploy.sh
```

## 🔒 Security

### Security Principles

1. **Secrets in GitHub** - no passwords in code
2. **SSH Keys** - key-based authentication only
3. **Environment Variables** - not committed to repository
4. **Health Checks** - service state monitoring
5. **Access Rights** - minimal necessary permissions

### Recommendations

- **Regularly update** SSH keys
- **Use complex passwords** for database
- **Restrict access** to server by IP
- **Configure firewall** (ufw)
- **Regularly update** system and packages

### Firewall Configuration

```bash
# Install ufw
sudo apt install ufw

# Configure rules
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## 📚 Additional Resources

### Useful Commands

```bash
# Clean Docker
docker system prune -f

# Check disk usage
df -h

# Check memory usage
free -h

# View active processes
htop
```

### Links

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### Support

When encountering issues:

1. **Check GitHub Actions logs**
2. **Check server logs**
3. **Check service status**
4. **Use health checks** for diagnostics

---

**🎉 Congratulations!** You now have a fully automated production deployment.

**Next steps:**
1. Configure GitHub Secrets
2. Prepare your server
3. Make your first push to main
4. Enjoy automatic deployment! 🚀
