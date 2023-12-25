import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page title
st.title("Data Visualization App")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read the uploaded data
    df = pd.read_csv(uploaded_file)

    # Choose a chart type
    chart_type = st.selectbox("Select a chart type", [
        "Line Chart",
        "Bar Chart",
        "Pie Chart",
        "Scatter Plot",
        "Area Chart",
        "Bubble Chart",
        "Histogram",
        "Funnel Chart",
        "Waterfall Chart",
        "Bullet Chart",
        "Column Chart",
        "TreeMap",
        "Gantt Chart",
        "Gauge",
        "Stacked Bar Graph",
        "Radar Chart",
        "Heatmap",
        "Boxplot",
        "Donut Chart",
        "Maps",
        "Tables",
        "Venn Diagram",
        "Flowchart"
    ])

    # Visualize the selected chart
    if chart_type == "Line Chart":
        selected_columns = st.multiselect("Select columns for Y-axis", df.columns)
        if selected_columns:
            st.line_chart(df[selected_columns])
        else:
            st.warning("Please select at least one column.")
    elif chart_type == "Bar Chart":
        selected_columns = st.multiselect("Select columns for Y-axis", df.columns)
        if selected_columns:
            st.bar_chart(df[selected_columns])
        else:
            st.warning("Please select at least one column.")
    elif chart_type == "Pie Chart":
        selected_column = st.selectbox("Select a column for the pie chart", df.columns)
        if selected_column:
            pie_data = df[selected_column].value_counts()
            st.pie_chart(pie_data)
        else:
            st.warning("Please select a column.")
    # Add similar sections for other chart types...

    # Display the data table
    st.write("Data Table:")
    st.dataframe(df)
