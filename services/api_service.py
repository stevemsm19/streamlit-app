import time
import requests
import streamlit as st

from streamlit.runtime.uploaded_file_manager import UploadedFile

from typing import List, Optional, Tuple, Dict, Any

from utils.constants.endpoints import (
    DOCUMENTS_ENDPOINT,
    EMBEDDING_ENDPOINT,
    PREDICT_CASH_ENDPOINT,
    SEARCH_ENDPOINT,
    get_documents_name_ENDPOINT,
)

from config.settings import get_settings

SETTINGS = get_settings()
base_url = f"http://{SETTINGS.api_host}:{SETTINGS.api_port}/api/v1/"


def upload_files(
    documents: Optional[List[UploadedFile]],
) -> Tuple[Optional[str], Optional[str]]:
    if not documents:
        return None, "No hay documentos"

    with st.spinner("Cargando documento(s)...", show_time=True):
        file_payload = [("files", (doc.name, doc, doc.type)) for doc in documents]

        try:
            response = requests.post(
                f"{base_url}{DOCUMENTS_ENDPOINT}",
                files=file_payload,
            )
            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"

            response_json = response.json()
            total_pages = response_json.get("total_pages")
            total_chunks = response_json.get("total_chunks")
            total_documents = len(documents)

            return (
                f"Se han cargado {total_documents} documentos, con un total de {total_pages} páginas "
                f"divididas en {total_chunks} chunks.",
                None,
            )

        except requests.exceptions.RequestException:
            return None, "Error de conexión"


def get_agent_response(
    prompt: str,
    num_results: int = 9,
    similarity_threshold: float = 0.5,
    documents_name: Optional[List[str]] = None,
    bills: Optional[List[str]] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    payload = {
        "query": prompt,
        "num_results": num_results,
        "similarity_threshold": similarity_threshold,
    }

    if documents_name is not None:
        payload["documents_name"] = documents_name

    if bills is not None:
        payload["bills"] = bills

    with st.spinner("Pensando...", show_time=True):
        try:
            response = requests.post(url=f"{base_url}{SEARCH_ENDPOINT}", json=payload)

            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"

            return response.json(), None

        except requests.exceptions.Timeout:
            return None, "Error: Tiempo de espera agotado"
        except requests.exceptions.ConnectionError:
            return None, "Error: No se pudo conectar con el servidor"
        except requests.exceptions.RequestException as e:
            return None, f"Error de conexión: {str(e)}"


def get_embeddings() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.get(
            url=f"{base_url}{EMBEDDING_ENDPOINT}",
        )

        if response.status_code != 200:
            return None, f"Error {response.status_code}: {response.text}"

        return response.json(), None

    except requests.exceptions.RequestException:
        return None, "Error de conexión"


def get_documents_name() -> Tuple[Optional[List[str]], Optional[str]]:
    with st.spinner("Analizando documento(s)...", show_time=True):
        try:
            response = requests.get(
                url=f"{base_url}{get_documents_name_ENDPOINT}",
            )

            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"

            data = response.json()
            return data.get("names", []), None

        except requests.exceptions.RequestException:
            return None, "Error de conexión"


def detect_cash(
    images: List[UploadedFile],
    conf: float,
    max_det: int,
) -> Tuple[Optional[List[str]], Optional[str]]:
    if not images:
        return None, "No se enviaron imágenes"

    files_payload = [("files", (img.name, img.getvalue(), img.type)) for img in images]

    data_payload = {
        "conf": conf,
        "max_det": max_det,
    }

    with st.spinner("Detectando...", show_time=True):
        try:
            response = requests.post(
                f"{base_url}{PREDICT_CASH_ENDPOINT}",
                files=files_payload,
                data=data_payload,
            )

            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"

            response_json = response.json()

            categories: List[str] = []
            for item in response_json:
                for det in item.get("detections", []):
                    category = det.get("category_name")
                    categories.append(category)

            return categories, None

        except requests.exceptions.RequestException:
            return None, "Error de conexión con el servicio de detección"
