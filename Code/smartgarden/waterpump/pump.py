from machine import Pin
import time
import utime
from smartgarden.soil_sensor import read_soil_moisture

# Pin setup
pump_pin = Pin(27, Pin.OUT)
taster = Pin(0, Pin.IN, Pin.PULL_UP)

# Global variables
pump_on = False
last_pump_timestamp = utime.localtime()

# Function to control the pump
def control_pump(state):
    pump_pin.value(state)
    if state == 0:
        print("Pumpa je aktivna")
    else:
        print("Pumpa nije aktivna")

# Function to record the last pump activation time
def record_last_pump_on():
    global last_pump_timestamp
    last_pump_timestamp = utime.localtime()

# Function to get the last pump activation time
def get_last_pump_on():
    return last_pump_timestamp

# Function to get the current pump state
def get_pump_on():
    return pump_on

activepump=False

def get_activepump():
    return activepump

# Function to toggle the pump state
def toggle_pump(pin):
    global pump_on
    pump_on = not pump_on
    control_pump(pump_on)
    if pump_on:
        print("Pump is OFF")
    else:
        print("Pump is ON")
        record_last_pump_on()

# Main function to handle manual pump control
def togglepump_main():
    prev_taster_value = taster.value()

    current_taster_value = taster.value()

    if prev_taster_value == 1 and current_taster_value == 0:
        toggle_pump(taster)

    prev_taster_value = current_taster_value


# Main function to handle automatic pump control
def toggleautomaticpump_main():
    moisture_value = read_soil_moisture()
    print("Soil Moisture Value:", moisture_value)

    if moisture_value < 0.4:
        print("Vlaznost tla je niska, ukljucivanje pumpe...")
        control_pump(0)
        activepump=True
        time.sleep(5)  
        print("Iskljucivanje pumpe nakon 5 sekundi...")
        control_pump(1)  
    else:
        print("Vlaznost tla je dovoljno visoka, pumpa nije potrebna.")
        control_pump(1)  


# Combined main function
def pump_main():
    # Start both automatic and manual control in parallel
    import _thread

    # Start the manual pump control in a separate thread
    _thread.start_new_thread(togglepump_main, ())

    # Run the automatic pump control in the main thread
    toggleautomaticpump_main()

