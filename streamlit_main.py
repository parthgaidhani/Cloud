import altair as alt
import pandas as pd
import streamlit as st
from scipy.stats import chi2_contingency

# Page Configuration
st.set_page_config(
    page_title="Advanced Data Analysis",
    page_icon="📊",
    layout="wide",
)

# Title and Sidebar
st.title("Advanced Data Analysis")

# File Upload
data_file = st.file_uploader("Upload Your Data CSV (default provided)")

# Data Processing
if data_file is not None:
    df = pd.read_csv(data_file)
else:
    st.warning("No file selected. Please upload a dataset.")
    df = pd.DataFrame()

# Data Summary
st.subheader("Data Summary")
if not df.empty:
    st.write("Number of Rows:", df.shape[0])
    st.write("Number of Columns:", df.shape[1])
    st.dataframe(df.head())

    # Descriptive Statistics
    st.subheader("Descriptive Statistics")
    st.write(df.describe())

    # Correlation Analysis
    st.subheader("Correlation Analysis")

    # Numeric Correlation
    st.write("Numeric Correlation:")
    numeric_columns = df.select_dtypes(include=['number']).columns
    numeric_correlation_df = df[numeric_columns].corr()
    st.write(numeric_correlation_df)

    # Categorical Correlation
    st.write("Categorical Correlation:")
    categorical_columns = df.select_dtypes(exclude=['number']).columns
    if not categorical_columns.empty:
        categorical_correlation_df = pd.DataFrame(index=categorical_columns, columns=categorical_columns)
        for col1 in categorical_columns:
            for col2 in categorical_columns:
                if col1 != col2:
                    cross_table = pd.crosstab(df[col1], df[col2])
                    _, p, _, _ = chi2_contingency(cross_table)
                    categorical_correlation_df.loc[col1, col2] = p
        st.write(categorical_correlation_df)

# Data Selection and Analysis
if not df.empty:
    columns = df.columns.tolist()

    selected_x_var = st.selectbox("Select the X variable", columns)
    selected_y_var = st.selectbox("Select the Y variable", columns)

    # Chart Type Selection
    chart_type = st.selectbox("Select Chart Type", ["Scatterplot", "Bar Chart", "Line Chart"])

    # Chart Generation
    if chart_type == "Scatterplot":
        chart = (
            alt.Chart(df, title="Scatterplot of Selected Data")
            .mark_circle()
            .encode(
                x=selected_x_var,
                y=selected_y_var,
                color=alt.Color("Origin:N", legend=None),
                tooltip=list(df.columns),
            )
            .interactive()
        )
    elif chart_type == "Bar Chart":
        chart = (
            alt.Chart(df, title="Bar Chart of Selected Data")
            .mark_bar()
            .encode(
                x=selected_x_var,
                y=selected_y_var,
                color=alt.Color("Origin:N", legend=None),
                tooltip=list(df.columns),
            )
            .interactive()
        )
    elif chart_type == "Line Chart":
        chart = (
            alt.Chart(df, title="Line Chart of Selected Data")
            .mark_line()
            .encode(
                x=selected_x_var,
                y=selected_y_var,
                color=alt.Color("Origin:N", legend=None),
                tooltip=list(df.columns),
            )
            .interactive()
        )

    # Display Chart
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Please upload a dataset to analyze.")

