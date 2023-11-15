import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load Data
df = pd.read_csv('Data/data_by_year.csv')

st.dataframe(df)

fig = px.histogram(df, x="loudness")
st.plotly_chart(fig)
