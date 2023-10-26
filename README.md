# Cloud
This is visualizing data when user input their data like 20.2,9000,122,etc.
When user input their data it shows the graph of your data.
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.header("SoftGrow")
st.write("Welcome to SoftGrow!")


# Function to convert user input to float list
@st.cache
def convert_input(user_input):
    return list(map(float, user_input.split(',')))

# Get user inputs
input_data1 = st.text_input("Enter your data on x_axis ")
input_data2 = st.text_input("Enter your data on y-axis ")

# user data check missing values
def check_missing(self):
    self.df = pd.DataFrame({'1': input_data1, '2': input_data2})
    st.print(self.df.isnull())


# Check if inputs are not empty
if input_data1 and input_data2:
    # Convert inputs to appropriate data types (e.g., lists, arrays)
    # Here assuming the inputs are comma-separated values
    data1 = convert_input(input_data1)
    data2 = convert_input(input_data2)

    # Create a plot
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.plot(data1, label='Data 1')
    ax.plot(data2, label='Data 2')
    ax.set_title('Your Data Plot')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    st.write("Please enter data in both fields.")
    st.write('Please give me your feedback on my Email.parthgaidhani94@gmail.com')
