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

# st.dataframe(df_artist)
# st.dataframe(df_artist.describe())

# Separate Tabs

tab1, tab2, tab3, tab4 = st.tabs(["Single Artist Overview", "Artist Comparison", "Top & Bottom K Artists", "Data"])


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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Ref: https://medium.com/codefile/streamlit-text-gets-colourful-d92c21ab8cf6
    with col1:
        st.markdown(f"""**Tempo :blue[{artist_row['tempo']}] Loudness :green[{artist_row['loudness']}] Mode :orange[{artist_row['mode']}]**""")
    
    with col2:
        st.title(artist_row["artist_name"])
        
    with col3:
        st.markdown(f"""**Popularity :rainbow[{artist_row['popularity']}] Duration_ms :violet[{artist_row['duration_ms']}] Key :red[{artist_row['key']}]**""")
    
with tab2:
    
    df_filtered = df_artist[df_artist["popularity"] == 0]
    zero_pop_artists = df_filtered["artist_name"].to_list()
    # print(zero_pop_artists)
    
    df_artist = df_artist[df_artist["popularity"] > 0]
    
    artist_choices = st.multiselect("Choose artist from list:",
                 df_artist["artist_name"].sort_values(),
                 placeholder="Choose artist",
                 max_selections=8,
                 default=["Frank Sinatra", "El Guincho", "Justin Timberlake", "The Flying Lizards", "Pixinguinha", "Billie Eilish", "*NSYNC"])
    
    # print(artist_choices)
    
    cols = ["danceability", "energy", "valence", "acousticness", "instrumentalness", "liveness", "speechiness"]

    plot_data = list()

    for artist_choice in artist_choices:
        artist_row = df_artist[df_artist["artist_name"] == artist_choice].squeeze()
        plot_data.append(go.Scatterpolar(r=artist_row[cols].to_list(), theta=cols, fill="toself", name=artist_row["artist_name"]))

    
    fig1 = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=""),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )

    st.plotly_chart(fig1, use_container_width=True)
    
    # st.dataframe(df_artist[df_artist["artist_name"].isin(artist_choices)])
    
    df_filtered = df_artist[df_artist["artist_name"].isin(artist_choices)]
    # st.dataframe(df_filtered)
    
    k = df_filtered.shape[0]

    fig2 = alt.Chart(
        df_filtered,
        title=f"Popularity Ranking of Selected Artists",
        # width="container"
    ).mark_bar().encode(
        alt.X("popularity:Q", title="Artist Popularity Score"),
        alt.Y("artist_name:N", title="Artist Name", sort=("-x")),
        # alt.Color("popularity:Q"),
        # fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="magma")),
        tooltip=["artist_name", "popularity", "count"]

    ).transform_window(
        rank="rank(popularity)",
        sort=[alt.SortField("popularity", order="descending")]
    ).transform_filter(
        (alt.datum.rank <= k)
    )
    
    st.altair_chart(fig2, use_container_width=True)
    
    st.write("🌟 Click on the legend of the artists to enable or disable the overlay on the chart")
    st.write("🌟 You can double-click on the the legend to focus on the radar chart of a single artist")
    st.write("🌟 Use the icon on the top-right of the chart to enter full-screen mode")
    
with tab3:
    
    col1, col2 = st.columns(2)
    
    df_filtered = df_artist[df_artist["popularity"] > 0]
    
    # choice of k
    k = col1.slider("Choose k (top/bottom):", min_value=1, max_value=25, value=10)
    
    # limit popularity range
    pop = col2.slider("Choose popularity score range:",
                int(df_filtered['popularity'].min()),
                int(df_filtered['popularity'].max()),
                (int(df_filtered['popularity'].min()), int(df_filtered['popularity'].max()))
            )
    
    df_filtered = df_filtered.query("@pop[0] <= popularity <= @pop[1]")
    
    # most popular
    top_k_df = df_filtered.sort_values(by="popularity", ascending=False).head(k) 
    
    # bottom k - unpopular
    bottom_k_df = df_filtered.sort_values(by="popularity", ascending=False).tail(k)
    
    # print(top_k_df)
    # print(bottom_k_df)
    
    # REF: https://altair-viz.github.io/gallery/top_k_items.html
    fig1 = alt.Chart(
        top_k_df,
        title=f"Top {k} Popular Artists",
        # width="container"
    ).mark_bar().encode(
        alt.X("popularity:Q", title="Artist Popularity Score"),
        alt.Y("artist_name:N", title="Artist Name", sort=("-x")),
        # alt.Color("popularity:Q"),
        fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="goldgreen"), legend=alt.Legend(orient="bottom")),
        tooltip=["artist_name", "popularity", "count"]

    ).transform_window(
        rank="rank(popularity)",
        sort=[alt.SortField("popularity", order="descending")]
    ).transform_filter(
        (alt.datum.rank <= k)
    )
    
    fig2 = alt.Chart(
        bottom_k_df,
        title=f"Bottom {k} UnPopular Artists",
        # width="container"
    ).mark_bar().encode(
        alt.X("popularity:Q", title="Artist Popularity Score"),
        alt.Y("artist_name:N", title="Artist Name", sort=("x")),
        # alt.Color("popularity:Q"),
        fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="purplered"), legend=alt.Legend(orient="bottom")),
        tooltip=["artist_name", "popularity", "count"]

    ).transform_window(
        rank="rank(popularity)",
        sort=[alt.SortField("popularity", order="descending")]
    ).transform_filter(
        (alt.datum.rank <= k)
    )
    
    top_plot_data=list()
    
    top_pop_artists = top_k_df["artist_name"].to_list()

    for artist_choice in top_pop_artists:
        artist_row = top_k_df[top_k_df["artist_name"] == artist_choice].squeeze()
        top_plot_data.append(go.Scatterpolar(r=artist_row[cols].to_list(), theta=cols, fill="toself", name=artist_row["artist_name"]))

    fig_top = go.Figure(
        data=top_plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=f"Top {k} Artists"),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )
    
    bottom_plot_data=list()
    
    bottom_pop_artists = bottom_k_df["artist_name"].to_list()

    for artist_choice in bottom_pop_artists:
        artist_row = bottom_k_df[bottom_k_df["artist_name"] == artist_choice].squeeze()
        bottom_plot_data.append(go.Scatterpolar(r=artist_row[cols].to_list(), theta=cols, fill="toself", name=artist_row["artist_name"]))

    fig_bottom = go.Figure(
        data=bottom_plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=f"Bottom {k} Artists"),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )
    
    with col1:
        st.altair_chart(fig1, use_container_width=True)
    
    with col2: 
        st.altair_chart(fig2, use_container_width=True)
        
    st.plotly_chart(fig_top)
    st.plotly_chart(fig_bottom)
    
with tab4:
    st.title("Artist Data All")
    st.dataframe(df_artist)
    st.dataframe(df_artist.describe())
    
    # df_filtered = df_artist[df_artist["popularity"] == 0]
    
    # st.title("Artists with Popularity score 0")
    # st.dataframe(df_filtered)
    
