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

# --- Apply filters to dataframe ---
filtered_df = df.copy()

if selected_border != "All":
    filtered_df = filtered_df[filtered_df["Border"] == selected_border]

if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]

if selected_measure != "All":
    filtered_df = filtered_df[filtered_df["Measure"] == selected_measure]


# --- KPI Section ---
with st.container():
    st.markdown("### 🚦 Border Crossing Metrics")
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        st.metric("Total Crossings", f"{filtered_df['Value'].sum():,.0f}")
    with col2:
        st.metric("Unique Ports", filtered_df['Port Name'].nunique())
    with col3:
        st.metric("States Covered", filtered_df['State'].nunique())
    with col4:
        st.metric("Border Types", filtered_df['Border'].nunique())
    with col5:
        top_measure = filtered_df['Measure'].value_counts().idxmax()
        st.metric("Top Measure", top_measure)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Bar Chart Section ---
with st.container():
    st.markdown("### 🛂 Top 10 Ports by Total Crossings")
    st.markdown("_Measured by total number of people/vehicles crossing per port_")

    top_ports_df = (
        filtered_df.groupby("Port Name", as_index=False)["Value"]
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
        color="Value",  # Use Value to create intensity
        color_continuous_scale="Blues",  # or "Viridis", "Cividis", etc.
        labels={"Value": "Total Crossings", "Port Name": "Port"},
    )

    fig.update_layout(coloraxis_showscale=False)  # optional: hide the color scale legend
    st.plotly_chart(fig, use_container_width=True)


st.markdown("<br><br>", unsafe_allow_html=True)

# --- Time Series Section ---
with st.container():
    st.markdown("### 📈 Monthly Border Crossings Over Time")

    monthly = (
        filtered_df.groupby(pd.Grouper(key="Date", freq="M"))["Value"]
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

st.markdown("### 🗺️ Border Crossing Map")

# Group by location to get total crossings per port
map_df = (
    filtered_df.groupby(["Port Name", "Latitude", "Longitude"], as_index=False)["Value"]
    .sum()
    .sort_values(by="Value", ascending=False)
)

# Only keep rows with valid lat/lon
map_df = map_df.dropna(subset=["Latitude", "Longitude"])

# Plotly map
fig = px.scatter_map(
    map_df,
    lat="Latitude",
    lon="Longitude",
    size="Value",
    hover_name="Port Name",
    hover_data={"Value": True, "Latitude": False, "Longitude": False},
    color="Value",
    color_continuous_scale="Blues",
    size_max=20,
    zoom=3,
    height=600,
)

fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

