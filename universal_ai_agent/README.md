
# Universal AI Agent for Digital Equity & Global Resilience

**Empowering every community with offline, multimodal, multilingual AI for real-world impact.**


This project is a local-first, multilingual, multimodal AI agent powered by Gemma 4, designed to empower underserved communities worldwide.

## Features
- Works fully offline on low-cost devices (edge/phone/laptop)
- Supports voice, text, and image input/output
- Multilingual translation with automatic language detection
- Local function calling (e.g., SMS, GPS, camera, environmental sensors)
- Modular, extensible codebase

## Structure
- `src/` — Core agent code and modules
- `data/` — Example datasets and language resources
- `notebooks/` — Prototyping and experiments
- `outputs/` — Model outputs and logs
- `media/` — Images, audio, and demo files

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest`
3. Launch the web UI: `streamlit run src/universal_ai_agent/web/streamlit_app.py`
4. Explore and run example notebooks in `notebooks/`

## Modular Architecture
- `src/universal_ai_agent/agent/` - orchestration runtime and public facade
- `src/universal_ai_agent/plugins/` - plugin contracts, registry, loader, and built-ins
- `src/universal_ai_agent/core/` - shared config, logging, and context types
- `src/universal_ai_agent/providers/` - model and device adapters used by plugins
- `src/universal_agent.py` - compatibility shim for legacy imports
- `tests/` - unit and smoke tests for the modular architecture

## Compatibility
Existing imports such as `from universal_agent import UniversalAIAgent` still work. The class now delegates to a modular runtime with built-in capability plugins for text chat, voice chat, image handling, translation, text-to-speech, and device actions.

## Translation
The translation capability now uses a multilingual model path designed for 50+ languages and automatic source-language detection.

Example:
```python
from universal_agent import UniversalAIAgent

agent = UniversalAIAgent()
print(agent.detect_language("Hola, como estas?"))
print(agent.translate("Hola, como estas?", "en"))
```

## Image Q&A
The image capability now supports real vision inference through Hugging Face pipelines:
- Prompted image questions use a visual question answering model
- Promptless image calls fall back to image captioning

Example:
```python
from universal_agent import UniversalAIAgent

agent = UniversalAIAgent()
print(agent.image_chat("sample_image.jpg", prompt="What is the person holding?"))
print(agent.image_chat("sample_image.jpg"))
```


## Device Plugins
The agent supports modular device plugins for real-world integration. Example built-in plugins:

- `send_sms`: Simulate sending an SMS message
- `get_gps_location`: Simulate reading GPS coordinates
- `capture_image`: Simulate capturing an image from a device camera
- `read_environment`: Simulate reading environmental sensors
- `trigger_emergency_alert`: Simulate triggering an emergency alert

Example usage:
```python
agent.register_plugin("custom_status", lambda: "ok")

print(agent.call_local_function("send_sms", "+1234567890", message="Hello!"))
print(agent.call_local_function("get_gps_location"))
print(agent.call_local_function("capture_image"))
print(agent.call_local_function("read_environment"))
print(agent.call_local_function("trigger_emergency_alert", "This is a test!"))
print(agent.call_local_function("custom_status"))
```

## Web UI
A basic Streamlit interface is included for interactive use across text chat, image Q&A, translation, and device actions.

Run it with:
```bash
streamlit run src/universal_ai_agent/web/streamlit_app.py
```

## Next Steps
- Add your Gemma 4 model weights and configuration
- Extend agent capabilities (translation, Q&A, device integration)
- Build a demo for your target community

---
This project is designed for the Gemma 4 Good Hackathon. See the competition page for submission requirements and inspiration.
