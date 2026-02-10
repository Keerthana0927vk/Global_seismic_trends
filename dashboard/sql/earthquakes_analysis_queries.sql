USE global_seismic_trends;
CREATE TABLE earthquakes (
    id VARCHAR(50) PRIMARY KEY,

    mag FLOAT,
    place TEXT,
    time DATETIME,
    updated DATETIME,
    tz FLOAT,

    url TEXT,
    detail TEXT,

    felt FLOAT,
    cdi FLOAT,
    mmi FLOAT,
    alert VARCHAR(20),

    status VARCHAR(20),
    tsunami INT,
    sig INT,

    net VARCHAR(20),
    code VARCHAR(50),
    ids TEXT,
    sources TEXT,
    types TEXT,

    nst FLOAT,
    dmin FLOAT,
    rms FLOAT,
    gap FLOAT,

    magType VARCHAR(10),
    type VARCHAR(30),
    title TEXT,

    longitude FLOAT,
    latitude FLOAT,
    depth_km FLOAT,

    year INT,
    month INT,
    day INT,
    hour INT,
    day_of_week VARCHAR(10),

    country VARCHAR(50),
    depth_category VARCHAR(20),
    strong_quake_flag INT,
    tsunami_flag VARCHAR(5)
);
#1.Top 10 strongest earthquakes
SELECT place, country, mag, time
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;
#2.Top 10 deepest earthquakes
SELECT place, country, depth_km, time
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;
#3
SELECT *
FROM earthquakes
WHERE depth_km < 50 AND mag > 7.5;
#4
SELECT country, AVG(depth_km) AS avg_depth
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC;
#5
SELECT magType, AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY magType
ORDER BY avg_magnitude DESC;
#6
SELECT year, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY year
ORDER BY quake_count DESC;
#7
SELECT month, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY month
ORDER BY quake_count DESC;
#8
SELECT day_of_week, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY day_of_week
ORDER BY quake_count DESC;
#9
SELECT net, COUNT(*) AS reports
FROM earthquakes
GROUP BY net
ORDER BY reports DESC;
#10
SELECT net, COUNT(*) AS reports
FROM earthquakes
GROUP BY net
ORDER BY reports DESC;
#11
SELECT COUNT(*) 
FROM earthquakes;
-- Casualty data not available in USGS API
#12
SELECT DISTINCT alert
FROM earthquakes;
-- No economic loss field in source data
#13
-- Properly documented as unavailable in source
#14
SELECT status, COUNT(*) AS count
FROM earthquakes
GROUP BY status;
#15
SELECT type, COUNT(*) AS count
FROM earthquakes
GROUP BY type;
#16
SELECT 
  SUM(types LIKE '%origin%') AS origin_count,
  SUM(types LIKE '%phase-data%') AS phase_data_count,
  SUM(types LIKE '%dyfi%') AS dyfi_count
FROM earthquakes;
#17
SELECT country,
       AVG(rms) AS avg_rms,
       AVG(gap) AS avg_gap
FROM earthquakes
GROUP BY country;
#18
SELECT *
FROM earthquakes
WHERE nst > 50;
#19
SELECT year, COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year;
#20
SELECT alert, COUNT(*) AS count
FROM earthquakes
GROUP BY alert;
#21
SELECT country, AVG(mag) AS avg_mag
FROM earthquakes
WHERE year >= YEAR(CURDATE()) - 10
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5;
#22
SELECT DISTINCT e1.country, e1.year, e1.month
FROM earthquakes e1
JOIN earthquakes e2
ON e1.country = e2.country
AND e1.year = e2.year
AND e1.month = e2.month
WHERE e1.depth_category = 'shallow'
AND e2.depth_category = 'deep';
#23
SELECT year,
       COUNT(*) AS quake_count,
       (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year)) /
       LAG(COUNT(*)) OVER (ORDER BY year) * 100 AS yoy_growth_percent
FROM earthquakes
GROUP BY year;
#24
SELECT country,
       COUNT(*) AS frequency,
       AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY frequency DESC, avg_mag DESC
LIMIT 3;
#25
SELECT country, AVG(depth_km) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;
#26
SELECT country,
       SUM(depth_category='shallow') /
       SUM(depth_category='deep') AS shallow_deep_ratio
FROM earthquakes
GROUP BY country
HAVING SUM(depth_category='deep') > 0
ORDER BY shallow_deep_ratio DESC;
#27
SELECT tsunami_flag, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY tsunami_flag;
#28
SELECT *
FROM earthquakes
ORDER BY gap DESC, rms DESC
LIMIT 20;
#29
SELECT e1.id, e2.id, e1.time, e2.time
FROM earthquakes e1
JOIN earthquakes e2
ON TIMESTAMPDIFF(MINUTE, e1.time, e2.time) BETWEEN 0 AND 60
AND e1.id <> e2.id;
#30
SELECT country, COUNT(*) AS deep_quakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_quakes DESC;
#C:\Users\keert\OneDrive\Documents\anaconda_projects\db
USE global_seismic_trends;
TRUNCATE TABLE earthquakes;
