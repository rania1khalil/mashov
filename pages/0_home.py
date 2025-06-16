import streamlit as st

st.set_page_config(page_title="📊 מערכת הערכה", layout="wide")
st.title("📊 מערכת הערכה - דף הבית")

st.markdown('''
מערכת זו מאפשרת העלאת עד 4 קבצי סקר וניתוח תחומים.
''')

uploaded_files = st.file_uploader("📤 העלאת קבצי סקר (Excel)", type=["xlsx"], accept_multiple_files=True)
if uploaded_files:
    st.session_state["uploaded_surveys"] = uploaded_files
    st.success("✅ הקבצים נטענו בהצלחה! השתמשי בתפריט לניתוח.")
else:
    st.info("⬆️ העלי קבצים כדי להתחיל.")
