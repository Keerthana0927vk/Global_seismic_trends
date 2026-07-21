# analyze_data.py

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Database Connection
DB_USER = "root"
DB_PASSWORD = quote_plus("Keerthana7886@")
DB_HOST = "localhost"
DB_NAME = "global_seismic_trends"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)


# 1. Top 10 Strongest Earthquakes

query = """
SELECT place, country, mag, time
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;
"""
print("\n1. Top 10 Strongest Earthquakes")
print(pd.read_sql(query, engine))


# 2. Top 10 Deepest Earthquakes

query = """
SELECT place, country, depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;
"""
print("\n2. Top 10 Deepest Earthquakes")
print(pd.read_sql(query, engine))


# 3. High Magnitude Shallow Quakes

query = """
SELECT *
FROM earthquakes
WHERE mag > 7.5
AND depth_km < 50;
"""
print("\n3. High Magnitude Shallow Quakes")
print(pd.read_sql(query, engine))


# 4. Average Depth per Country

query = """
SELECT country,
AVG(depth_km) AS avg_depth
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC
LIMIT 10;
"""
print("\n4. Average Depth per Country")
print(pd.read_sql(query, engine))


# 5. Average Magnitude by magType

query = """
SELECT magType,
AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY magType
ORDER BY avg_mag DESC;
"""
print("\n5. Average Magnitude by magType")
print(pd.read_sql(query, engine))


# 6. Earthquakes per Year

query = """
SELECT year,
COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY year;
"""
print("\n6. Earthquakes per Year")
print(pd.read_sql(query, engine))


# 7. Earthquakes per Month

query = """
SELECT month,
COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY month
ORDER BY month;
"""
print("\n7. Earthquakes per Month")
print(pd.read_sql(query, engine))


# 8. Earthquakes per Day of Week

query = """
SELECT day_of_week,
COUNT(*) AS total
FROM earthquakes
GROUP BY day_of_week;
"""
print("\n8. Earthquakes per Day")
print(pd.read_sql(query, engine))


# 9. Top Networks

query = """
SELECT net,
COUNT(*) AS total
FROM earthquakes
GROUP BY net
ORDER BY total DESC
LIMIT 10;
"""
print("\n9. Top Networks")
print(pd.read_sql(query, engine))


# 10. Total Earthquakes

query = """
SELECT COUNT(*) AS Total_Earthquakes
FROM earthquakes;
"""
print("\n10. Total Earthquakes")
print(pd.read_sql(query, engine))


# 11. Alert Levels

query = """
SELECT DISTINCT alert
FROM earthquakes;
"""
print("\n11. Alert Levels")
print(pd.read_sql(query, engine))


# 12. Status Distribution

query = """
SELECT status,
COUNT(*) AS total
FROM earthquakes
GROUP BY status;
"""
print("\n12. Status Distribution")
print(pd.read_sql(query, engine))


# 13. Type Distribution

query = """
SELECT type,
COUNT(*) AS total
FROM earthquakes
GROUP BY type
ORDER BY total DESC;
"""
print("\n13. Type Distribution")
print(pd.read_sql(query, engine))


# 14. Data Quality

query = """
SELECT
SUM(types LIKE '%%origin%%') AS origin,
SUM(types LIKE '%%phase-data%%') AS phase_data,
SUM(types LIKE '%%dyfi%%') AS dyfi
FROM earthquakes;
"""
print("\n14. Data Quality")
print(pd.read_sql(query, engine))

# 15. Average RMS & GAP per Country

query = """
SELECT country,
AVG(rms) AS avg_rms,
AVG(gap) AS avg_gap
FROM earthquakes
GROUP BY country
LIMIT 10;
"""
print("\n15. Average RMS & GAP per Country")
print(pd.read_sql(query, engine))

# 16. High Station Count (nst > 50)

query = """
SELECT *
FROM earthquakes
WHERE nst > 50;
"""
print("\n16. High Station Count")
print(pd.read_sql(query, engine))


# 17. Tsunami Events per Year

