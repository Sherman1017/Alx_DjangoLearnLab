#!/bin/bash

# Deployment script for Social Media API

set -e  # Exit on error

echo "🚀 Starting deployment of Social Media API..."

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo "❌ Error: .env.production file not found!"
    echo "Create .env.production from .env.example and fill in your values"
    exit 1
fi

# Load environment variables
set -a
source .env.production
set +a

echo "1. Building Docker images..."
docker-compose build

echo "2. Running database migrations..."
docker-compose run --rm web python manage.py migrate

echo "3. Collecting static files..."
docker-compose run --rm web python manage.py collectstatic --noinput

echo "4. Creating superuser if not exists..."
docker-compose run --rm web python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
END

echo "5. Starting services..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "📊 Application is running at: http://localhost:8000"
echo "📊 API endpoints available at: http://localhost:8000/api/"
echo ""
echo "📋 Useful commands:"
echo "   docker-compose logs -f web    # View application logs"
echo "   docker-compose ps             # Check service status"
echo "   docker-compose down           # Stop all services"
