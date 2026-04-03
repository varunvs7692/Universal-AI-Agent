import sys
sys.path.append('../src')

from universal_agent import UniversalAIAgent
from device_plugins import send_sms
from device_plugins_extra import read_temperature_sensor, trigger_emergency_alert
from device_plugins_sensors import read_humidity_sensor, read_light_sensor

# Demo: Universal AI Agent core features

agent = UniversalAIAgent(language='en')
agent.register_plugin("send_sms", send_sms)
agent.register_plugin("read_temperature_sensor", read_temperature_sensor)
agent.register_plugin("trigger_emergency_alert", trigger_emergency_alert)
agent.register_plugin("read_humidity_sensor", read_humidity_sensor)
agent.register_plugin("read_light_sensor", read_light_sensor)

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
