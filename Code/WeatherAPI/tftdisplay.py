# tftdisplay.py

from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import tt24
import time

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
    display.erase()
    time_str = "{:.2f}".format(moisture_value)
    x = CENTER_X - (len(time_str) * 14 // 2)
    y = CENTER_Y + 30
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print(f"Soil Moisture: {time_str}")

# Function to display current time
def display_current_time():
    now = time.localtime()
    time_str = "{:02}:{:02}:{:02}".format(now[3], now[4], now[5])
    x = CENTER_X - (len(time_str) * 14 // 2)
    y = CENTER_Y - (24 // 2)
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print(time_str)

# Example of combining both displays (you can integrate this into your application flow)
def display_all():
    display.erase()
    display_current_time()
    display_soil_moisture(0.0)  # Ovdje ćemo prikazati primjer vlažnosti tla, može se prilagoditi stvarnom čitanju

