#!/bin/bash

echo "🔍 Health check for Social Media API..."

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ All services are running"
else
    echo "❌ Some services are not running"
    docker-compose ps
    exit 1
fi

# Check if Django is responding
if curl -s http://localhost:8000/api/ | grep -q "api"; then
    echo "✅ Django API is responding"
else
    echo "❌ Django API is not responding"
    exit 1
fi

# Check database connection
if docker-compose exec db pg_isready -U django; then
    echo "✅ Database is accessible"
else
    echo "❌ Database is not accessible"
    exit 1
fi

echo "🎉 All health checks passed!"
