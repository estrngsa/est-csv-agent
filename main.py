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
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() in ("1", "true", "yes")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def t(key):
    lang = "pt" if not st.session_state.get("lang", False) else "en"
    try:
        return translation(key, lang)
    except:
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

if "csv_data" not in st.session_state:
    raw = load_csvs_from_folder()
    st.session_state.csv_data = mount_nfe(raw) if raw != "ERROR" else "ERROR"
if st.session_state.csv_data == "ERROR":
    st.error(t("error_csv"))
    st.stop()

if "csv_meta" not in st.session_state:
    raw_meta = load_csvs_from_folder()
    st.session_state.csv_meta = (
        build_metadata(raw_meta) if raw_meta != "ERROR" else "ERROR"
    )

if "vectordb" not in st.session_state:
    raw_meta = load_csvs_from_folder()
    st.session_state.vectordb = (
        build_vector_index(raw_meta) if raw_meta != "ERROR" else "ERROR"
    )

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])

st.write("Perguntas comuns:")
col1, col2 = st.columns(2)

if col1.button(t("common_question_quantity")):
    user_query = t("common_question_quantity")
elif col2.button(t("common_question_supplier")):
    user_query = t("common_question_supplier")
else:
    user_query = None

if not user_query:
    user_query = st.chat_input(t("input_label"))

if user_query:
    st.session_state.history.append({"role": "user", "content": user_query})
    ql = user_query.lower()

    if t("quantity") in ql:
        info = get_max_item_info(st.session_state.csv_data)
        reply = (
            format_summary(info, OPENAI_API_KEY, lang="pt", query=user_query)
            if info
            else t("error_no_item_found")
        )

    elif t("amount") in ql:
        info = get_max_head_info(st.session_state.csv_data)
        reply = (
            format_summary(info, OPENAI_API_KEY, lang="pt", query=user_query)
            if info
            else t("error_no_supplier_found")
        )

    else:
        docs = query_vector_index(st.session_state.vectordb, user_query, k=5)
        reply = (
            ask_agent(
                user_query,
                docs,
                st.session_state.csv_meta,
                OPENAI_API_KEY,
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
