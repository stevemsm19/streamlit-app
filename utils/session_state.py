import streamlit as st
from typing import Any, Callable, Dict, Optional, Union


def apply_session_states(defaults: Dict[str, Any]) -> None:
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def handle_page_change(
    current_page: Union[str, int],
    reset_fn: Optional[Callable[[], None]] = None,
) -> None:
    if st.session_state.get("last_page") != current_page:
        if reset_fn:
            reset_fn()
        st.session_state["last_page"] = current_page
