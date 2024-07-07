from machine import Pin, Timer
import time
import utime
from smartgarden.soil_sensor import read_soil_moisture
from smartgarden.main import get_weather


pump_pin = Pin(27, Pin.OUT)
taster = Pin(0, Pin.IN, Pin.PULL_UP)
pump_on = False
last_pump_timestamp = utime.localtime()
debounce_timer = Timer()
debounce_delay = 2000 
activepump=False
last_interrupt_time = 0
taster.irq(trigger=Pin.IRQ_RISING,handler=togglepump_main)
openweather_api_key = "bae091179466b890b842f5a4dd85ac83"
units = "metric"


#Mainly used to see automatic pump
def control_pump(state):
    pump_pin.value(state)
    if state == 0:
        print("Pump is active")
    else:
        print("Pumpa is not active")

#Record the time when the pump was last on
def record_last_pump_on():
    global last_pump_timestamp
    last_pump_timestamp = utime.localtime()

#Return the last pump timestamp
def get_last_pump_on():
    return last_pump_timestamp

#Return the pump value (Check if the Manual irrigation is on)
def get_pump_on():
    return pump_on

#Get automatic pump value (Check if the Automatic irrigation is on)
def get_activepump():
    return activepump

def toggle_pump(pin):
    global pump_on
    pump_on = not pump_on
    control_pump(pump_on)
    if pump_on:
        print("Pump is OFF")
    else:
        print("Pump is ON")
        record_last_pump_on()

#Manual activation mode
def togglepump_main(p):
    global last_interrupt_time
    current_time = time.ticks_ms()

    # Debouncing 
    if time.ticks_diff(current_time, last_interrupt_time) < debounce_delay:
        return

    # Update the last interrupt time
    last_interrupt_time = current_time
    print("Manual pump")
    current_taster_value = taster.value()
    print("Taster value:", current_taster_value)
    toggle_pump(taster.value())
    time.sleep(1)
    
#Automatic activation mode
def toggleautomaticpump_main():
    moisture_value = read_soil_moisture()
    weather_data = get_weather('sarajevo', openweather_api_key, units=units)
    weather = weather_data["weather"][0]["main"]

    print("Soil Moisture Value:", moisture_value)

    if moisture_value < 0.4 and str(weather)!='rainy' and str(weather)!='Rainy':
        print("Vlaznost tla je niska, ukljucivanje pumpe...")
        control_pump(0)
        activepump=True
        time.sleep(5)  
        print("Iskljucivanje pumpe nakon 5 sekundi...")
        control_pump(1)  
    else:
        print("Vlaznost tla je dovoljno visoka, pumpa nije potrebna.")
        control_pump(1)  

def pump_main():
    # Start both automatic and manual control in parallel
    import _thread

    # Start the manual pump control in a separate thread
    _thread.start_new_thread(togglepump_main, ())

    # Run the automatic pump control in the main thread
    toggleautomaticpump_main()
