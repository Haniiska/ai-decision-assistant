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
# Paste your entire Streamlit code here
