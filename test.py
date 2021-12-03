import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import numpy as np
from numpy import random, arctan2, sqrt, pi
import board

import qwiic_button

import adafruit_mpu6050
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

from mail import sendEmail

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
fall = False
g = 9.81


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def streamAccGyr():
    global maxAcc
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    acc = str("Acc: %.2f, %.2f, %.2f " % (mpu.acceleration))
    gyr = str("Gyro: %.2f, %.2f, %.2f" % (mpu.gyro))
    accX, accY, accZ= mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]
    gyrX, gyrY, gyrZ = mpu.gyro[0], mpu.gyro[1], mpu.gyro[2]

    rmsAcc = sqrt(accX**2+accY**2+accZ**2)
    angVel = sqrt(gyrX**2+gyrY**2+gyrZ**2)

    orientation = unit_vector(mpu.acceleration)

    if rmsAcc >= maxAcc:
        maxAcc = rmsAcc

    font = getFont(20)
    x_1 = width/2 - font.getsize(acc)[0]/2
    y_1 = height/2 - font.getsize(acc)[1]/2
    draw.text((x_1, y_1), acc, font=font, fill="#FFFFFF")

    # strmaxAcc = 'Max: ' + str(maxAcc)
    # x_3 = width/2 - font.getsize(strmaxAcc)[0]/2
    # y_1 += font.getsize(acc)[1]
    # draw.text((x_3, y_1), strmaxAcc, font=font, fill="#FFFFFF")

    strrmsAcc = 'Max: ' + str(rmsAcc)
    x_3 = width/2 - font.getsize(strrmsAcc)[0]/2
    y_1 += font.getsize(acc)[1]
    draw.text((x_3, y_1), strrmsAcc, font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.001)

    return rmsAcc, angVel, orientation

while True:
    # start_time = time.time()

    currAcc, angVel, orientation = streamAccGyr()
    print(currAcc, angVel, orientation)
    # print("My program took", time.time() - start_time, "to run")

    # if 0.72 * g <= currAcc <= 1.28 * g:

    def draw_text(strDraw):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        font = getFont(15)
        x_1 = width/2 - font.getsize(strDraw)[0]/2
        y_1 = height/2 - font.getsize(strDraw)[1]/2
        draw.text((x_1, y_1), strDraw, font=font, fill="#FFFFFF")
        disp.image(image, rotation)


    if currAcc >= 2.5 * g and angVel >= 3:
        for x in range(20):
            currAcc, angVel, _ = streamAccGyr()

        i = 0

        for x in range(20):
            currAcc, _, _ = streamAccGyr()
            if 0.72 * g <= currAcc <= 1.28 * g:
                i += 1
        if i > 16:
            fall = True
            strAlarm = 'Fall is detected! \n Press bttnA if wrong'
            print(strAlarm)

            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            font = getFont(15)
            x_1 = width/2 - font.getsize('Fall is detected!')[0]/2
            y_1 = height/2 - font.getsize(strAlarm)[1]/2
            draw.text((x_1, y_1), strAlarm, font=font, fill="#FFFFFF")
            disp.image(image, rotation)
            time.sleep(1)

            j = 0

            start_time = time.time()

            for x in range(1500):
                my_button = qwiic_button.QwiicButton()
                my_button.LED_on((1500-j)%100)

                if j%100 == 0:
                    toPrint = str((1500-j)/100)+'s left to cancel'
                    print(toPrint)
                    draw_text(toPrint)

                if my_button.is_button_pressed():
                    draw_text('Alert cancelled')
                    break
                


                # print(digitalio.DigitalInOut(board.D23).value)
                # if not digitalio.DigitalInOut(board.D23).value:
                #     draw_text('Alert cancelled')
                #     break

                time.sleep(0.01)
                j += 1

                if j == 1499:
                    print ("Sending email...")
                    sendEmail()
                    print ("done!")
                    draw_text('Alert sent')
            
            
            break





            



    # # Draw a black filled box to clear the image.
    # draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 


    # ### render clock
    # # date = strftime("%m/%d/%Y")
    # # timer = strftime("%H:%M:%S")
    # acc = str("Acc: %.2f, %.2f, %.2f " % (mpu.acceleration))
    # # gyr = str("Gyro: %.2f, %.2f, %.2f" % (mpu.gyro))
    # # accX, accY, accZ= round(mpu.acceleration[0],2), round(mpu.acceleration[1],2), round(mpu.acceleration[2],2)
    # accX, accY, accZ= mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]

    # rmsAcc = sqrt(accX**2+accY**2+accZ**2)

    # if rmsAcc >= maxAcc:
    #     maxAcc = rmsAcc

    # if rmsAcc >= 2.5 * g:
    #     accWindow = [0]*1000
    #     i = 0
    #     for x in accWindow:
    #         accWindow[i] = rmsAcc




    # pitch = -(arctan2(accX, sqrt(accY**2 + accZ**2))*180.0)/pi
    # roll = (arctan2(accY, accZ)*180.0)/pi

    # print(maxAcc)


    # font = getFont(20)
    

    # x_1 = width/2 - font.getsize(acc)[0]/2
    # y_1 = height/2 - font.getsize(acc)[1]/2

    # draw.text((x_1, y_1), acc, font=font, fill="#FFFFFF")

    # # font = getFont(18)
    # # x_2 = width/2 - font.getsize(acc)[0]/2
    # # y_1 -= font.getsize(acc)[1]
    # # draw.text((x_2, y_1), acc, font=font, fill="#FFFFFF")



    # strmaxAcc = 'Max: ' + str(maxAcc)
    # x_3 = width/2 - font.getsize(strmaxAcc)[0]/2
    # y_1 += font.getsize(acc)[1]

    # draw.text((x_3, y_1), strmaxAcc, font=font, fill="#FFFFFF")

    # # Display image.
    # disp.image(image, rotation)
    # time.sleep(0.001)