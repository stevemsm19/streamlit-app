import streamlit as st


class Settings:
    api_host: str = st.secrets["API_HOST"]


def get_settings():
    return Settings()
