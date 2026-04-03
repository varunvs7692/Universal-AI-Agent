import random

def read_humidity_sensor():
    # Simulate reading a humidity sensor
    humidity = round(40 + 30 * random.random(), 2)
    print(f"[Device] Humidity sensor reading: {humidity}%")
    return f"Humidity: {humidity}%"

def read_light_sensor():
    # Simulate reading a light sensor
    light = round(100 + 900 * random.random(), 2)
    print(f"[Device] Light sensor reading: {light} lux")
    return f"Light: {light} lux"
