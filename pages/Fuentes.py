import streamlit as st

from services.api_service import get_documents_name
from config.settings import settings

setting = settings()

current_page = "sources"
st.session_state.last_page = current_page

st.set_page_config(page_title="Fuentes", layout="wide")
st.title("📚 Fuentes")
st.write("Aquí puedes descargar los recursos utilizados por el sistema:")

DOWNLOAD_BASE_URL = (
    f"https://{settings.api_host}/api/v1/documents/download"
)

documents_name, error = get_documents_name()

if error:
    st.error(error)
    st.stop()

if not documents_name:
    st.info("No hay documentos disponibles para descargar.")
    st.stop()

for filename in documents_name:
    with st.container():
        st.html(
            f"""
            <div style="
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <b>{filename}</b>
            </div>
            """
        )

        st.link_button(
            label="Descargar",
            url=f"{DOWNLOAD_BASE_URL}/{filename}",
            icon=":material/download:",
        )
