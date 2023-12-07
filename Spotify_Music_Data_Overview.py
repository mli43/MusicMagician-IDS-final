import streamlit as st

st.title('Exploring Music Characteristics and Artist Relationships')

st.subheader("Motivation")

st.write(
"""
Music has been an integral part of human societies for centuries. Thanks to
rapid advances in technology, we are presented with this great opportunity to
explore how music has influenced the collective human experience. Our goal is
to visualize the evolution of music multiple perspectives, such as from the
traditional time perspective, artist perspective, songs characteristic
perspective, and artist influence.
\n
There are a number of interesting questions that we think our dataset and our
visualizations can help to answer. 
1. What are some major trend changes that have occurred in music over the past century?
2. How does the music of different artists vary in terms of song characteristics? How do these characteristics affect popularity?
3. Does the individual song's characteristic affect its popularity?
4. How does one genre influence the other? What are the most impactful artists in music history and how do they interact?
"""
)

st.divider()

st.subheader("Dataset Overview")

st.write(
"""
The data that we used for this application was created by Spotify using their
internal track databases and curated into the final dataset Interdisciplinary Contest
in Modeling (ICM) for Problem D in 2021. The dataset contains information about 
98,340 songs released between the years of 1921 and 2020.
- Important to note is that songs in this dataset are not necessarily distinct
(a live recording versus a studio recording of the same song would be considered
two separate tracks and thus would be in two separate rows in the dataset).
- Additionally, the dataset is not representative
of the full discography of the artists it contains.
\n
The full dataset of songs is then split into two separate datasets: one containing
information about song characteristics aggregated by year, and another containing
information about song characteristics aggregated by artist. We examine both of
these datasets in separate pages accessible from the sidebar.
\n
An additional dataset containing data about artist influences was also provided
by the ICM. We use this dataset to visualize the relationships between artists
and the strength of an artist's influence on other artists.
"""
)

st.divider()

st.subheader("Pages Overview")

st.write(
"""
This application is split into several pages, each of which can be accessed from
the sidebar. A brief description of the pages are as follows:
\n
- Data by Year
    - In this page, we explore how the characteristics of music have changed
    over time and provide some context as to why these changes occurred. We also
    provide the user with the opportunity to examine these time series in more
    detail through a customizable graph.
- Data by Artist
    - In this page, we explore and compare different artists based on their music.
    We provide the user with the opportunity to examine the prevalent musical characteristics
    (danceability, energy, valence, acousticness, instrumentalness, liveness, speechiness, etc) of artists freely.
    Additionally, we also let users explore how these characteristics vary based on popularity score.
- Data by Song
    - In this page, we explore and compare different characteristics of the
      full music dataset. We provide the user with the opportunity to examine
      individual songs freely in more details, and allow the user to compare
      characteristics of different songs
- Artist Influence
    - add description here
"""
)

st.divider()

st.subheader("Feature Definitions")

st.write(
"""
This section gives a brief overview of the characteristics of music that are
present in this dataset. These characteristics are from Spotify's official
dataset and are defined as follows:
\n
- **Danceability**: How suitable a track is for dancing based on a combination
of musical elements including tempo, rhythm stability, beat strength, and
overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
\n
- **Energy**: A perceptual measure between 0.0 and 1.0 of intensity and activity.
Typically, energetic tracks feel fast, loud, and noisy. For example, death metal
has high energy, while a Bach prelude scores low on the scale. Perceptual features
contributing to this attribute include dynamic range, perceived loudness, timbre,
onset rate, and general entropy.
\n
- **Speechiness**: The presence of spoken words in a track. The more exclusively
speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0
the attribute value.
    - Values above 0.66 describe tracks that are probably made entirely of spoken words.
    - Values between 0.33 and 0.66 describe tracks that may contain both music and
    speech, either in sections or layered, including such cases as rap music. 
    - Values below 0.33 most likely represent music and other non-speech-like tracks.
\n
- **Acousticness**: A confidence measure of whether the track is acoustic. A
score of 1.0 indicates high confidence the track is acoustic.
\n
- **Instrumentalness**: Predicts whether a track contains no vocals. “Ooh” and
“aah” sounds are treated as instrumental in this context. Rap or spoken word
tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0,
the greater likelihood the track contains no vocal content. Values above 0.5
are intended to represent instrumental tracks, but confidence is higher as the
value approaches 1.0.
\n
- **Liveness**: Detects the presence of an audience in the recording. Higher
liveness values represent an increased probability that the track was performed
live. A value above 0.8 provides strong likelihood that the track is live.
\n
- **Valence**: A measure from 0.0 to 1.0 describing the musical positiveness
conveyed by a track. Tracks with high valence sound more positive (e.g. happy,
cheerful, euphoric), while tracks with low valence sound more negative
(e.g. sad, depressed, angry).
\n
- **Tempo**: The overall estimated tempo of a track in beats per minute (BPM).
In musical terminology, tempo is the speed or pace of a given piece and derives
directly from the average beat duration.
\n
- **Loudness**: The overall loudness of a track in decibels (dB). Loudness values
are averaged across the entire track and are useful for comparing relative
loudness of tracks. Loudness is the quality of a sound that is the primary
psychological correlate of physical strength (amplitude). Values typical range
between -60 and 0 db.
\n
- **Explicitness**: A boolean value indicating whether or not the track contains
explicit lyrics (1 = contains explicit lyrics; 0 = does not contain explicit
lyrics OR unknown).
\n
- **Duration**: The duration of the track in milliseconds.
\n
- **Key**: The estimated overall key of the track. Integers map to pitches using
standard Pitch Class Notation where 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key
was detected, the value is -1.
\n
- **Mode**: Mode indicates the modality (major or minor) of a track, the type of
scale from which its melodic content is derived. Major is represented by 1 and
minor is 0.
\n
- **Popularity**: The popularity of a track is a value between 0 and 100, with
100 being the most popular. Popularity is calculated by algorithm and is based,
in the most part, on the total number of plays the track has had and how recent
those plays are. This metric is not from Spotify, rather it was generated by the
ICM.
"""
)

st.divider()

st.subheader("References")

st.write(
"""
- [Spotify Track Audio Features](https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features)
- [ICM 2021 Problem D Prompt](https://www.mathmodels.org/Problems/2021/ICM-D/2021_ICM_Problem_D.pdf)
- [ICM 2021 Problem D Data](https://www.mathmodels.org/Problems/2021/ICM-D/2021_ICM_Problem_D_Data.zip)
"""
)
