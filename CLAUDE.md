# CLAUDE.md - Technical Reference

This file contains technical details for AI assistants (like Claude) to help with future modifications to this project.

## Project Overview

**Purpose:** Display real-time system information (hostname, IP, MAC address) on a 128x32 OLED display connected to a Raspberry Pi via I2C.

**Target Platform:** Raspberry Pi (tested on models with I2C support)
**Display:** SSD1306 OLED (128x32 resolution)
**Language:** Python 3
**Service Manager:** systemd

## Architecture

### File Structure
- `system_info_display.py` - Main application (infinite loop, updates every 10s)
- `requirements.txt` - Python dependencies
- `pi-oled-display.service` - systemd service configuration
- `install.sh` - Automated deployment script
- `fonts/` - Custom fonts directory (optional, has fallback)

### Key Design Decisions

1. **Self-contained project directory** (`~/projects/pi-oled-display/`)
   - All dependencies in local venv
   - Fonts stored locally with fallback to system fonts
   - Easy to git clone and deploy

2. **Systemd service for auto-start**
   - Starts on boot
   - Auto-restarts on failure
   - Runs as user `manager` (not root)

3. **Relative paths via `Path(__file__).parent`**
   - Makes project portable
   - No hardcoded absolute paths in Python code
   - Font path: `SCRIPT_DIR / "fonts" / "Minecraftia-Regular.ttf"`

## Dependencies

```
adafruit-circuitpython-ssd1306  # OLED display driver
adafruit-blinka                 # CircuitPython compatibility layer
pillow                          # Image creation and font rendering
```

## Code Structure

### Main Components

**Display Initialization** (lines 14-16):
```python
i2c = busio.I2C(board.SCL, board.SDA)
disp = SSD1306_I2C(128, 32, i2c)
```

**Display Loop** (`draw_info()` function):
1. Creates PIL Image (1-bit bitmap)
2. Fetches system info via subprocess commands
3. Renders text with alignment
4. Pushes to OLED display
5. Sleeps 10 seconds
6. Repeats infinitely

### System Info Collection
- **Hostname:** `hostname`
- **IP Address:** `hostname -I | cut -d' ' -f1` (first IP)
- **MAC Address:** `cat /sys/class/net/wlan0/address` (WiFi interface)

**Note:** Assumes WiFi interface is `wlan0`. May need adjustment for ethernet-only setups.

## Service Configuration

**Service file:** `pi-oled-display.service`
- **Type:** simple (long-running process)
- **User:** Current user (non-root, set during installation)
- **WorkingDirectory:** `$HOME/projects/pi-oled-display`
- **ExecStart:** Uses venv Python interpreter
- **Restart:** on-failure with 10s delay
- **Note:** User and paths are templated and replaced during `install.sh` execution

## Common Modifications

### Adding New Display Fields

1. Add subprocess command to fetch data (around line 35-37)
2. Add label to `labels` list (line 40)
3. Add value to `values` list (line 41)
4. Adjust `y += 10` spacing if needed (line 53)

**Height constraint:** 32 pixels ÷ 10 pixels per line = 3 lines max (currently used)

### Changing Update Interval

Modify `time.sleep(10)` on line 58. Value is in seconds.

### Supporting Different Display Sizes

Change line 13: `SSD1306_I2C(128, 32, i2c)`
- First param: width (pixels)
- Second param: height (pixels)

Update `y += 10` increment to fit more/fewer lines.

### Using Different Network Interface

Replace `wlan0` on line 37:
- Ethernet: `eth0`
- List interfaces: `ip link show`

### Changing Font

Replace font file in `fonts/` directory, or modify line 28-32:
```python
font_path = SCRIPT_DIR / "fonts" / "YourFont.ttf"
```

## Deployment Workflow

### Initial Deployment
1. Push code to GitHub from Windows development machine
2. SSH to Raspberry Pi
3. `git clone` to `~/projects/pi-oled-display`
4. Copy font to `fonts/` directory (if using custom font)
5. Run `./install.sh`
6. Service starts automatically

### Updates
1. Make changes on Windows machine
2. Commit and push to GitHub
3. SSH to Pi: `cd ~/projects/pi-oled-display && git pull`
4. `sudo systemctl restart pi-oled-display`

### Testing Before Deployment
On Raspberry Pi:
```bash
cd ~/projects/pi-oled-display
source venv/bin/activate
python system_info_display.py  # Ctrl+C to stop
```

## Troubleshooting Guide

### Service Issues
```bash
# Check service status
sudo systemctl status pi-oled-display

# View recent logs
sudo journalctl -u pi-oled-display -n 50

# View live logs
sudo journalctl -u pi-oled-display -f

# Restart after code changes
sudo systemctl restart pi-oled-display
```

### I2C Issues
```bash
# Enable I2C
sudo raspi-config  # Interface Options → I2C → Enable

# Verify I2C device detected
i2cdetect -y 1
# Should show device at address 0x3C (typical for SSD1306)

# Check I2C permissions
groups  # Should include 'i2c' group
```

### Python/Venv Issues
```bash
# Recreate venv
cd ~/projects/pi-oled-display
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Display Shows Nothing
- Check I2C connection physically
- Verify correct I2C address (some displays use 0x3D instead of 0x3C)
- Check display voltage (3.3V or 5V depending on model)

## Security Notes

- Service runs as unprivileged user (current user, not root)
- No network listening ports
- Read-only system info queries
- No external network requests
- No sensitive data displayed (hostname/IP/MAC are public on local network)

## Performance

- CPU usage: Minimal (~0.1% on Pi 4)
- Memory: ~50MB (mostly Python runtime)
- I2C bandwidth: Negligible (128x32 = 4KB every 10s)
- No storage I/O except initial font load

## Future Enhancement Ideas

- Display CPU temperature
- Display memory usage
- Display disk space
- Add button to cycle through info screens
- Web interface to configure what's displayed
- Support multiple display sizes via config file
- Add WiFi signal strength (RSSI)
