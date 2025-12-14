from typing import Optional
import streamlit as st

from app.frontend.features.chat.agent_response_handler import generate_agent_response
from app.frontend.features.chat.user_prompt_handler import add_user_prompt
from app.frontend.services.api_service import get_documents_name, upload_files
from app.frontend.utils.constants.chat_suggestions import CHAT_SUGGESTIONS


def display_chat_intro() -> None:
    with st.container():
        st.chat_input(
            "Escribe tu pregunta aquí...",
            key="temp_user_input",
            disabled=getattr(st.session_state, "is_processing_answer", False),
        )

        selected_suggestion: Optional[str] = st.pills(
            label="Preguntas sugeridas",
            label_visibility="collapsed",
            options=CHAT_SUGGESTIONS,
            key="selected_suggestion",
        )

    if selected_suggestion:
        st.session_state.selected_suggestion = selected_suggestion


def display_chat_history() -> None:
    for message in getattr(st.session_state, "messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_chat_flow(
    user_prompt: Optional[str],
    num_results: int,
    similarity_threshold: float,
) -> None:
    documents = st.session_state.get("documents")

    if not user_prompt and not getattr(st.session_state, "messages", []):
        display_chat_intro()
        st.stop()

    display_chat_history()

    st.chat_input(
        "Escribe tu pregunta aquí...",
        key="user_input",
        disabled=getattr(st.session_state, "is_processing_answer", False),
    )

    if user_prompt:
        add_user_prompt(user_prompt)

        documents_name = None

        if documents:
            documents_name = [doc.name for doc in documents]

            existing_names, error = get_documents_name()
            if error:
                st.error(error)
                return

            existing_names = existing_names or []

            new_documents = [doc for doc in documents if doc.name not in existing_names]

            if new_documents:
                _, error = upload_files(new_documents)
                if error:
                    st.error(error or "Error al cargar documentos")
                    return

        generate_agent_response(
            user_prompt,
            num_results,
            similarity_threshold,
            documents_name,
        )
