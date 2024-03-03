import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import plotly.express as px

# Load your time series data (you can replace this with your own dataset)
# For demonstration purposes, let's create some random data
np.random.seed(42)
time_steps = np.arange(0, 1000)
values = np.sin(0.1 * time_steps) + np.random.normal(0, 0.1, size=len(time_steps))
df = pd.DataFrame({"Time": time_steps, "Value": values})

# Create a TensorFlow model (you can replace this with your own model)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu", input_shape=(1,)),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer="adam", loss="mse")

# Train the model (you can replace this with your own training process)
model.fit(df["Time"], df["Value"], epochs=100)

# Streamlit app
st.title("Time Series Forecasting App")
user_input = st.number_input("Enter a time step:", min_value=0, max_value=20000, value=100)

# Make predictions
prediction = model.predict(np.array([user_input]))

# Display prediction
st.write(f"Predicted value at time step {user_input}: {prediction[0][0]:.2f}")

# Visualize predictions
fig = px.line(df, x="Time", y="Value", title="Time Series Forecasting")
fig.add_scatter(x=[user_input], y=[prediction[0][0]], mode='markers', name='Predicted Value')
st.plotly_chart(fig)
