#!/bin/bash
# =====================================================
# Gilead Vital Signs - Quick Run Script (Mac/Linux)
# Winners Chapel International Arlington
# Runs the app in a desktop window
# =====================================================

echo "Starting Gilead Vital Signs Medical Records..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if dependencies are installed, if not install them
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies for first run..."
    pip3 install -r requirements_desktop.txt
fi

# Run the desktop app
python3 app_desktop.py
