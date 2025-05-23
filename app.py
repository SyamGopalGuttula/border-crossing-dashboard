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

# --- Sidebar Filters ---
st.sidebar.header("🎛️ Filter Options")
with st.sidebar.expander("Select Filters", expanded=True):
    selected_border = st.sidebar.radio("Border", ["All"] + sorted(df["Border"].unique()))
    selected_state = st.sidebar.radio("State", ["All"] + sorted(df["State"].unique()))
    selected_measure = st.sidebar.radio("Measure", ["All"] + sorted(df["Measure"].unique()))

# --- Apply filters ---
filtered_df = df.copy()
if selected_border != "All":
    filtered_df = filtered_df[filtered_df["Border"] == selected_border]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]
if selected_measure != "All":
    filtered_df = filtered_df[filtered_df["Measure"] == selected_measure]

# --- Layout: Three Columns ---
col1, col2, col3 = st.columns([1.5, 4.5, 2])

# --- Column 1: KPIs ---
with col1:
    st.markdown("### 🚦 Metrics")

    def small_metric(label, value):
        st.markdown(
            f"""
            <div style='margin-bottom: 1rem'>
                <span style='font-size: 14px; color: #999;'>{label}</span><br>
                <span style='font-size: 20px; font-weight: 600; color: #fff;'>{value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    small_metric("Total Crossings", f"{filtered_df['Value'].sum():,.0f}")
    small_metric("Unique Ports", filtered_df['Port Name'].nunique())
    small_metric("States Covered", filtered_df['State'].nunique())
    small_metric("Top Measure", filtered_df['Measure'].value_counts().idxmax())


# --- Column 2: Line Chart + Map ---
with col2:
    st.markdown("### 🗺️ Crossing Locations Map")
    map_df = filtered_df.groupby(["Port Name", "Latitude", "Longitude"], as_index=False)["Value"].sum()
    map_df = map_df.dropna(subset=["Latitude", "Longitude"])
    fig_map = px.scatter_map(
        map_df,
        lat="Latitude",
        lon="Longitude",
        size="Value",
        hover_name="Port Name",
        color="Value",
        color_continuous_scale="Blues",
        zoom=3,
        height=600
    )
    fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
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

# --- Column 3: Bar Chart + About ---
with col3:
    st.markdown("### 🛂 Top Ports")
    top_ports_df = (
        filtered_df.groupby("Port Name", as_index=False)["Value"]
        .sum()
        .sort_values(by="Value", ascending=False)
        .head(10)
    )
    fig_bar = px.bar(
        top_ports_df,
        x="Port Name",
        y="Value",
        color="Value",
        color_continuous_scale="Blues",
        labels={"Value": "Total Crossings", "Port Name": "Port"},
    )
    fig_bar.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### ℹ️ About")
    st.info(
        "Source: U.S. Customs and Border Protection\n\n"
        "Data reflects number of individuals or vehicles crossing into the U.S. by port, border, and measure.\n"
        "Updated monthly from [data.gov](https://catalog.data.gov/dataset/border-crossing-entry-data-683ae)."
    )
