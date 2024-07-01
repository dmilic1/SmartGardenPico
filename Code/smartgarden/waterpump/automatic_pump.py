from machine import Pin
import time
from smartgarden.soil_sensor import read_soil_moisture

# Pins setup
pump_pin = Pin(27, Pin.OUT)

# Function to control the pump
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

        # Check soil moisture level and control pump automatically
        if moisture_value < 0.4:
            print("Vlaznost tla je niska, ukljucivanje pumpe...")
            control_pump(0)  # Turn on the pump
            time.sleep(5)  # Keep the pump on for 5 seconds (adjust as needed)
            print("Iskljucivanje pumpe nakon 5 sekundi...")
            control_pump(1)  # Turn off the pump
        else:
            print("Vlaznost tla je dovoljno visoka, pumpa nije potrebna.")
            control_pump(1)  # Ensure the pump is off when not needed

        time.sleep(600)  # Wait 10 minutes before the next measurement

