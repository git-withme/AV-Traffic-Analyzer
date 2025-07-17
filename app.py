import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart City AV Traffic Flow Predictor", layout="wide")

st.title("🚦 Smart City AV Traffic Flow Predictor – Line Chart Dashboard")

# Load dataset
try:
    df = pd.read_csv('simulated_traffic_v2i.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    st.write("### Sample Data")
    st.dataframe(df.head())

    # Sidebar: Time Group Controls
    st.sidebar.header("Dashboard Controls")
    time_group = st.sidebar.radio("Group Data By:", ["Raw Data", "Monthly", "Yearly"])

    # Grouping Logic
    if time_group == "Monthly":
        df_grouped = df.groupby(df['Timestamp'].dt.to_period('M')).sum().reset_index()
        df_grouped['Timestamp'] = df_grouped['Timestamp'].dt.to_timestamp()
        x_labels = df_grouped['Timestamp']
    elif time_group == "Yearly":
        df_grouped = df.groupby(df['Timestamp'].dt.year).sum().reset_index()
        df_grouped.rename(columns={"Timestamp": "Year"}, inplace=True)
        x_labels = df_grouped['Year']
    else:
        df_grouped = df.sort_values('Timestamp').tail(50)  # Show last 50 rows for clarity
        x_labels = df_grouped['Timestamp']

    # Dashboard Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Vehicle Count", int(df_grouped['Vehicle_Count'].sum()))
    col2.metric("Total AV Vehicle Count", int(df_grouped['AV_Vehicle_Count'].sum()))

    # Plot Line Chart
    fig, ax = plt.subplots(figsize=(7, 3))

    ax.plot(x_labels, df_grouped['Vehicle_Count'], marker='o', label="Total Vehicles", color="blue", linewidth=2)
    ax.plot(x_labels, df_grouped['AV_Vehicle_Count'], marker='o', label="AV Vehicles", color="orange", linewidth=2)

    ax.set_title(f"Traffic Data – Line Chart ({time_group})")
    ax.set_ylabel("Vehicle Count")
    ax.legend()
    plt.xticks(rotation=45)

    st.pyplot(fig)

except FileNotFoundError:
    st.error("File 'simulated_traffic_v2i.csv' not found. Please upload it to continue.")
