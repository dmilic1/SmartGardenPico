import smartgarden.ntptime
from smartgarden.tftdisplay import setup_display, display_time
import utime
from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import glcdfont
import tt24
import time


pump = Pin(27, Pin.OUT)
pump.value(1)
setup_display()

# Main loop to display time on TFT display
while True:
    display_time()
    utime.sleep(1)

