'''

    Ugradbeni sistemi
    
    Primjer korištenja MQTT za postavljanje stanja LED i očitavanje pritiska na taster na sistemu picoETF.
    Demonstrira korištenje mqtt.robust i ujson. Koriste se zbirne teme za sve LED odnosno za sve tastere. Pojedinačne
    LED/tasteri se identificiraju korištenjem JSON-formatiranih poruka.
    
    Samim Konjicija, 13.4.2023. godine

'''

from machine import Pin
import time
import network
from umqtt.robust import MQTTClient
import ujson

t1=Pin(0)
t2=Pin(1)
t3=Pin(2)
t4=Pin(3)

led0=Pin(4,Pin.OUT)
led1=Pin(5,Pin.OUT)
led2=Pin(6,Pin.OUT)
led3=Pin(7,Pin.OUT)
led4=Pin(8,Pin.OUT)
led5=Pin(9,Pin.OUT)
led6=Pin(10,Pin.OUT)
led7=Pin(11,Pin.OUT)

ledice=[led0,led1,led2,led3,led4,led5,led6,led7]


# Uspostavljanje WiFI konekcije
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('ETF-WiFi-Guest', 'ETF-WiFi-Guest')

while not nic.isconnected():
    print("Čekam konekciju ...")
    time.sleep(5)

print("WLAN konekcija uspostavljena")
ipaddr=nic.ifconfig()[0]

print("Mrežne postavke:")
print(nic.ifconfig())

# Funkcija koja se izvršava na prijem MQTT poruke
def sub(topic,msg):
    parsed=ujson.loads(msg)
    led=parsed["led"]
    stanje=parsed["stanje"]
    print('Tema: '+str(topic))
    print('Poruka: '+str(msg))
    print('LED: '+str(led))
    print('Stanje: '+str(stanje))
    
    if stanje==1:
        ledice[led].on()
    else:
        ledice[led].off()
    
# Funkcije za slanje MQTT poruka na pritisak tastera
def t1_publish(p):
    msg=b'{ "taster": 1,"stanje": 1 }'
    mqtt_conn.publish(b'picoetf/tasteri',msg)
def t2_publish(p):
    msg=b'{ "taster": 2,"stanje": 1 }'
    mqtt_conn.publish(b'picoetf/tasteri',msg)
def t3_publish(p):
    msg=b'{ "taster": 3,"stanje": 1 }'
    mqtt_conn.publish(b'picoetf/tasteri',msg)
def t4_publish(p):
    msg=b'{ "taster": 4,"stanje": 1 }'
    mqtt_conn.publish(b'picoetf/tasteri',msg)


# Uspostavljanje konekcije sa MQTT brokerom
mqtt_conn = MQTTClient(client_id='picoETF', server='broker.hivemq.com',user='',password='',port=1883)
mqtt_conn.set_callback(sub)
mqtt_conn.connect()
mqtt_conn.subscribe(b"picoetf/ledice")

print("Konekcija sa MQTT brokerom uspostavljena")

t1.irq(trigger=Pin.IRQ_RISING,handler=t1_publish)
t2.irq(trigger=Pin.IRQ_RISING,handler=t2_publish)
t3.irq(trigger=Pin.IRQ_RISING,handler=t3_publish)
t4.irq(trigger=Pin.IRQ_RISING,handler=t4_publish)

# U glavnoj petlji se čeka prijem MQTT poruke
while True:
    mqtt_conn.wait_msg()

