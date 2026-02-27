#!/bin/bash
# =====================================================
# Gilead Vital Signs - Mac/Linux Build Script
# Winners Chapel International Arlington
# Creates a standalone executable
# =====================================================

echo ""
echo "========================================"
echo " Gilead Vital Signs - Desktop App Builder"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv build_env
source build_env/bin/activate

echo ""
echo "[2/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements_desktop.txt

echo ""
echo "[3/4] Building executable..."
pyinstaller VitalSigns.spec --clean

echo ""
echo "[4/4] Cleaning up..."
rm -rf build
rm -rf build_env
find . -name "*.pyc" -delete

echo ""
echo "========================================"
echo " BUILD COMPLETE!"
echo "========================================"
echo ""
echo "Your executable is located at:"
echo "  dist/VitalSigns"
echo ""

# Make the executable runnable
chmod +x dist/VitalSigns 2>/dev/null

# Detect OS for specific instructions
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "On macOS, you may need to allow the app in:"
    echo "  System Preferences > Security & Privacy"
    echo ""
fi

echo "You can copy VitalSigns to any computer with"
echo "the same operating system and run it!"
echo ""
