# DSA210_Project_BaranUtkuGuler

# Health Data Analysis Project

This project focuses on analyzing personal health data from **Apple Health** and **e-Nabız** to gain insights into various health metrics such as heart rhythm, activity levels, and blood test results. The aim is to process the raw data, visualize key metrics, and analyze relationships between them to detect anomalies and better understand personal health trends.

 Dataset Description

The analysis is based on two main data sources:

1. Apple Health Data:
   - Includes heart rate, activity levels, and step count data.
   - Provides daily metrics for visualization and correlation analysis.
   - Format: Exported `.xml` and `.csv` files.

2. e-Nabız Data:
   - Blood test results in PDF format.
   - Parameters include:
     - Iron (Demir):70-236 µg/dL
     -Ferritin: 7-154 ng/mL
     - Vitamin B12:179-417 pg/ml
     - Creatine Kinase (CK): 1.12-2705 U/L
   - Format: Exported PDF files.

## Project Objectives

 1. Data Processing
   - Convert raw Apple Health and e-Nabız data into a structured and analyzable format.
   - Extract health metrics (e.g., heart rate, activity levels, and blood test results).
   - Handle inconsistencies and missing data to ensure accurate analysis.

 2. Health Analysis
   - Evaluate individual metrics such as heart rhythm trends, daily activity patterns, and blood parameter variations.
   - Investigate relationships between datasets, such as:
     - Correlation between physical activity and iron levels.
     - Effects of vitamin B12 on heart rhythm.
     - CK trends and recovery metrics.
   - Identify potential anomalies in the data and their possible implications.

 3. Visualization
   - Create interactive charts and graphs to visualize:
     - Time series data for heart rate and activity levels.
     - Trends in blood test results over time.
     - Relationships between different health metrics.

## Project Plan

 Phase 1: Data Preparation
- Objective: Extract, clean, and preprocess Apple Health and e-Nabız data.
- Tasks:
  - Parse and clean Apple Health `.xml` and `.csv` files.
  - Extract tables from e-Nabız PDFs using OCR and parsing tools.
  - Merge datasets into a unified structure.

 Phase 2: Data Analysis
- Objective:Analyze individual and relational health metrics.
- Tasks:
  - Perform descriptive analysis for heart rate, activity, and blood parameters.
  - Use statistical methods to identify patterns and correlations.
  - Detect outliers or anomalies in health data.

 Phase 3: Visualization
- Objective: Present findings through meaningful visualizations.
- Tasks:
  - Create plots for time series and trends (e.g., heart rate vs. activity).
  - Develop scatterplots and correlation matrices for relational insights.
  - Highlight anomalies or critical insights.

 Phase 4: Reporting
- Objective: Summarize results and share actionable insights.
- Tasks:
  - Write a detailed report on findings and methodology.
  - Provide recommendations for users with similar data to improve their health tracking.

Potential Impact

This project aims to achieve two primary outcomes:
1. Personal Insights:Enable users to better understand their own health data and detect potential anomalies that may require attention.
2. General Awareness: Provide a roadmap for others to analyze similar datasets and uncover actionable health insights.

By bridging activity levels, heart rhythm, and blood metrics, this project offers a comprehensive look into personal health trends and encourages proactive health management.
