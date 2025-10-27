#!/bin/bash

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Create certs directory if it doesn't exist
mkdir -p certs

# Check if certificates already exist
if [ -f "certs/cert.pem" ] && [ -f "certs/key.pem" ]; then
    echo "✓ Certificates already exist"
else
    echo "📜 Generating SSL certificates..."
    
    # Generate self-signed certificate
    openssl req -x509 -newkey rsa:4096 \
        -keyout certs/key.pem \
        -out certs/cert.pem \
        -days 365 \
        -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    
    # Set proper permissions
    chmod 600 certs/key.pem
    chmod 644 certs/cert.pem
    
    echo "✓ SSL certificates generated"
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Build and start the application
echo "🔨 Building and starting the application..."
docker-compose up -d --build

# Wait for the service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 5

# Check if the service is running
if docker-compose ps | grep -q "fastapi-app.*Up"; then
    echo "✅ Deployment successful!"
else
    echo "❌ Deployment failed. Check logs with: docker-compose logs"
    exit 1
fi
