# clean_usgs_data.py

import pandas as pd
import os
import re

# -------------------------
# Base directory
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Raw data path
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "usgs_earthquakes_raw.csv")

# -------------------------
# Load raw dataset
# -------------------------
df = pd.read_csv(RAW_PATH)
print("RAW data columns loaded successfully")

print("Initial shape:", df.shape)
print(df.head())
print(df.dtypes)

# -------------------------
# Convert time columns
# -------------------------
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], errors="coerce")
df["tz"] = pd.to_numeric(df["tz"], errors="coerce").fillna(0)

print(df[["time", "updated"]].dtypes)

# -------------------------
# Missing values check
# -------------------------
print(df.isna().sum().sort_values(ascending=False))

# -------------------------
# Time based features
# -------------------------
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["hour"] = df["time"].dt.hour
df["day_of_week"] = df["time"].dt.day_name()

print(df[["time", "year", "month", "hour", "day_of_week"]].head())

# -------------------------
# Handle missing values
# -------------------------
df["alert"] = df["alert"].fillna("unknown")
df["tz"] = df["tz"].fillna(0)

# -------------------------
# Country extraction
# -------------------------
def extract_country(place):
    if pd.isna(place):
        return "unknown"
    match = re.search(r",\s*([A-Za-z\s]+)$", place)
    if match:
        return match.group(1).strip()
    return "unknown"

df["country"] = df["place"].apply(extract_country)

print(df[["place", "country"]].head(10))

# -------------------------
# Depth category (domain knowledge)
# -------------------------
def depth_category(depth):
    if pd.isna(depth):
        return "unknown"
    if depth < 70:
        return "shallow"
    elif depth < 300:
        return "intermediate"
    else:
        return "deep"

df["depth_category"] = df["depth_km"].apply(depth_category)
print(df["depth_category"].value_counts())

# -------------------------
# Strong earthquake flag
# -------------------------
df["strong_quake_flag"] = df["mag"].apply(lambda x: 1 if x >= 6.0 else 0)
print(df["strong_quake_flag"].value_counts())

# -------------------------
# Tsunami flag (readable)
# -------------------------
df["tsunami_flag"] = df["tsunami"].apply(lambda x: "Yes" if x == 1 else "No")

# -------------------------
# Final validation
# -------------------------
print("Final columns:")
print(df.columns)

print("Final shape:")
print(df.shape)

# -------------------------
# Save cleaned data
# -------------------------
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

CLEAN_PATH = os.path.join(PROCESSED_DIR, "usgs_earthquakes_cleaned.csv")
df.to_csv(CLEAN_PATH, index=False)

print("✅ Cleaned earthquake data saved successfully.")
