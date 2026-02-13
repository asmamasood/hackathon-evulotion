#!/bin/bash

# Vercel deployment script for Todo Application Frontend

set -e  # Exit immediately if a command exits with a non-zero status

echo "Preparing to deploy Todo Application frontend to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI is not installed. Installing..."
    npm install -g vercel
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing frontend dependencies..."
npm install

# Build the application
echo "Building the application..."
npm run build

# Deploy to Vercel
echo "Deploying to Vercel..."
if [ "$1" = "prod" ]; then
    # Production deployment
    vercel --prod --token="$VERCEL_TOKEN"
else
    # Preview deployment (default)
    vercel --token="$VERCEL_TOKEN"
fi

echo "Deployment completed successfully!"
echo "Application URL: $(vercel url --token=$VERCEL_TOKEN)"