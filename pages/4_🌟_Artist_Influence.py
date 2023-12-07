import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import networkx as nx 
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config

df = pd.read_csv('Data/influence_data.csv')
st.title('Music Influence')

st.write('Welcome to the Music Influence page! 🌐')
st.write('Feel free to explore the dynamics of genres and artists in this page. ')
st.write('Start by targeting the period and top genres/artists you are interested in.')
st.divider()
st.write('')
c1,c2,c3 = st.columns(3)



with c1:
    year_tuple = st.slider('Time period to focus on:', df['influencer_active_start'].min(), df['influencer_active_start'].max(), (df['influencer_active_start'].min(), df['influencer_active_start'].max()) )

with c2:
    top_g = st.number_input('Top N genres to focus on:', 1, 10, 7)

with c3:
    top_num = st.number_input('Top N influencers to focus on:', 1, df['influencer_name'].nunique(), 10)

tab1, tab2, tab3 = st.tabs(['Overview', 'By Genre', 'By Artist'])
# dataset preparation
# first filter by time period
df2 = df[(df['influencer_active_start']>= year_tuple[0]) & (df['influencer_active_start']<= year_tuple[1])& (df['follower_active_start']>= year_tuple[0])& (df['follower_active_start']<= year_tuple[1])]

inf = df2[['influencer_id','influencer_name','influencer_main_genre','influencer_active_start']].rename(columns = {'influencer_id':'id','influencer_name':'name','influencer_main_genre':'genre','influencer_active_start':'start'})
#st.write('influencer data')
#st.write(inf.shape)


flw = df2[['follower_id','follower_name','follower_main_genre','follower_active_start']].rename(columns = {'follower_id':'id','follower_name':'name','follower_main_genre':'genre','follower_active_start':'start'})
#st.write('follower data')
#st.write(flw.shape)

# concat influencer with follower vertically
all_artists_dup = pd.concat([inf, flw])
#st.write('all artists')
#st.write(all_artists_dup)


# pie chart

# granularity: artist id
# reason: a single artist may possess different style and itentity throughout his/her career
# we treat each id as a unit, to show the rise and fall of different genres
id_genre = all_artists_dup[['id','genre']]
id_genre_unique = id_genre.drop_duplicates()

#st.write(id_genre_unique)
#st.write(id_genre_unique['genre'].value_counts().reset_index().rename(columns = {'index':'genre', 'genre':'count'}))
genre_counts = id_genre_unique['genre'].value_counts().reset_index()#.rename(columns = {'index':'genre', 'genre':'count'})

#st.write('genre counts')
#st.write(genre_counts.index)
#st.write(genre_counts['genre'])
#st.write(genre_counts)


# hover your tooltip around each pie to see the genre!



#pie = base.mark_arc(outerRadius=120)

#text = base.mark_text(radius=200, size=10,radiusOffset=10).encode(text="index:N")

with tab1:
    
    #st.altair_chart(pie)
    fig = px.pie(genre_counts, values='count', names='genre',title='Overall Distribution of Artist Genres')
    fig.update_layout(legend_title_text='Genre')
    st.plotly_chart(fig, use_container_width=True)
    st.write('🌟Hover your mouse around each slice to see the genre & count')
    #st.write(genre_counts)
    genre_chart = alt.Chart(genre_counts,title = f'Artist Counts in All Genres').mark_bar().encode(
    alt.X('count:Q', title = 'Artist Count'),
    y = alt.Y('genre:O', title = 'Genre').sort('-x')
    ).properties(height = 700, width = 700)

    st.altair_chart(genre_chart)
    st.write('🌟Hover your mouse around each bar to see the genre & count')
    


