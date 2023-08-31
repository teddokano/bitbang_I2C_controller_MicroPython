# Bitbang I²C controller by MicroPython

## What is this?
Bitbang I²C sample using Arduino-Pico. This code has been made to explain how an I²C controller to can be implemanted.  
The **maximum bit clock frequency is 20kHz** due to MicroPython's IO speed.  
![mp_write_read_20kHz.png](https://github.com/teddokano/bitbang_I2C_controller_MicroPython/blob/main/reference/pic/mp_write_read_20kHz.png)

## Features
This bitbang I²C controller supports basic operations of I²C bus.  
It can read/write data from/into target devices.  
A NACK response from target can be handled as an error which returned from methods.  

Clock stretch and further options (clock syns/multi-controller) are not supported.  

