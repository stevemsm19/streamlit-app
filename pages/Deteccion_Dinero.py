import streamlit as st
from PIL import Image

from app.frontend.services.api_service import detect_cash, get_agent_response
from app.frontend.utils.messages import show_temporary_message

st.set_page_config(
    page_title="Detector de billetes",
    layout="wide",
)

st.title("🖼️ Detector de billetes")
st.write("Sube una imagen y presiona **Detectar** para que el sistema inicie la detección de billetes.")

st.sidebar.header("Cargar imagen")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

uploaded_file = st.sidebar.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg"],
)

st.sidebar.divider()
st.sidebar.header("Parámetros de detección")
st.sidebar.caption("Estos valores se pasan al detector para ajustar su comportamiento.")

conf = st.sidebar.slider(
    "Confianza mínima",
    min_value=0.1,
    max_value=1.0,
    value=0.8,
    step=0.05,
    help="Nivel mínimo de confianza para aceptar una detección",
)

max_det = st.sidebar.slider(
    "Máximo de detecciones",
    min_value=1,
    max_value=10,
    value=1,
    step=1,
    help="Número máximo de objetos a detectar en la imagen",
)

with st.sidebar.expander("Recomendaciones"):
    st.write(
        """
        - Tamaño máximo: 10MB
        - Formatos soportados: PNG, JPG, JPEG
        - Ajusta la confianza para tener detecciones más precisas
        """
    )

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Imagen adjunta")

    image = None
    if uploaded_file:
        if uploaded_file.size > MAX_FILE_SIZE:
            show_temporary_message(
                "La imagen supera el tamaño máximo permitido (10MB)",
                "error",
            )
        else:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
    else:
        st.info("👈 Sube una imagen desde el panel lateral")

with col2:
    st.subheader("Acciones")

    if uploaded_file:
        detectar = st.button("🔍 Detectar", use_container_width=True)

        if detectar:

            categories, error = detect_cash(
                images=[uploaded_file],
                conf=conf,
                max_det=max_det,
            )

            if error:
                show_temporary_message(error, "error")
            elif not categories:
                show_temporary_message(
                    "No se logró detectar ningún billete en la imagen. "
                    "Intenta con otra imagen o ajusta los parámetros. "
                    "Recuerda que el sistema solo detecta billetes colombianos.",
                    "error",
                    duration=6,
                )
            else:
                show_temporary_message(
                    "Detección completada correctamente",
                    "success",
                    duration=2,
                )

                response, error = get_agent_response(
                    prompt="Cuenta estos billetes", bills=categories
                )

                if error:
                    st.error(f"Error: {error}")
                else:
                    reply = response.get("reply", "No se recibió respuesta")
                    st.subheader("Resultados")
                    st.markdown(reply)
