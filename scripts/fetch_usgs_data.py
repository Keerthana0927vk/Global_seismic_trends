#fetch_usgs_data.py

from cmath import e
import requests
import pandas as pd
import time

#1.USGS API base URL
BASE_URL= "https://earthquake.usgs.gov/fdsnws/event/1/query"

#2.define time range (last 5 years example)
START_YEAR=2021
END_YEAR =2025

#Minimum magnitude to reduce noise
MIN_MAGNITUDE=2.5
LIMIT=20000

#3.Empty list to store all records
all_earthquakes=[]

#4.Loop through year and month
for year in range(START_YEAR,END_YEAR+1):
    for month in range (1,13):
        print("YEAR:", year, "MONTH:", month)
        #create start and end date
        start_date=f"{year}-{month:02d}-01"
        if month==12:
            end_date=f"{year+1}-01-01"
        else:
            end_date=f"{year}-{month+1:02d}-01"
        offset=1           
        while True:
            #5.Build parameters
            params={
                "format":"geojson",
                "starttime":start_date,
                "endtime":end_date,
                "minmagnitude":MIN_MAGNITUDE,
                "limit":LIMIT,
                "offset":offset
            }
            try:
                response=requests.get(BASE_URL,params=params)
                response.raise_for_status()
                data=response.json()
                features=data.get("features",[])
                if not features:
                    break
                for feature in features:
                    properties=feature.get("properties",{}).copy()
                    properties["id"]=feature.get("id")
                    coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
                    properties["longitude"] = coords[0]
                    properties["latitude"] = coords[1]
                    properties["depth_km"] = coords[2]
                    all_earthquakes.append(properties)

                if len(features)<LIMIT:
                    break
                offset+=len(features)
                time.sleep(1)
            except Exception as e:
                print(f"Error fetching data for {start_date}: {e}")
                break

#6.Convert to DataFrame
df_raw=pd.DataFrame(all_earthquakes)

#7.convert timestamps(ms->datetime)
df_raw["time"]=pd.to_datetime(df_raw["time"],unit="ms",errors="coerce")
df_raw["updated"]=pd.to_datetime(df_raw["updated"],unit="ms",errors="coerce")

#8.Basic validation
print("Data shape:",df_raw.shape)
print(df_raw.head())
print(df_raw.dtypes)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

df_raw.to_csv(os.path.join(RAW_DIR, "usgs_earthquakes_raw.csv"), index=False)

print("Raw earthquake data saved successfully.")