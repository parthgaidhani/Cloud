
import streamlit as st
import pandas as pd

# Display a simple text
st.title("SoftGrow!")

# Display a title on the app
st.title('Data visualization!')
st.write("Upload your data file and visualize it according to your choice.")

# User uploads a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        


        # Display a title for the scatterplot
        st.markdown('Use this Streamlit app to make your own scatterplot!')

        # User selects x and y variables for the scatterplot from the dropdown menu which contains all column names of the uploaded CSV file
        selected_x_var = st.selectbox('What do want the x variable to be?', df.columns) 
        selected_y_var = st.selectbox('What about the y?', df.columns) 

        # Display scatterplot with selected x and y variables
        chart_data = df[[selected_x_var, selected_y_var]]
        st.line_chart(chart_data)

    except Exception as e:
        # Display any error that occurs during the process
        st.write("An error occurred:", e)
else:
    # Ask the user to upload a file if no file is uploaded
    st.write("Please upload a CSV file")
