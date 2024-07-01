from machine import ADC, Pin
import time
from Sensors.soil_sensor import read_soil_moisture

# podesiti na pin koji koristimo u implementaciji
relay_pin = Pin(15, Pin.OUT)


# Funkcija kontrolise rad pumpe
def control_pump(state):
    if state:
        relay_pin.value(1)  # Turn on the pump
        print("Pumpa je aktivna")
    else:
        relay_pin.value(0)  # Turn off the pump
        print("Pumpa nije aktivna")


# Main loop
while True:
    moisture_value = read_soil_moisture()
    print("Soil Moisture Value:", moisture_value)

    # Da li je vlaznost zemljista manja od thresholda?
    if moisture_value < 0.4:
        control_pump(True)  # upali pumpu
        time.sleep(5)  # pumpa je aktivna 5 sekundi / potrebno podesiti
        control_pump(False)  # ugasimo pumpu
    else:
        control_pump(False)  # osiguravamo da pumpa nije aktivna kada nije potrebno

    time.sleep(600)  # Sacekaj 10 min do sljedeceg mjerenja
