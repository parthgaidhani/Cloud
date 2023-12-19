import altair as alt
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Advanced Data Visualization",
    page_icon="✨",
    layout="wide",
)

# Title and Sidebar
st.title("Advanced Data Visualization")
st.sidebar.header("Settings")

# File Upload
data_file = st.sidebar.file_uploader("Upload Your Data CSV (default provided)")

# Data Processing
if data_file is not None:
    df = pd.read_csv(data_file)
else:
    st.sidebar.warning("No file selected. Please upload a dataset.")
    df = pd.DataFrame()

# Data Summary
st.sidebar.subheader("Data Summary")
if not df.empty:
    st.sidebar.write("Number of Rows:", df.shape[0])
    st.sidebar.write("Number of Columns:", df.shape[1])
    st.sidebar.dataframe(df.head())

# Data Selection
if not df.empty:
    columns = df.columns.tolist()

    selected_x_var = st.sidebar.selectbox(
        "Select the X variable",
        columns,
    )

    selected_y_var = st.sidebar.selectbox(
        "Select the Y variable",
        columns,
    )

    # Filter Data
    filter_col = st.sidebar.selectbox("Filter Data by Column", ["None"] + columns)
    filter_value = (
        st.sidebar.text_input("Filter Value") if filter_col != "None" else None
    )

    if filter_value is not None:
        df = df[df[filter_col] == filter_value]

    # Scatterplot
    alt_chart = (
        alt.Chart(df, title="Scatterplot of Uploaded Data")
        .mark_circle()
        .encode(
            x=selected_x_var,
            y=selected_y_var,
            color=alt.Color("Origin:N", legend=None),
            tooltip=list(df.columns),
        )
        .interactive()
    )

    # Display Scatterplot
    st.altair_chart(alt_chart, use_container_width=True)
else:
    st.warning("Please upload a dataset to visualize.")
