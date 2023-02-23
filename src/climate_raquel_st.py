# IMPORT NEEDED PACKAGES
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from copy import deepcopy
st.set_page_config(layout="wide")


# SAVE DATA IN CACHE
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# RAW COPY OF THE DATA
df_raw_car = load_data(path="../data/car_clean.csv")
df_car = deepcopy(df_raw_car)
df_raw_co2 = load_data(path="../data/co2_clean.csv")
df_co2 = deepcopy(df_raw_co2)
df_raw_oce = load_data(path="../data/oce_clean.csv")
df_oce = deepcopy(df_raw_oce)
df_raw_ter = load_data(path="../data/ter_clean.csv")
df_ter = deepcopy(df_raw_ter)
df_raw_wat = load_data(path="../data/wat_clean.csv")
df_wat = deepcopy(df_raw_wat)

# BEGINNING APP
#st.title('Clean Energy Sources in Switzerland')
#st.subheader("All renewable-energy power plants supported by the feed-in-tariff KEV")
st.markdown('<div style="text-align:center; font-size:50px; font-weight:bold;">Clean Energy Sources in Switzerland</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:25px; font-weight:normal;">All renewable-energy power plants supported by the feed-in-tariff KEV</div>', unsafe_allow_html=True)
st.markdown('#')

with st.expander("More information "):
    st.write(
        "The feed-in tariff system (KEV) was introduced in 2009 to promote electricity generation from renewable energy. "
        "The processing is carried out by Pronovo AG, but no new systems can be included in the funding."
    )
st.markdown('#')
st.markdown('#')


# BAR PLOT WITH DIFFERENT TYPES OF RENEWAL ENERGY
    #Widget
st.markdown('<div style="text-align:center; font-size:35px; font-weight:bold;">Production and investment in clean energy sources</div>', unsafe_allow_html=True)
st.markdown('#')
energies = ['All'] + sorted(pd.unique(df['energy_source_level_2']))
energy = st.selectbox('Choose clean energy source:', energies)

    #Control flow
if energy == 'All':
    reduced_df = df
else:
    reduced_df = df[df['energy_source_level_2'] == energy]

    #Plot1
col1, padding, col2 = st.columns((4,1,4))

with col1:
    st.markdown('<div style="text-align:center; font-size:20px; font-weight:bold;">Total production per canton</div>', unsafe_allow_html=True)
    bar_plot1 = px.bar(reduced_df, x='canton', y='production', height=None, width=None)
    st.plotly_chart(bar_plot1, use_container_width=True)

    #Plot2
with col2:
    st.markdown('<div style="text-align:center; font-size:20px; font-weight:bold;">Total investment per canton</div>', unsafe_allow_html=True)
    bar_plot2 = px.bar(reduced_df, x='canton', y='tariff', height=None, width=None)
    st.plotly_chart(bar_plot2, use_container_width=True)

st.markdown('#')
st.markdown('#')
st.markdown('#')
st.markdown('#')



# CHOROPLETH WITH DIFFERENT TYPES OF RENEWAL ENERGY
    #Widget
st.markdown('<div style="text-align:center; font-size:35px; font-weight:bold;">Production per Swiss Canton</div>', unsafe_allow_html=True)
st.markdown('#')
energies = ['All'] + sorted(pd.unique(df['energy_source_level_2']) + [' '])
energy2 = st.selectbox('Choose clean energy source:', energies)

    #Plot1: CHOROPLETH MAP1: Production per canton
col3, padding, col4 = st.columns((2,1,2))
col3.markdown('<div style="text-align:left; font-size:20px; font-weight:bold;">Total production per canton</div>', unsafe_allow_html=True)
st.markdown('#')
st.markdown('#')
df_canton = reduced_df.groupby('canton').sum().reset_index()
fig_map1 = px.choropleth_mapbox(df_canton, geojson=geojson, locations='canton', color='production',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           featureidkey="properties.kan_name",
                           zoom=6, center = {"lat": 46.7985624, "lon": 8.2319736},
                           labels={'production'}
                          )
fig_map1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
col3.plotly_chart(fig_map1)


    #Plot 2: CHOROPLETH MAP2: Production per electrical capacity per canton
#right_column.subheader("Total Production / Electrical Capacity")
col4.markdown('<div style="text-align:left; font-size:20px; font-weight:bold;">Total Production / Electrical Capacity per canton</div>', unsafe_allow_html=True)
st.markdown('#')
st.markdown('#')
reduced_df['production/installed MW'] = reduced_df['production']/reduced_df['electrical_capacity']
df_canton2 = reduced_df.groupby('canton').sum().reset_index()

fig_map2 = px.choropleth_mapbox(df_canton2, geojson=geojson, locations='canton', color='production/installed MW',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           featureidkey="properties.kan_name",
                           zoom=6, center = {"lat": 46.7985624, "lon": 8.2319736},
                           labels={'production'}
                          )
fig_map2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
col4.plotly_chart(fig_map2)


# WIDGET: SHOW DATAFRAME
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df)