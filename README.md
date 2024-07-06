### [SmartGarden Pico Video](https://www.youtube.com/watch?v=-gpheuza-9c)

# Automatic Plant Watering System

This project involves creating an automatic plant watering system using a Raspberry Pi Pico. The system uses soil moisture sensors to detect when the soil is dry and activates a water pump to irrigate the plants as needed. Additional functionalities include manual watering, remote control and notifications via Wi-Fi, scheduling watering times, and displaying the last watering time and current system status. The automatic plant watering system is designed to optimize plant care by providing the right amount of water at the right time.


## Required Hardware Components
- 1 x Raspberry Pi Pico / PicoETF
- 1 x Soil moisture sensor (e.g., capacitive moisture sensor)
- 1 x Water pump (e.g., mini submersible pump)
- 1 x Relay module (for pump control)
- 1 x ILI9341 TFT LCD screen
- Power supply (USB cable for Pico, power supply for the pump)
- Water tubing
- Water reservoir (e.g., bottle)
- Breadboard and connecting wires
- DHT11 sensor for room humidity

## System Functionalities
### Automatic Watering
- The system automatically waters plants when the soil moisture sensor detects dryness. The pump activates when moisture readings drop below a set threshold, ensuring plants are watered only when necessary.

### Manual Watering Mode
- Users can manually activate the water pump via a button press or an app, allowing for additional watering as needed.

### Remote Control and Notifications
- Users can manage watering and monitor sensor readings remotely using mobile devices over a Wi-Fi connection, potentially utilizing the MQTT protocol.

### Scheduled Watering
- The system can be programmed to water plants at specific intervals, such as every morning or evening, beneficial for plants needing regular watering at certain times of the day.

### Display Last Watering Time & Current System Status
- The display shows the last watering time, current soil moisture levels, pump activity status, and other parameters.

### Weather Forecast API Integration
- Utilizing weather forecast APIs to predict rain and adjust watering schedules accordingly. For example, delaying watering if rain is forecasted.

### Additional Sensors
- Adding sensors for temperature, light, or UV radiation to provide comprehensive environmental condition insights.
