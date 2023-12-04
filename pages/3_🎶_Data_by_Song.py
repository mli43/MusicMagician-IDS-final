import streamlit as st
import pandas as pd
import numpy as np
import datetime

import altair as alt
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

# load data
# df = pd.read_csv('../data/full_music_data.csv')
# 
# df.drop_duplicates(subset=['song_title (censored)'], inplace=True, keep='first')
# 
# df['release_date'] = pd.to_datetime(df['release_date'], format='mixed')
# df = df[ df['release_date'] < datetime.datetime(2023, 12, 1) ]

df = pd.read_csv('data/full_music_filtered_by_date.csv')
df['release_date'] = pd.to_datetime(df['release_date'], format='mixed')

st.title("Data by Song")

st.markdown("This interactive page allows you to explore characteristics of different songs. You can navigate to the overview tabs to view the full music distribution, the song ranking tab to see top or least favored songs in different time range, and the comparison tab to compare characteristics of different songs")

df.iloc[:, 2:14] = df.iloc[:, 2:14].astype('float')
st.dataframe(df.describe())

# Numeric columns only
subset = df[df.columns[2:-2]]


# Create three tabs
tab1, tab2, tab3 = st.tabs(['Overview', 'Song Ranking', 'Song Comparison'])


# Show overview graphs
with tab1:
    st.header("Dataset distribution")
    f = plt.figure(figsize=(15,15))
    plt.matshow(subset.corr(), fignum=f.number)
    plt.xticks(range(subset.select_dtypes(['number']).shape[1]), subset.select_dtypes(['number']).columns, fontsize=14, rotation=45)
    plt.yticks(range(subset.select_dtypes(['number']).shape[1]), subset.select_dtypes(['number']).columns, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    st.pyplot(f)



# Show song rankings
with tab2:
    st.header("Top & bottom k songs")
    col1, col2 = st.columns(2)
    with col1:
        # filter by date
        date_range = st.slider(
                "Range",
                df['release_date'].min(), 
                df['release_date'].max(),
                (
                    df['release_date'].min().to_pydatetime(), df['release_date'].max().to_pydatetime()
                    )
                )


    with col2:
        # filter by top/bottom k
        k = st.number_input(
                "Choose k",
                1, 50, 10
                )

    rank_subset = df[df['release_date'] >= date_range[0]]
    rank_subset = rank_subset[rank_subset['release_date'] <= date_range[1]]
    rank_subset = rank_subset[rank_subset['popularity'] != 0]

    # cap max popularity
    cap_pop = st.slider("Maximum/minimum popularity of shown songs",
                int(rank_subset['popularity'].min()),
                int(rank_subset['popularity'].max()),
                (int(rank_subset['popularity'].min()), int(rank_subset['popularity'].max()))
            )


    rank_subset = rank_subset[rank_subset["popularity"] <= cap_pop[1]]
    rank_subset = rank_subset[rank_subset["popularity"] >= cap_pop[0]]

    rank_subset = rank_subset.sort_values(by='popularity' )

    fig1 = alt.Chart(
            rank_subset.tail(k)[::-1],
            title=f"Top {k} popular songs"
        ).mark_bar().encode(
            alt.X("popularity:Q"),
            alt.Y("song_title (censored):N", sort=("-x")),
            fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="greenblue")),
            tooltip=["song_title (censored)", "popularity", "artist_names"]
        ).transform_window(
            rank="rank(popularity)",
            sort=[alt.SortField("popularity", order="ascending")]
        ).transform_filter(
            (alt.datum.rank <= k)
        )
    st.altair_chart(fig1, use_container_width=True)

    fig2 = alt.Chart(
            rank_subset.head(k)[::-1],
            title=f"Bottom {k} least popular songs"
        ).mark_bar().encode(
            alt.X("popularity:Q"),
            alt.Y("song_title (censored):N", sort=("x")),
            fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="darkred")),
            tooltip=["song_title (censored)", "popularity", "artist_names"]
        ).transform_window(
            rank="rank(popularity)",
            sort=[alt.SortField("popularity", order="ascending")]
        ).transform_filter(
            (alt.datum.rank <= k)
        )
    st.altair_chart(fig2, use_container_width=True)




# Compare songs
df['song_artist'] = df['song_title (censored)'] + " by " + df['artist_names']

with tab3:
    st.header("Song Comparison")

    songs = st.multiselect("Select up to 6 songs to compare", df['song_artist'].sort_values(),
            placeholder="Choose songs", 
            max_selections = 6,
            default = ["New Rules by ['Dua Lipa']"]) 

    comp_subset = df[ df['song_artist'].isin(songs) ]

    cols = ["danceability", "energy", "valence", "acousticness", "instrumentalness", "liveness", "speechiness"]

    comp_subset[cols] = comp_subset[cols]*10

    plot_data = list()
    for song in songs:
        song_row = comp_subset[comp_subset['song_artist'] == song].squeeze()

        plot_data.append(go.Scatterpolar(r=song_row[cols].to_list(), theta=cols, fill="toself", name=song_row["song_artist"]))

    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=""),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.2,
        xanchor="right",
        x=1
    ))

    st.markdown('')
    st.markdown('')

    st.plotly_chart(fig)


