import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from universal_agent import UniversalAIAgent
from device_plugins import send_sms
from device_plugins_extra import read_temperature_sensor, trigger_emergency_alert
from device_plugins_sensors import read_humidity_sensor, read_light_sensor
from device_plugins_gps_camera import get_gps_location, capture_camera_image
from device_plugins_health import read_air_quality_sensor, read_step_counter
from utils_history_export import ConversationHistory, export_device_readings_to_csv

# Demo: Universal AI Agent core features

agent = UniversalAIAgent(language='en')
agent.register_plugin("send_sms", send_sms)
agent.register_plugin("read_temperature_sensor", read_temperature_sensor)
agent.register_plugin("trigger_emergency_alert", trigger_emergency_alert)
agent.register_plugin("read_humidity_sensor", read_humidity_sensor)
agent.register_plugin("read_light_sensor", read_light_sensor)
agent.register_plugin("get_gps_location", get_gps_location)
agent.register_plugin("capture_camera_image", capture_camera_image)
agent.register_plugin("read_air_quality_sensor", read_air_quality_sensor)
agent.register_plugin("read_step_counter", read_step_counter)

# Text chat
print(agent.text_chat("How can I help my community with AI?"))

# Voice chat (simulate with file path)
print(agent.voice_chat("sample_audio.wav"))

# Image chat (ask a question about an image)
print(agent.image_chat("sample_image.jpg", prompt="What do you see in this image?"))

# Image chat without a prompt falls back to image captioning
print(agent.image_chat("sample_image.jpg"))

# Translation
print(agent.translate("Welcome to the future!", "fr"))

# Local function call (simulate SMS)
print(agent.call_local_function("send_sms", "+1234567890", message="Hello from Universal AI Agent!"))
# Local function call (simulate temperature sensor)
print(agent.call_local_function("read_temperature_sensor"))
# Local function call (simulate emergency alert)
print(agent.call_local_function("trigger_emergency_alert", "This is a test emergency!"))
# Local function call (simulate humidity sensor)
print(agent.call_local_function("read_humidity_sensor"))
# Local function call (simulate light sensor)
print(agent.call_local_function("read_light_sensor"))
# Local function call (simulate GPS location)
print(agent.call_local_function("get_gps_location"))
# Local function call (simulate camera image capture)
print(agent.call_local_function("capture_camera_image"))
# Local function call (simulate air quality sensor)
print(agent.call_local_function("read_air_quality_sensor"))
# Local function call (simulate step counter)
print(agent.call_local_function("read_step_counter"))

# Example usage for conversation history
history = ConversationHistory()
user_msg = "How is the air quality?"
agent_msg = agent.call_local_function("read_air_quality_sensor")
history.add(user_msg, agent_msg)
print("\nConversation history:\n", history)
# Save and load history
history.save("conversation_history.csv")
history.load("conversation_history.csv")

# Example usage for device readings export
import time
readings = []
for device in ["read_air_quality_sensor", "read_step_counter"]:
    value = agent.call_local_function(device)
    readings.append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "device": device, "value": value})
export_device_readings_to_csv(readings, "device_readings.csv")
print("Device readings exported to device_readings.csv")
