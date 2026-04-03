import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from universal_agent import UniversalAIAgent

def test_text_chat():
    agent = UniversalAIAgent()
    out = agent.text_chat("Test message")
    assert isinstance(out, str)
    assert "Test" in out or "You said" in out

def test_translate():
    agent = UniversalAIAgent()
    out = agent.translate("Hello", "fr")
    assert isinstance(out, str)
    assert len(out) > 0

def test_detect_language():
    agent = UniversalAIAgent()
    assert agent.detect_language("Bonjour") == "fr"
    assert agent.detect_language("Hola") == "es"
    assert agent.detect_language("Hello") == "en"

def test_device_plugins():
    from device_plugins import send_sms
    from device_plugins_extra import read_temperature_sensor, trigger_emergency_alert
    from device_plugins_sensors import read_humidity_sensor, read_light_sensor
    from device_plugins_gps_camera import get_gps_location, capture_camera_image
    agent = UniversalAIAgent()
    agent.register_plugin("send_sms", send_sms)
    agent.register_plugin("read_temperature_sensor", read_temperature_sensor)
    agent.register_plugin("trigger_emergency_alert", trigger_emergency_alert)
    agent.register_plugin("read_humidity_sensor", read_humidity_sensor)
    agent.register_plugin("read_light_sensor", read_light_sensor)
    agent.register_plugin("get_gps_location", get_gps_location)
    agent.register_plugin("capture_camera_image", capture_camera_image)
    assert "SMS sent" in agent.call_local_function("send_sms", "+123", message="hi")
    assert "Temperature" in agent.call_local_function("read_temperature_sensor")
    assert "EMERGENCY ALERT" in agent.call_local_function("trigger_emergency_alert", "test")
    assert "Humidity" in agent.call_local_function("read_humidity_sensor")
    assert "Light" in agent.call_local_function("read_light_sensor")
    assert "GPS location" in agent.call_local_function("get_gps_location")
    assert "Camera image" in agent.call_local_function("capture_camera_image")
