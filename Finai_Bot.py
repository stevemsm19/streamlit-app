from typing import Optional
import streamlit as st


from features.chat.chat_sidebar import handle_sidebar
from features.chat.chat_state import init_chat_state
from features.chat.user_prompt_handler import get_user_prompt
from features.chat.chat_handler import handle_chat_flow
from utils.session_state import apply_session_states


def init_view_state() -> None:
    defaults = {
        "last_page": None,
    }
    apply_session_states(defaults)


def setup_app() -> None:
    st.set_page_config("Finai Bot", layout="wide")
    st.title("Finai Bot 💬")
    st.write("Haz tus preguntas relacionadas a finanzas y recibe respuestas basadas en nuestros documentos y recursos. " \
    "Si lo deseas, también puedes subir tus propios documentos en 'Cargar Documentos'.")

    init_chat_state()
    init_view_state()

    current_page: str = "chat_bot"
    st.session_state.last_page = current_page


def main() -> None:
    setup_app()

    user_prompt: Optional[str] = get_user_prompt()
    num_results, similarity_threshold = handle_sidebar()

    handle_chat_flow(user_prompt, num_results, similarity_threshold)


if __name__ == "__main__":
    main()
