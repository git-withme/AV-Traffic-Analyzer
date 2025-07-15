import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("simulated_traffic_v2i.csv", parse_dates=['Timestamp'])

st.set_page_config(page_title="Urban Traffic Flow Predictor", layout="wide")
st.title("🚦 Urban Traffic Flow Prediction Dashboard")

# Sidebar: Date range filter
st.sidebar.header("🔎 Filter Options")

min_date = df['Timestamp'].min()
max_date = df['Timestamp'].max()

start_date = st.sidebar.date_input("Start Date", pd.to_datetime(min_date))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(max_date))

# Filtered data
filtered_df = df[(df['Timestamp'] >= pd.to_datetime(start_date)) & (df['Timestamp'] <= pd.to_datetime(end_date))]

st.write(f"### Showing data from {start_date} to {end_date}")
st.dataframe(filtered_df.head())

# Traffic Count Comparison Plot
st.write("## 📊 Vehicle Count vs. AV Vehicle Count")

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(filtered_df['Timestamp'], filtered_df['Vehicle_Count'], label="Total Vehicles", color='blue')
ax1.plot(filtered_df['Timestamp'], filtered_df['AV_Vehicle_Count'], label="AV Vehicles", color='orange', linestyle='--')
ax1.set_xlabel("Timestamp")
ax1.set_ylabel("Vehicle Count")
ax1.legend()
ax1.grid(True)

st.pyplot(fig1)

# Signal Status Pie Chart
st.write("## 🚥 Signal Status Distribution")

signal_counts = filtered_df['Signal_Status'].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(signal_counts, labels=signal_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
ax2.axis('equal')

st.pyplot(fig2)

# Download Option
st.write("## 📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_traffic_data.csv',
    mime='text/csv'
)

st.success("App loaded successfully. Adjust the date range to explore traffic trends!")
