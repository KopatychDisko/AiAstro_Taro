#!/bin/bash

# Tarot MCP Server Deployment Script

set -e

echo "🔮 Starting Tarot MCP Server deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build the application
echo "📦 Building the application..."
npm run build

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t tarot-mcp .

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Start the services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Health check
echo "🏥 Performing health check..."
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Tarot MCP Server is running successfully!"
    echo "🌐 Server URL: http://localhost:3000"
    echo "📊 Health check: http://localhost:3000/health"
    echo "📖 API info: http://localhost:3000/api/info"
    echo "📡 SSE endpoint: http://localhost:3000/sse"
    echo "🎯 MCP endpoint: http://localhost:3000/mcp"
else
    echo "❌ Health check failed. Please check the logs:"
    docker-compose logs tarot-mcp
    exit 1
fi

echo "🎉 Deployment completed successfully!"
