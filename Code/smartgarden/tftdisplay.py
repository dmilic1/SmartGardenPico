from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
from smartgarden.soil_sensor import read_soil_moisture
from smartgarden.pumpa import get_last_pump_on,get_pump_on,get_activepump
from smartgarden.mqtt import run_smart_garden_system
import tt24
import time
import socket
import struct
import utime
import urequests
from dht import DHT11

senzor = DHT11(Pin(28))

openweather_api_key = "bae091179466b890b842f5a4dd85ac83"
TEMPERATURE_UNITS = {
    "standard": "K",
    "metric": "°C",
    "imperial": "°F",
}
 
SPEED_UNITS = {
    "standard": "m/s",
    "metric": "m/s",
    "imperial": "mph",
}
 
units = "metric"

def get_weather(city, api_key, units='metric', lang='en'):
        '''
        Get weather data from openweathermap.org
            city: City name, state code and country code divided by comma, Please, refer to ISO 3166 for the state codes or country codes. https://www.iso.org/obp/ui/#search
            api_key: Your unique API key (you can always find it on your openweather account page under the "API key" tab https://home.openweathermap.org/api_keys
            unit: Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. More: https://openweathermap.org/current#data
            lang: You can use this parameter to get the output in your language. More: https://openweathermap.org/current#multi
        '''
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}"
        print(url)
        res = urequests.post(url)
        return res.json()
    
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)

CENTER_X = int(SCR_WIDTH / 2)
CENTER_Y = int(SCR_HEIGHT / 2)

TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(19)
TFT_MISO_PIN = const(16)
TFT_CS_PIN = const(17)
TFT_RST_PIN = const(20)
TFT_DC_PIN = const(15)

spi = SPI(
    0,
    baudrate=62500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN)
)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT
)

display.erase()

def display_soil_moisture(moisture_value):
    moisture_str = "{:.2f}%".format(moisture_value*100)
    x = CENTER_X - (len(moisture_str) * 49 // 2)
    y = CENTER_Y - 60
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Soil Moisture: {}".format(moisture_str))

def display_last_pump_time():
    last_pump_time = get_last_pump_on()
    if last_pump_time is not None:
        time_str = "{:02}:{:02}:{:02}".format(last_pump_time[3], last_pump_time[4], last_pump_time[5])
        x = CENTER_X - (len(time_str) * 35 // 2)
        y = CENTER_Y - 25
        display.set_pos(x, y)
        display.set_font(tt24)
        display.print("Last Pump Activation: {}".format(time_str))
    else:
        x = CENTER_X - (len("Last Pump Activation: Never") * 30 // 2)
        y = CENTER_Y - 25
        display.set_pos(x, y)
        display.set_font(tt24)
        display.print("Last Pump Activation: Never")

def display_pump_status():
    pump_status = "OFF" if get_pump_on() else "ON"
    x = CENTER_X - (len("Pump Status: " + pump_status) * 28 // 3)
    y = CENTER_Y + 35
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Pump Status: {}".format(pump_status))

def display_automatic_pump_status():
    moisture_value = read_soil_moisture()
    if moisture_value < 0.4:
        x = CENTER_X - (len("Low soil moisture: pump on, off in 5s.") * 15 // 2)
        y = CENTER_Y + 90
        display.set_pos(x, y)
        display.set_font(tt24)
        display.print("Low soil moisture: pump on, off in 5s.")

def display_weather(weather_data):
    weather = weather_data["weather"][0]["main"]
    x = CENTER_X - (len("Weather") * 40 // 2)
    y = CENTER_Y + 70
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Weather: {}".format(weather))

def display_temp(weather_data):
    temp = weather_data["main"]["temp"]

    x = CENTER_X - (len("Weather") * 40 // 2)
    y = CENTER_Y + 100
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Temperature: {}C".format(temp))

def display_humidity(weather_data):
    humidity = weather_data["main"]["humidity"]

    x = CENTER_X - (len("Weather") * 40 // 2)
    y = CENTER_Y + 135
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Humidity: {}%".format(humidity))

def display_room_humidity():
    senzor.measure()
    room_humidity = senzor.humidity()
    x = CENTER_X - (len("Weather") * 40 // 2)
    y = CENTER_Y - 90
    display.set_pos(x, y)
    display.set_font(tt24)
    display.print("Room Humidity: {}%".format(room_humidity))

def display_all():
    weather_data = get_weather('sarajevo', openweather_api_key, units=units)
    print("Display all call")
    if get_activepump()==True:
        display.erase()
        display_automatic_pump_status()
    else:
        display.erase()
        display_room_humidity()
        display_soil_moisture(read_soil_moisture()) 
        display_last_pump_time()
        display_pump_status()
        display_weather(weather_data)
        display_temp(weather_data)
        display_humidity(weather_data)
        

    