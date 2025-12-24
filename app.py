import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM STYLE ----------------
st.markdown("""
<style>
    body {
        background-color: #0e1117;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0,0,0,0.15);
    }
    .metric-title {
        font-size: 14px;
        color: #6b7280;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #111827;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("AI Decision Assistant")
st.sidebar.caption("Business-ready data insights")

file = st.sidebar.file_uploader(
    "Upload Excel file",
    type=["xls", "xlsx"]
)

# ---------------- MAIN TITLE ----------------
st.title("AI Decision Assistant")
st.caption("Upload your data and get instant priority & deadline insights")

if file is None:
    st.info("Upload an Excel file from the left sidebar to begin analysis.")
    st.stop()

# ---------------- LOAD DATA ----------------
data = pd.read_excel(file)

# ---------------- COLUMN VALIDATION ----------------
REQUIRED_COLUMNS = ["Last Date"]

for col in REQUIRED_COLUMNS:
    if col not in data.columns:
        st.error(f"Required column '{col}' not found in the uploaded file.")
        st.stop()

# ---------------- DATE STATUS LOGIC ----------------
today = datetime.today()

def get_status(value):
    if pd.isna(value):
        return "Unknown"

    if str(value).strip().lower() == "open":
        return "Open"

    try:
        # Force Indian date format: DD.MM.YYYY
        last_date = pd.to_datetime(value, format="%d.%m.%Y")

        if last_date < today:
            return "Closed"
        elif last_date - today <= timedelta(days=7):
            return "Urgent"
        else:
            return "Upcoming"
    except:
        return "Unknown"

data["Status"] = data["Last Date"].apply(get_status)

# ---------------- DASHBOARD METRICS ----------------
total_records = len(data)
open_count = (data["Status"] == "Open").sum()
urgent_count = (data["Status"] == "Urgent").sum()
closed_count = (data["Status"] == "Closed").sum()

st.subheader("Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Total Records</div>
        <div class="metric-value">{total_records}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Open Opportunities</div>
        <div class="metric-value">{open_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Urgent (≤ 7 days)</div>
        <div class="metric-value">{urgent_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Closed</div>
        <div class="metric-value">{closed_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- DATA QUALITY ----------------
st.subheader("Data Quality Check")
missing = data.isnull().sum()

if missing.sum() == 0:
    st.success("No missing values found. Data quality is good.")
else:
    st.warning("Missing values detected.")
    st.dataframe(missing)

# ---------------- FILTER ----------------
st.subheader("Filter Records")

status_filter = st.selectbox(
    "Select Status",
    options=["All", "Open", "Urgent", "Upcoming", "Closed"]
)

if status_filter != "All":
    filtered_data = data[data["Status"] == status_filter]
else:
    filtered_data = data

st.dataframe(filtered_data, use_container_width=True)

# ---------------- DOWNLOAD ----------------
st.subheader("Download Analyzed Data")

csv = data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="analyzed_data.csv",
    mime="text/csv"
)
