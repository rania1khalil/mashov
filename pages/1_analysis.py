import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 ניתוח תחומים", layout="wide")
st.title("📊 ניתוח לפי תחומים")

if "uploaded_surveys" not in st.session_state:
    st.warning("🔁 אנא חזרי לדף הבית והעלי קבצים")
    st.stop()

uploaded_files = st.session_state["uploaded_surveys"]
st.write("קבצים שהועלו:", [f.name for f in uploaded_files])
