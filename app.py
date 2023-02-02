import streamlit as st
import  pandas as pd
import plotly_express as px
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import calendar
import numpy as np
st.set_page_config(initial_sidebar_state="expanded")
st.title('California Wildfire Analysis')
st.text('This Webapp Analysis the California wildfire between year 2013 to 2019')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: visible;}
            footer:after{
                content: 'Made by Vedant Goswami';
                display: block;
                position: relative;
                color: tomato;
                top: 3px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Data cleaning
def df_cleaning(df):
    columns_to_drop = ['Active','Featured', 'Final', 'PercentContained','Public', 'SearchKeywords', 'Status']
    df.drop(columns_to_drop, axis='columns', inplace=True)
    df['Started'] = pd.to_datetime(df['Started'])
    df['Updated'] = pd.to_datetime(df['Updated'])
    df['Extinguished'] = pd.to_datetime(df['Extinguished'])

    df['YearStarted'] = df['Started'].dt.year
    df['MonthStarted'] = df['Started'].dt.month
    df = df[df.YearStarted != 1969]

    df.fillna({'AcresBurned': 0, 'AirTankers': 0, 'ConditionStatement':'', 'ControlStatement':'', 
                    'CrewsInvolved': 0, 'Dozers': 0, 'Engines': 0, 'Extinguished': 0, 'Fatalities': 0,
                'FuelType':'', 'Helicopters': 0, 'Injuries': 0, 'PersonnelInvolved': 0,
                'SearchDescription':'', 'StructuresDamaged': 0, 'StructuresDestroyed': 0,
                'StructuresEvacuated': 0, 'StructuresThreatened': 0, 'WaterTenders': 0}, inplace=True)

    df['AcresBurned'] = df['AcresBurned'].astype('int64')
    df['AirTankers'] = df['AirTankers'].astype('int64')
    df['CrewsInvolved'] = df['CrewsInvolved'].astype('int64')
    df['Dozers'] = df['Dozers'].astype('int64')
    df['Engines'] = df['Engines'].astype('int64')
    df['Fatalities'] = df['Fatalities'].astype('int64')
    df['Injuries'] = df['Injuries'].astype('int64')
    df['Helicopters'] = df['Helicopters'].astype('int64')
    df['PersonnelInvolved'] = df['PersonnelInvolved'].astype('int64')
    df['StructuresDamaged'] = df['StructuresDamaged'].astype('int64')
    df['StructuresDestroyed'] = df['StructuresDestroyed'].astype('int64')
    df['StructuresEvacuated'] = df['StructuresEvacuated'].astype('int64')
    df['StructuresThreatened'] = df['StructuresThreatened'].astype('int64')
    df['WaterTenders'] = df['WaterTenders'].astype('int64')
def stats(data):
    st.header('Data Statistics')
    st.write(data.describe())

def data_header(data):
    st.header('Data Header')
    st.write(data.head())


df = pd.read_csv('California_Fire_Incidents.csv')
df_cleaning(df)
st.sidebar.title('Navigation')
options = st.sidebar.selectbox(
    'Select the Page',
    ('Home',
    'Statistics',
     'Data Header',
     'Affected Counties',
     'Geospatial Visualization',
     'Fire Incident Frequency')
)

if options == 'Home':
    st.markdown("California is one of the places having the most deadliest and destructive wildfire seasons. The dataset contains the list of Wildfires that has occurred in California between 2013 and 2020. The dataset contains the location where wildfires have occurred including the County name, latitude and longitude values and also details on when the wildfire has started.")
    st.image("image.jpeg")
elif options == 'Statistics':
    stats(df)
elif options == 'Data Header':
    data_header(df)
elif options == 'Fire Incident Frequency':
    st.header('Fire Incident Frequency')
    sel = st.radio('Type',options=['Year wise','Month wise'])
    if sel == 'Year wise':
        df['YearStarted'].value_counts().sort_index().plot(kind='bar', figsize=(12,7))
        new_df=df['YearStarted'].value_counts().sort_index()
        new_df = pd.DataFrame({'YearStarted': new_df.index,'counts': new_df.values}).iloc[1:]
        fig = px.bar(new_df,x="YearStarted",y="counts",color='counts')
        # plt.xlabel('Year')
        # plt.ylabel('Number of Fire Incidents')
        # plt.title('Frequency of Fire Incidents per Year Between 2013-2019')
        st.plotly_chart(fig)
    else:
        df['MonthStarted'].value_counts().sort_index().plot(kind='bar', figsize=(12,7))
        new_df=df['MonthStarted'].value_counts().sort_index()
        new_df = pd.DataFrame({'MonthStarted': new_df.index,'counts': new_df.values})
        mapping = {index: month for index, month in enumerate(calendar.month_abbr) if month}
        print(mapping)
        new_df['MonthStarted']=new_df['MonthStarted'].apply(lambda x: mapping[x])
        fig = px.bar(new_df,x="MonthStarted",y="counts",color='counts')
        # plt.xlabel('Year')
        # plt.ylabel('Number of Fire Incidents')
        # plt.title('Frequency of Fire Incidents per Year Between 2013-2019')
        st.plotly_chart(fig)
elif options=="Affected Counties":
    st.header('Top Most Counties where Fires Occur Between 2013-2019')
    sel = st.radio('Top',options=['10','20','30','ALL'],horizontal=True)
    counties=0
    if sel=='10':
        counties = 10
    elif sel == '20':
        counties = 20
    elif sel == '30':
        counties = 30
    else:
        counties=len(df.Counties.unique())
    new_df=df['Counties'].value_counts().sort_values()[::-1][:counties]
    new_df = pd.DataFrame({'Counties': new_df.index,'counts': new_df.values})
    fig = px.bar(new_df,x="Counties",y="counts",color='counts')
        # plt.xlabel('Year')
        # plt.ylabel('Number of Fire Incidents')
        # plt.title('Frequency of Fire Incidents per Year Between 2013-2019')
    st.plotly_chart(fig)
elif options == 'Geospatial Visualization':
    sel = st.radio('Type',options=['HeatMap','Scatter Plot'],horizontal=True)
    zoom_factor = 5
    radius_scaling = 50
    if sel == 'HeatMap':
        my_map_2 = folium.Map(location=[36,-120], zoom_start=zoom_factor)
        HeatMap(data=df[['Latitude', 'Longitude']], radius=10).add_to(my_map_2)
        st_data=folium_static(my_map_2,width=725)
    else:
        my_map_1 = folium.Map(location=[36,-120], zoom_start=zoom_factor)
        for i in range(0,df.shape[0]):
            folium.Circle(
                location=[df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
                radius=np.sqrt(df.iloc[i]['AcresBurned'])*radius_scaling,
                color='red',
                popup='CanonicalUrl:' + df.iloc[i]['CanonicalUrl'] + ' - Year:' + str(int(df.iloc[i]['ArchiveYear'])) + ' - Acres Burned:' 
                + str(df.iloc[i]['AcresBurned']),
                fill=True,
                fill_color='red'
            ).add_to(my_map_1)
        st_data=folium_static(my_map_1,width=725)