import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Urban Traffic Flow Prediction with AV Impact")

df = pd.read_csv('simulated_traffic_v2i.csv')

st.write("### Sample Data", df.head())

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pd.to_datetime(df['Timestamp']), df['Vehicle_Count'], label="Vehicle Count")
ax.plot(pd.to_datetime(df['Timestamp']), df['AV_Vehicle_Count'], label="AV Vehicle Count", linestyle='--')
ax.legend()
st.pyplot(fig)

