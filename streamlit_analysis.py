import streamlit as st
import pandas as pd
import plotly.express as px

# Display a title for the app
st.title("SoftGrow Data Visualization!")

# Sidebar for user inputs
st.sidebar.title("User Inputs")

# User uploads a CSV file
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Display summary statistics of the dataset
        st.sidebar.subheader("Dataset Summary")
        st.sidebar.write(df.describe())

        # Allow users to customize chart options
        st.sidebar.subheader("Chart Customization")
        selected_chart_type = st.sidebar.selectbox("Select Chart Type", ["Line Chart", "Scatter Plot"])
        selected_x_var = st.sidebar.selectbox('Select X Variable', df.columns)
        selected_y_var = st.sidebar.selectbox('Select Y Variable', df.columns)

        # Display the selected chart
        st.markdown(f"## {selected_chart_type}")
        if selected_chart_type == "Line Chart":
            st.line_chart(df[[selected_x_var, selected_y_var]])
        elif selected_chart_type == "Scatter Plot":
            fig = px.scatter(df, x=selected_x_var, y=selected_y_var, title="Scatter Plot")
            st.plotly_chart(fig)

    except Exception as e:
        # Display any error that occurs during the process
        st.sidebar.error(f"An error occurred: {e}")

else:
    # Ask the user to upload a file if no file is uploaded
    st.write("Please upload a CSV file")
