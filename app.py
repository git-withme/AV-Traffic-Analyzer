import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="AV-Enabled Urban Traffic Dashboard", layout="wide")

st.title("🚦 AV-Enabled Urban Traffic Flow Dashboard")

# Sidebar Options
st.sidebar.header("Dashboard Controls")

try:
    df = pd.read_csv('simulated_traffic_v2i.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Date Range Filter via Sidebar
    min_date = df['Timestamp'].min().date()
    max_date = df['Timestamp'].max().date()
    date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date])

    # Filter Data
    mask = (df['Timestamp'].dt.date >= date_range[0]) & (df['Timestamp'].dt.date <= date_range[1])
    filtered_df = df.loc[mask]

    # Layout Columns
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Vehicle Count", int(filtered_df['Vehicle_Count'].sum()))
    with col2:
        st.metric("Total AV Vehicle Count", int(filtered_df['AV_Vehicle_Count'].sum()))

    # Smaller Graph Style
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(8, 3))  # Reduced size
    ax.plot(filtered_df['Timestamp'], filtered_df['Vehicle_Count'], label="Vehicle Count", color="#4CAF50", linewidth=1.8)
    ax.plot(filtered_df['Timestamp'], filtered_df['AV_Vehicle_Count'], label="AV Count", color="#FF5722", linestyle='--', linewidth=1.8)

    ax.set_xlabel("Time")
    ax.set_ylabel("Count")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("Traffic Flow Trend", fontsize=12, fontweight="bold")
    ax.tick_params(axis='x', rotation=30)

    st.pyplot(fig)

    # Data Table Option
    with st.expander("Show Filtered Data Table"):
        st.dataframe(filtered_df)

except FileNotFoundError:
    st.error("File 'simulated_traffic_v2i.csv' not found. Please upload it to continue.")


