import streamlit as st
import time


def show_temporary_message(content: str, message_type: str, duration: int = 4) -> None:
    msg = st.empty()
    if message_type == "success":
        msg.success(content, icon="✅")
    elif message_type == "error":
        msg.error(content, icon="❌")
    else:
        msg.write(content)
    time.sleep(duration)
    msg.empty()
