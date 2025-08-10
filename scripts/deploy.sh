#!/bin/bash
set -e

echo "🚀 Starting production deployment..."

# Configuration
PROJECT_DIR="/opt/myapp"
PROJECT_NAME="easy-test-mvp"
GITHUB_REPO="your-username/easy-test-mvp"  # Замените на ваш репозиторий

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    print_status "Creating project directory: $PROJECT_DIR"
    sudo mkdir -p "$PROJECT_DIR"
    sudo chown $USER:$USER "$PROJECT_DIR"
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if project is already cloned
if [ ! -d "$PROJECT_NAME" ]; then
    print_status "Cloning repository..."
    git clone "git@github.com:$GITHUB_REPO.git" "$PROJECT_NAME"
else
    print_status "Updating existing repository..."
    cd "$PROJECT_NAME"
    git fetch origin
    git reset --hard origin/main
    cd ..
fi

# Navigate to project
cd "$PROJECT_NAME"

# Create production environment file
print_status "Creating production environment file..."
cat > .env.prod << 'ENV_EOF'
POSTGRES_USER=$PROD_DB_USER
POSTGRES_PASSWORD=$PROD_DB_PASSWORD
POSTGRES_DB=$PROD_DB_NAME
DATABASE_URL=postgresql://$PROD_DB_USER:$PROD_DB_PASSWORD@localhost/$PROD_DB_NAME
NODE_ENV=production
LOG_LEVEL=info
ENV_EOF

# Create frontend production environment file
print_status "Creating frontend production environment file..."
cat > front/.env.prod << 'FRONTEND_ENV_EOF'
VITE_API_BASE_URL=$PROD_API_URL
FRONTEND_ENV_EOF

# Build frontend
print_status "Building frontend..."
docker-compose -f docker-compose.prod.yml --profile build up frontend-builder

# Start services
print_status "Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 30

# Apply database migrations
print_status "Applying database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

# Create nginx configuration
print_status "Creating nginx configuration..."
sudo tee /etc/nginx/sites-available/$PROJECT_NAME > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name $PROD_DOMAIN www.$PROD_DOMAIN;
    
    # Frontend static files
    location / {
        root $PROJECT_DIR/$PROJECT_NAME/front/dist;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Backend API proxy
    location /api/ {
        proxy_pass http://localhost:8000/\;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check
    location /health {
        proxy_pass http://localhost:8000/health\;
        access_log off;
    }
}
NGINX_EOF

# Enable nginx site
print_status "Enabling nginx site..."
sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Health check
print_status "Performing health check..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "✅ Backend health check passed"
else
    print_error "❌ Backend health check failed"
    exit 1
fi

if curl -f http://localhost/ > /dev/null 2>&1; then
    print_status "✅ Frontend health check passed"
else
    print_error "❌ Frontend health check failed"
    exit 1
fi

print_status "🎉 Production deployment completed successfully!"
print_status "🌐 Frontend: http://$PROD_DOMAIN"
print_status "🔌 Backend API: http://$PROD_DOMAIN/api"
