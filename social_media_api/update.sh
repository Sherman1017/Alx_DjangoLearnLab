#!/bin/bash

echo "🔄 Updating Social Media API..."

# Backup database
echo "1. Backing up database..."
docker-compose exec db pg_dump -U django social_media_api > backup_$(date +%Y%m%d_%H%M%S).sql

# Pull latest code
echo "2. Pulling latest code..."
git pull origin main

# Update dependencies
echo "3. Updating dependencies..."
docker-compose build --no-cache web

# Run migrations
echo "4. Running migrations..."
docker-compose run --rm web python manage.py migrate

# Collect static files
echo "5. Collecting static files..."
docker-compose run --rm web python manage.py collectstatic --noinput

# Restart services
echo "6. Restarting services..."
docker-compose down
docker-compose up -d

# Run health check
echo "7. Running health check..."
sleep 10
./health_check.sh

echo "✅ Update complete!"
