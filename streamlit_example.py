import altair as alt
import pandas as pd
import streamlit as st
import statsmodels.api as sm

# Set Streamlit app title and description
st.title("Interactive Data Analysis")
st.markdown("Explore your data with customizable scatterplots and regression analysis!")

# User uploads a data file
data_file = st.file_uploader("Upload Your Data File (CSV, Excel, etc.)")

# Initialize DataFrame
df = pd.DataFrame()

# Check if a file is uploaded
if data_file is not None:
    file_extension = data_file.name.split('.')[-1]
    
    # Read data based on the file extension
    if file_extension.lower() in ['csv', 'xlsx', 'xls']:
        if file_extension.lower() == 'csv':
            df = pd.read_csv(data_file)
        else:
            df = pd.read_excel(data_file)
    else:
        st.warning("Unsupported file format. Please upload a CSV or Excel file.")

# Display dataset summary and allow modification
if not df.empty:
    st.sidebar.title("Data Modification")

    # Display current dataset
    st.subheader("Current Dataset:")
    st.write(df)  # Display DataFrame as a table

    # Allow users to modify data
    if st.sidebar.checkbox("Modify Data"):
        st.subheader("Modify Data:")
        st.write("Edit the data below:")
        edited_data = st.text_area("Modified Data (CSV format)", value=df.to_csv(index=False), height=300)

        # Update the DataFrame with edited data
        try:
            df = pd.read_csv(pd.compat.StringIO(edited_data))
        except pd.errors.ParserError:
            st.warning("Invalid CSV format. Please check your modifications.")

    # Display dataset summary with style
    st.sidebar.subheader("Dataset Summary")
    st.sidebar.table(df.describe())  # Display summary statistics as a table

    # Get column names
    columns = df.columns.tolist()

    # Allow users to customize chart options
    selected_x_var = st.sidebar.selectbox("Select X Variable", columns)
    selected_y_var = st.sidebar.selectbox("Select Y Variable", columns)

    # Additional chart customization options
    chart_color = st.sidebar.selectbox("Select Chart Color", ["red", "green", "orange"])

    # Fit linear latent model
    X = sm.add_constant(df[selected_x_var])
    model = sm.OLS(df[selected_y_var], X).fit()

    # Determine if the selected variables are numerical or categorical
    is_numeric_x = pd.api.types.is_numeric_dtype(df[selected_x_var])
    is_numeric_y = pd.api.types.is_numeric_dtype(df[selected_y_var])

    # Create Altair chart based on variable types
    if is_numeric_x and is_numeric_y:
        chart = alt.Chart(df, title="Scatterplot of Uploaded Data with Regression Line").mark_circle()
    else:
        chart = alt.Chart(df, title="Scatterplot of Uploaded Data with Regression Line").mark_point()

    alt_chart = (
        chart.encode(
            x=selected_x_var,
            y=selected_y_var,
            color=alt.value(chart_color),
            tooltip=list(df.columns)
        )
        .interactive()
    )

    # Add regression line to the chart for numerical variables
    if is_numeric_x and is_numeric_y:
        reg_line = (
            alt.Chart(pd.DataFrame({selected_x_var: [df[selected_x_var].min(), df[selected_x_var].max()]}))
            .mark_line(color='blue')
            .encode(
                x=selected_x_var,
                y=selected_x_var,
                tooltip=[alt.Tooltip(selected_x_var, title=selected_x_var)]
            )
        )
        alt_chart += reg_line

    # Display the Altair chart with regression line
    st.altair_chart(alt_chart, use_container_width=True)

    # Display regression model summary with style
    st.subheader("Regression Model Summary:")
    
    # Extract and display relevant information from the summary
    summary_table = pd.DataFrame({
        'Coefficient': model.params,
        'Std. Error': model.bse,
        't-value': model.tvalues,
        'P-value': model.pvalues,
        '95% Conf. Interval': list(zip(model.conf_int()[0], model.conf_int()[1]))
    }, index=[selected_x_var] + ['const'])

    # Additional statistics for numerical variables
    if is_numeric_x and is_numeric_y:
        summary_table['R-squared'] = model.rsquared
        summary_table['MSE'] = model.mse_model

    st.table(summary_table)

else:
    st.warning("Please upload a dataset to visualize.")
