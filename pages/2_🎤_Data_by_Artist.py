import streamlit as st

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import altair as alt


# Setup page heading

st.header("Data by Artist")

st.markdown("This interactive page allows you to explore information about the different artists in the dataset. The first tab gives you a summary of the song characteristics of a single artist, the second tab lets you compare song characteristics of several artists (upto 8) and, the third tab lets you visualize the top and bottom k (max. 25) artists based on popularity scores. This page is a work in progress, subject to change based on feedback.")

# Load Data
df_artist = pd.read_csv("./processed-data/cleaned_data_by_artist.csv")

st.dataframe(df_artist)
st.dataframe(df_artist.describe())

# Separate Tabs

tab1, tab2, tab3 = st.tabs(["Single Artist Overview", "Artist Comparison", "Top & Bottom K Artists"])


with tab1:
    
    artist_choice = st.selectbox("Choose artist from list:",
                 df_artist["artist_name"].sort_values(),
                 placeholder="Choose artist")
    
    cols = ["danceability", "energy", "valence", "acousticness", "instrumentalness", "liveness", "speechiness"]
    artist_row = df_artist[df_artist["artist_name"] == artist_choice].squeeze()
    # print(artist_row)
    
    fig = go.Figure(
        data=[
            go.Scatterpolar(r=artist_row[cols].to_list(), theta=cols, fill="toself", name=artist_row["artist_name"]),
        ],
        layout=go.Layout(
            title=go.layout.Title(text=""),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )

    st.plotly_chart(fig)
    
with tab2:
    
    artist_choices = st.multiselect("Choose artist from list:",
                 df_artist["artist_name"].sort_values(),
                 placeholder="Choose artist",
                 max_selections=8,
                 default=["Taylor Swift", "Frank Sinatra", "El Guincho"])
    
    # print(artist_choices)
    
    cols = ["danceability", "energy", "valence", "acousticness", "instrumentalness", "liveness", "speechiness"]

    plot_data = list()

    for artist_choice in artist_choices:
        artist_row = df_artist[df_artist["artist_name"] == artist_choice].squeeze()
        plot_data.append(go.Scatterpolar(r=artist_row[cols].to_list(), theta=cols, fill="toself", name=artist_row["artist_name"]))

    
    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=""),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )

    st.plotly_chart(fig)
    
with tab3:
    
    df_filtered = df_artist[df_artist["popularity"] != 0]
    
    k = st.slider("Choose k", min_value=1, max_value=25, value=10)
    
    # most popular
    
    top_k_df = df_filtered.sort_values(by="popularity", ascending=False).head(k) 
    
    bottom_k_df = df_filtered.sort_values(by="popularity", ascending=False).tail(k)
    
    # print(top_k_df)
    # print(bottom_k_df)
    
    col1, col2 = st.columns(2)
    
    # REF: https://altair-viz.github.io/gallery/top_k_items.html
    fig1 = alt.Chart(
        top_k_df,
        title=f"Top {k} Popular Artists"
    ).mark_bar().encode(
        alt.X("popularity:Q"),
        alt.Y("artist_name:N", sort=("-x")),
        # alt.Color("popularity:Q"),
        fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="greenblue")),
        tooltip=["artist_name", "popularity", "count"]

    ).transform_window(
        rank="rank(popularity)",
        sort=[alt.SortField("popularity", order="descending")]
    ).transform_filter(
        (alt.datum.rank <= k)
    )
    
    col1.altair_chart(fig1)
    
    fig2 = alt.Chart(
        bottom_k_df,
        title=f"Bottom {k} UnPopular Artists"
    ).mark_bar().encode(
        alt.X("popularity:Q"),
        alt.Y("artist_name:N", sort=("x")),
        # alt.Color("popularity:Q"),
        fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="darkred")),
        tooltip=["artist_name", "popularity", "count"]

    ).transform_window(
        rank="rank(popularity)",
        sort=[alt.SortField("popularity", order="descending")]
    ).transform_filter(
        (alt.datum.rank <= k)
    )
    
    col2.altair_chart(fig2)

