import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AV-Enabled Urban Traffic Dashboard", layout="wide")

st.title("🚦 AV-Enabled Urban Traffic Flow Analyzer")

# Load your dataset
try:
    df = pd.read_csv('simulated_traffic_v2i.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Sidebar for selecting chart type and time filter
    st.sidebar.header("Dashboard Controls")
    chart_type = st.sidebar.selectbox("Select Chart Type:", ["Bar Chart", "Line Chart", "Area Chart"])
    group_by = st.sidebar.radio("Group Data By:", ["Raw", "Monthly", "Yearly"])

    # Grouping logic
    if group_by == "Monthly":
        df_grouped = df.groupby(df['Timestamp'].dt.to_period('M')).sum().reset_index()
        df_grouped['Timestamp'] = df_grouped['Timestamp'].dt.to_timestamp()
    elif group_by == "Yearly":
        df_grouped = df.groupby(df['Timestamp'].dt.year).sum().reset_index()
        df_grouped.rename(columns={"Timestamp": "Year"}, inplace=True)
    else:
        df_grouped = df

    # Show sample table
    with st.expander("📊 View Sample Data"):
        st.dataframe(df.head())

    # Traffic Summary Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Vehicle Count", int(df['Vehicle_Count'].sum()))
    col2.metric("Total AV Vehicle Count", int(df['AV_Vehicle_Count'].sum()))

    # Plot based on user choice
    fig, ax = plt.subplots(figsize=(7, 3))

    if chart_type == "Bar Chart":
        if group_by in ["Monthly", "Yearly"]:
            x_labels = df_grouped['Timestamp'] if group_by == "Monthly" else df_grouped['Year']
        else:
            x_labels = df_grouped['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')

        ax.bar(x_labels, df_grouped['Vehicle_Count'], label='Total Vehicles', color='skyblue')
        ax.bar(x_labels, df_grouped['AV_Vehicle_Count'], label='AV Vehicles', color='orange', bottom=df_grouped['Vehicle_Count'] - df_grouped['AV_Vehicle_Count'])
        ax.set_xticks(ax.get_xticks()[::max(1, len(x_labels)//10)])

    elif chart_type == "Line Chart":
        ax.plot(df_grouped['Timestamp'] if group_by != "Yearly" else df_grouped['Year'],
                df_grouped['Vehicle_Count'], label="Total Vehicles", color="blue")
        ax.plot(df_grouped['Timestamp'] if group_by != "Yearly" else df_grouped['Year'],
                df_grouped['AV_Vehicle_Count'], label="AV Vehicles", color="orange")

    elif chart_type == "Area Chart":
        ax.fill_between(df_grouped['Timestamp'] if group_by != "Yearly" else df_grouped['Year'],
                        df_grouped['Vehicle_Count'], color="skyblue", alpha=0.5, label="Total Vehicles")
        ax.fill_between(df_grouped['Timestamp'] if group_by != "Yearly" else df_grouped['Year'],
                        df_grouped['AV_Vehicle_Count'], color="orange", alpha=0.5, label="AV Vehicles")

    ax.set_title(f"Traffic Data ({chart_type})")
    ax.set_ylabel("Vehicle Count")
    ax.legend()
    plt.xticks(rotation=45)

    st.pyplot(fig)

except FileNotFoundError:
    st.error("File 'simulated_traffic_v2i.csv' not found. Please upload it to continue.")


