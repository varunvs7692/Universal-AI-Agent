import random

def get_gps_location():
    # Simulate getting GPS coordinates
    lat = round(37.7749 + random.uniform(-0.01, 0.01), 6)
    lon = round(-122.4194 + random.uniform(-0.01, 0.01), 6)
    print(f"[Device] GPS location: ({lat}, {lon})")
    return f"GPS location: ({lat}, {lon})"

def capture_camera_image():
    # Simulate capturing an image from a camera
    print("[Device] Camera image captured (simulated)")
    return "Camera image captured (simulated)"
