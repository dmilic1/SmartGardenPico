from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
from smartgarden.soil_sensor import read_soil_moisture
from smartgarden.pumpa import get_last_pump_on
import tt24
import time
import socket
import struct
import utime

# Display dimensions
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)

# Center coordinates
CENTER_X = int(SCR_WIDTH / 2)
CENTER_Y = int(SCR_HEIGHT / 2)

# SPI communication settings with display
TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(19)
TFT_MISO_PIN = const(16)
TFT_CS_PIN = const(17)
TFT_RST_PIN = const(20)
TFT_DC_PIN = const(15)

# SPI initialization
spi = SPI(
    0,
    baudrate=62500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN)
)

# Display initialization
display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT
)

# Clear display to black
display.erase()

# Function to display soil moisture
def display_soil_moisture(moisture_value):
    moisture_str = "{:.10f}".format(moisture_value)
    x = CENTER_X - (len(moisture_str) * 14 // 2)
    y = CENTER_Y + 30
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Soil Moisture: {}".format(moisture_str))

def display_last_pump_time():
    last_pump_time = get_last_pump_on()
    if last_pump_time is not None:
        time_str = "{:02}:{:02}:{:02}".format(last_pump_time[3], last_pump_time[4], last_pump_time[5])
        x = CENTER_X - (len(time_str) * 14 // 2)
        y = CENTER_Y - (24 // 2)
        display.set_pos(x, y)
        display.set_font(tt24)
        display.print("Last Pump On: {}".format(time_str))
    else:
        x = CENTER_X - (len("Last Pump On: Never") * 14 // 2)
        y = CENTER_Y + 60
        display.set_pos(x, y)
        display.set_font(tt24)
        display.print("Last Pump On: Never")

def display_all():
    display.erase()
    display_soil_moisture(read_soil_moisture())  # Here you can show actual soil moisture reading
    display_last_pump_time()


if __name__ == "__main__":

    while True:
        display_all()  # Update display with current time and soil moisture
        utime.sleep(1)  # Adjust as needed for your application timing

