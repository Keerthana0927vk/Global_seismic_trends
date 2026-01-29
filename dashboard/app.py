import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
#page config
st.set_page_config(
    page_title="Global seismic trends",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Global seismic Trends Dashboard")
st.markdown("Interactive analysis of worldwide earthquakes (Last 5 Years)")

#Database connection
def load_data():
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Keerthana7886@",
        database="global_seismic_trends"
    )

    query="SELECT * FROM earthquakes"
    df=pd.read_sql(query,conn)
    conn.close()
    return df
df=load_data()
#sidebar filters
st.sidebar.subheader("Map Controls")

max_points = st.sidebar.slider(
    "Number of earthquakes to display on map",
    min_value=500,
    max_value=10000,
    value=3000,
    step=500
)
st.sidebar.header("Filters")

year_filter=st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique()),
)
mag_range=st.sidebar.slider(
    "Magnitude_range",
    float(df["mag"].min()),
    float(df["mag"].max()),
    (float(df["mag"].min()),float(df["mag"].max()))
)

country_filter=st.sidebar.multiselect(
    "Country",
    options=sorted(df["country"].unique()),
    default=[]
)
#Apply filters
filtered_df=df[
    (df["year"].isin(year_filter))&
    (df["mag"].between(mag_range[0],mag_range[1]))
]
if country_filter:
    filtered_df=filtered_df[filtered_df["country"].isin(country_filter)]
#KPIs
col1,col2,col3,col4=st.columns(4)

col1.metric("Total Earthquakes",len(filtered_df))
avg_mag=round(filtered_df["mag"].mean(),2)if len(filtered_df)>0 else 0
col2.metric("Avg Magnitude",avg_mag)
col3.metric("Strong Quakes(mag>6)",filtered_df["strong_quake_flag"].sum())
col4.metric("Tsunamis Triggered",(filtered_df["tsunami"]==1).sum())

st.divider()
#charts
year_chart=(
    filtered_df.groupby("year")
    .size()
    .reset_index(name="count")
)
fig_year=px.bar(
    year_chart,
    x="year",
    y="count",
    title="Earthquakes per year"
)
st.plotly_chart(fig_year,use_container_width=True)
#2.magnitude distribution
fig_mag=px.histogram(
    filtered_df,
    x="mag",
    nbins=30,
    title="Magnitude Distribution"
)
st.plotly_chart(fig_mag,use_container_width=True)
#3.Top countries by earthquakes
top_countries=(
    filtered_df.groupby("country")
    .size()
    .reset_index(name="count")
    .sort_values("count",ascending=False)
    .head(10)
)
fig_country=px.bar(
    top_countries,
    x="country",
    y="count",
    title="Top 10 Countries by Eartquake count"
)
st.plotly_chart(fig_country,use_container_width=True)
#4.Earthquake map
# 4. Earthquake Map (User-controlled)
map_df = (
    filtered_df
    .sort_values("mag", ascending=False)
    .head(max_points)
)

fig_map = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    color="mag",
    size="mag",
    projection="natural earth",
    title=f"Global Earthquake Map (Top {max_points} by Magnitude)"
)

st.plotly_chart(fig_map, use_container_width=True)

#Data perview
st.subheader("Data perview")
st.dataframe(filtered_df.head(100))