import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: #e5e7eb;
}

.metric-box {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}

.metric-title {
    font-size: 13px;
    color: #6b7280;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
}

.card-open { border-left: 6px solid #2563eb; }
.card-urgent { border-left: 6px solid #dc2626; }
.card-closed { border-left: 6px solid #16a34a; }
.card-total { border-left: 6px solid #9333ea; }

.section {
    margin-top: 30px;
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

# ---------------- HEADER ----------------
st.title("AI Decision Assistant")
st.caption("Upload your data and get instant priority & deadline insights")

if file is None:
    st.info("Upload an Excel file from the left sidebar to begin analysis.")
    st.stop()

# ---------------- LOAD DATA ----------------
data = pd.read_excel(file)

# ---------------- VALIDATION ----------------
REQUIRED_COLUMNS = ["Last Date"]

for col in REQUIRED_COLUMNS:
    if col not in data.columns:
        st.error(f"Required column '{col}' not found in the uploaded file.")
        st.stop()

# ---------------- STATUS LOGIC ----------------
today = datetime.today()

def get_status(value):
    if pd.isna(value):
        return "Unknown"

    if str(value).strip().lower() == "open":
        return "Open"

    try:
        last_date = pd.to_datetime(value, dayfirst=True)

        if last_date.date() < today.date():
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

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-box card-total">
        <div class="metric-title">TOTAL RECORDS</div>
        <div class="metric-value">{total_records}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-box card-open">
        <div class="metric-title">OPEN OPPORTUNITIES</div>
        <div class="metric-value">{open_count}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-box card-urgent">
        <div class="metric-title">URGENT (≤ 7 DAYS)</div>
        <div class="metric-value">{urgent_count}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-box card-closed">
        <div class="metric-title">CLOSED</div>
        <div class="metric-value">{closed_count}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CHART ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Status Distribution")

chart_data = data["Status"].value_counts()
st.bar_chart(chart_data)

# ---------------- DATA QUALITY ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Data Quality Check")

missing = data.isnull().sum()

if missing.sum() == 0:
    st.success("No missing values found. Data quality is good.")
else:
    st.warning("Missing values detected.")
    st.dataframe(missing)

# ---------------- FILTER ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Filter Records")

status_filter = st.selectbox(
    "Select Status",
    ["All", "Open", "Urgent", "Upcoming", "Closed"]
)

if status_filter != "All":
    filtered_data = data[data["Status"] == status_filter]
else:
    filtered_data = data

st.dataframe(filtered_data, use_container_width=True)

# ---------------- DOWNLOAD ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Download Analyzed Data")

csv = data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="analyzed_data.csv",
    mime="text/csv"
)
