import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from numpy import random

import board

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape! 135
width = disp.height #240
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

def getFont(size):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    return font

def getRandomXY():
    x = random.randint(240, size=10)
    y = random.randint(135, size=10) 
    return x, y

x, y = getRandomXY()

reset = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    ### render snowflake
    if buttonA.value and buttonB.value:
        font = getFont(18)
        offset_x = 1
        offset_y = 1
        for i in range(10):
            draw.text((x[i], y[i]), "❄", font=font, fill="#0000FF")
            x[i] = x[i] + offset_x if x[i] + offset_x < width else x[i] + offset_x - width
            y[i] = y[i] + offset_y if y[i] + offset_y < height else y[i] + offset_y - height
        reset = True
    elif not buttonA.value and buttonB.value:
        offset_x = 2
        offset_y = 6
        for i in range(10):
            draw.text((x[i], y[i]), "\\", font=font, fill="#BFE7F6")
            x[i] = x[i] + offset_x if x[i] + offset_x < width else x[i] + offset_x - width
            y[i] = y[i] + offset_y if y[i] + offset_y < height else y[i] + offset_y - height
        reset = True
    elif buttonA.value and not buttonB.value:
        offset_x = random.randint(-1, high=1, size=10)
        offset_y = random.randint(5, size=10)
        offset_y = -offset_y
        if reset:
            x1, y1 = getRandomXY()
        for i in range(10):
            draw.text((x[i], y[i]), "❄", font=font, fill="#0000FF")
            draw.text((x1[i], y1[i]), ".", font=font, fill="#0000FF")
            x[i] = x[i] + offset_x[i] if x[i] + offset_x[i] < width else x[i] + offset_x[i] - width
            y[i] = y[i] + offset_y[i] if y[i] + offset_y[i] < height else y[i] + offset_y[i] - height
            x1[i] = x1[i] + offset_x[i] if x1[i] + offset_x[i] < width else x1[i] + offset_x[i] - width
            y1[i] = y1[i] + offset_y[i] if y1[i] + offset_y[i] < height else y1[i] + offset_y[i] - height
        reset = False

    ### render clock
    date = strftime("%m/%d/%Y")
    timer = strftime("%H:%M:%S")
    font = getFont(44)
    
    x_1 = width/2 - font.getsize(timer)[0]/2
    y_1 = height/2 - font.getsize(timer)[1]/2
    draw.text((x_1, y_1), timer, font=font, fill="#FFFFFF")

    font = getFont(18)
    x_2 = width/2 - font.getsize(date)[0]/2
    y_1 -= font.getsize(date)[1]
    draw.text((x_2, y_1), date, font=font, fill="#FFFFFF")
    # Display image.
    disp.image(image, rotation)
    time.sleep(0.001)