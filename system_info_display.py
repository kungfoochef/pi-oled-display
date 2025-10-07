import time
import board
import busio
import os
from pathlib import Path
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import subprocess
from adafruit_ssd1306 import SSD1306_I2C

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# Raspberry Pi I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the OLED display (128x32 resolution, adjust if different)
disp = SSD1306_I2C(128, 32, i2c)

# Function to draw system info on the display
def draw_info():
    # Create a blank image for drawing
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))

    # Get drawing object
    draw = ImageDraw.Draw(image)

    # Load font - try project font first, fall back to system font
    font_path = SCRIPT_DIR / "fonts" / "Minecraftia-Regular.ttf"
    if font_path.exists():
        font = ImageFont.truetype(str(font_path), 8)
    else:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 9)

    while True:
        # Clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Fetch system info
        HOST = subprocess.check_output("hostname", shell=True).decode("utf-8").strip()
        IP = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).decode("utf-8").strip()
        MAC = subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True).decode("utf-8").strip()

        # Define labels and values
        labels = ["HOST:", "IP:", "MAC:"]
        values = [HOST, IP, MAC]

        # Measure the maximum label width to align the values
        label_widths = [font.getbbox(label)[2] for label in labels]
        max_label_width = max(label_widths) + 5  # Add a small gap for spacing

        # Draw the labels and values
        y = 0
        for i in range(len(labels)):
            draw.text((0, y), labels[i], font=font, fill=255)  # Draw the label
            draw.text((max_label_width, y), values[i], font=font, fill=255)  # Align the value next to the label
            y += 10  # Move to the next line (adjust based on font size)

        # Display the image on the OLED
        disp.image(image)
        disp.show()
        time.sleep(10)  # Update every 10 seconds

# Ensure the display is cleared on startup
disp.fill(0)
disp.show()

# Start displaying information
draw_info()
