from machine import ADC, Pin
import time

soil_moisture_pin = ADC(Pin(26))

def read_soil_moisture():
    moisture_value = soil_moisture_pin.read_u16()  
    normalized = moisture_value / 65535
    normalized = 1 - normalized
    return normalized


