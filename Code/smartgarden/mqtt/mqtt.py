from machine import Pin
import utime
from umqtt.simple import MQTTClient
from smartgarden.pumpa import togglepump_main


# Define MQTT broker settings
broker = 'w866624e.ala.dedicated.aws.emqxcloud.com'
port = 1883
client_id = 'imola'
username = 'admin'
password = 'admin'

# Define MQTT topics
toggle_pump_topic = b'imola/toggle_pump'

# Initialize pump and button pins
pump = Pin(27, Pin.OUT)
taster = Pin(0, Pin.IN, Pin.PULL_UP)

pump_on = True
last_pump_timestamp = None
last_toggle_time = utime.ticks_ms()

# Function to toggle pump and handle local debounce
def toggle_pump():
    global pump_on, last_toggle_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_toggle_time) < 500:  # Debounce period of 500 ms
        return
    
    pump_on = not pump_on
    pump.value(pump_on)
    if pump_on:
        print("Pump is OFF")
    else:
        print("Pump is ON")
    
    last_toggle_time = current_time

# MQTT client initialization
mqtt_client = MQTTClient(client_id, broker, port, user=username, password=password)

# Function to handle incoming MQTT messages
def sub_callback(topic, msg):
    print("Message received on topic:", topic)
    print("Payload:", msg)
    
    if topic == toggle_pump_topic:
        toggle_pump()

# Set callback function for MQTT messages
mqtt_client.set_callback(sub_callback)

# Connect to MQTT broker
mqtt_client.connect()
print("Connected to MQTT broker")

# Subscribe to MQTT topic for pump control
mqtt_client.subscribe(toggle_pump_topic)

# Main loop to handle MQTT messages and button press
while True:
    mqtt_client.check_msg()  # Check for MQTT messages
    
    # Check for button press (simulate button press event)
    if not taster.value():
        togglepump_main()

        utime.sleep_ms(500)  # Debounce delay

    utime.sleep_ms(100)  # Adjust sleep time as needed

