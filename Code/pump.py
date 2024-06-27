from machine import Pin
import time

pump = Pin(27, Pin.OUT)
taster = Pin(0, Pin.IN, Pin.PULL_UP) 

pump_on = False

def toggle_pump(pin):
    global pump_on
    pump_on = not pump_on
    pump.value(pump_on)
    if pump_on:
        print("Pump is ON")
    else:
        print("Pump is OFF")

prev_taster_value = taster.value()

while True:
    current_taster_value = taster.value()
    
    # Check if the button was pressed (transition from HIGH to LOW)
    if prev_taster_value == 1 and current_taster_value == 0:
        toggle_pump(taster)
    
    prev_taster_value = current_taster_value
    
    # Debouncing delay
    time.sleep(0.1)
