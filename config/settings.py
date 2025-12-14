import streamlit as st


class Settings:
    api_host: str = st.secrets["API_HOST"]
    api_port: int = st.secrets["API_PORT"]


def get_settings():
    return Settings()
