import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.utils import column_index_from_string

st.set_page_config(page_title="📈 גרפים לפי תחום", layout="wide")

st.title("📈 גרפים ויזואליים וניתוח לפי תחומים")

if "uploaded_surveys" not in st.session_state:
    st.warning("🔁 אנא חזרי לדף הבית והעלי לפחות קובץ אחד לניתוח.")
    st.stop()

uploaded_files = st.session_state["uploaded_surveys"]
survey_data = {}

# קריאת קובץ היגדים לצורך מיפוי אותות → טקסט
statement_map_file = "היגדים.xlsx"
try:
    map_df = pd.read_excel(statement_map_file, header=None)
    map_df.columns = ["text", "code"]
    code_to_text = dict(zip(map_df["code"], map_df["text"]))
except Exception as e:
    st.error("לא ניתן לקרוא את קובץ ההיגדים: " + str(e))
    code_to_text = {}

# קריאת קבצים ללא כותרות
for file in uploaded_files:
    try:
        df = pd.read_excel(file, header=None)
        survey_data[file.name] = df
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ {file.name}: {e}")

# מיפוי התחומים לעמודות באותיות
# (כמו שהיה קודם - לא שינינו)
... (הקטע הזה נשאר כפי שהוא, לא מוצג כאן לשם קיצור) ...

chart_data = {}
detailed_data = {}

for domain, surveys in domains.items():
    domain_scores = []
    details = []
    for survey_name, columns in surveys.items():
        matching_file = next((f for f in survey_data if survey_name in f), None)
        if matching_file:
            df = survey_data[matching_file]
            try:
                col_indexes = [column_index_from_string(col) - 1 for col in columns if column_index_from_string(col) <= df.shape[1]]
                df_numeric = df.iloc[:, col_indexes].apply(pd.to_numeric, errors='coerce')
                col_means = df_numeric.mean()
                for col, mean in zip(columns, col_means):
                    label = code_to_text.get(col, col)  # תרגום היגד או שמירה על הקוד
                    details.append({"היגד": label, "ממוצע": round(mean, 2)})
                avg = col_means.mean()
                domain_scores.append(avg)
            except Exception as e:
                st.error(f"בעיה עם עמודות בתחום '{domain}' בקובץ '{matching_file}': {e}")
    if domain_scores:
        chart_data[domain] = round(sum(domain_scores) / len(domain_scores), 2)
        detailed_data[domain] = details

if chart_data:
    st.subheader("📋 טבלת ממוצעים לפי תחום")
    df_summary = pd.DataFrame(chart_data.items(), columns=["תחום", "ממוצע"])
    df_summary["אחוז"] = (df_summary["ממוצע"] / 5 * 100).round(1).astype(str) + "%"
    st.dataframe(df_summary, use_container_width=True)

    st.subheader("📊 גרף ממוצעים כלליים")
    fig, ax = plt.subplots()
    bars = ax.barh(df_summary["תחום"], df_summary["ממוצע"])
    ax.set_xlabel("ממוצע")
    ax.set_xlim(0, 5)
    ax.invert_yaxis()  # הפוך סדר תצוגה בעברית
    st.pyplot(fig)

    st.subheader("📌 ניתוח מפורט לפי תחום")
    for domain, items in detailed_data.items():
        st.markdown(f"### 🔹 {domain}")
        st.dataframe(pd.DataFrame(items), use_container_width=True)
else:
    st.info("לא נמצאו נתונים להצגה.")
