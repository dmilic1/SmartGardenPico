from machine import Pin
import time
from smartgarden.soil_sensor import read_soil_moisture

pump_pin = Pin(27, Pin.OUT)

def control_pump(state):
    pump_pin.value(state)
    if state == 0:
        print("Pumpa je aktivna")
    else:
        print("Pumpa nije aktivna")

def toggleautomaticpump_main():
    while True:
        moisture_value = read_soil_moisture()
        print("Soil Moisture Value:", moisture_value)

        if moisture_value < 0.4:
            print("Vlaznost tla je niska, ukljucivanje pumpe...")
            control_pump(0)  
            time.sleep(5)  
            print("Iskljucivanje pumpe nakon 5 sekundi...")
            control_pump(1)  
        else:
            print("Vlaznost tla je dovoljno visoka, pumpa nije potrebna.")
            control_pump(1)  

        time.sleep(600)  

