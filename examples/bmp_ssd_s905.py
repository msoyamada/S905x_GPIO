
import os
os.environ["BLINKA_FORCEBOARD"]="GENERIC_LINUX_PC"
os.environ["BLINKA_FORCECHIP"]="S905X"


import time
import board
import digitalio
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin


#import adafruit_bitbangio as bitbangio
import adafruit_bitbangio as io

from PIL import Image, ImageDraw, ImageFont
# Import the SSD1306 module.
import adafruit_ssd1306

import adafruit_bmp280

# Create sensor object, communicating over the board's default I2C bus


# Create the I2C interface.

SCL = Pin((0,0))
SDA = Pin ((0,1))

i2c = io.I2C(SCL, SDA)
#while not i2c.try_lock():
#    pass


#print(i2c)

display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
bmp280.sea_level_pressure = 1013.25


#print(i2c.scan())

display.fill(0)
display.show()

while (True):
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    print("Temperature ")
    print(bmp280.temperature)
    draw.text((2, 0 + 2), f'Temp {bmp280.temperature:.2f} C', font=font, fill=255)
    draw.text((2, 0 + 15), f'Pres {bmp280.pressure:.2f} hPa' , font=font, fill=255)
    draw.text((2, 0 + 30), f'Alt {bmp280.altitude:.2f} m' , font=font, fill=255)
    display.fill(0)
    display.image(image)
    display.show()
    time.sleep(5)
