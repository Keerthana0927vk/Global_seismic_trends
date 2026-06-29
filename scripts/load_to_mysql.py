import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# MySQL Configuration
DB_USER = "root"
DB_PASSWORD = quote_plus("Keerthana7886@")
DB_HOST = "localhost"
DB_NAME = "global_seismic_trends"

# File and Table Details
CSV_PATH = "data/processed/usgs_earthquakes_cleaned.csv"
TABLE_NAME = "earthquakes"

# Read CSV
print("Reading cleaned CSV...")
df = pd.read_csv(CSV_PATH)

# Connect to MySQL
print("Connecting to MySQL...")
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

# Load Data
print("Loading data into MySQL table...")

df.to_sql(
    TABLE_NAME,
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=5000
)

print(" Data successfully loaded into MySQL!")
print("Total rows loaded:", len(df))