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
st.write("### Sample of the data")
st.dataframe(df.head(10))
