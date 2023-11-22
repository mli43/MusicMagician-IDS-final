import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load Data
df = pd.read_csv('Data/data_by_year.csv')
df_full = pd.read_csv('Data/full_music_data.csv')

# Calculate % songs containing explicit music by year using full dataset
df['explicit'] = df_full.groupby(['year'])['explicit'].mean().reset_index().explicit

# Title
st.title('Data by Year')

st.write(
    """
The visualizations on this page aim to examine how cultural changes and 
advancements in music technology are reflected in music characteristics and 
vice versa.
    """
)

st.header("The Rise of Electronic Music")
fig = px.line(df, x="year", y=["energy", "acousticness", "instrumentalness"],
              title="Energy, Acousticness, and Instrumentalness Over Time")
fig.update_layout(xaxis_title='Year', yaxis_title='Value')
st.plotly_chart(fig, use_container_width=True)

st.write(
    """
Starting in the 1950s with the introduction of electronic augmentation, we can 
visually discern how quickly it takes over. Acousticness and instrumentalness
in music experienced a stark decline starting in the 1950s and leveling off
around 1980, while energy saw a steady increase over the same time period. Since
then, all three characteristics have remained relatively stable.
    """
)


st.header("Faster, Louder, More Explicit")
st.header("NEED TO FIX THIS GRAPH")
fig = px.area(df, x="year", y=["loudness", "tempo", "explicit"],
              title="Energy, Acousticness, and Instrumentalness Over Time")
fig.update_layout(xaxis_title='Year', yaxis_title='Value')
st.plotly_chart(fig, use_container_width=True)



st.header("G and A# Rule All Other Keys")

fig = px.pie(df, values=df.key.value_counts(), names=df.key.unique(),
             title='Average Key Distribution of Songs Betweeen 1921-2020')
fig.update_layout(legend_title_text='Key')
st.plotly_chart(fig, use_container_width=True)

st.write(
    """
In this dataset, keys for each year are calculated as the estimated overall key 
of each track, and then taking the dominant key of each year as the key with the
most occurrences in that year. This is not a perfect method, as it does not
account for the key changes within songs, but it serves as a decent 
approximation of the key distribution of songs over time.
\n
Using standard pitch class notation where pitches are mapped to an integer, 
we can see that the dominant keys are 7 and 10, which correspond to G and A#,
respectively.
    """
)

st.write(
    """
NEED TO ADD MORE CONTEXT
    """
)

st.dataframe(df)

# References

# https://courses.lumenlearning.com/suny-musicapp-medieval-modern/chapter/electronic-music/#:~:text=Music%20produced%20solely%20from%20electronic,the%20purpose%20of%20composing%20music.

# https://www.digitaltrends.com/music/whats-the-most-popular-music-key-spotify/

# https://mixedinkey.com/captain-plugins/wiki/best-chords-for-edm/

# https://plotly.com/python/multiple-axes/


