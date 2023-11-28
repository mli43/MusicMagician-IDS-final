import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# load data
df = pd.read_csv('Data/full_music_data.csv')

df.release_date = pd.to_datetime(df.release_date, format='mixed')
df.drop_duplicates(subset=['song_title (censored)'])

df = df[df['release_date'] < '2023-12-01']

st.title("Data by Song")

st.markdown("This interactive page allows you to explore characteristics of different songs. You can navigate to the overview tabs to view the full music distribution, the song ranking tab to see top or least favored songs in different time range, and the comparison tab to compare characteristics of different songs")

df.iloc[:, 2:16] = df.iloc[:, 2:16].astype('float')
st.dataframe(df)

# Numeric columns only
subset = df[df.columns[2:-2]]


tab1, tab2, tab3 = st.tabs(['Overview', 'Song Ranking', 'Song Comparison'])

with tab1:
    st.header("Dataset distribution")
    f = plt.figure(figsize=(15,15))
    plt.matshow(subset.corr(), fignum=f.number)
    plt.xticks(range(subset.select_dtypes(['number']).shape[1]), subset.select_dtypes(['number']).columns, fontsize=14, rotation=45)
    plt.yticks(range(subset.select_dtypes(['number']).shape[1]), subset.select_dtypes(['number']).columns, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    st.pyplot(f)

with tab2:
    st.header("Song ranking")
    col1, col2 = st.columns(2)
    date_range = st.slider(
            "Range",
            df['release_date'].min().to_pydatetime(), 
            df['release_date'].max().to_pydatetime(),
            (
                df['release_date'].min().to_pydatetime(), df['release_date'].max().to_pydatetime()
                )
            )

    with col1:
        num_top = st.number_input(
                "How many top songs?",
                1, 50, 10
                )


    with col2:
        reverse = st.checkbox("Rank by least popular?")

with tab3:
    st.header("Song Comparison")
