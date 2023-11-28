import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import datetime

# load data
df = pd.read_csv('Data/full_music_data.csv')

df.drop_duplicates(subset=['song_title (censored)'], inplace=True, keep='first')

df['release_date'] = pd.to_datetime(df['release_date'], format='mixed')
df = df[ df['release_date'] < datetime.datetime(2023, 12, 1) ]

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
    col1, col2, col3 = st.columns(3)
    date_range = st.slider(
            "Range",
            df['release_date'].min(), 
            df['release_date'].max(),
            (
                df['release_date'].min().to_pydatetime(), df['release_date'].max().to_pydatetime()
                )
            )

    with col1:
        num_top = st.number_input(
                "How many top songs?",
                1, 50, 10
                )


    with col3:
        reverse = st.checkbox("Rank by least popular?")

    rank_subset = df[df['release_date'] >= date_range[0]]
    rank_subset = rank_subset[rank_subset['release_date'] <= date_range[1]]



    if not reverse:
        rank_subset.sort_values(by=['popularity'], ascending=False, inplace=True)
        with col2:
            pop_floor = st.number_input(
                    "Highest popularity to show",
                    0, int(max(rank_subset['popularity'].unique())), int(max(rank_subset['popularity'].unique()))
                    )
            rank_subset = rank_subset[rank_subset['popularity'] <= pop_floor]
    else:
        rank_subset.sort_values(by=['popularity'], inplace=True)
        with col2:
            pop_ceil = st.number_input(
                    "Lowest popularity to show",
                    int(min(rank_subset['popularity'].unique())), int(max(rank_subset['popularity'].unique())), int(min(rank_subset['popularity'].unique()))
                    )
            rank_subset = rank_subset[rank_subset['popularity'] >= pop_ceil]

    st.dataframe(rank_subset.iloc[:num_top, [-1,-3, -2, -4, 0]])


def format_option(row):
    st.markdown(row)
    return row['song_title (censored)'] + "by " + row['artist_names']

df['song_artist'] = df['song_title (censored)'] + " by " + df['artist_names']

with tab3:
    st.header("Song Comparison")

    songs = st.multiselect("Select songs to compare", df['song_artist']) 

    comp_subset = df[ df['song_artist'].isin(songs) ]


    st.dataframe(comp_subset)
