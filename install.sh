#!/bin/bash

# Installation script for Raspberry Pi OLED Display
# Run this script on your Raspberry Pi after cloning the repository

set -e  # Exit on error

PROJECT_DIR="$HOME/projects/pi-oled-display"
SERVICE_FILE="pi-oled-display.service"
CURRENT_USER="$(whoami)"

echo "=== Raspberry Pi OLED Display Installation ==="
echo ""

# Create project directory if it doesn't exist
echo "Creating project directory..."
mkdir -p "$PROJECT_DIR"

# Copy files from current directory to project directory if needed
if [ "$PWD" != "$PROJECT_DIR" ]; then
    echo "Copying files to $PROJECT_DIR..."
    cp -r "$(dirname "$0")"/* "$PROJECT_DIR/"
fi

cd "$PROJECT_DIR"

# Create fonts directory if it doesn't exist
mkdir -p fonts

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install systemd service (replace placeholders with actual values)
echo "Installing systemd service..."
sed "s|{{USER}}|$CURRENT_USER|g; s|{{PROJECT_DIR}}|$PROJECT_DIR|g" "$SERVICE_FILE" | sudo tee /etc/systemd/system/"$SERVICE_FILE" > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_FILE"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To start the service now:"
echo "  sudo systemctl start pi-oled-display"
echo ""
echo "To check service status:"
echo "  sudo systemctl status pi-oled-display"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u pi-oled-display -f"
echo ""
echo "To stop the service:"
echo "  sudo systemctl stop pi-oled-display"
echo ""
