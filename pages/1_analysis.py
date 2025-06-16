import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 ניתוח לפי תחומים", layout="wide")
st.title("📊 ניתוח תחומי הערכה מהקבצים שהועלו")

if "uploaded_surveys" not in st.session_state:
    st.warning("🟡 אנא חזרי לדף הבית והעלי קבצים לפני שמתחילים בניתוח.")
    st.stop()

uploaded_files = st.session_state["uploaded_surveys"]

# קריאת כל הקבצים לקובץ אחד לפי שם
survey_data = {}
for f in uploaded_files:
    try:
        df = pd.read_excel(f)
        survey_data[f.name] = df
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ {f.name}: {e}")

# מיפוי עמודות לפי תחומים
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

results = {}

for domain, surveys in domains.items():
    domain_scores = []
    for survey_name, cols in surveys.items():
        match_file = next((key for key in survey_data if survey_name in key), None)
        if match_file:
            df = survey_data[match_file]
            valid_cols = [col for col in cols if col in df.columns]
            if valid_cols:
                df_numeric = df[valid_cols].apply(pd.to_numeric, errors='coerce')
                avg = df_numeric.mean().mean()
                domain_scores.append(avg)
    if domain_scores:
        results[domain] = round(sum(domain_scores) / len(domain_scores), 2)

# הצגת טבלה
if results:
    result_df = pd.DataFrame(list(results.items()), columns=["תחום", "ממוצע"])
    st.dataframe(result_df, use_container_width=True)
else:
    st.info("לא נמצאו נתונים מתאימים לניתוח.")
