import streamlit as st

from typing import cast


def get_user_prompt() -> str | None:
    st.session_state.is_processing_answer = False
    prompt_sources = ["selected_suggestion", "temp_user_input", "user_input"]

    for key in prompt_sources:
        value = st.session_state.get(key)
        if value:
            value = cast(str | None, st.session_state.get(key))
            st.session_state.is_processing_answer = True
            st.session_state[key] = None
            return value

    return None


def add_user_prompt(prompt: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
