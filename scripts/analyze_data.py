# analyze_data.py

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# DB connection
DB_USER = "root"
DB_PASSWORD = quote_plus("Keerthana7886@")
DB_HOST = "localhost"
DB_NAME = "global_seismic_trends"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

print("Loading data...")
df = pd.read_sql("SELECT * FROM earthquakes", engine)
df["time"] = pd.to_datetime(df["time"], errors="coerce")

print("Data Loaded:", df.shape)

# ===============================
# 🔍 30 ANALYTICAL INSIGHTS
# ===============================

# 1
print("\n1. Top 10 strongest earthquakes")
print(df.nlargest(10, "mag")[["place", "country", "mag", "time"]])

# 2
print("\n2. Top 10 deepest earthquakes")
print(df.nlargest(10, "depth_km")[["place", "country", "depth_km"]])

# 3
print("\n3. High magnitude shallow quakes")
print(df[(df["depth_km"] < 50) & (df["mag"] > 7.5)].shape[0])

# 4
print("\n4. Avg depth per country")
print(df.groupby("country")["depth_km"].mean().sort_values(ascending=False).head(10))

# 5
print("\n5. Avg magnitude per magType")
print(df.groupby("magType")["mag"].mean().sort_values(ascending=False))

# 6
print("\n6. Earthquakes per year")
print(df.groupby("year").size())

# 7
print("\n7. Earthquakes per month")
print(df.groupby("month").size())

# 8
print("\n8. Earthquakes per day of week")
print(df.groupby("day_of_week").size())

# 9
print("\n9. Top networks")
print(df["net"].value_counts().head(10))

# 10
print("\n10. Total earthquakes")
print(len(df))

# 11
print("\n11. Unique alert levels")
print(df["alert"].unique())

# 12
print("\n12. Status distribution")
print(df["status"].value_counts())

# 13
print("\n13. Type distribution")
print(df["type"].value_counts())

# 14
print("\n14. Data quality (origin / dyfi etc)")
print({
    "origin": df["types"].str.contains("origin", na=False).sum(),
    "phase_data": df["types"].str.contains("phase-data", na=False).sum(),
    "dyfi": df["types"].str.contains("dyfi", na=False).sum()
})

# 15
print("\n15. Avg RMS & GAP per country")
print(df.groupby("country")[["rms", "gap"]].mean().head(10))

# 16
print("\n16. High station count (nst > 50)")
print(df[df["nst"] > 50].shape[0])

# 17
print("\n17. Tsunami events per year")
print(df[df["tsunami"] == 1].groupby("year").size())

# 18
print("\n18. Alert level count")
print(df["alert"].value_counts())

# 19
print("\n19. Top 5 countries last 10 years")
recent = df[df["year"] >= df["year"].max() - 10]
print(recent.groupby("country")["mag"].mean().sort_values(ascending=False).head(5))

# 20
print("\n20. Countries with shallow & deep quakes same month")
combo = df.groupby(["country", "year", "month"])["depth_category"].nunique()
print(combo[combo > 1].head(10))

# 21
print("\n21. Year-over-year growth")
year_counts = df.groupby("year").size()
growth = year_counts.pct_change() * 100
print(growth)

# 22
print("\n22. Top 3 countries by frequency & magnitude")
print(df.groupby("country").agg(
    freq=("id", "count"),
    avg_mag=("mag", "mean")
).sort_values(["freq", "avg_mag"], ascending=False).head(3))

# 23
print("\n23. Equatorial region analysis")
print(df[(df["latitude"] >= -5) & (df["latitude"] <= 5)]
      .groupby("country")["depth_km"].mean().head(10))

# 24
print("\n24. Shallow vs deep ratio")
ratio = df.groupby("country")["depth_category"].value_counts().unstack().fillna(0)
ratio["ratio"] = ratio.get("shallow", 0) / (ratio.get("deep", 0) + 1)
print(ratio.sort_values("ratio", ascending=False).head(10))

# 25
print("\n25. Tsunami vs magnitude")
print(df.groupby("tsunami_flag")["mag"].mean())

# 26
print("\n26. Poor quality signals")
print(df.sort_values(["gap", "rms"], ascending=False).head(10))

# 27
print("\n27. Close-time earthquakes (<1hr)")
df_sorted = df.sort_values("time")
df_sorted["time_diff"] = df_sorted["time"].diff().dt.total_seconds() / 60
print(df_sorted[df_sorted["time_diff"] < 60].head(10))

# 28
print("\n28. Deep quakes (>300km)")
print(df[df["depth_km"] > 300].groupby("country").size().head(10))

# 29
print("\n29. Strong quake percentage")
print(df["strong_quake_flag"].mean() * 100)

# 30
print("\n30. Avg magnitude by depth category")
print(df.groupby("depth_category")["mag"].mean())

print("\n✅ All 30 insights generated successfully!")