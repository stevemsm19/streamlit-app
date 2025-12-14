import streamlit as st

current_page = "about_project"
st.session_state.last_page = current_page

st.set_page_config(page_title="Información", layout="wide")
st.title("ℹ️ Información")

st.html(
    """
    <div style="background-color: #cce6f4; padding: 15px; border-left: 6px solid #133c55; border-radius: 5px;">
        Puedes hacer preguntas sobre <em>conceptos básicos de finanzas</em>, como:<br><br>
        • Definiciones financieras esenciales (ahorro, interés, crédito, etc.)<br>
        • Tipos de productos financieros comunes<br>
        • Conceptos generales sobre manejo del dinero<br><br>
        También puedes subir <strong>tus propios documentos</strong> (PDF o TXT), y nuestro bot te ayudará a responder preguntas basadas únicamente en la información contenida en ellos.
    </div>
    """
)
