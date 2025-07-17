import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AV-Enabled Urban Traffic Analyzer", layout="wide")

st.title("🚦 AV-Enabled Urban Traffic Flow Analyzer")

# Load dataset
df = pd.read_csv('simulated_traffic_v2i.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

st.write("### Sample Data Overview")
st.dataframe(df.head())

# Area Chart
fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(df['Timestamp'], df['Vehicle_Count'], alpha=0.4, label="Total Vehicle Count", color='skyblue')
ax.fill_between(df['Timestamp'], df['AV_Vehicle_Count'], alpha=0.5, label="AV Vehicle Count", color='orange')

ax.set_xlabel("Time")
ax.set_ylabel("Vehicle Count")
ax.set_title("Traffic Flow Over Time with AV Impact")
ax.legend()

st.pyplot(fig)

