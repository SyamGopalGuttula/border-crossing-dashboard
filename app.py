import streamlit as st
import pandas as pd

st.set_page_config(page_title="Border Entry Dashboard", layout="wide")

st.title("U.S. Border Crossing Entry Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Border_Crossing_Entry_Data.csv")
    return df

# Load and preview
with st.spinner("Loading data..."):
    df = load_data()

st.success(f"Loaded {len(df):,} records.")

# --- KPI Cards ---
st.markdown("### 🚦 Border Crossing Metrics")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric("Total Crossings", f"{df['Value'].sum():,.0f}")

with col2:
    st.metric("Unique Ports", df['Port Name'].nunique())

with col3:
    st.metric("States Covered", df['State'].nunique())

with col4:
    st.metric("Border Types", df['Border'].nunique())

with col5:
    top_measure = df['Measure'].value_counts().idxmax()
    st.metric("Top Measure", top_measure)

