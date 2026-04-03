import random

def read_air_quality_sensor():
    # Simulate reading an air quality sensor (AQI)
    aqi = random.randint(0, 200)
    print(f"[Device] Air Quality Index: {aqi}")
    return f"Air Quality Index: {aqi} (0=Good, 200=Very Unhealthy)"

def read_step_counter():
    # Simulate reading a step counter
    steps = random.randint(0, 20000)
    print(f"[Device] Steps counted: {steps}")
    return f"Steps counted: {steps}"
