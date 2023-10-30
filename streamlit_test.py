import streamlit as st
import numpy as np

st.write("SoftGrow!")

# Title of the app
st.title('User Input Numbers Line Chart')

# User inputs numbers
user_input = st.text_input("Enter some numbers (comma separated):")

if user_input:
    try:
        numbers = list(map(int, user_input.split(',')))
        # Display line chart with user input numbers
        st.line_chart(numbers)
    except ValueError:
        st.write("Please enter only comma separated numbers.")
else:
    st.write("Please enter some numbers.")
