import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="Border Crossing Dashboard", layout="wide")
st.title("🧭 U.S. Border Crossing Entry Dashboard")

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Border_Crossing_Entry_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

with st.spinner("Loading data..."):
    df = load_data()

st.success(f"Loaded {len(df):,} records.")

# --- KPI Section ---
with st.container():
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

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Bar Chart Section ---
with st.container():
    st.markdown("### 🛂 Top 10 Ports by Total Crossings")
    st.markdown("_Measured by total number of people/vehicles crossing per port_")

    top_ports_df = (
        df.groupby("Port Name", as_index=False)["Value"]
        .sum()
        .sort_values(by="Value", ascending=False)
        .head(10)
    )
    top_ports_df = top_ports_df.sort_values(by="Value")

    fig = px.bar(
        top_ports_df,
        x="Value",
        y="Port Name",
        orientation='h',
        color="Port Name",
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={"Value": "Total Crossings", "Port Name": "Port"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Time Series Section ---
with st.container():
    st.markdown("### 📈 Monthly Border Crossings Over Time")

    monthly = (
        df.groupby(pd.Grouper(key="Date", freq="M"))["Value"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Date",
        y="Value",
        title="Total Border Crossings by Month",
        labels={"Value": "Total Crossings", "Date": "Month"},
        markers=True
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=4))
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)
