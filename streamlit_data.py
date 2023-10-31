import streamlit as st
import pandas as pd

st.write("SoftGrow!")
st.title('User Input CSV File Analysis')

# User uploads a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # User selects a column to analyze
        column_to_analyze = st.selectbox('Choose a column to analyze:', df.columns)

        # Display line chart with selected column data
        st.line_chart(df[column_to_analyze])

    except Exception as e:
        st.write("An error occurred:", e)
else:
    st.write("Please upload a CSV file.")
st.write("Please tell, me what you think about this!")