query = """
SELECT year,
COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year
ORDER BY year;
"""
print("\n17. Tsunami Events per Year")
print(pd.read_sql(query, engine))


# 18. Alert Level Count

query = """
SELECT alert,
COUNT(*) AS total
FROM earthquakes
GROUP BY alert;
"""
print("\n18. Alert Level Count")
print(pd.read_sql(query, engine))


# 19. Top 5 Countries by Average Magnitude

query = """
SELECT country,
AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY country
ORDER BY avg_magnitude DESC
LIMIT 5;
"""
print("\n19. Top 5 Countries by Average Magnitude")
print(pd.read_sql(query, engine))


# 20. Countries with Shallow & Deep Quakes in Same Month

query = """
SELECT country,
year,
month,
COUNT(DISTINCT depth_category) AS depth_types
FROM earthquakes
GROUP BY country, year, month
HAVING COUNT(DISTINCT depth_category) > 1;
"""
print("\n20. Countries with Shallow & Deep Quakes")
print(pd.read_sql(query, engine))


# 21. Year-over-Year Growth

query = """
WITH yearly AS
(
SELECT year,
COUNT(*) AS total
FROM earthquakes
GROUP BY year
)
SELECT year,
total,
LAG(total) OVER(ORDER BY year) AS previous_year,
ROUND(
((total-LAG(total) OVER(ORDER BY year))
/
LAG(total) OVER(ORDER BY year))*100,2
) AS growth_percent
FROM yearly;
"""
print("\n21. Year-over-Year Growth")
print(pd.read_sql(query, engine))


# 22. Top 3 Countries by Frequency & Magnitude

query = """
SELECT country,
COUNT(*) AS frequency,
AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY country
ORDER BY frequency DESC,
avg_magnitude DESC
LIMIT 3;
"""
print("\n22. Top 3 Countries")
print(pd.read_sql(query, engine))


# 23. Equatorial Region Analysis

query = """
SELECT country,
AVG(depth_km) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;
"""
print("\n23. Equatorial Region Analysis")
print(pd.read_sql(query, engine))


# 24. Shallow vs Deep Ratio

query = """
SELECT country,
SUM(depth_category='Shallow') AS shallow,
SUM(depth_category='Deep') AS deep
FROM earthquakes
GROUP BY country;
"""
print("\n24. Shallow vs Deep Ratio")
print(pd.read_sql(query, engine))


# 25. Tsunami vs Average Magnitude

query = """
SELECT tsunami_flag,
AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY tsunami_flag;
"""
print("\n25. Tsunami vs Magnitude")
print(pd.read_sql(query, engine))


# 26. Poor Quality Signals

query = """
SELECT place,
country,
gap,
rms
FROM earthquakes
ORDER BY gap DESC,rms DESC
LIMIT 10;
"""
print("\n26. Poor Quality Signals")
print(pd.read_sql(query, engine))


# 27. Close-Time Earthquakes (<1 Hour)

query = """
SELECT
id,
place,
time,
TIMESTAMPDIFF(
MINUTE,
LAG(time) OVER(ORDER BY time),
time
) AS time_difference
FROM earthquakes;
"""
print("\n27. Close-Time Earthquakes")
print(pd.read_sql(query, engine))


# 28. Deep Earthquakes (>300 km)

query = """
SELECT country,
COUNT(*) AS total
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY total DESC;
"""
print("\n28. Deep Earthquakes")
print(pd.read_sql(query, engine))


# 29. Strong Earthquake Percentage

query = """
SELECT
ROUND(
AVG(strong_quake_flag)*100,2
) AS strong_percentage
FROM earthquakes;
"""
print("\n29. Strong Earthquake Percentage")
print(pd.read_sql(query, engine))


# 30. Average Magnitude by Depth Category

query = """
SELECT depth_category,
AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY depth_category;
"""
print("\n30. Average Magnitude by Depth Category")
print(pd.read_sql(query, engine))

print("\n✅ All 30 SQL Analyses Completed Successfully")