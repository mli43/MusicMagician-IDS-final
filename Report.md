# Final Project Report

**Project URL**: TODO
**Video URL**: TODO

Short (~250 words) abstract of the concrete data science problem and how the solutions addresses the problem.

## 1 Introduction
Music has been an integral part of human societies for centuries. As part of an
effort to understand the role of music in the collective human experience, we
used the curated dataset from the Interdisciplinary Contest in Modeling (ICM)
for Problem D in 2021 and developed a Streamlit application to visualize music
evolution. There are many influence factors for music creation such as the
artist's own personal experience, social events, or access to new piece of
technology. Our goal is to understand the evolution of music from multiple
perspectives including time series, artist characteristics, song
characteristics, and measure the influence of previously produced music on new
music and artists. 

## 2 Related Work

For the Data by Year page of this application, we incorporated information that
aims to provide some context for trends in the data. We conducted research into
the history of Western music in the 20th century, as Western music makes up the 
bulk of this dataset. The sources we used for contextual information to explain
these trends are cited at the bottom of each page, if any souurces were used.
The trajectory of our research was dictated by first inspecting the trends in 
the Data by Year dataset, picking out notable changes in the trends (eg. a large
change in the values for acousticness starting in the 1950s), and using that as
a starting point for events to look into.

## 3 Methods

### 3.1 Data by Year
This page inspects the Data by Year dataset which aggregates the music characteristic
values of all songs in the dataset released in the same year. Below, we discuss
the content shown on this page and the design of its layout.

#### 3.1.1 Page Content

#### 3.1.2 Page Design

### 3.3 Data by Song
In this section, we summarize the steps we took for data cleaning, design choices, and developing Streamlit application for the Data by Song page. 

#### 3.3.1 Data Clearning
The dataset we used in this section is the full music dataset that contains
information for 98,340 songs released between 1921 and 2020. Since we obtained
the dataset from ICM, it has already been sufficiently cleaned. To adapt the
data for use in our Streamlit application, we did minimal changes to the data,
such as converting datatypes of specific columns. 

#### 3.3.2 Page Design
To effectively and thoroughly understand the data, we decided to use three tabs
within this page: an overview tab, a song ranking tab, and a song comparison
tab. 

First, the **overview tab** is a static tab that shows the user the original
dataset, and statistics of numerical features of the original dataset such as
min, max, and standard deviation, and a correlation matrix of the numerical
features in the dataset. We decided to use this tab to serve as an introduction
that allow the user to directly examine the data. We hope this static
introduction will help the users appreciate the interactivities in other tabs
more.

Next, the **song ranking tab** has will allow the user to see the most and least
popular songs in the dataset. The user will be able to filter songs by date,
choose how many songs to display, and set minimum and maximum popularity of
songs to be displayed. We used altair to create two horizontal bar plots and
plot the top and bottom at the same time and color code the popularity, which
allows the user to easily visualize the difference in popularity. 

Lastly, the **song comparison tab** will allow the user to freely choose up to 6
songs in the dataset and compare their characteristics. The reason we decided on
6 songs is for aesthetic reasons, as more songs included in the visualization
makes it harder to distinguish. The visualization we decided to use is polar
graph with plotly, which can easily allow comparison of multiple entries with
multiple numeric features. For the convenience of song searching, we sorted the
dataset by song title and concatenated the artist names to the end of the song
title so that users can search songs by title or artist. 

#### 3.3.3 Development
We used Streamlit as our main framework for creating the application. In the
Data by Song page, we also used python libraries including pandas for data
processing, matplotlib, altair, and plotly for creating visualizations. More
specifically, matplotlib was used to create the static correlation matrix in the
overview tab, altair was used to create the dynamic song ranking bar plot, and
plotly was used to create the dynamic song comparison polar plot. 

### 3.4 Music Influence
#### 3.4.1 Data Preparation
The influence dataset proves to be pretty neat without null values or duplicates. There are two unique attributes about this dataset. Firstly, it contains 42770 influencer-follower relationships. Secondly, this dataset has a "main genre" feature associated with each artist, which is found in no other datasets. To best leverage both, we analyze the data at "genre" level and "influencer" level. When computing statistics at genre level, "influencers" and "followers" are "equivalent"- both are artists. So we prepare a "full_artists" dataframe that vertically stack influencer and follower data. When focusing on influencer level, we aim to answer questions such as "who is the most impactful artist of all time?" Thus, we prepare another "influencer" dataframe, extracting information only regarding the influencers. With these datasets prepared, we efficiently pave way for following steps. 

#### 3.4.2 Key Techniques
Among various data manipulation techniques, the most creative one must be the "pivot-melt" approach for constructing the "Artist Population In Top N Genres Over Time", which is a stacked distribution chart. Pivot table is an efficient technique to re-structure our dataframe so that one of its column contents may be pivoted as the row, making subtotal/total summary extra convenient. After we obtain this summary pivot table, we "melt" it to conform to the input standard of altair, reformating a wide dataframe to a long one. These transformations make our analysis flexible and efficient. 

#### 3.4.3 Visualization Highlight
One highlight of this section is our incorporation of network visualizations. A network is a graph consisting of nodes and edges. Based on our research, there are various ways to visualize a network via libraries such as "networkx", "pyvis", etc. To cater to the interactive nature of our app, however, we choose a library that 1) is compatible with streamlit, 2) is fun to interact with. "streamlit-agraph" perfectly meets our criteria. It not only allows users to add nodes and edges with customized attribtues, but also provides an interactive interface where user could "drag" the network around to inspect the details. We implemented networks for both genres and artists for the audience to fully explore the dynamics.

## 4 Results

### 4.3 Data by Song

#### 4.3.1 Overview tab:
This is the correlation matrix shown in the overview tab. 

![](eda_notebooks/images/full_music_corr.png "This plot displays the correlation between numeric features in the dataset")

#### 4.3.2 Song Ranking tab:
This is an example of the visualization created in the song ranking tab for top
songs ranking. The date range for this graph is from 2000-1-11 to 2020-6-16,
with a k of 15 and a maximum popularity of 94.
![Song ranking tab top song example](./assets/top_15_songs_2000_2020.png "This plot displays the top 15 songs fron 2000-1-11 to 2020-6-16.")

This is an example of the visualization created in the song ranking tab for
bottom songs ranking. The date range for this graph is from 2000-1-11 to
2020-6-16, with a k of 15 and a minimum popularity of 10.
![Song ranking tab bottom song example](./assets/bottom_15_songs_2000_2020.png "This plto displays the bottom 15 least popular songs from 2000-1-11 to 2022-6-16 with a popularity of at least 10.")

#### 4.3.3 Song comparison tab:
This is an example of the visualization created in the song comparison tab. The
two songs chosen are "Stuck with U (with Justin Bieber) by ['Ariana Grande',
'Justin Bieber']" and "I Know You Care by ['Ellie Goulding']". The reason for
choosing the two songs is because they have distinct characteristics and show up
very differently in song ranking.
![Song comparison tab example](./assets/song_comparison.png "This plot displays polar graph that compares two songs in multiple attributes.")


## 5 Discussion

## 6 Future Work

## 7 Reference