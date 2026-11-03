# Project Card

**Project Title:** NYC TLC Trip Record Data Analysis (Yellow Taxi)
**Student Name:** Lida Majidi
**Course:** Data Analysis (Fall 1405)
**Project Track:** Track A - Time-Series, Event, and Anomaly Analysis

## 1. Problem Definition
The goal of this project is to analyze the New York City yellow taxi trip data to understand trip patterns, evaluate data quality, and build predictive models for trip duration or fare amount. The final goal is to extract actionable insights for taxi fleet management or urban planning.

## 2. Dataset
- **Source:** NYC TLC Official Website (Parquet format)
- **Subset Selected:** January 2024 (`yellow_tripdata_2024-01.parquet`)
- **Size:** ~2.96 million rows, 19 columns
- **Why this subset?** 
  - Yellow taxis cover all 5 boroughs and represent the largest volume of trips.
  - January 2024 provides a complete, stable dataset with recent schema updates.
  - Parquet format is highly efficient for large-scale data processing.

## 3. Initial Data Quality Findings (Phase 1)
- **Missing Values:** ~140,000 rows (~4.7%) missing in `passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`. (Likely due to mixed vendor systems or green taxi inclusion).
- **Impossible Records:**
  - 38,341 trips with `fare_amount <= 0` (Canceled or free rides).
  - 31,465 trips with `passenger_count == 0`.
  - 56 trips with `dropoff_datetime < pickup_datetime`.
  - 1,024 trips with calculated speed > 100 mph.
- **Duplicates:** 0 fully duplicated rows.

## 4. Candidate Questions
1. **How does trip demand vary by hour of day and day of week, and what factors drive these temporal patterns?**
2. **What is the relationship between trip distance and fare amount, and how do outliers (like JFK flat fares) affect this relationship?**
3. **Can we accurately predict trip duration based on time, location, and distance features?**

**Selected Final Question:** Question 3 (Predicting Trip Duration). 
**Justification:** Predicting trip duration is a challenging but practically valuable regression problem. It allows us to explore both temporal (time of day) and spatial (location) features. It also forces us to deal with real-world data quality issues (like impossible speeds) and understand how they impact model performance.

## 5. Baseline Definition
For predicting trip duration, a very simple, understandable baseline is:
**Baseline = Average trip duration for the given hour of the day.**
For example, if the average trip at 5 PM takes 25 minutes, our baseline model will predict 25 minutes for any 5 PM trip, regardless of distance or location. We will compare our advanced models against this baseline in Phase 3.

## 6. Data Leakage Risks
Before modeling, we must ensure no information from the future or target leaks into the features:
- **Target Leakage:** We cannot use `tpep_dropoff_datetime` or `trip_duration_mins` as a feature when predicting trip duration, as they are the direct result of the target.
- **Indirect Leakage:** `total_amount` includes `fare_amount`, `tip_amount`, and `tolls_amount`. If we were predicting fare, using `total_amount` would be leakage. For duration prediction, `total_amount` is known only *after* the trip ends, so it cannot be used as a feature.
- **Operational Leakage:** Features like `payment_type` or `congestion_surcharge` are often recorded post-trip and might leak outcome information.