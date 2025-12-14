from typing import List, Optional
import streamlit as st

from services.api_service import get_agent_response


def generate_agent_response(
    prompt: str,
    num_results: int,
    similarity_threshold: float,
    documents_name: Optional[List[str]] = None,
) -> None:

    if st.session_state.messages[-1]["role"] == "assistant":
        return

    response_data, error = get_agent_response(
        prompt, num_results, similarity_threshold, documents_name
    )

    if response_data is None:
        answer = error
    else:
        answer = response_data.get("reply")

    st.session_state.messages.append({"role": "assistant", "content": f"{answer}"})

    st.session_state.is_processing_answer = False
    st.rerun()
