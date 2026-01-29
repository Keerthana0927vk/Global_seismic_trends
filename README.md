Global Seismic Trends
End-to-End Data Science Project
Project Overview

This project is an end-to-end data science application designed to analyze global earthquake trends using real-world data. The dataset is collected from the USGS Earthquake API and processed using Python. The cleaned data is stored in a MySQL database, analyzed using SQL queries, and finally visualized through an interactive Streamlit dashboard.

The main objective of this project is to understand global seismic patterns, earthquake frequency, magnitude distribution, depth characteristics, and tsunami-related events over recent years.

Project Objectives

The key objectives of this project are:

To collect real-time earthquake data from a reliable public source

To clean and preprocess raw seismic data

To store structured data in a relational database

To perform analytical queries using SQL

To visualize insights using an interactive dashboard

To present meaningful patterns and trends from global earthquake data

Data Source

The earthquake data is obtained from the United States Geological Survey (USGS) Earthquake API.
This API provides detailed information such as:

Earthquake magnitude

Location and coordinates

Depth

Time and date

Tsunami indicators

Reporting network and event metadata

Project Architecture

The project follows a clear step-by-step pipeline:

Data Extraction using USGS API

Data Cleaning and Feature Engineering using Python

Data Storage in MySQL Database

SQL-based Data Analysis

Interactive Visualization using Streamlit

Each stage of the pipeline is implemented as a separate Python script for better modularity and clarity.

Tools and Technologies Used
Programming and Libraries

Python

Pandas

Requests

Plotly

Streamlit

Database and Querying

MySQL

SQL

Development and Version Control

Visual Studio Code

Git

GitHub

Data Collection

The data collection process is implemented using Python and the USGS API.
The script fetches earthquake records in batches and extracts both property-level data and geographical coordinates.
The raw data is saved in CSV format for further processing.

Data Cleaning and Feature Engineering

The raw data contains missing values, nested fields, and inconsistent formats.
The cleaning process includes:

Handling missing and null values

Extracting latitude, longitude, and depth from coordinate arrays

Converting timestamps to readable datetime format

Creating new features such as year, month, day, hour, and day of week

Categorizing earthquakes based on depth

Creating flags for strong earthquakes and tsunami events

The cleaned dataset is saved as a processed CSV file.

Database Design

The cleaned data is loaded into a MySQL database.
A structured table is created with appropriate data types for numerical, categorical, and datetime fields.
Each earthquake event is uniquely identified using its USGS event ID.

SQL Analysis

SQL queries are used to analyze the stored earthquake data.
The analysis focuses on:

Earthquake count by year, month, and day of week

Average and maximum earthquake magnitudes

Distribution of earthquakes by depth category

Country-wise earthquake frequency

Strong earthquake occurrences

Tsunami-related earthquake analysis

Network-wise reporting statistics

These queries help convert raw data into meaningful analytical insights.

Streamlit Dashboard

An interactive dashboard is built using Streamlit to visualize the analysis results.
The dashboard includes:

Filters for year, magnitude range, and country

Key performance indicators such as total earthquakes and average magnitude

Bar charts showing earthquake frequency over time

Histogram for magnitude distribution

Country-wise earthquake comparison

A user-controlled global earthquake map displaying top events by magnitude

The dashboard allows users to explore the data dynamically based on their preferences.

Key Insights

Based on the analysis, the following insights are observed:

Earthquake activity varies significantly across different regions

Shallow earthquakes occur more frequently than deep earthquakes

Strong earthquakes are less frequent but contribute significantly to seismic risk

Tsunami-triggering earthquakes are rare but critical events

Certain countries and regions consistently show higher seismic activity

Project Outcomes

This project demonstrates the complete lifecycle of a data science solution, from data acquisition to visualization.
It highlights practical skills in data engineering, SQL analysis, and dashboard development.
The project is scalable and can be extended with real-time updates, predictive models, or cloud deployment.

Conclusion

The Global Seismic Trends project successfully transforms raw earthquake data into actionable insights.
It showcases a structured approach to solving real-world data problems using Python, SQL, and visualization tools.
This project reflects practical data science skills and analytical thinking applicable to industry-level problems.

Author

Keerthana
