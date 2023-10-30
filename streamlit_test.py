import streamlit as st
import numpy as np

st.write("SoftGrow!")

# Title of the app
st.title('User Input Numbers Line Chart')

# User inputs numbers
user_input = st.text_input("Enter some numbers1 (comma separated):")
user_input = st.text_input("Enter some numbers2 (comma separated):")

if user_input:
    try:
        numbers1 = list(map(int, user_input.split(',')))
        numbers2 = list(map(int, user_input.split(',')))
        # Display line chart with user input numbers
        st.line_chart(numbers1 and numbers2)
    except ValueError:
        st.write("Please enter only comma separated numbers.")
else:
    st.write("Please enter some numbers.")
