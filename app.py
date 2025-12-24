import streamlit as st

st.set_page_config(
    page_title="AI Decision Assistant",
    layout="wide"
)

st.title("AI Decision Assistant")
st.write("✅ App is running")

file = st.file_uploader("Upload Excel file")

if file is None:
    st.info("⬅️ Please upload an Excel file to continue")
    st.stop()
import pandas as pd
import streamlit as st

file = st.file_uploader("Upload Excel file", type=["xls", "xlsx"])

if file is not None:
    df = pd.read_excel(file)

    st.success("✅ File uploaded successfully")

    st.subheader("Preview of Data")
    st.dataframe(df)

    st.subheader("Basic Info")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])
else:
    st.info("⬆️ Please upload an Excel file to see analysis")

