import utime
import machine
from smartgarden.tftdisplay import display_soil_moisture, display_current_time
from smartgarden.soil_sensor import read_soil_moisture

# Set up display and other configurations (setup_display() function if needed)

# Example of displaying time and soil moisture
font = tt24
while True:
    moisture_value = read_soil_moisture()
    print("Moisture value:", moisture_value)  # Dijagnostički ispis, možete ga izbrisati nakon provjere
    display_soil_moisture(moisture_value)
    display_current_time()
    utime.sleep(3)  # Prilagodite pauzu prema potrebi vaše aplikacije

