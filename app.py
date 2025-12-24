import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision Assistant",
    page_icon="🚀",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {background-color: #0e1117;}
.metric {
    background: #ffffff;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.metric h1 {color:#111; font-size:34px;}
.metric p {color:#6b7280;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 AI Decision Assistant")
st.sidebar.caption("Business-ready insights")

file = st.sidebar.file_uploader(
    "📂 Upload Excel file",
    type=["xls", "xlsx"]
)

# ---------------- HEADER ----------------
st.title("AI Decision Assistant 🚀")
st.caption("Upload Excel & get instant priority and deadline insights")

if file is None:
    st.info("⬅️ Upload an Excel file from sidebar")
    st.stop()

# ---------------- LOAD DATA ----------------
# ---------------- LOAD DATA ----------------
try:
    df = pd.read_excel(file)
except Exception as e:
    st.error("Excel file read panna mudiyala. Please download & upload a proper .xlsx file.")
    st.stop()

# ---------------- COLUMN VALIDATION ----------------
if "Last Date" not in df.columns:
    st.error("❌ Required column 'Last Date' not found in Excel.")
    st.stop()


# ---------------- STATUS LOGIC ----------------
today = datetime.today()

def status_logic(val):
    if pd.isna(val):
        return "Unknown"
    if str(val).lower() == "open":
        return "Open"
    try:
        d = pd.to_datetime(val, format="%d.%m.%Y")
        if d < today:
            return "Closed"
        elif d - today <= timedelta(days=7):
            return "Urgent"
        else:
            return "Upcoming"
    except:
        return "Unknown"

df["Status"] = df["Last Date"].apply(status_logic)

# ---------------- METRICS ----------------
total = len(df)
open_c = (df["Status"]=="Open").sum()
urgent_c = (df["Status"]=="Urgent").sum()
closed_c = (df["Status"]=="Closed").sum()

st.subheader("📊 Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='metric'><p>Total Records</p><h1>{total}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric'><p>Open</p><h1>{open_c}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric'><p>Urgent (≤7 days)</p><h1>{urgent_c}</h1></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric'><p>Closed</p><h1>{closed_c}</h1></div>", unsafe_allow_html=True)

st.divider()

# ---------------- CHART ----------------
st.subheader("📈 Status Distribution")
chart_df = df["Status"].value_counts().reset_index()
chart_df.columns = ["Status", "Count"]
st.bar_chart(chart_df, x="Status", y="Count")

# ---------------- FILTER ----------------
st.subheader("🔍 Filter Records")

status = st.selectbox(
    "Select Status",
    ["All", "Open", "Urgent", "Upcoming", "Closed"]
)

if status != "All":
    df = df[df["Status"] == status]

st.dataframe(df, use_container_width=True)

# ---------------- DOWNLOAD ----------------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download CSV",
    csv,
    "analyzed_data.csv",
    "text/csv"
)
