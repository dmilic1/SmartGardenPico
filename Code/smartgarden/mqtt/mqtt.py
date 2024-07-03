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

def run_smart_garden_system():
    # Inicijalizacija
    pump = Pin(27, Pin.OUT)
    taster = Pin(0, Pin.IN, Pin.PULL_UP)
    pump_on = True

    # Spajanje na WiFi
    ssid = 'Lab220'
    password = 'lab220lozinka'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print("Waiting for connection...")
        time.sleep(5)

    print("WiFi connected")
    print("Network config:", wlan.ifconfig())
    
    openweather_api_key = "bae091179466b890b842f5a4dd85ac83"
        # Open Weather
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
    
    import ntptime
    while True:
        try:
            ntptime.settime()
            print('Time Set Successfully')
            break
        except OSError:
            print('Time Setting...')
            continue
     
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

    # Glavna petlja za obradu MQTT poruka i događaja pritiska tipke
    while True:
        try:
            mqtt_client.check_msg()  # Provjeri MQTT poruke
            
            # Čitanje vlage tla i slanje na MQTT
            moisture_value = read_soil_moisture()
            moisture_percent = format_moisture_percent(moisture_value)
            
            weather_data = get_weather('sarajevo', openweather_api_key, units=units)
            senzor.measure()
            room_humidity = senzor.humidity()
            weather = weather_data["weather"][0]["main"]
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            last_pump_time = get_last_pump_on()
            
            # Slanje formatirane vrijednosti na MQTT
            mqtt_client.publish(b'imola/soil_moisture', moisture_percent.encode())
            mqtt_client.publish(b'imola/room_humidity', "{}%".format(room_humidity).encode())
            mqtt_client.publish(b'imola/weather', str(weather).encode())
            mqtt_client.publish(b'imola/lastpump', "{:02}:{:02}:{:02}".format(last_pump_time[3], last_pump_time[4], last_pump_time[5]).encode())
            mqtt_client.publish(b'imola/temperature', "{:.2f} °C".format(temp).encode())
            mqtt_client.publish(b'imola/humidity', "{:}%".format(humidity).encode())

            
            time.sleep(5)  # Pauza između čitanja i slanja
            
        except Exception as e:
            print("Exception occurred:", e)
            time.sleep(5)  # Pauza prije ponovnog pokušaja



