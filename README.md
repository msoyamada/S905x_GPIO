# TVBOX com SoC Amlogic 905x
Exemplo realizado com a TVBOX TG3
<img src="https://github.com/msoyamada/XPlus_GPIO/blob/main/images/tg3,jpg" width="270" height="95"> 

<img src="https://github.com/msoyamada/XPlus_GPIO/blob/main/screenshots/LogoCC-Copia.png" width="100" height="97">
Ciência da Computação - Campus Cascavel


# Instalar o Armbian
Sugestão: https://github.com/ophub/amlogic-s9xxx-armbian/releases
Imagem (https://github.com/ophub/amlogic-s9xxx-armbian/releases/download/Armbian_noble_save_2024.11/Armbian_24.11.0_amlogic_s905x-t95_noble_6.6.62_server_2024.11.20.img.gz)


# X905x GPIO 
Dois controladores GPIO
gpiochip0 - 11 lines (AO)
gpiochip1 - 100 lines 

* Todos os pinos são multiplexados, e podem ter mais de uma funcionalidade *
Na TG3 não foi possível mapear nenhum GPIO disponível, apenas o TX/RX disponível na porta serial 
TX= GPIO (0, 0)  - chip 0, porta 0
RX= GPIO (0, 1) - chip 0, porta 1
Na (X in Plus)[https://github.com/msoyamada/XPlus_GPIO] o número de pinos foi maior, inclusive foram identificadas portas I2C.


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
**Nao esquecer de dar um `source .env/bin/activate` a cada inicialização da placa**


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


Código python [blink.py](Examples/blink.py)

