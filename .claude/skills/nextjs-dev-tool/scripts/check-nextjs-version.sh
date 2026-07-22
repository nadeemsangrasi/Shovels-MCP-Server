#!/bin/bash

# Check Next.js Version Script
# Verifies Next.js version is 16+ for MCP support

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Checking Next.js Version..."
echo ""

# Check if package.json exists
if [ ! -f package.json ]; then
    echo "${RED}❌ package.json not found${NC}"
    echo "   Run this script from your Next.js project root"
    exit 1
fi

# Check if Next.js is installed
if ! grep -q '"next"' package.json; then
    echo "${RED}❌ Next.js not found in package.json${NC}"
    echo "   Install with: npm install next"
    exit 1
fi

# Get Next.js version
NEXT_VERSION=$(npm list next --depth=0 2>/dev/null | grep next@ | sed 's/.*next@//' | sed 's/ .*//')

if [ -z "$NEXT_VERSION" ]; then
    echo "${RED}❌ Could not determine Next.js version${NC}"
    echo "   Try: npm install"
    exit 1
fi

echo "📦 Next.js Version: $NEXT_VERSION"
echo ""

# Extract major version
MAJOR_VERSION=$(echo "$NEXT_VERSION" | cut -d. -f1)

# Check if version is 16 or higher
if [ "$MAJOR_VERSION" -ge 16 ]; then
    echo "${GREEN}✅ Next.js $NEXT_VERSION supports MCP${NC}"
    echo "   MCP endpoint available at: /_next/mcp"
    echo ""

    # Check if dev server is running
    if curl -s http://localhost:3000/_next/mcp > /dev/null 2>&1; then
        echo "${GREEN}✅ MCP endpoint is accessible${NC}"
        echo "   Dev server running on port 3000"
    elif curl -s http://localhost:3001/_next/mcp > /dev/null 2>&1; then
        echo "${GREEN}✅ MCP endpoint is accessible${NC}"
        echo "   Dev server running on port 3001"
    else
        echo "${YELLOW}⚠️  MCP endpoint not accessible${NC}"
        echo "   Start dev server with: npm run dev"
    fi

    exit 0
else
    echo "${RED}❌ Next.js $NEXT_VERSION does not support MCP${NC}"
    echo "   MCP requires Next.js 16.0.0 or higher"
    echo ""
    echo "Upgrade with:"
    echo "  npm install next@latest"
    echo ""
    echo "Or use the nextjs-dev-tool MCP upgrade tool:"
    echo "  upgrade_nextjs_16"
    exit 1
fi
