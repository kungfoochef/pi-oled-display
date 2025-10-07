# Raspberry Pi OLED Display

Displays system information (hostname, IP address, MAC address) on a small OLED screen connected to a Raspberry Pi.

## Hardware Requirements

- Raspberry Pi (any model with I2C support)
- SSD1306 OLED display (128x32 resolution)
- I2C connection between Pi and display

## Project Structure

```
~/projects/pi-oled-display/
├── venv/                        # Virtual environment (created during install)
├── fonts/                       # Custom fonts
│   └── Minecraftia-Regular.ttf
├── system_info_display.py       # Main display script
├── requirements.txt             # Python dependencies
├── pi-oled-display.service      # Systemd service file
├── install.sh                   # Installation script
├── README.md                    # This file
└── CLAUDE.md                    # Technical reference for AI assistance
```

## Installation

### First Time Setup

1. **Clone this repository on your Raspberry Pi:**
   ```bash
   mkdir -p ~/projects
   cd ~/projects
   git clone <your-repo-url> pi-oled-display
   cd pi-oled-display
   ```

2. **Copy your font file (optional):**

   The Minecraftia font is **not included** in this repository due to copyright restrictions.

   **Option A:** Download Minecraftia font (free for personal use):
   - Download from: https://www.dafont.com/minecraftia.font
   - Extract and copy to: `~/projects/pi-oled-display/fonts/Minecraftia-Regular.ttf`

   **Option B:** Use system font (no setup needed):
   - The script will automatically fall back to DejaVu Sans Mono if Minecraftia is not found

3. **Run the installation script:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. **Start the service:**
   ```bash
   sudo systemctl start pi-oled-display
   ```

## Usage

### Service Management

**Start the display:**
```bash
sudo systemctl start pi-oled-display
```

**Stop the display:**
```bash
sudo systemctl stop pi-oled-display
```

**Check status:**
```bash
sudo systemctl status pi-oled-display
```

**View logs:**
```bash
sudo journalctl -u pi-oled-display -f
```

**Restart after changes:**
```bash
sudo systemctl restart pi-oled-display
```

### Manual Testing

To run manually without the service:
```bash
cd ~/projects/pi-oled-display
source venv/bin/activate
python system_info_display.py
```

Press `Ctrl+C` to stop.

## Updating

To pull updates from GitHub:

```bash
cd ~/projects/pi-oled-display
git pull
sudo systemctl restart pi-oled-display
```

If dependencies changed:
```bash
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart pi-oled-display
```

## Troubleshooting

**Display not working:**
- Check I2C is enabled: `sudo raspi-config` → Interface Options → I2C
- Verify display connection: `i2cdetect -y 1`
- Check service logs: `sudo journalctl -u pi-oled-display -n 50`

**Service won't start:**
- Check Python path: `which python` in venv
- Verify permissions: `ls -la ~/projects/pi-oled-display`
- Check service status: `sudo systemctl status pi-oled-display`

## Configuration

Update interval and display settings can be modified in `system_info_display.py`:
- Line 58: `time.sleep(10)` - Change update interval (seconds)
- Line 13: `SSD1306_I2C(128, 32, i2c)` - Change display resolution if different
