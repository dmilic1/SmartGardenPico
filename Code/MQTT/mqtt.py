from machine import Pin, ADC, PWM
import time
import network
from umqtt.robust import MQTTClient
import ujson
from dht import DHT11

# potrebni pinovi
taster = Pin(0, Pin.IN)
potenciometar = ADC(28)
led0 = Pin(4, Pin.OUT)
led1 = Pin(5, Pin.OUT)
led2 = PWM(Pin(6))
led2.freq(1000)
red = PWM(Pin(14))
green = PWM(Pin(12))
blue = PWM(Pin(13))
blue.freq(1000)
green.freq(1000)
red.freq(1000)
senzor = DHT11(Pin(26))

# WiFi connection
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('ETF-Logosoft', '')
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
    elif topic == b'imola/red':
        duty_cycle = int(float(msg) * 65535.0)
        red.duty_u16(duty_cycle)
    elif topic == b'imola/green':
        duty_cycle = int(float(msg) * 65535.0)
        green.duty_u16(duty_cycle)
    elif topic == b'imola/blue':
        duty_cycle = int(float(msg) * 65535.0)
        blue.duty_u16(duty_cycle)

# MQTT connection
mqtt_conn = MQTTClient(client_id='imola', server='broker.hivemq.com', port=1883)
mqtt_conn.set_callback(sub)
mqtt_conn.connect()
print("Connected to MQTT broker")

# Pretplata
mqtt_conn.subscribe(b'imola/led1')
mqtt_conn.subscribe(b'imola/led2')
mqtt_conn.subscribe(b'imola/led3')
mqtt_conn.subscribe(b'imola/red')
mqtt_conn.subscribe(b'imola/blue')
mqtt_conn.subscribe(b'imola/green')

# Stanje tastera
def taster_publish(p):
    mqtt_conn.publish(b'imola/taster', str(taster.value()))

taster.irq(trigger=Pin.IRQ_RISING, handler=taster_publish)

def publish_temperature_humidity():
    senzor.measure()
    temperature = senzor.temperature()
    humidity = senzor.humidity()
    msg = b'{ \n "Temperature" : ' + str(temperature).encode() + b', \n "Humidity" : ' + str(humidity).encode() + b' \n }'
    mqtt_conn.publish(b'imola/senzor', msg)

# Main
pot = 0
while True:
    mqtt_conn.check_msg()
    # Promjena vrijednosti potenciometra
    current_pot = potenciometar.read_u16()
    if current_pot != pot:
        pot = current_pot
        pot_value = pot / 65535.0
        mqtt_conn.publish(b'imola/potenciometar', str(pot_value))
    
    # dht
    publish_temperature_humidity()
    
    time.sleep(1)

