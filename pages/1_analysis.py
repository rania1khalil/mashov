import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.utils import column_index_from_string

st.set_page_config(page_title="📈 גרפים לפי תחום", layout="wide")

st.title("📈 גרפים ויזואליים לפי תחומים")

if "uploaded_surveys" not in st.session_state:
    st.warning("🔁 אנא חזרי לדף הבית והעלי לפחות קובץ אחד לניתוח.")
    st.stop()

uploaded_files = st.session_state["uploaded_surveys"]

survey_data = {}

# קריאת קבצים ללא כותרות
for file in uploaded_files:
    try:
        df = pd.read_excel(file, header=None)
        survey_data[file.name] = df
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ {file.name}: {e}")

# מיפוי התחומים לעמודות באותיות
domains = {
    "רלוונטיות הקורס והתאמה לצרכים": {
        "סקר מסכם": ['AF','AJ','BB','AL','AM','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY'],
        "סקר סביבה": ['R','X','Y'],
        "סקר טלפוני": ['E']
    },
    "איכות סביבת הלמידה": {
        "סקר מסכם": ['AV','AW','AX','AG'],
        "סקר סביבה": ['G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB']
    },
    "יישום בפועל והשפעה על עבודת המורה": {
        "סקר מסכם": ['BJ','AM','AN','AO','BE'],
        "סקר אמצע": ['B','C','E','F'],
        "סקר טלפוני": ['F','L'],
        "סקר סביבה": ['Z']
    },
    "איכות ההנחייה": {
        "סקר מסכם": ['BC','AW','AV'],
        "סקר אמצע": ['G','H','I'],
        "סקר טלפוני": ['G'],
        "סקר סביבה": ['AA']
    },
    "שביעות רצון כללית": {
        "סקר מסכם": ['BH','BI','AF','AO'],
        "סקר אמצע": ['L']
    },
    "למידת עמיתים": {
        "סקר מסכם": ['AZ','BA','AY','AX','BD'],
        "סקר אמצע": ['D'],
        "סקר טלפוני": ['I','J'],
        "סקר סביבה": ['V','W','AB']
    },
    "חדשנות טכנולוגית ובינה מלאכותית": {
        "סקר מסכם": ['AR','AS','AT','AU','AL'],
        "סקר אמצע": ['J'],
        "סקר סביבה": ['T']
    }
}

# יצירת גרפים
chart_data = {}
for domain, surveys in domains.items():
    domain_scores = []
    for survey_name, columns in surveys.items():
        matching_file = next((f for f in survey_data if survey_name in f), None)
        if matching_file:
            df = survey_data[matching_file]
            try:
                col_indexes = [column_index_from_string(col) - 1 for col in columns if column_index_from_string(col) <= df.shape[1]]
                df_numeric = df.iloc[:, col_indexes].apply(pd.to_numeric, errors='coerce')
                avg = df_numeric.mean().mean()
                domain_scores.append(avg)
            except Exception as e:
                st.error(f"בעיה עם עמודות בתחום '{domain}' בקובץ '{matching_file}': {e}")
    if domain_scores:
        chart_data[domain] = sum(domain_scores) / len(domain_scores)

# הצגת גרף סופי
if chart_data:
    st.subheader("ממוצע כללי לפי תחום")
    fig, ax = plt.subplots()
    ax.barh(list(chart_data.keys()), list(chart_data.values()))
    ax.set_xlabel("ממוצע")
    ax.set_xlim(0, 5)
    st.pyplot(fig)
else:
    st.info("לא נמצאו נתונים להצגה.")
