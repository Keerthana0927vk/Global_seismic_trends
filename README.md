# Global Seismic Trends Analysis (2021–2025)

## Project Overview

This project analyzes global earthquake data collected from the United States Geological Survey (USGS) API for the period **2021 to 2025**. The objective is to build a complete data pipeline that collects, cleans, stores, analyzes, and visualizes earthquake data to identify global seismic trends.

The project follows an end-to-end data analytics workflow using **Python**, **MySQL**, **SQL**, and **Streamlit**.

---

## Objectives

* Collect global earthquake data from the USGS API.
* Clean and preprocess the raw dataset.
* Store the processed data in a MySQL database.
* Perform SQL-based exploratory and analytical queries.
* Build an interactive Streamlit dashboard for data visualization.

---

## Technologies Used

* Python
* Pandas
* Requests
* Regular Expressions (Regex)
* SQLAlchemy
* MySQL
* SQL
* Streamlit
* Plotly

---

## Project Workflow

### 1. Data Collection

The `fetch_usgs_data.py` script retrieves earthquake records from the USGS Earthquake API.

Tasks performed:

* Connects to the USGS API.
* Downloads earthquake records from 2021 to 2025.
* Retrieves earthquake details such as magnitude, location, depth, coordinates, and timestamps.
* Converts the API response into a Pandas DataFrame.
* Saves the raw dataset as a CSV file.

Output:

```
data/raw/usgs_earthquakes_raw.csv
```

---

### 2. Data Cleaning and Preprocessing

The `clean_usgs_data.py` script prepares the raw dataset for analysis.

Tasks performed:

* Converts timestamp columns into datetime format.
* Handles missing values.
* Creates new columns:

  * Year
  * Month
  * Day
  * Hour
  * Day of Week
* Extracts country names from the location column using Regular Expressions.
* Categorizes earthquake depth into:

  * Shallow
  * Intermediate
  * Deep
* Creates a Strong Earthquake Flag.
* Creates a Tsunami Flag.
* Saves the cleaned dataset.

Output:

```
data/processed/usgs_earthquakes_cleaned.csv
```

---

### 3. Data Loading

The `load_to_mysql.py` script loads the processed dataset into MySQL.

Tasks performed:

* Reads the cleaned CSV file.
* Connects to the MySQL database.
* Loads all earthquake records into the `earthquakes` table using SQLAlchemy.

Database:

```
global_seismic_trends
```

Table:

```
earthquakes
```

---

### 4. SQL Analysis

The `analyze_data.py` script performs SQL analysis on the stored earthquake data.

The project includes **30 SQL analytical queries**, including:

* Strongest earthquakes
* Deepest earthquakes
* Earthquakes by year
* Earthquakes by month
* Earthquakes by country
* Average magnitude
* Average depth
* Tsunami analysis
* Alert level analysis
* Network analysis
* Strong earthquake percentage
* Deep earthquake analysis
* Year-over-year growth
* Data quality analysis

---

### 5. Interactive Dashboard

The project includes a Streamlit dashboard for interactive analysis.

Features:

* Year filter
* Country filter
* Minimum magnitude filter
* 30 SQL analysis options
* Interactive Plotly visualizations
* Query result table
* User-friendly interface

---

## Database Schema

The project stores earthquake information including:

* Earthquake ID
* Magnitude
* Place
* Time
* Updated Time
* Time Zone
* Coordinates
* Depth
* Country
* Magnitude Type
* Alert Level
* Status
* Tsunami Information
* Strong Earthquake Flag
* Depth Category
* Date and Time Features

---

## Key Insights

* A total of **137,461 earthquake events** were analyzed between 2021 and 2025.
* The strongest earthquake had a magnitude of **8.8**.
* The deepest earthquake occurred near **Vanuatu**.
* **2025** recorded the highest number of earthquakes.
* **2024** recorded the lowest number of earthquakes.
* **July** and **December** experienced the highest earthquake activity.
* **Alaska** recorded the highest number of earthquakes.
* **Fiji** had the highest number of deep earthquakes.
* Strong earthquakes (Magnitude ≥ 6) were very rare.
* Earthquakes associated with tsunamis generally had higher magnitudes.
* Most earthquake records were reviewed, indicating good data quality.
* Deep earthquakes had a higher average magnitude than shallow earthquakes.

---

## Project Structure

```text
Global_Seismic_Trends/
│
├── data/
│   ├── raw/
│   │   └── usgs_earthquakes_raw.csv
│   │
│   └── processed/
│       └── usgs_earthquakes_cleaned.csv
│
├── scripts/
│   ├── fetch_usgs_data.py
│   ├── clean_usgs_data.py
│   ├── load_to_mysql.py
│   └── analyze_data.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

## Future Enhancements

* Deploy the Streamlit dashboard online.
* Add interactive map visualization of earthquake locations.
* Implement real-time earthquake monitoring using the USGS API.
* Build machine learning models for earthquake trend prediction.

---

## Conclusion

This project demonstrates a complete end-to-end data analytics workflow by integrating API-based data collection, data preprocessing, relational database management, SQL analytics, and interactive dashboard development. The resulting dashboard enables users to explore global earthquake trends efficiently through visualizations and SQL-driven insights.
