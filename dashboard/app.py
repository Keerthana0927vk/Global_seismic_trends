import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import plotly.express as px


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Seismic Trends Dashboard",
    layout="wide"
)

st.title(" Global Seismic Trends Dashboard")
st.write("Interactive Dashboard for Earthquake Analysis")


# DATABASE CONNECTION
DB_USER = "root"
DB_PASSWORD = quote_plus("Keerthana7886@")
DB_HOST = "localhost"
DB_NAME = "global_seismic_trends"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)


# SIDEBAR FILTERS
st.sidebar.header("Filters")

# Year Filter
year_df = pd.read_sql(
    "SELECT DISTINCT year FROM earthquakes ORDER BY year",
    engine
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + year_df["year"].astype(str).tolist()
)

# Country Filter
country_df = pd.read_sql(
    "SELECT DISTINCT country FROM earthquakes WHERE country IS NOT NULL ORDER BY country",
    engine
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + country_df["country"].tolist()
)

# Magnitude Filter
selected_mag = st.sidebar.slider(
    "Minimum Magnitude",
    min_value=2.5,
    max_value=10.0,
    value=2.5,
    step=0.1
)


# SQL ANALYSIS
st.subheader("SQL Analysis")

sql_queries = {

"1. Top 10 Strongest Earthquakes":
"""
SELECT place,country,mag,time
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;
""",

"2. Top 10 Deepest Earthquakes":
"""
SELECT place,country,depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;
""",

"3. High Magnitude Shallow Quakes":
"""
SELECT *
FROM earthquakes
WHERE mag>7.5
AND depth_km<50;
""",

"4. Average Depth per Country":
"""
SELECT country,
AVG(depth_km) AS avg_depth
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC
LIMIT 10;
""",

"5. Average Magnitude by magType":
"""
SELECT magType,
AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY magType
ORDER BY avg_mag DESC;
""",

"6. Earthquakes per Year":
"""
SELECT year,
COUNT(*) AS total
FROM earthquakes
GROUP BY year
ORDER BY year;
""",

"7. Earthquakes per Month":
"""
SELECT month,
COUNT(*) AS total
FROM earthquakes
GROUP BY month
ORDER BY month;
""",

"8. Earthquakes per Day":
"""
SELECT day_of_week,
COUNT(*) AS total
FROM earthquakes
GROUP BY day_of_week;
""",

"9. Top Networks":
"""
SELECT net,
COUNT(*) AS total
FROM earthquakes
GROUP BY net
ORDER BY total DESC
LIMIT 10;
""",

"10. Total Earthquakes":
"""
SELECT COUNT(*) AS Total_Earthquakes
FROM earthquakes;
""",

"11. Alert Levels":
"""
SELECT DISTINCT alert
FROM earthquakes;
""",

"12. Status Distribution":
"""
SELECT status,
COUNT(*) AS total
FROM earthquakes
GROUP BY status;
""",

"13. Type Distribution":
"""
SELECT type,
COUNT(*) AS total
FROM earthquakes
GROUP BY type;
""",

"14. Data Quality":
"""
SELECT
SUM(types LIKE '%origin%') AS origin,
SUM(types LIKE '%phase-data%') AS phase_data,
SUM(types LIKE '%dyfi%') AS dyfi
FROM earthquakes;
""",

"15. Average RMS & GAP":
"""
SELECT country,
AVG(rms) AS avg_rms,
AVG(gap) AS avg_gap
FROM earthquakes
GROUP BY country;
""",

"16. High Station Count":
"""
SELECT *
FROM earthquakes
WHERE nst>50;
""",

"17. Tsunami Events per Year":
"""
SELECT year,
COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami=1
GROUP BY year;
""",

"18. Alert Level Count":
"""
SELECT alert,
COUNT(*) AS total
FROM earthquakes
GROUP BY alert;
""",

"19. Top 5 Countries by Average Magnitude":
"""
SELECT country,
AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5;
""",

"20. Countries with Shallow & Deep":
"""
SELECT country,year,month,
COUNT(DISTINCT depth_category) AS depth_types
FROM earthquakes
GROUP BY country,year,month
HAVING COUNT(DISTINCT depth_category)>1;
""",

"21. Year over Year Growth":
"""
SELECT year,
COUNT(*) AS total
FROM earthquakes
GROUP BY year;
""",

"22. Top 3 Countries":
"""
SELECT country,
COUNT(*) AS frequency,
AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY frequency DESC
LIMIT 3;
""",

"23. Equatorial Region":
"""
SELECT country,
AVG(depth_km) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;
""",

"24. Shallow vs Deep":
"""
SELECT country,
SUM(depth_category='Shallow') AS shallow,
SUM(depth_category='Deep') AS deep
FROM earthquakes
GROUP BY country;
""",

"25. Tsunami vs Magnitude":
"""
SELECT tsunami_flag,
AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY tsunami_flag;
""",

"26. Poor Quality Signals":
"""
SELECT place,country,gap,rms
FROM earthquakes
ORDER BY gap DESC,rms DESC
LIMIT 10;
""",

"27. Close Time Earthquakes":
"""
SELECT id,place,time
FROM earthquakes
ORDER BY time;
""",

"28. Deep Earthquakes":
"""
SELECT country,
COUNT(*) AS total
FROM earthquakes
WHERE depth_km>300
GROUP BY country;
""",

"29. Strong Earthquake Percentage":
"""
SELECT ROUND(AVG(strong_quake_flag)*100,2) AS strong_percentage
FROM earthquakes;
""",

"30. Average Magnitude by Depth":
"""
SELECT depth_category,
AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY depth_category;
"""

}

