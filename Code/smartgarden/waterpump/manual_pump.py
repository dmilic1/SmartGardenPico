from machine import Pin
import time
import utime

pump = Pin(27, Pin.OUT)
taster = Pin(0, Pin.IN, Pin.PULL_UP) 

pump_on = True
last_pump_timestamp = None

def record_last_pump_on():
    global last_pump_timestamp
    last_pump_timestamp = utime.time()

def get_last_pump_on():
    return last_pump_timestamp
 

def toggle_pump(pin):
    global pump_on
    pump_on = not pump_on
    pump.value(pump_on)
    if pump_on:
        print("Pump is OFF")
    else:
        print("Pump is ON")
        record_last_pump_on()

prev_taster_value = taster.value()

while True:
    current_taster_value = taster.value()
    
    # Check if the button was pressed (transition from HIGH to LOW)
    if prev_taster_value == 1 and current_taster_value == 0:
        toggle_pump(taster)
    
    prev_taster_value = current_taster_value
    
    # Debouncing delay
    time.sleep(0.1)

