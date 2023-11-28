import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import networkx as nx 
from streamlit_agraph import agraph, Node, Edge, Config

df = pd.read_csv('data/influence_data.csv')

c1,c2,c3 = st.columns(3)

with c1:
	year_tuple = st.slider('Influencer Start Year:', df['influencer_active_start'].min(), df['influencer_active_start'].max(), (df['influencer_active_start'].min(), df['influencer_active_start'].max()) )

with c2:
	st.write('')

with c3:
	top_num = st.number_input('Top N influencers to focus on:', 1, df['influencer_name'].nunique(), 10)

st.write('min year',year_tuple[0])
st.write('max year',year_tuple[1])

st.write('original len', len(df))

df2 = df[(df['influencer_active_start']>= year_tuple[0]) & (df['influencer_active_start']<= year_tuple[1])]

st.write('year filtered len', len(df2))

topn_inf = pd.DataFrame(df2['influencer_name'].value_counts().iloc[:top_num])
topn_inf = topn_inf.rename(columns={'influencer_name':'count'})
topn_data = df2[(df2['influencer_name'].isin(topn_inf.index)) & (df2['follower_name'].isin(topn_inf.index))]
st.title(f"Top {top_num} Influencers and Their Follower Count")

st.write(topn_inf)
st.write(topn_data)


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
	

        
st.title(f"Top {top_num} Influencers Network")
config = Config(width=400,
                height=400,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)