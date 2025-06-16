import streamlit as st

# הגדרות עמוד עם תפריט קבוע
st.set_page_config(page_title="📊 מערכת הערכה", layout="wide")

# תפריט צד תמידי
with st.sidebar:
    st.title("📑 תפריט ניווט")
    page = st.radio("בחרי עמוד", [
        "📤 העלאת סקרים",
        "📊 ניתוח תחומים",
        "📈 גרפים",
        "🖨️ דוח להדפסה"
    ])

# ניווט לפי בחירה
if page == "📤 העלאת סקרים":
    st.title("📤 העלאת קבצי סקר")
    uploaded_files = st.file_uploader("בחרי עד 4 קבצים", type=["xlsx"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state["uploaded_surveys"] = uploaded_files
        st.success("✅ הקבצים הועלו בהצלחה!")

elif page == "📊 ניתוח תחומים":
    st.switch_page("pages/1_analysis.py")

elif page == "📈 גרפים":
    st.switch_page("pages/2_charts.py")

elif page == "🖨️ דוח להדפסה":
    st.switch_page("pages/3_report.py")
