import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="AV-Enabled Urban Traffic Analyzer", layout="wide")

st.title("🚦 AV-Enabled Urban Traffic Flow Analyzer")

# Load dataset
try:
    df = pd.read_csv('simulated_traffic_v2i.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    st.write("### Sample Data Overview")
    st.dataframe(df.head())

    # Custom color palette
    sns.set_style("whitegrid")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df['Timestamp'], df['Vehicle_Count'], label="Total Vehicle Count", color="#1f77b4", linewidth=2)
    ax.plot(df['Timestamp'], df['AV_Vehicle_Count'], label="AV Vehicle Count", color="#ff7f0e", linestyle='--', linewidth=2)

    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Vehicle Count", fontsize=12)
    ax.set_title("Traffic Flow Over Time with AV Impact", fontsize=14, fontweight='bold')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)

    st.pyplot(fig)

except FileNotFoundError:
    st.error("The file 'simulated_traffic_v2i.csv' was not found. Please check the file path and try again.")


