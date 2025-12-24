import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="AI Decision Assistant",
    layout="wide"
)

# Title
st.title("AI Decision Assistant")
st.write("App is running")

# ONE file uploader only
file = st.file_uploader(
    "Upload Excel file",
    type=["xls", "xlsx"]
)

# If no file, stop here
if file is None:
    st.info("Please upload an Excel file to continue")
    st.stop()

# Read Excel
df = pd.read_excel(file, engine=None)


st.success("File uploaded successfully")

# Preview
st.subheader("Preview of Data")
st.dataframe(df, use_container_width=True)

# Basic info
st.subheader("Basic Info")
col1, col2 = st.columns(2)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
