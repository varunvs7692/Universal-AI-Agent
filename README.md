# Universal AI Agent for Digital Equity & Global Resilience

**Empowering every community with offline, multimodal, multilingual AI for real-world impact.**

This repository contains the `universal_ai_agent` project, a local-first, multilingual, multimodal AI agent powered by Gemma-style models and designed to support underserved communities worldwide.

## Features
- Works fully offline on low-cost devices
- Supports voice, text, and image input/output
- Multilingual translation with automatic language detection
- Local function calling for SMS, GPS, camera, and environmental sensors
- Modular, extensible plugin-based architecture

## Project Layout
- `universal_ai_agent/src/universal_ai_agent/agent/` - runtime orchestration and public facade
- `universal_ai_agent/src/universal_ai_agent/plugins/` - plugin contracts, registry, loader, and built-ins
- `universal_ai_agent/src/universal_ai_agent/providers/` - model and device adapters
- `universal_ai_agent/tests/` - unit and smoke tests
- `universal_ai_agent/notebooks/` - demo scripts and experiments

## Quick Start
1. `cd universal_ai_agent`
2. `pip install -r requirements.txt`
3. `pytest`
4. `streamlit run src/universal_ai_agent/web/streamlit_app.py`

## Compatibility
Legacy imports such as `from universal_agent import UniversalAIAgent` still work through the compatibility shim in `universal_ai_agent/src/universal_agent.py`.

## Core Examples
```python
from universal_agent import UniversalAIAgent

agent = UniversalAIAgent()
print(agent.text_chat("How can AI help my community?"))
print(agent.detect_language("Hola, como estas?"))
print(agent.translate("Hola, como estas?", "en"))
print(agent.image_chat("sample_image.jpg", prompt="What is the person holding?"))
print(agent.call_local_function("get_gps_location"))
```

## Web UI
Run the Streamlit UI from inside `universal_ai_agent/`:

```bash
streamlit run src/universal_ai_agent/web/streamlit_app.py
```
