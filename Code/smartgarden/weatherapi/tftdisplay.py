from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
from smartgarden.soil_sensor import read_soil_moisture
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
    moisture_str = "{:.2f}".format(moisture_value)
    x = CENTER_X - (len(moisture_str) * 14 // 2)
    y = CENTER_Y + 30
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Soil Moisture: {}".format(moisture_str))

# Function to display current time
def display_current_time():
    now = utime.localtime()
    time_str = "{:02}:{:02}:{:02}".format(now[3], now[4], now[5])
    x = CENTER_X - (len(time_str) * 14 // 2)
    y = CENTER_Y - (24 // 2)
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Time: {}".format(time_str))

# Example of combining both displays (you can integrate this into your application flow)
def display_all():
    display.erase()
    display_current_time()
    display_soil_moisture(read_soil_moisture())  # Here you can show actual soil moisture reading

# Function to fetch NTP time
def get_ntp_time():
    NTP_DELTA = 3155673600
    host = "pool.ntp.org"
    try:
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        print("NTP time fetched successfully:", val - NTP_DELTA)
        return val - NTP_DELTA
    except Exception as e:
        print("Failed to get NTP time:", e)
        return None

# Function to set MicroPython RTC time from NTP
def settime():
    t = get_ntp_time() + 7200  # Add 2 hours (7200 seconds) for timezone adjustment
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    import machine
    machine.RTC().datetime(tm)
    print("Current time set to:", utime.localtime())

# Main loop for continuous display updates
if __name__ == "__main__":
    settime()  # Set the MicroPython RTC time initially

    while True:
        display_all()  # Update display with current time and soil moisture
        utime.sleep(1)  # Adjust as needed for your application timing

