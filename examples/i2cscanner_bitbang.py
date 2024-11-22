
import os
os.environ["BLINKA_FORCEBOARD"]="GENERIC_LINUX_PC"
os.environ["BLINKA_FORCECHIP"]="S905X"


import time
import board
import digitalio
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin



import adafruit_bitbangio as bitbangio

SCL = Pin((0,0))
SDA = Pin ((0,1))

i2c = bitbangio.I2C(SCL, SDA)
while not i2c.try_lock():
    pass

print(i2c.scan())
i2c.deinit()
