import random

def read_temperature_sensor():
    # Simulate reading a temperature sensor
    temp = round(20 + 10 * random.random(), 2)
    print(f"[Device] Temperature sensor reading: {temp}°C")
    return f"Temperature: {temp}°C"

def trigger_emergency_alert(message):
    # Simulate triggering an emergency alert
    print(f"[Device] EMERGENCY ALERT: {message}")
    return f"EMERGENCY ALERT triggered: {message}"
