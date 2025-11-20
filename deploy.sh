#!/bin/bash

echo "Deploying CRM System..."

if [ ! -f .env ]; then
    echo ".env file not found. Create from .env.example"
    exit 1
fi

docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "Deployment completed!"
echo "Check logs: docker-compose logs -f web"
echo "API available at: http://localhost:8000"
echo "Docs at: http://localhost:8000/docs"