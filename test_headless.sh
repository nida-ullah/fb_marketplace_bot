#!/bin/bash

# Test Script for Headless Mode Configuration
# This script helps you test both visible and headless modes

echo "=========================================="
echo "FB Marketplace Bot - Headless Mode Test"
echo "=========================================="
echo ""

# Function to test current configuration
test_configuration() {
    local mode=$1
    echo "Testing $mode mode..."
    echo ""
    
    # Show current setting
    echo "Environment variable: PLAYWRIGHT_HEADLESS=$PLAYWRIGHT_HEADLESS"
    
    # Check Python environment
    python -c "
import os
from django.conf import settings
import django
django.setup()

headless = os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true'
print(f'Headless mode: {headless}')
print(f'Browser will be: {\"Hidden (background)\" if headless else \"Visible (window opens)\"}')
print(f'Console window: {\"No\" if headless else \"Yes (on Windows)\"}')
"
    echo ""
}

# Menu
echo "Select test mode:"
echo "1) Test VISIBLE mode (development - browser opens)"
echo "2) Test HEADLESS mode (production - browser hidden)"
echo "3) Show current configuration"
echo "4) Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "=========================================="
        echo "VISIBLE MODE TEST"
        echo "=========================================="
        export PLAYWRIGHT_HEADLESS=false
        test_configuration "VISIBLE"
        
        echo "Starting Django server..."
        echo "Go to: http://localhost:8000/dashboard/posts"
        echo "1. Select a pending post"
        echo "2. Click 'Start Posting'"
        echo "3. Browser window should OPEN"
        echo ""
        read -p "Press Enter to start server..."
        python manage.py runserver
        ;;
        
    2)
        echo ""
        echo "=========================================="
        echo "HEADLESS MODE TEST"
        echo "=========================================="
        export PLAYWRIGHT_HEADLESS=true
        test_configuration "HEADLESS"
        
        echo "Starting Django server..."
        echo "Go to: http://localhost:8000/dashboard/posts"
        echo "1. Select a pending post"
        echo "2. Click 'Start Posting'"
        echo "3. Browser window should NOT open"
        echo "4. Check logs: logs/posting_process.log"
        echo ""
        read -p "Press Enter to start server..."
        python manage.py runserver
        ;;
        
    3)
        echo ""
        echo "=========================================="
        echo "CURRENT CONFIGURATION"
        echo "=========================================="
        test_configuration "CURRENT"
        ;;
        
    4)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
