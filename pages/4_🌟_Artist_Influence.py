import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import networkx as nx 
from vega_datasets import data
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
	top_num = st.number_input('Top N influencers to focus on:', 1, df['influencer_name'].nunique(), 11)

tab1, tab2, tab3 = st.tabs(['Overview', 'By Genre', 'By Artist'])
# dataset preparation
# first filter by time period
df2 = df[(df['influencer_active_start']>= year_tuple[0]) & (df['influencer_active_start']<= year_tuple[1])]

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
genre_counts = pd.read_csv('Data/genre_counts.csv')

#st.write('genre counts')
#st.write(genre_counts)


# hover your tooltip around each pie to see the genre!
base = alt.Chart(genre_counts, title = 'Overall Distribution of Artist Genres').encode(
    alt.Theta("genre:Q", stack=True),
    alt.Color("index:N"),
    tooltip=['index']
)

pie = base.mark_arc(outerRadius=120)
#text = base.mark_text(radius=200, size=10,radiusOffset=10).encode(text="index:N")

with tab1:
	st.altair_chart(pie)


with tab2:
# Top 4 genres distribution


	top4_genres = genre_counts.head(top_g)['index']
	st.write(genre_counts)
	st.write(top4_genres )
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

	top4_genre_counts = genre_counts.head(top_g).set_index(['index'])


	top4_genre_viz = top4_genre_counts.reset_index()
	#st.write(topn_viz)
	top4_genre_chart = alt.Chart(top4_genre_viz,title = f'Artist Counts in Top {top_g} Genres').mark_bar().encode(
		alt.X('genre:Q', title = 'Artist Count'),
		y = alt.Y('index:O', title = 'Genre').sort('-x')

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
					size = 5+ top4_genre_counts.loc[genre]['genre']* 0.02,
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

	config1 = Config(width=500,
	                height=400,
	                directed=True, 
	                physics=True, 
	                hierarchical=False,
	                title = f"Influence Dynamic Among Top {top_g} Genres"
	                # **kwargs
	                )

	st.write(f"**Influence Dynamic Among Top {top_g} Genres**")

	return_value_g = agraph(nodes=nodesg, 
	      edges=edgesg, 
	      config=config1)
	st.write('🌟Drag the network around to better see the influence')




#st.write('min year',year_tuple[0])
#st.write('max year',year_tuple[1])

#st.write('original len', len(df))

with tab3:
#st.write('year filtered len', len(df2))

	topn_inf = pd.DataFrame(df2['influencer_name'].value_counts().iloc[:top_num])
	topn_inf = topn_inf.rename(columns={'influencer_name':'count'})
	topn_data = df2[(df2['influencer_name'].isin(topn_inf.index)) & (df2['follower_name'].isin(topn_inf.index))]

	#st.write('topn_inf')
	#st.write(topn_inf)
	#st.write('topn_data')
	#st.write(topn_data)
	topn_viz = topn_inf.reset_index()
	#st.write(topn_viz)
	topn_chart = alt.Chart(topn_viz, title = f"Top {top_num} Influencers and Their Follower Count").mark_bar().encode(
		x = alt.X('count:Q', title = 'Follower Count'),
		y = alt.Y('index:O',title = 'Influencer Name').sort('-x')

		).properties(height = 400, width = 700)

	st.altair_chart(topn_chart)

	nodes = []
	edges = []

	for name in topn_inf.index:
		nodes.append(
				Node(id = name,
					label = name,
					size = 10 + topn_inf.loc[name]['count']* 0.05,
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
	
	config2 = Config(width=700,
	                height=500,
	                directed=True, 
	                physics=True, 
	                hierarchical=False,
	                # **kwargs
	                )

	return_value = agraph(nodes=nodes, 
	                      edges=edges, 
	                      config=config2)
	st.write('🌟Drag the network around to better see the influence')























