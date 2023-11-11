import altair as alt
import pandas as pd
import streamlit as st

st.title("Data Analysis!!")
st.markdown("Use this Streamlit app to make your own scatterplot!")

data_file = st.file_uploader("Upload Your Data CSV (default provided)")

if data_file is not None:
    df = pd.read_csv(data_file)
else:
    st.write("No file selected. Please upload a dataset.")
    df = pd.DataFrame()

if not df.empty:
    columns = df.columns.tolist()

    selected_x_var = st.selectbox(
        "Select the x variable",
        columns,
    )

    selected_y_var = st.selectbox(
        "Select the y variable",
        columns,
    )

    alt_chart = (
        alt.Chart(df, title="Scatterplot of Uploaded Data")
        .mark_circle()
        .encode(
            x=selected_x_var,
            y=selected_y_var,
            color=alt.Color('Origin:N', legend=None),
            tooltip=list(df.columns)
        )
        .interactive()
    )

    st.altair_chart(alt_chart, use_container_width=True)
else:
    st.write("Please upload a dataset to visualize.")
