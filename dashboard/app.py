import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

#  PAGE CONFIG 
st.set_page_config(
    page_title="Global Seismic Trends",
    layout="wide"
)

st.title(" Global Seismic Trends Dashboard")
st.markdown("Interactive analysis of worldwide earthquakes (Last 5 Years)")

#  DB CONNECTION 
@st.cache_data
def load_data():
    DB_USER = "root"
    DB_PASSWORD = quote_plus("Keerthana7886@")
    DB_HOST = "localhost"
    DB_NAME = "global_seismic_trends"

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    df = pd.read_sql("SELECT * FROM earthquakes", engine)
    return df

df = load_data()

#  SIDEBAR FILTERS 
st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

mag_range = st.sidebar.slider(
    "Magnitude Range",
    float(df["mag"].min()),
    float(df["mag"].max()),
    (float(df["mag"].min()), float(df["mag"].max()))
)

country_filter = st.sidebar.multiselect(
    "Country",
    options=sorted(df["country"].unique()),
    default=[]
)

# Apply filters
filtered_df = df[
    (df["year"].isin(year_filter)) &
    (df["mag"].between(mag_range[0], mag_range[1]))
]

if country_filter:
    filtered_df = filtered_df[filtered_df["country"].isin(country_filter)]

#  KPI 
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Earthquakes", len(filtered_df))
col2.metric("Avg Magnitude", round(filtered_df["mag"].mean(), 2))
col3.metric("Strong Quakes (mag>6)", filtered_df["strong_quake_flag"].sum())
col4.metric("Tsunamis", (filtered_df["tsunami"] == 1).sum())

st.divider()

#  OVERVIEW CHARTS  

# Year chart
year_chart = filtered_df.groupby("year").size().reset_index(name="count")
st.plotly_chart(px.bar(year_chart, x="year", y="count", title="Earthquakes per Year"), use_container_width=True)

# Magnitude distribution
st.plotly_chart(px.histogram(filtered_df, x="mag", nbins=30, title="Magnitude Distribution"), use_container_width=True)

# Top countries
top_countries = filtered_df.groupby("country").size().reset_index(name="count").sort_values("count", ascending=False).head(10)
st.plotly_chart(px.bar(top_countries, x="country", y="count", title="Top Countries"), use_container_width=True)

# Map
map_df = filtered_df.sort_values("mag", ascending=False).head(3000)
st.plotly_chart(px.scatter_geo(map_df, lat="latitude", lon="longitude", size="mag", color="mag"), use_container_width=True)

#  INSIGHTS SIDEBAR 

st.sidebar.divider()
st.sidebar.header(" Insights Explorer")

category = st.sidebar.selectbox(
    "Select Category",
    ["Basic Insights", "Trend Analysis", "Advanced Insights"]
)

if category == "Basic Insights":
    options = [
        "Top 10 Strongest Earthquakes",
        "Top 10 Deepest Earthquakes",
        "Total Earthquakes",
        "Top Networks",
        "Alert Levels",
        "Status Distribution",
        "Type Distribution",
        "Strong Earthquake %",
        "Tsunami Distribution",
        "Magnitude Distribution"
    ]

elif category == "Trend Analysis":
    options = [
        "Yearly Trend",
        "Monthly Trend",
        "Day-wise Trend",
        "Top Countries",
        "Avg Magnitude by Country",
        "Tsunami per Year",
        "High Station Count",
        "Depth Category Analysis",
        "Equatorial Analysis",
        "Deep Earthquakes by Country"
    ]

else:
    options = [
        "High Magnitude Shallow Quakes",
        "Avg Depth per Country",
        "Avg Magnitude by magType",
        "Data Quality Metrics",
        "RMS & GAP Analysis",
        "YOY Growth",
        "Shallow vs Deep Ratio",
        "Tsunami vs Magnitude",
        "Close-Time Earthquakes",
        "Top Countries by Frequency & Magnitude"
    ]

insight_option = st.sidebar.selectbox("Select Insight", options)

#  INSIGHT OUTPUT 

st.divider()
st.subheader(" Selected Insight")

# BASIC
if insight_option == "Top 10 Strongest Earthquakes":
    st.dataframe(filtered_df.nlargest(10, "mag"))

