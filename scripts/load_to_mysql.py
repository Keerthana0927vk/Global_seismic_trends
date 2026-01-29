import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------- CONFIG ----------
DB_USER = "root"
DB_PASSWORD =quote_plus("Keerthana7886@")   # <-- replace this
DB_HOST = "localhost"
DB_NAME = "global_seismic_trends"

CSV_PATH = "data/processed/usgs_earthquakes_cleaned.csv"
TABLE_NAME = "earthquakes"
# ----------------------------

print("Reading cleaned CSV...")
df = pd.read_csv(CSV_PATH)
print("Rows in CSV:", df.shape[0])

print(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
print("Connecting to MySQL...")
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

print("Loading data into MySQL table...")
df.to_sql(
    TABLE_NAME,
    con=engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("✅ Data successfully loaded into MySQL!")
print(df.columns)

