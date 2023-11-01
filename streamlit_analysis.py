# Import necessary libraries
import streamlit as st
import pandas as pd

# Display a simple text
st.title("SoftGrow!")

# Display a title on the app
st.title('User Input Data File Analysis')

# User uploads a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # User selects a column to analyze from the dropdown menu which contains all column names of the uploaded CSV file
        column_to_analyze = st.selectbox('Choose a column to analyze:', df.columns)

        # Display line chart with selected column data
        st.line_chart(df[column_to_analyze])

        # Print if there are any null values in the DataFrame
        missing_values = df.isnull().sum()
        st.write("Missing values in each column: ", missing_values)

    except Exception as e:
        # Display any error that occurs during the process
        st.write("An error occurred:", e)
else:
    # Ask the user to upload a file if no file is uploaded
    st.write("Please upload a CSV file")
