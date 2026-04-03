from __future__ import annotations

import streamlit as st

from universal_ai_agent import UniversalAIAgent


@st.cache_resource
def get_agent() -> UniversalAIAgent:
    return UniversalAIAgent()


def main() -> None:
    st.set_page_config(page_title="Universal AI Agent", layout="wide")
    st.title("Universal AI Agent")
    st.caption("Local-first multimodal assistant for text, image, translation, and device workflows.")

    agent = get_agent()
    tab_chat, tab_image, tab_translate, tab_device = st.tabs(
        ["Text", "Image Q&A", "Translation", "Device Actions"]
    )

    with tab_chat:
        prompt = st.text_area("Ask a question", value="How can AI help my community?")
        if st.button("Generate reply", key="text_submit"):
            st.write(agent.text_chat(prompt))

    with tab_image:
        uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="image_uploader")
        image_prompt = st.text_input("Optional image question", value="What is in this image?")
        if uploaded is not None:
            temp_path = st.session_state.get("uploaded_image_path", "uploaded_image.jpg")
            with open(temp_path, "wb") as temp_file:
                temp_file.write(uploaded.getbuffer())
            st.image(uploaded, caption="Uploaded image", use_container_width=True)
            if st.button("Analyze image", key="image_submit"):
                prompt = image_prompt.strip() or None
                st.write(agent.image_chat(temp_path, prompt=prompt))

    with tab_translate:
        source_text = st.text_area("Text to translate", value="Hello from the Universal AI Agent")
        target_language = st.text_input("Target language", value="fr")
        if st.button("Detect language", key="detect_submit"):
            st.write(f"Detected language: {agent.detect_language(source_text)}")
        if st.button("Translate", key="translate_submit"):
            st.write(agent.translate(source_text, target_language))

    with tab_device:
        st.write("Available device actions:")
        st.write(agent.list_device_plugins())
        selected_action = st.selectbox("Action", agent.list_device_plugins())
        action_arg = st.text_input("Optional argument", value="")
        if st.button("Run device action", key="device_submit"):
            if selected_action == "send_sms":
                st.write(agent.call_local_function("send_sms", "+1234567890", message=action_arg or "Test message"))
            elif selected_action == "trigger_emergency_alert":
                st.write(agent.call_local_function(selected_action, action_arg or "Test alert"))
            elif selected_action == "read_environment":
                st.write(agent.call_local_function(selected_action, action_arg or "all"))
            elif action_arg:
                st.write(agent.call_local_function(selected_action, action_arg))
            else:
                st.write(agent.call_local_function(selected_action))


if __name__ == "__main__":
    main()
