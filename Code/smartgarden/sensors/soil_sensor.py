from machine import ADC, Pin
import time

# Set up the ADC (Analog to Digital Converter) on pin GP26 (ADC0)
soil_moisture_pin = ADC(Pin(26))

# Function to read the soil moisture level
def read_soil_moisture():
    moisture_value = soil_moisture_pin.read_u16()  # Read the raw analog value (0-65535)
    normalized = moisture_value / 65535
    normalized = 1 - normalized
    return normalized

# Main loop
while True:
    moisture_value = read_soil_moisture()
    print("Soil Moisture Value:", moisture_value)
    time.sleep(3)  # Delay for 3 seconds