selected_query = st.selectbox(
    "Select SQL Analysis",
    list(sql_queries.keys())
)

run = st.button(" Run Query")

# RUN QUERY

if run:

    query = sql_queries[selected_query]

    try:

        result = pd.read_sql(query, engine)

        st.success(" Query Executed Successfully")

        
        # CHART
        st.subheader(" Visualization")

        if selected_query == "4. Average Depth per Country":

            fig = px.bar(
                result,
                x="country",
                y="avg_depth",
                title="Average Depth by Country"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "5. Average Magnitude by magType":

            fig = px.bar(
                result,
                x="magType",
                y="avg_mag",
                title="Average Magnitude by magType"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "6. Earthquakes per Year":

            fig = px.line(
                result,
                x="year",
                y="total",
                markers=True,
                title="Earthquakes per Year"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "7. Earthquakes per Month":

            fig = px.bar(
                result,
                x="month",
                y="total",
                title="Earthquakes per Month"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "8. Earthquakes per Day":

            fig = px.bar(
                result,
                x="day_of_week",
                y="total",
                title="Earthquakes by Day of Week"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "9. Top Networks":

            fig = px.bar(
                result,
                x="net",
                y="total",
                title="Top Networks"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "17. Tsunami Events per Year":

            fig = px.line(
                result,
                x="year",
                y="tsunami_events",
                markers=True,
                title="Tsunami Events per Year"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "18. Alert Level Count":

            fig = px.pie(
                result,
                names="alert",
                values="total",
                title="Alert Level Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "19. Top 5 Countries by Average Magnitude":

            fig = px.bar(
                result,
                x="country",
                y="avg_mag",
                title="Top 5 Countries by Average Magnitude"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "22. Top 3 Countries":

            fig = px.bar(
                result,
                x="country",
                y="frequency",
                title="Top 3 Countries"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "28. Deep Earthquakes":

            fig = px.bar(
                result,
                x="country",
                y="total",
                title="Deep Earthquakes (>300 km)"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif selected_query == "30. Average Magnitude by Depth":

            fig = px.bar(
                result,
                x="depth_category",
                y="avg_mag",
                title="Average Magnitude by Depth Category"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:

            st.info("No chart available for this analysis.")


        # RESULT TABLE
        st.subheader(" Query Result")

        st.dataframe(result, use_container_width=True)

    except Exception as e:

        st.error(f" {e}")


# FOOTER


st.markdown("---")
st.markdown(
    "<center><b>Developed by Keerthana | Global Seismic Trends Project</b></center>",
    unsafe_allow_html=True
)