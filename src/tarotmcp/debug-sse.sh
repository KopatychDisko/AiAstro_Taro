#!/bin/bash

# Debug script for SSE connection issues

SERVER_URL=${1:-"http://localhost:3000"}

echo "🔍 Debugging SSE connection to: $SERVER_URL"
echo "================================================"

# Test basic connectivity
echo "1. Testing basic connectivity..."
if curl -f "$SERVER_URL/health" > /dev/null 2>&1; then
    echo "✅ Server is reachable"
    curl -s "$SERVER_URL/health" | jq '.' 2>/dev/null || curl -s "$SERVER_URL/health"
else
    echo "❌ Server is not reachable at $SERVER_URL"
    exit 1
fi

echo ""

# Test API info endpoint
echo "2. Testing API info endpoint..."
if curl -f "$SERVER_URL/api/info" > /dev/null 2>&1; then
    echo "✅ API info endpoint is working"
    curl -s "$SERVER_URL/api/info" | jq '.' 2>/dev/null || curl -s "$SERVER_URL/api/info"
else
    echo "❌ API info endpoint is not working"
fi

echo ""

# Test SSE endpoint
echo "3. Testing SSE endpoint..."
echo "Attempting to connect to SSE endpoint (will timeout after 5 seconds)..."

timeout 5s curl -N -H "Accept: text/event-stream" -H "Cache-Control: no-cache" "$SERVER_URL/sse" 2>&1 | head -10

echo ""
echo "4. Testing SSE endpoint with verbose output..."
curl -v -N -H "Accept: text/event-stream" -H "Cache-Control: no-cache" "$SERVER_URL/sse" 2>&1 | head -20

echo ""
echo "================================================"
echo "🔍 Debug complete!"
echo ""
echo "If you see 404 errors, check:"
echo "1. Server is running in HTTP/SSE mode (not stdio)"
echo "2. Server is listening on the correct port"
echo "3. No reverse proxy is interfering"
echo "4. Firewall allows the connection"
echo ""
echo "Expected SSE response should include:"
echo "- HTTP 200 status"
echo "- Content-Type: text/event-stream"
echo "- Connection: keep-alive"
