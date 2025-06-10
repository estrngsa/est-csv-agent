import streamlit as st
from csv_handler import load_csvs_from_folder, build_metadata
from agent import ask_agent
from dotenv import load_dotenv
from utils import t as translation
import os
import time

load_dotenv()

if "lang" not in st.session_state:
    st.session_state.lang = "pt"

lang = st.radio("🌐 Language / Idioma", options=["🇧🇷 pt", "🇺🇸 en"], horizontal=True)
st.session_state.lang = "pt" if lang.startswith("🇧🇷") else "en"
st.session_state.csv_metadata = {}


def t(key):
    return translation(key, lang=st.session_state.lang)


st.title(t("title"))
query = st.text_input(t("input_label"))

if "csv_data" not in st.session_state:
    st.session_state.csv_data = load_csvs_from_folder()
    if st.session_state.csv_data == "ERROR":
        st.error(t("error_csv"))

if query:
    if st.session_state.csv_data != "ERROR":
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            st.error(t("error_key"))
        else:
            response = ask_agent(
                query,
                st.session_state.csv_data,
                build_metadata(st.session_state.csv_data),
                api_key,
            )
            placeholder = st.empty()
            displayed = ""
            for c in response:
                displayed += c
                placeholder.markdown(f"**{t('response_label')}** {displayed}")
                time.sleep(0.02)
            placeholder.markdown(f"**{t('response_label')}** {response}")
    else:
        st.error(t("error_generic"))
