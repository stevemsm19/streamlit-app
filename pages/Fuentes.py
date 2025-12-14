import os
import streamlit as st

from services.api_service import get_documents_name

current_page = "sources"
st.session_state.last_page = current_page

st.set_page_config(page_title="Fuentes", layout="wide")
st.title("📚 Fuentes")
st.write("Aquí puedes descargar los recursos utilizados por el sistema:")

BASE_PATH = os.path.join(os.getcwd(), "src", "data", "temp_files")

document_names, error = get_documents_name()

if error:
    st.error(error)
    st.stop()

if not document_names:
    st.info("No hay documentos disponibles para descargar.")
    st.stop()

for filename in document_names:
    file_path = os.path.join(BASE_PATH, filename)

    with st.container():
        st.html(
            f"""
            <div style="
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                background-color: #f8f9fa;
                border: 1px solid #ddd;
            ">
                <b>{filename}</b>
            </div>
            """
        )

        if not os.path.exists(file_path):
            st.warning(
                f"El archivo **{filename}** no está disponible para descarga."
            )
            continue

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        st.download_button(
            label="Descargar",
            data=file_bytes,
            file_name=filename,
            mime="application/pdf",
            icon=":material/download:",
        )
