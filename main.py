import streamlit as st
from dotenv import load_dotenv
import os
import time

from csv_handler import load_csvs_from_folder, build_metadata, mount_nfe
from vector_store import build_vector_index, query_vector_index
from agent import ask_agent, format_summary
from utils import t as translation
from actions import get_max_item_info, get_max_head_info

load_dotenv()


# --- Função de tradução local
def t(key):
    lang = "en" if st.session_state.get("lang", False) else "pt"
    # Try to translate, fallback to key if not found
    try:
        return translation(key, lang)
    except Exception:
        return key


# --- Header e toggle de idioma
st.toggle("Language", key="lang", value=st.session_state.get("lang", False))
st.title(t("title"))

# --- Botões com perguntas comuns
col1, col2 = st.columns(2)
pressed_item = col1.button("Qual item teve maior volume entregue (em quantidade)?")
pressed_supl = col2.button("Qual é o fornecedor que teve maior montante recebido?")

# --- Caixa de texto padrão
query = ""
if pressed_item:
    query = "Qual item teve maior volume entregue (em quantidade)?"
elif pressed_supl:
    query = "Qual é o fornecedor que teve maior montante recebido?"
else:
    query = st.text_input(t("input_label"), placeholder=t("input_label"))

# --- Carregamento e montagem dos dados
if "csv_data" not in st.session_state:
    raw = load_csvs_from_folder()
    st.session_state.csv_data = "ERROR" if raw == "ERROR" else mount_nfe(raw)

if st.session_state.csv_data == "ERROR":
    st.error(t("error_csv"))
    st.stop()

# --- Metadados e vetor store
if "csv_meta" not in st.session_state:
    raw_meta = load_csvs_from_folder()
    if raw_meta == "ERROR":
        st.session_state.csv_meta = "ERROR"
    else:
        st.session_state.csv_meta = build_metadata(raw_meta)

if "vectordb" not in st.session_state:
    raw_meta = load_csvs_from_folder()
    if raw_meta == "ERROR":
        st.session_state.vectordb = "ERROR"
    else:
        st.session_state.vectordb = build_vector_index(raw_meta)


# --- Processamento da query
if query:
    ql = query.lower()
    if "maior volume" in query.lower():
        info = get_max_item_info(st.session_state.csv_data)

        if info is not None:
            text = format_summary(
                summary=info,
                api_key=os.getenv("OPENAI_API_KEY") or "",
                lang="pt",
                query=query,
            )
            st.markdown(text)
        else:
            st.error(t("error_no_item_found"))

    elif "maior montante" in query.lower():
        info = get_max_head_info(st.session_state.csv_data)

        if info is not None:
            text = format_summary(
                summary=info,
                api_key=os.getenv("OPENAI_API_KEY") or "",
                lang="pt",
                query=query,
            )
            st.markdown(text)
        else:
            st.error(t("error_no_supplier_found"))

    else:
        docs = query_vector_index(st.session_state.vectordb, query, k=5)
        api_key = os.getenv("OPENAI_API_KEY", "")
        if st.session_state.csv_meta == "ERROR":
            st.error(t("error_csv"))
        else:
            response = ask_agent(query, docs, st.session_state.csv_meta, api_key)
            placeholder = st.empty()
            display = ""
            for c in response:
                display += c
                placeholder.markdown(f"**{t('response_label')}** {display}▌")
                time.sleep(0.02)
            placeholder.markdown(f"**{t('response_label')}** {response}")
