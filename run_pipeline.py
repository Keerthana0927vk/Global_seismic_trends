# run_pipeline.py

import subprocess

print(" Starting Earthquake Data Pipeline...\n")

# Step 1: Fetch data
print("Step 1: Fetching data from USGS API...")
subprocess.run(["python", "scripts/fetch_usgs_data.py"])

# Step 2: Clean data
print("\nStep 2: Cleaning data...")
subprocess.run(["python", "scripts/clean_usgs_data.py"])

# Step 3: Load into MySQL
print("\nStep 3: Loading data into MySQL...")
subprocess.run(["python", "scripts/load_to_mysql.py"])

# Step 4: Run analysis
print("\nStep 4: Running analysis...")
subprocess.run(["python", "scripts/analyze_data.py"])

print("\n Pipeline completed successfully!")