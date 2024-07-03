from smartgarden.tftdisplay import display_all
from smartgarden.pumpa import togglepump_main, get_last_pump_on, pump_main, get_pump_on
from smartgarden.mqtt import run_smart_garden_system
import utime
from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import glcdfont
import tt24
import time
from smartgarden.soil_sensor import read_soil_moisture

pump = Pin(27, Pin.OUT)
pump.value(1)  

def display_callback(timer):
    display_all()
    
display_timer = Timer(period=5000, mode=Timer.PERIODIC, callback=display_callback)

while True:
    run_smart_garden_system()
    toggleautomaticpump_main()
    togglepump_main()
    time.sleep(1)  

