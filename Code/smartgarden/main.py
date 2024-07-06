from smartgarden.tftdisplay import display_all
from smartgarden.pumpa import togglepump_main, get_last_pump_on, pump_main, get_pump_on,toggleautomaticpump_main
from smartgarden.mqtt import run_smart_garden_system
import utime
from ili934xnew import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import glcdfont
import tt24
import time
from smartgarden.soil_sensor import read_soil_moisture
from dht import DHT11
from machine import Pin
import utime
import network
import time
from umqtt.simple import MQTTClient
from smartgarden.pumpa import togglepump_main, get_last_pump_on
from smartgarden.soil_sensor import read_soil_moisture
import urequests
from dht import DHT11

senzor = DHT11(Pin(28))
pump = Pin(27, Pin.OUT)
pump.value(1)
taster = Pin(0, Pin.IN, Pin.PULL_UP)
pump_on = True

# Connecting to WiFi
ssid = 'ETF-Logosoft'
password = ''
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Waiting for connection...")
    time.sleep(5)

print("WiFi connected")
print("Network config:", wlan.ifconfig())

# Open Weather API
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

#NTP Time
import ntptime
while True:
    try:
        ntptime.settime()
        print('Time Set Successfully')
        break
    except OSError:
        print('Time Setting...')
        continue

#Get Weather info from OpenWeatherAPI 
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
 
def print_weather(weather_data):
    print(f'Timezone: {int(weather_data["timezone"] / 3600)}')
    sunrise = time.localtime(weather_data['sys']['sunrise']+weather_data["timezone"])
    sunset = time.localtime(weather_data['sys']['sunset']+weather_data["timezone"])
    print(f'Sunrise: {sunrise[3]}:{sunrise[4]}')
    print(f'Sunset: {sunset[3]}:{sunset[4]}')   
    print(f'Country: {weather_data["sys"]["country"]}')
    print(f'City: {weather_data["name"]}')
    print(f'Coordination: [{weather_data["coord"]["lon"]}, {weather_data["coord"]["lat"]}')
    print(f'Visibility: {weather_data["visibility"]}m')
    print(f'Weather: {weather_data["weather"][0]["main"]}')
    print(f'Temperature: {weather_data["main"]["temp"]}{TEMPERATURE_UNITS[units]}')
    print(f'Temperature min: {weather_data["main"]["temp_min"]}{TEMPERATURE_UNITS[units]}')
    print(f'Temperature max: {weather_data["main"]["temp_max"]}{TEMPERATURE_UNITS[units]}')
    print(f'Temperature feels like: {weather_data["main"]["feels_like"]}{TEMPERATURE_UNITS[units]}')
    print(f'Humidity: {weather_data["main"]["humidity"]}%')
    print(f'Pressure: {weather_data["main"]["pressure"]}hPa')
    print(f'Wind speed: {weather_data["wind"]["speed"]}{SPEED_UNITS[units]}')
    #print(f'Wind gust: {weather_data["wind"]["gust"]}{SPEED_UNITS[units]}')
    print(f'Wind direction: {weather_data["wind"]["deg"]}°')
    if "clouds" in weather_data:
        print(f'Cloudiness: {weather_data["clouds"]["all"]}%')
    elif "rain" in weather_data:
        print(f'Rain volume in 1 hour: {weather_data["rain"]["1h"]}mm')
        print(f'Rain volume in 3 hour: {weather_data["rain"]["3h"]}mm')
    elif "snow" in weather_data:
        print(f'Snow volume in 1 hour: {weather_data["snow"]["1h"]}mm')
        print(f'Snow volume in 3 hour: {weather_data["snow"]["3h"]}mm')

def sub_callback(topic, msg):
    print("Message received on topic:", topic)
    print("Payload:", msg)
    
    if topic == b'imola/toggle_pump':
        switch_state = int(msg.decode())  # Decode the message and convert to integer
        if switch_state == 0:
            pump.value(1)  # Pump is OFF
            print("Pump is OFF")
        elif switch_state == 1:
            pump.value(0)  # Pump is ON
            print("Pump is ON")
        else:
            print("Invalid switch state received:", switch_state)

# MQTT Client Connection
mqtt_client = MQTTClient(client_id='picoETF', 
                         server='broker.hivemq.com', 
                         user='', 
                         password='', 
                         port=1883)
mqtt_client.set_callback(sub_callback)
mqtt_client.connect()
mqtt_client.subscribe(b'imola/toggle_pump')
print("Connected to MQTT broker")

def format_moisture_percent(moisture_value):
    return "{:.2f}%".format(moisture_value * 100)

def display_callback():
    print("display callback")
    display_all()

def toggle_callback():
    print("automatic pump callback")
    toggleautomaticpump_main()
 
def togglemain_callback(p):
    print("manual pump callback")
    togglepump_main()
    
# Time tracking variables
last_display_time = 0
last_toggle_time = 0

# Define the periods in timers in milliseconds
DISPLAY_PERIOD = 5000
TOGGLE_PERIOD = 15000
TOGGLE_MANUAL_PERIOD = 3000

while True:
    current_time = time.ticks_ms()

    # Check and run display task
    if time.ticks_diff(current_time, last_display_time) >= DISPLAY_PERIOD:
        display_callback()
        last_display_time = current_time

    # Check and run automatic toggle pump task
    if time.ticks_diff(current_time, last_toggle_time) >= TOGGLE_PERIOD:
        toggle_callback()
        last_toggle_time = current_time
    
   
    try:
        mqtt_client.check_msg() 
        moisture_value = read_soil_moisture()
        moisture_percent = format_moisture_percent(moisture_value)
        weather_data = get_weather('sarajevo', openweather_api_key, units=units)
        senzor.measure()
        room_humidity = senzor.humidity()
        weather = weather_data["weather"][0]["main"]
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        last_pump_time = get_last_pump_on()
        
        # Sending values to MQTT
        mqtt_client.publish(b'imola/soil_moisture', moisture_percent.encode())
        mqtt_client.publish(b'imola/room_humidity', "{}%".format(room_humidity).encode())
        mqtt_client.publish(b'imola/weather', str(weather).encode())
        mqtt_client.publish(b'imola/lastpump', "{:02}:{:02}:{:02}".format(last_pump_time[3], last_pump_time[4], last_pump_time[5]).encode())
        mqtt_client.publish(b'imola/temperature', "{:.2f} °C".format(temp).encode())
        mqtt_client.publish(b'imola/humidity', "{:}%".format(humidity).encode())
        
    except Exception as e:
        print("Exception occurred:", e)
        

    time.sleep(1)  