with tab2:
# Top 4 genres distribution

    #st.write(genre_counts.head(top_g)['genre'])
    top4_genres = genre_counts[:top_g]['genre'].values
    #st.write('top 4 genres')
    #st.write(top4_genres)
    id_genre_start = all_artists_dup[['id','genre','start']].drop_duplicates()
    id_genre_start_top4 = id_genre_start[id_genre_start['genre'].isin(top4_genres)]
    year_genre_counts = pd.pivot_table(id_genre_start_top4 , index = 'start',columns = 'genre', aggfunc = 'count').fillna(0)
    year_genre_counts = year_genre_counts['id']
    year_genre_counts = year_genre_counts.reset_index()
    

    genre_viz = year_genre_counts.melt(id_vars=["start"],
            var_name="Genre",
            value_name="Value")
    area_title =f'Artist Population in Top {top_g} Genres Over Time'
    areas = alt.Chart(genre_viz, title = area_title).mark_area(
        interpolate='monotone',
        fillOpacity=0.5,
        stroke='lightgray',
        strokeWidth=0.5

    ).encode(

        alt.X('start',title = 'Artist Active Start'),
        alt.Y('Value',title = 'Count'),
        alt.Color('Genre',legend = None),
      alt.Row('Genre', center = True, title = 'Genre',sort ={"op": "count", "field": "Genre"})

        ).properties(
        width = 570,
        height = 50

        )


    # Genre network

    top4_genre_counts = genre_counts[:top_g]
    #st.write('top 4 genre counts')
    #st.write(top4_genre_counts)


    top4_genre_viz = top4_genre_counts.reset_index()
    #st.write(top4_genre_viz )
    #st.write(topn_viz)
    top4_genre_chart = alt.Chart(top4_genre_viz,title = f'Artist Counts in Top {top_g} Genres').mark_bar().encode(
        alt.X('count:Q', title = 'Artist Count'),
        y = alt.Y('genre:O', title = 'Genre').sort('-x')

        ).properties(height = 400, width = 700)

    st.altair_chart(top4_genre_chart)

    st.altair_chart(areas)


    nodesg = []
    edgesg = []

    # add nodes
    iter = 0
    for genre in top4_genres:
      nodesg.append(
                Node(id = genre,
                    label = genre,
                    size = 5+ int(top4_genre_counts[top4_genre_counts['genre'] == genre]['count'])* 0.02,
                    #sshape = 'circularImage',
                    )
       )


     # focus on influence relationship only
    inf_flw_genre = df[['influencer_main_genre','follower_main_genre']]
    inf_flw_genre.drop_duplicates(inplace=True)


    # filter out influence relationship among top 4 genres
    top4_genres_inf = inf_flw_genre[(inf_flw_genre['influencer_main_genre'].isin(top4_genres)) & (inf_flw_genre['follower_main_genre'].isin(top4_genres)) & (inf_flw_genre['influencer_main_genre']!=inf_flw_genre['follower_main_genre'])]


    # add edges
    for row in top4_genres_inf.itertuples(index = False):
        
        edgesg.append(
                Edge(source= row.influencer_main_genre,
                    #label = 'influence',
                    target =  row.follower_main_genre
                    )
            )

    st.write(f"#### Influence Dynamic Among Top {top_g} Genres")
    st.write('🌟Drag the network around to better see the influence')
    on = st.toggle('Fix the genre network in place')

    if on:
        st.write('Network position fixed!')
        phys = False
    else:
        st.write('Network position free to drag!')
        phys = True

    config1 = Config(width=600,
                    height=500,
                    directed=True, 
                    physics= phys, 
                    hierarchical=False,
                    # **kwargs
                    )

    #st.write(f"**Influence Dynamic Among Top {top_g} Genres**")
    

    return_value_g = agraph(nodes=nodesg, 
          edges=edgesg, 
          config=config1)



with tab3:
#st.write('year filtered len', len(df2))
    influencer_counts = pd.DataFrame(df2['influencer_name'].value_counts()).reset_index()#.rename(columns = {'influencer_name':'count','index':'influencer_name'})
    #st.write(influencer_counts)
    #influencer_counts = pd.read_csv('Data/influencer_count.csv')
    #st.write('influencer counts')
    #st.write(influencer_counts)
    topn_inf = pd.DataFrame(influencer_counts.iloc[:top_num])
    #st.write('topn_inf')
    #st.write(topn_inf)
    #st.dataframe(topn_inf)
    topn_data = df2[(df2['influencer_name'].isin(topn_inf.influencer_name)) & (df2['follower_name'].isin(topn_inf.influencer_name))]
    #st.write('topn_data')
    #st.write(topn_data)

    #st.write('topn_inf')
    #st.write(topn_inf)
    #st.write('topn_data')
    #st.write(topn_data)
    #st.write(topn_viz)
    topn_chart = alt.Chart(topn_inf, title = f"Top {top_num} Influencers and Their Follower Count").mark_bar().encode(
        x = alt.X('count:Q', title = 'Follower Count'),
        y = alt.Y('influencer_name:O',title = 'Influencer Name').sort('-x')

        ).properties(height = 400, width = 700)

    st.altair_chart(topn_chart)

    #st.write(int(topn_inf[topn_inf['influencer_name'] == 'Bob Dylan']['count']))

    nodes = []
    edges = []
    #st.write(topn_inf[topn_inf['influencer_name'] == 'The Beatles']['count'][0])
    for name in topn_inf['influencer_name']:
        nodes.append(
                Node(id = name,
                    label = name,
                    size = 10 + int(topn_inf[topn_inf['influencer_name'] == name]['count'])* 0.05,
                    #sshape = 'circularImage',
                    )
            )

    for row in topn_data.itertuples(index = False):
        #st.write(row)
        edges.append(
                Edge(source= row.influencer_name,
                    #label = 'influence',
                    target =  row.follower_name

                    )
            )
        

            
    st.write(f"**Influence Dynamics Among Top {top_num} Influencers**")
    st.write('')
    st.write('🌟Drag the network around to better see the influence')

    on2 = st.toggle('Fix the artist network in place')

    if on2:
        st.write('Network position fixed!')
        phys2 = False
    else:
        st.write('Network position free to drag!')
        phys2 = True

    config2 = Config(width=700,
                    height=500,
                    directed=True, 
                    physics=phys2, 
                    hierarchical=False,
                    # **kwargs
                    )
    return_value = agraph(nodes=nodes, 
                          edges=edges, 
                          config=config2)
    























