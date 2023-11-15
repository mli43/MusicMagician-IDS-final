# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-Fall-2023/final-project-musicmagicians/tree/main

**A short summary (3-4 paragraphs, about one page) of the data science problem you are addressing and what your solution will address. Feel free to include a figure or sketch to illustrate your project.**

Complete Project proposal: https://docs.google.com/document/d/12_InTimLdOuIm3lGfAHxmgSYuEV3K-SWiDrrchgJ_KY/edit?usp=sharing

Music has been an integral part of human societies for centuries. To understand how music has influenced the collective human experience, we will use a music dataset from Interdisciplinary Contest in Modeling (ICM) problem D in 2021. Our goal is to visualize the evolution of music from different perspectives, such as artist influence and genre evolution. This dataset can be accessed from ICM’s official website. It consists of four sub-datasets that can be used to answer different questions, two of which are transformed from the ‘full_music_data.csv’ dataset by grouping by artist and year.

There are a number of potential questions we can answer from this dataset. We hope that these questions can help us gain better insight into how mucis influences the collective human experience and how social events impact the evolution of music. Here're some initial questions we hope to answer:

1. How could we define “music influence”? By our definition, who are the most influential artists in music history? Could we find patterns of how one major genre influences the other? What are the relationships between top artists from 1921-2020?
2. What attributes distinguish a genre? How does each genre/artist evolve? 
3. How does the evolution of music attributes reflect the social, cultural, and technological climate?

There are a number of features that our appllication can have. At this phase of the project, we plan to have hierarchical visualization of how different artists influence each other, a cluster that help visualize the similarity between different genres, and charts and graphs that correlate the most popular music genre and music charasteristic such as danceability with historical events. We will continue to add more and adjust our visualizations as we continue development to ensure we gain a deeper understanding of how music interacts with our daily lives and how music is affect by it. 

## Data Analysis
### Data Processing
No tables in this dataset contained any null or duplicate values. As a result, we did not feel the need to drop any rows or remove any malformed columns. There was some processing to be done in the full music dataset. More specifically, the type of the artist_name column is string, where it should be a list. However, naively splitting the string with "," is tricky because some artists, such as bands, use comma in their name. This will cause discrepancy between artist name and artist id column, making it impossible to explode the dataset. One method to get around this is to convert the id column into list of ints, and use the data by artist dataset to map back the artist name from the id. 

Additionally, we performed some EDA on all four tables and a subset of our plots from EDA are shown below.

### Full music dataset visualizations
![](eda_notebooks/images/full_music_corr.png "This plot displays the correlation between numeric features in the dataset")


![](eda_notebooks/images/full_music_violin.png "This plot displays the violin plot that shows the distribution of selected features")


![](eda_notebooks/images/full_music_year_explicit.png "This plot shows year vs mean explicit in the aggregated-by-year full dataset. More recent songs are more explicit.")


#### Data by Year


<img width="650" alt="Screenshot 2023-11-13 at 12 15 19 PM" src="https://github.com/CMU-IDS-Fall-2023/final-project-musicmagicians/assets/80061658/b3b83777-e09b-4d9c-b05c-47fb4f868013">
<br>
This plot displays the correlations between all columns in the dataset. We can observe that year is strongly negatively correlated with certain music characteristics like acousticness and instrumentalness and positively correlated energy and loudness, but less strongly so.
<br>
<br>

<img width="582" alt="Screenshot 2023-11-13 at 12 11 59 PM" src="https://github.com/CMU-IDS-Fall-2023/final-project-musicmagicians/assets/80061658/7a403657-62a5-4478-9422-83980a5949bc">
<br>
Although years are not taken into acount in these histograms, we can get a sense of the distribution of these features in music over the past century. For the features on a decimal scale, larger values indicate a higher confidence in the presence of that feature and lower values indicate unlikeliness in the presence of that feature.
<br>
<br>

<img width="634" alt="Screenshot 2023-11-13 at 12 44 32 PM" src="https://github.com/CMU-IDS-Fall-2023/final-project-musicmagicians/assets/80061658/ad92cec2-03e2-4344-9702-0b5aaf6f41f8">
<br>
We observed in the correlation matrix that acousticness and energy were strongly negatively and positively correlated with year, so we plotted both features on the same graph to observe the magnitude and direction of both relationships. Interesting to note is that both features experienced rapid changes starting at around 1950 and leveling off in 1980.
<br>

### Data by artist


### Influence data
![](eda_notebooks/images/active_year.png "This plot displays the start of career for influencers and followers")
<br>
We plot the career start of influencers and followers side-by-side. As shown in the influencer graph, number of influencers reaches a peak around 1960. As shown in the follower graph, number of followers surges around 1990. The lag is reasonable given the influencer-follower dynamic. One surprising aspect is that there is a gap from 1960-1970 in both graphs. Whether this is due to data collection issue or social issue is up to further investigation.
<br>

