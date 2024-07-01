import smartgarden.ntptime
from smartgarden.tftdisplay import display_all
from smartgarden.pumpa import togglepump_main, get_last_pump_on
#from smartgarden.pumpautomatic import toggleautomaticpump_main
import utime
from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import glcdfont
import tt24
import time

pump = Pin(27, Pin.OUT)
pump.value(1)

# Main loop to display time on TFT display
while True:
    display_all()
    togglepump_main()
    #toggleautomaticpump_main()
    utime.sleep(1)

