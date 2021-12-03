import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from numpy import random, arctan2, sqrt, pi
import board

import adafruit_mpu6050
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default Min is 24mhz):
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

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_8_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_250_DPS
maxAcc = 0
fall = 0


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 


    ### render clock
    # date = strftime("%m/%d/%Y")
    # timer = strftime("%H:%M:%S")
    acc = str("Acc: %.2f, %.2f, %.2f " % (mpu.acceleration))
    gyr = str("Gyro: %.2f, %.2f, %.2f" % (mpu.gyro))
    # accX, accY, accZ= round(mpu.acceleration[0],2), round(mpu.acceleration[1],2), round(mpu.acceleration[2],2)
    accX, accY, accZ= mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]

    rmsAcc = sqrt(accX**2+accY**2+accZ**2)

    if rmsAcc >= maxAcc:
        maxAcc = rmsAcc

    pitch = -(arctan2(accX, sqrt(accY**2 + accZ**2))*180.0)/pi
    roll = (arctan2(accY, accZ)*180.0)/pi

    print(maxAcc)


    font = getFont(20)
    

    x_1 = width/2 - font.getsize(acc)[0]/2
    y_1 = height/2 - font.getsize(acc)[1]/2

    draw.text((x_1, y_1), acc, font=font, fill="#FFFFFF")

    # font = getFont(18)
    # x_2 = width/2 - font.getsize(acc)[0]/2
    # y_1 -= font.getsize(acc)[1]
    # draw.text((x_2, y_1), acc, font=font, fill="#FFFFFF")



    strmaxAcc = 'Max: ' + str(maxAcc)
    x_3 = width/2 - font.getsize(strmaxAcc)[0]/2
    y_1 += font.getsize(acc)[1]

    draw.text((x_3, y_1), strmaxAcc, font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.001)