elif insight_option == "Top 10 Deepest Earthquakes":
    st.dataframe(filtered_df.nlargest(10, "depth_km"))

elif insight_option == "Total Earthquakes":
    st.metric("Total Earthquakes", len(filtered_df))

elif insight_option == "Top Networks":
    st.bar_chart(filtered_df["net"].value_counts().head(10))

elif insight_option == "Alert Levels":
    st.bar_chart(filtered_df["alert"].value_counts())

elif insight_option == "Status Distribution":
    st.bar_chart(filtered_df["status"].value_counts())

elif insight_option == "Type Distribution":
    st.bar_chart(filtered_df["type"].value_counts().head(10))

elif insight_option == "Strong Earthquake %":
    st.metric("Strong %", f"{filtered_df['strong_quake_flag'].mean()*100:.2f}%")

elif insight_option == "Tsunami Distribution":
    st.bar_chart(filtered_df["tsunami_flag"].value_counts())

elif insight_option == "Magnitude Distribution":
    st.plotly_chart(px.histogram(filtered_df, x="mag"))

# TREND
elif insight_option == "Yearly Trend":
    st.bar_chart(filtered_df.groupby("year").size())

elif insight_option == "Monthly Trend":
    st.line_chart(filtered_df.groupby("month").size())

elif insight_option == "Day-wise Trend":
    st.bar_chart(filtered_df.groupby("day_of_week").size())

elif insight_option == "Top Countries":
    st.bar_chart(filtered_df["country"].value_counts().head(10))

elif insight_option == "Avg Magnitude by Country":
    st.bar_chart(filtered_df.groupby("country")["mag"].mean().head(10))

elif insight_option == "Tsunami per Year":
    st.bar_chart(filtered_df[filtered_df["tsunami"] == 1].groupby("year").size())

elif insight_option == "High Station Count":
    st.metric("Count", filtered_df[filtered_df["nst"] > 50].shape[0])

elif insight_option == "Depth Category Analysis":
    st.bar_chart(filtered_df["depth_category"].value_counts())

elif insight_option == "Equatorial Analysis":
    st.dataframe(filtered_df[(filtered_df["latitude"].between(-5, 5))].head(100))

elif insight_option == "Deep Earthquakes by Country":
    st.bar_chart(filtered_df[filtered_df["depth_km"] > 300]["country"].value_counts().head(10))

# ADVANCED
elif insight_option == "High Magnitude Shallow Quakes":
    st.dataframe(filtered_df[(filtered_df["depth_km"] < 50) & (filtered_df["mag"] > 7.5)])

elif insight_option == "Avg Depth per Country":
    st.bar_chart(filtered_df.groupby("country")["depth_km"].mean().head(10))

elif insight_option == "Avg Magnitude by magType":
    st.bar_chart(filtered_df.groupby("magType")["mag"].mean())

elif insight_option == "Data Quality Metrics":
    st.write({
        "origin": filtered_df["types"].str.contains("origin", na=False).sum(),
        "phase": filtered_df["types"].str.contains("phase", na=False).sum()
    })

elif insight_option == "RMS & GAP Analysis":
    st.dataframe(filtered_df.groupby("country")[["rms", "gap"]].mean().head(20))

elif insight_option == "YOY Growth":
    st.line_chart(filtered_df.groupby("year").size().pct_change()*100)

elif insight_option == "Shallow vs Deep Ratio":
    ratio = filtered_df.groupby("country")["depth_category"].value_counts().unstack().fillna(0)
    ratio["ratio"] = ratio.get("shallow",0)/(ratio.get("deep",0)+1)
    st.dataframe(ratio.head(20))

elif insight_option == "Tsunami vs Magnitude":
    st.bar_chart(filtered_df.groupby("tsunami_flag")["mag"].mean())

elif insight_option == "Close-Time Earthquakes":
    temp = filtered_df.sort_values("time")
    temp["diff"] = temp["time"].diff().dt.total_seconds()/60
    st.dataframe(temp[temp["diff"] < 60].head(20))

elif insight_option == "Top Countries by Frequency & Magnitude":
    st.dataframe(filtered_df.groupby("country").agg(freq=("id","count"), avg_mag=("mag","mean")).head(10))