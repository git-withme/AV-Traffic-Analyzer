import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart City AV Traffic Flow Predictor")

st.title("🚦 Smart City AV Traffic Flow Predictor - Bar Chart Example")

# Load your actual dataset
try:
    df = pd.read_csv('simulated_traffic_v2i.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Display table
    st.write("### Sample Data")
    st.dataframe(df.head())

    # Select only a small recent portion for clarity in bar chart
    recent_df = df.sort_values('Timestamp').tail(10)

    # Bar Chart using real CSV data
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(recent_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M'), 
           recent_df['Vehicle_Count'], 
           label='Total Vehicles', color='skyblue')

    ax.bar(recent_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M'), 
           recent_df['AV_Vehicle_Count'], 
           label='AV Vehicles', color='orange', bottom=recent_df['Vehicle_Count'] - recent_df['AV_Vehicle_Count'])

    ax.set_xticklabels(recent_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M'), rotation=45, ha='right')
    ax.set_ylabel("Vehicle Count")
    ax.set_title("Recent Traffic Counts (Bar Chart)")
    ax.legend()

    st.pyplot(fig)

except FileNotFoundError:
    st.error("File 'simulated_traffic_v2i.csv' not found. Please upload it to continue.")


