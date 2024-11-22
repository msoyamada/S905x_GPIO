# Acesso GPIO TVBOX com SoC Amlogic 905x
Exemplo realizado com a TVBOX TG3
<img src="https://github.com/msoyamada/s905x_GPIO/blob/main/images/tg3.jpg" width="270" height="140"> 

<img src="https://github.com/msoyamada/XPlus_GPIO/blob/main/screenshots/LogoCC-Copia.png" width="100" height="97">
Ciência da Computação - Campus Cascavel


# Instalar o Armbian
Sugestão: https://github.com/ophub/amlogic-s9xxx-armbian/releases

Imagem (https://github.com/ophub/amlogic-s9xxx-armbian/releases/download/Armbian_noble_save_2024.11/Armbian_24.11.0_amlogic_s905x-t95_noble_6.6.62_server_2024.11.20.img.gz)


# X905x GPIO 
Dois controladores GPIO

gpiochip0 - 11 lines (AO)

gpiochip1 - 100 lines 

* Todos os pinos são multiplexados e podem ter mais de uma funcionalidade 
  
Na TG3 não foi possível mapear nenhum GPIO disponível, apenas o TX/RX disponível na porta serial 

* TX= GPIO (0, 0)  - chip 0, porta 0

* RX= GPIO (0, 1) - chip 0, porta 1

<img src="https://github.com/msoyamada/s905x_GPIO/blob/main/images/serial.jpg" width="400" height="380"> 

Na (X in Plus)[https://github.com/msoyamada/XPlus_GPIO] o número de pinos foi maior, inclusive foram identificadas portas I2C disponíveis.


## Blinka 
Blinka: Blinka brings CircuitPython APIs and, therefore, CircuitPython libraries to single board computers (SBCs). https://circuitpython.org/blinka

Popular na Raspberry, possibilita o acesso nas portas GPIO. Possui também uma vasta biblioteca de acesso a placas via I2C.


Instalação de pacotes
```
apt install gcc
apt install python3-pip
apt install python3-venv
apt install python3-dev
apt install python3-libgpiod
apt install libgpiod2
apt install libgpiod-dev
update-alternatives --install /usr/bin/python python /usr/bin/python3 10
```

Criar um ambiente virtual python
```
mkdir s905x && cd s905x
python -m venv .env
source .env/bin/activate 
```
**Nao esquecer de executar um `source .env/bin/activate` a cada inicialização da placa**


Instalar os pacotes python
```
pip install click 
pip install adafruit-python-shell 
pip install adafruit_blinka 
pip install gpiod
```

*Para fazer a instalação sem utilizar um ambiente virtual é necessário usar a opção `--break-system-packages` no comando `pip`. Ex: `pip install --break-system-packages`

### Led Blink 
Conexão
GPIO0_0 -> LED -> RESISTOR 220 Ohm -> GND


Código python [blink.py](examples/s905x_blink.py) É necessário definir o chip como S905X explicitamente, pois o platform detector do Blinka não reconhece o chip.

```
import os
os.environ["BLINKA_FORCEBOARD"]="GENERIC_LINUX_PC"
os.environ["BLINKA_FORCECHIP"]="S905X"

import time
import board
import digitalio
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

pin = Pin((0,0))

print("hello blinky!")

led = digitalio.DigitalInOut(pin)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

```

### Conexão i2c
Como não foi identificado nenhuma porta I2C, uma solução para o interfaceamento é utilizar a implementação bitbangIO da CircuitPython. Essa biblioteca, implementa o protocolo I2C na CPU sem utilizar um controlador em hardware.

```
pip install adafruit-circuitpython-bitbangio
```

Para a conexão, pode-se utilizar os pinos disponíveis para a conexão serial disponível na placa 
```
3.3V
RX  - SDA
TX  - SCL
GND
```

Como primeiro teste, é possível fazer a busca de dispositivos conectados [i2cscanner_bitbang.py](examples/i2cscanner_bitbang.py). 

```
import os
os.environ["BLINKA_FORCEBOARD"]="GENERIC_LINUX_PC"
os.environ["BLINKA_FORCECHIP"]="S905X"

import time
import board
import digitalio
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin
import adafruit_bitbangio as io
SCL = Pin((0,0))
SDA = Pin ((0,1))

i2c = io.I2C(SCL, SDA)
while not i2c.try_lock():
    pass

print(i2c.scan())
i2c.deinit()
```

Exemplo de saída (dois dispositivos foram detectados):
```
(.env) root@armbian:~/blinka# python i2cscanner_bitbang.py
[60, 118]
```

### Instalar o circuitpython-ssd1306 

OLED 

```
apt install libjpeg-dev
pip install pillow 
pip install adafruit-circuitpython-ssd1306 
```

### Instalar o circuitpython-bmp280
BMP280 - Temperatura e pressão

`pip install adafruit-circuitpython-bmp280`

- Leitura dos dados do BMP e apresentando no display
 
Código [displaybmp.py](examples/bmp_ssd_s905.py)

```
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
```



<img src="https://github.com/msoyamada/S905X_GPIO/blob/main/images/bmp_display.jpg" width="300" height="300">







 
