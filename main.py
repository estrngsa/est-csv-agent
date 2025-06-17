import streamlit as st
from dotenv import load_dotenv
import os
import time

from csv_handler import load_csvs_from_folder, build_metadata2, mount_nfe
from vector_store import build_vector_index, query_vector_index
from agent import CsvAgent
from utils import t as translation, extract_archive, save_to_temp
from actions import get_max_item_info, get_max_head_info

load_dotenv()
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() in ("1", "true", "yes")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CHROMA_KEY = os.getenv("CHROMA_KEY", 5)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.1))


def t(key):
    lang = "pt" if not st.session_state.get("lang", False) else "en"
    try:
        return translation(key, lang)
    except Exception:
        return key


st.write(t("language"))
lang_label = "🇧🇷 Português" if not st.session_state.get("lang", False) else "🇺🇸 English"
st.toggle(lang_label, key="lang", value=st.session_state.get("lang", False))
st.title(t("title"))

if not USE_OPENAI:
    st.markdown(
        "<div style='border:2px solid #f39c12; border-radius:8px; padding:1em; background:#fffbe6; color:#b9770e; text-align:center; font-weight:bold;'>"
        "Demo mode is not activated, please request the activation."
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

uploaded = st.session_state.get("uploaded", False)
raw = "ERROR"

if not uploaded:
    uploaded = st.file_uploader(
        t("upload_label"), type=["zip", "tar", "tar.gz"], disabled=uploaded
    )

if uploaded and (
    "csv_data" not in st.session_state
    or "csv_meta" not in st.session_state
    or "vectordb" not in st.session_state
    or "agent" not in st.session_state
):
    filepath = save_to_temp(uploaded)
    csv_folder = extract_archive(filepath)
    raw = load_csvs_from_folder(csv_folder)

    if raw != "ERROR":
        with st.spinner(t("loading_embeddings")):
            st.session_state.csv_data = mount_nfe(raw)
            st.session_state.csv_meta = build_metadata2(st.session_state.csv_data)
            st.session_state.vectordb = build_vector_index(st.session_state.csv_data)
            st.session_state.agent = CsvAgent(OPENAI_API_KEY, MODEL, TEMPERATURE)

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])

if uploaded and "csv_data" in st.session_state and "vectordb" in st.session_state:
    st.write(t("common"))
    col1, col2 = st.columns(2)

    if col1.button(t("common_question_quantity")):
        user_query = t("common_question_quantity")
    elif col2.button(t("common_question_supplier")):
        user_query = t("common_question_supplier")
    else:
        user_query = None

    if not user_query:
        user_query = st.chat_input(t("input_label"))
else:
    user_query = None

if user_query and uploaded:
    st.session_state.history.append({"role": "user", "content": user_query})
    ql = user_query.lower()

    if t("quantity") in ql:
        info = get_max_item_info(st.session_state.csv_data)
        reply = (
            st.session_state.agent.format_summary(info, lang="pt", query=user_query)
            if info
            else t("error_no_item_found")
        )

    elif t("amount") in ql:
        info = get_max_head_info(st.session_state.csv_data)
        reply = (
            st.session_state.agent.format_summary(info, lang="pt", query=user_query)
            if info
            else t("error_no_supplier_found")
        )

    else:
        docs = query_vector_index(
            st.session_state.vectordb, user_query, k=int(CHROMA_KEY)
        )
        print(f"Found {len(docs)} relevant documents.")
        reply = (
            st.session_state.agent.ask(
                user_query,
                docs,
                st.session_state.csv_meta,
            )
            if st.session_state.csv_meta != "ERROR"
            else t("error_csv")
        )

    assistant_msg = {"role": "assistant", "content": ""}
    st.session_state.history.append(assistant_msg)

    placeholder = st.empty()
    display = ""

    for c in reply:
        display += c
        placeholder.markdown(display + "▌")
        assistant_msg["content"] = display
        time.sleep(0.02)
    placeholder.markdown(display)
    assistant_msg["content"] = display

    st.rerun()

st.markdown("---")
if len(st.session_state.history) > 0:
    if st.button(t("clear_history")):
        st.session_state.history = []
        st.rerun()
