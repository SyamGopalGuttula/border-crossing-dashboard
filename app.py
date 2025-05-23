import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page config ---
st.set_page_config(page_title="Border Crossing Dashboard", layout="wide")
st.title("U.S. Border Crossing Entry Dashboard")

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Border_Crossing_Entry_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

with st.spinner("Loading data..."):
    df = load_data()

#st.success(f"Loaded {len(df):,} records.")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
with st.sidebar.expander("Select Filters", expanded=False):
    selected_border = st.sidebar.selectbox("Border", ["All"] + sorted(df["Border"].unique()))
    selected_state = st.sidebar.selectbox("State", ["All"] + sorted(df["State"].unique()))
    selected_measure = st.sidebar.selectbox("Measure", ["All"] + sorted(df["Measure"].unique()))

# --- Apply filters ---
filtered_df = df.copy()
if selected_border != "All":
    filtered_df = filtered_df[filtered_df["Border"] == selected_border]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]
if selected_measure != "All":
    filtered_df = filtered_df[filtered_df["Measure"] == selected_measure]

if filtered_df.empty:
    st.warning("No data available for the selected filters. Try changing your selection.")
    st.stop()

# LAYOUT
col1, col2 = st.columns([2, 8])  # Left = metrics/info | Right = charts

# Metrics + Info
with col1:
    st.markdown("### Metrics")
    st.markdown("**Total Crossings**")
    st.markdown(f"#### {filtered_df['Value'].sum():,.0f}")
    st.markdown("**Unique Ports**")
    st.markdown(f"#### {filtered_df['Port Name'].nunique()}")
    st.markdown("**States Covered**")
    st.markdown(f"#### {filtered_df['State'].nunique()}")
    st.markdown("**Top Measure**")
    st.markdown(f"#### {filtered_df['Measure'].value_counts().idxmax()}")

    st.markdown("### 🛂 Top Ports")
    top_ports_df = (
        filtered_df.groupby("Port Name", as_index=False)["Value"]
       .sum()
       .sort_values(by="Value", ascending=False)
       .head(10)
    )
    top_ports_df = top_ports_df.sort_values(by="Value")
    fig_bar = px.bar(
        top_ports_df.sort_values(by="Value", ascending=False),
        x="Port Name",
        y="Value",
        color="Value",
        color_continuous_scale="Blues",
        labels={"Value": "Total Crossings", "Port Name": "Port"},
    )

    fig_bar.update_layout(
        xaxis_tickangle=-45,
        margin=dict(t=10, b=50, l=10, r=10),
        coloraxis_showscale=False  # Optional: hide color bar
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Map + Bar side-by-side
with col2:
    map_col, about_col = st.columns([8,2])

    with map_col:
        st.markdown("### 🗺️ Map")
        map_df = filtered_df.groupby(["Port Name", "Latitude", "Longitude"], as_index=False)["Value"].sum()
        map_df = map_df.dropna(subset=["Latitude", "Longitude"])
        fig_map = px.scatter_mapbox(
            map_df,
            lat="Latitude",
            lon="Longitude",
            size="Value",
            hover_name="Port Name",
            color="Value",
            color_continuous_scale="Blues",
            zoom=2.5,
            height=350
        )
        fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with about_col:
        st.markdown("### ℹ️ About")
        st.info(
            "**Source:** [U.S. Border Crossing Entry Data – data.gov](https://catalog.data.gov/dataset/border-crossing-entry-data-683ae)\n\n"
            "Data shows the number of border crossings by port, date, and measure."
        )

    # Line chart
    st.markdown("### 📈 Monthly Trend")
    monthly = filtered_df.groupby(pd.Grouper(key="Date", freq="M"))["Value"].sum().reset_index()
    fig_line = px.line(
        monthly,
        x="Date",
        y="Value",
        labels={"Value": "Total Crossings", "Date": "Month"},
        markers=True
    )
    fig_line.update_traces(line=dict(width=2), marker=dict(size=4))
    fig_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)