![](eda_notebooks/images/genre_dist.png "This plot displays main genres ordered by number of artists")
<br>
We plot the distribution of main genres for influencers and followers side-by-side. As shown above, "Pop/Rock" is the most popular genre for both influencers and followers, followed by "R&B", "Country", and "Jazz". For the influencers, the 5th popular genre is "Vocal", while for the followers, it's "Electronic". From this graph, we could also see that the genres are distributed unevenly with a majority class and several minority classes. This indicates in network visualization, we need to pay attention to the number of genre upperbound.

<br>

![](eda_notebooks/images/top10_artists.png "This plot displays top 10 most influential artists from 1930-2010")
<br>
We plot a horizontal bar plot of the artists sorted by their number of followers. As shown above, the Beatles is a dominant top artist with more than 600 followers, followed by Bob Dylan, the Rolling Stone, etc.
<br>


## Sketches and systen design
    
We will have one static dashboard page where the use can view the original four datasets. This will be out home page. We propose to have four pages that contains visualiztions and interactions for each dataset.

### Full music dataset 
In this page, we plan to implement three tabs in this page. The user can click on one tab and contents in other tabs will be invisible. This is our design decision because we don't want to crowd the page with too many information, visualizations, and interactions.

1. Overview tab: This tab will show the distribution of different features in the dataset such as danceability, valence, acousticness. We want to show some statistical information about the dataset for the user to get some high-level understanding of the dataset.
![](eda_notebooks/images/full_music_overview_tab.JPG "Sketch of the songs overview tab")

2. Songs rank tab: This tab will allow the users to input the desiged range of years to filter from, number of songs to show, and show the users the most or least popular songs in the desired year range. 
![](eda_notebooks/images/full_music_rank_songs_tab.JPG "Sketch of the songs ranking tab")

3. Compare songs tab: This tab will allow the user to search for two songs and plot two polar graphs for the two songs side by side. This can provide the user to look at songs of their choosing in more detail.
![](eda_notebooks/images/full_music_compare_tab.JPG "Sketch of the comparing songs tab")


### Data by year
In this page, we aim to examine how culural changes and advanvements in music technology is reflected in our dataset. This dataset consists of aggregated/averaged characteristics of music created in that year; we aim for this page to be more of an educational one rather than one centered around interactivity.

1. The Rise of Electronic Music
   We observe a strong negative relationship when we plot energy against acousticness and instrumentalness. Starting in the 1950s with the instroduction of electronic augmentation, we can visually discern how quickly it takes over. This plot is meant to be a line graph.
2. Faster, Louder, More Explicit
    This area chart will plot loudness, tempo, and explicitness in one area chart. The challenge of this graph will be working with 3 distinct axes and conveying the context of the axes to the audience without being too confusing.
4. G-Major and C-Major Rule All Other Keys
   We observed that the dominant keys over the past century are G-Major and C-Major, which is somewhat common knowledge in the music community. We will display this information in a smaller pie chart to break up the format of the page.
5. Custom Line or Area Graph Creation (Not shown in sketch)
   We will add one last graph at the bottom of the page where the user can customize the date range they want to see informaiton from, which characteristics they want to plot, and whether they prefer to have the plot as a line or an area chart. For the sake of generalizability, we will limit the available traits for this graph to be the characteristics on a 0-to-1 scale.
   
<img width="520" alt="Screenshot 2023-11-15 at 5 25 48 PM" src="https://github.com/CMU-IDS-Fall-2023/final-project-musicmagicians/assets/80061658/cb86bfce-4920-482c-8625-8d9c1b724c37">

### Data by artist


### Influence data
![](eda_notebooks/images/inf_sketch.jpg "This plot displays sketch for influence data"){width=520 height=1000}


1. Filtering: This step will feature one year slider and one number input to focus on data of interest specified by the users. In particular, since our influence data spans from 1930 to 2010, and includes 5854 unique artists, the information will overflow if we include all in a single visualization. Thus, we give users their options to focus on specific periods and a selection of artists.
2. Artist Network: In influence dataset, each row includes an influencer and his/her follower. This ordered structure naturally induces a directed network of artists, where each node represents an artist, and each outgoing edge indicating the influence. Following the previous selection step, we will visualize a network consisting of top n artists along with their influences on each other.
3. Genre Network: This step will focus on a larger granularity- influence on the genre level. Similar to step 2, we will incorporate a number input box for number of genres and visualize a relationship graph consisting of top n genres. This will facilitate our understanding of how genres imapce each other.



