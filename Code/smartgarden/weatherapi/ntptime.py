from machine import Pin, ADC, PWM
import time
import network
from umqtt.robust import MQTTClient
import ujson

# potrebni pinovi
taster = Pin(0, Pin.IN, Pin.PULL_UP)
soil_moisture_pin = ADC(Pin(26))  # Senzor vlažnosti tla
led0 = Pin(4, Pin.OUT)
led1 = Pin(5, Pin.OUT)
led2 = PWM(Pin(6))
led2.freq(1000)

# WiFi connection
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Lab220', 'lab220lozinka')

while not nic.isconnected():
    print("Waiting for connection...")
    time.sleep(5)

print("WiFi connected")
print("Network config:", nic.ifconfig())


# MQTT
def sub(topic, msg):
    print('Message arrived:', topic)
    print('Payload:', msg)

    if topic == b'imola/led1':
        led0.value(int(msg) == 1)

    elif topic == b'imola/led2':
        led1.value(int(msg) == 1)

    elif topic == b'imola/led3':
        duty_cycle = int(float(msg) * 65535.0)
        led2.duty_u16(duty_cycle)


# MQTT connection
from umqtt.simple import MQTTClient

# MQTT broker configuration
broker = 'w866624e.ala.dedicated.aws.emqxcloud.com'
port = 1883
client_id = 'imola'
username = 'admin'
password = 'admin'

# MQTT client initialization
mqtt_conn = MQTTClient(client_id, broker, port, user=username, password=password)

# Function to handle incoming messages (subscription callback)
def sub(topic, msg):
    print((topic, msg))

# Set the subscription callback
mqtt_conn.set_callback(sub)

# Connect to the MQTT broker
mqtt_conn.connect()
print("Connected to MQTT broker")


# Pretplata
mqtt_conn.subscribe(b'imola/led1')
mqtt_conn.subscribe(b'imola/led2')
mqtt_conn.subscribe(b'imola/led3')


# Stanje tastera
def taster_publish(p):
    mqtt_conn.publish(b'imola/taster', str(taster.value()))


taster.irq(trigger=Pin.IRQ_RISING, handler=taster_publish)


# Funkcija za čitanje vlažnosti tla
def read_soil_moisture():
    moisture_value = soil_moisture_pin.read_u16()  # Read the raw analog value (0-65535)
    normalized = moisture_value / 65535.0
    normalized = 1 - normalized
    return normalized


# Main
soil_moisture = 0

while True:
    mqtt_conn.check_msg()
    # Promjena vrijednosti vlažnosti tla
    current_moisture = read_soil_moisture()

    if current_moisture != soil_moisture:
        soil_moisture = current_moisture
        mqtt_conn.publish(b'imola/soil_moisture', str(soil_moisture))

    time.sleep(1)

