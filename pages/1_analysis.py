import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 ניתוח תחומים", layout="wide")
st.title("📊 ניתוח ממוצעים לפי תחומים")

if "uploaded_surveys" not in st.session_state or not st.session_state["uploaded_surveys"]:
    st.warning("🟡 אנא חזרי לעמוד הבית והעלי לפחות קובץ סקר אחד.")
    st.stop()

uploaded_files = st.session_state["uploaded_surveys"]
survey_data = {}

for file in uploaded_files:
    try:
        df = pd.read_excel(file)
        survey_data[file.name] = df
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ {file.name}: {e}")

domains = {
    "רלוונטיות הקורס והתאמה לצרכים": {
        "סקר מסכם": ['AF','AJ','BB','AL','AM','AO','AP','AQ','AR','AS','AT','AU','AV','AW','AX','AY'],
        "סקר סביבה": ['R','X','Y'],
        "סקר טלפוני": ['e']
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

results = {}

for domain, surveys in domains.items():
    domain_scores = []
    for survey_type, columns in surveys.items():
        file = next((f for f in survey_data if survey_type in f), None)
        if file:
            df = survey_data[file]
            valid_cols = [col for col in columns if col in df.columns]
            if valid_cols:
                numeric = df[valid_cols].apply(pd.to_numeric, errors='coerce')
                mean_score = numeric.mean().mean()
                domain_scores.append(mean_score)
    if domain_scores:
        results[domain] = round(sum(domain_scores) / len(domain_scores), 2)

if results:
    st.subheader("📋 טבלת ממוצעים")
    st.dataframe(pd.DataFrame(results.items(), columns=["תחום", "ממוצע"]), use_container_width=True)

    st.subheader("📊 גרף ממוצעים")
    st.bar_chart(pd.DataFrame(results, index=["ממוצע"]).T)
else:
    st.info("🔍 לא נמצאו נתונים להצגה.")
