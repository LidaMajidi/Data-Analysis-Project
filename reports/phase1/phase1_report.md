# Phase 1 Report: Data Understanding and Quality Assessment

**Project:** NYC TLC Trip Record Data Analysis (Yellow Taxi)
**Student:** Lida Majidi Aralan
**StudentID:**401103706
**Date:** November 2026

**Track:** Track A (Time-Series, Event, and Anomaly Analysis)

---

## 1. Abstract
This report covers the initial phase of the data analysis project focused on the NYC Yellow Taxi dataset (January 2024). We define the problem, explore the data structure, assess data quality (missing values, impossible records), and perform exploratory data analysis (EDA) on temporal and spatial patterns. Finally, we define the primary prediction question, establish a baseline, and identify potential data leakage risks for future modeling phases.

## 2. Problem Definition and Motivation
The NYC taxi system is a vital part of urban transportation. Understanding trip patterns and being able to predict trip duration can help with fleet management, dynamic pricing, and improving passenger experience. The main goal of this project is to build a reliable predictive model for trip duration using historical trip data. 

## 3. Data and Data Quality
### 3.1 Data Source
The dataset is the official NYC TLC Yellow Taxi Trip Record Data. We selected the January 2024 subset, provided in Parquet format (`yellow_tripdata_2024-01.parquet`), because it offers a stable, high-volume, and recent snapshot of the data.

### 3.2 Data Structure
- **Total Rows:** 2,964,624
- **Total Columns:** 19
- **Key Variables:** `tpep_pickup_datetime`, `tpep_dropoff_datetime`, `passenger_count`, `trip_distance`, `PULocationID`, `DOLocationID`, `fare_amount`, `total_amount`.
- **Data Types:** The dataset contains integers (IDs), floats (amounts, distances), and datetime objects.

### 3.3 Data Quality Assessment
Our initial audit revealed several quality issues:
- **Missing Values:** Approximately 140,162 rows (~4.7%) have missing values in `passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`. This is likely due to the inclusion of Green Taxi records or older vendor systems that do not capture these fields.
- **Impossible Records:**
  - **Negative/Zero Fares:** 38,341 trips had `fare_amount <= 0` (possibly canceled rides or free trips).
  - **Zero Passengers:** 31,465 trips reported 0 passengers (data entry error or canceled trips).
  - **Time Travel:** 56 trips had `dropoff_datetime` earlier than `pickup_datetime` (impossible physically; likely clock errors).
  - **Impossible Speeds:** 1,024 trips showed a calculated speed > 100 mph, which is physically impossible in NYC.
- **Duplicates:** 0 fully duplicated rows were found.

## 4. Exploratory Data Analysis (EDA)
### 4.1 Univariate Analysis
We plotted the distributions of the main continuous variables (after filtering out extreme outliers):
- **Trip Duration:** Right-skewed distribution, with most trips lasting between 5 and 15 minutes.
- **Trip Distance:** Right-skewed, with most trips under 3 miles.
- **Fare Amount:** Concentrated between $5 and $15. A prominent separate peak exists at $70, which corresponds to the flat fare to/from JFK Airport.

### 4.2 Temporal Patterns
- **Hour of Day:** Demand peaks between 5 PM and 6 PM (rush hour) and drops to its lowest between 3 AM and 5 AM.
- **Day of Week:** Wednesday showed the highest volume of trips, while Sunday showed the lowest.

### 4.3 Multivariate Analysis
- **Distance vs. Fare:** There is a strong positive correlation. However, the JFK flat fare creates a distinct horizontal line at $70, showing that fare does not always increase with distance (especially for airport trips).
- **Impossible Speed Anomaly:** We identified over 1,000 records with impossible speeds, which must be handled in future phases.

## 5. Primary Question and Baseline
- **Selected Question:** Can we predict trip duration based on time, location, and distance features?
- **Justification:** It's a practical regression problem that requires using both temporal and spatial features, and it forces us to address data quality issues (like impossible speeds).
- **Baseline Definition:** A very simple baseline is to predict the **average trip duration for the given hour of the day**. For example, predict 25 minutes for all 5 PM trips. This will be used as a comparison point in Phase 3.

## 6. Data Leakage Risks
When building models for trip duration, we must avoid the following leaks:
- **Target Leakage:** Do not use `tpep_dropoff_datetime` or any feature derived from it (like duration).
- **Indirect Leakage:** Do not use `total_amount` or other post-trip financial features, as they are only known after the trip ends.
- **Temporal Leakage:** Ensure future trips do not leak into the training data when doing time-based splits.

## 7. Conclusion and Next Steps
The dataset is rich but contains significant quality issues that require cleaning (Phase 2). We have identified clear temporal and spatial patterns. In the next phase, we will handle missing values, engineer new features (like cyclic time features), and prepare the data for predictive modeling.