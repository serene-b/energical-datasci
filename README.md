# ENERGICAL Data Intelligence

### Transforming Three Years of Customer Transactions into a Commercial Decision Support System

> DataFest 2026 – Challenge 2

## Overview

This project was developed for the **ENERGICAL Data Intelligence Challenge**, whose objective is to transform **17,263 customer transactions collected between 2022 and 2024** into actionable business insights that support commercial decision-making.

Rather than simply analyzing historical sales, our solution combines **Exploratory Data Analysis (EDA), Customer Segmentation, Time-Series Forecasting, and Customer Retention Analysis** into an interactive dashboard that helps managers answer practical business questions such as:

* Which products generate the highest revenue?
* Which wilayas should receive the next marketing campaign?
* Which customers should be prioritized for retention?
* When should seasonal products be restocked?
* How can inventory and marketing budgets be optimized?

The result is an end-to-end business intelligence pipeline that transforms raw transactional data into strategic recommendations.
---
# Features

## Data Preparation

* Comprehensive Exploratory Data Analysis (EDA)
* Missing value treatment and data validation
* Geographic standardization of Algerian wilayas
* Product catalogue enrichment
* Revenue and customer behavior analysis

## Customer Analytics

* RFM (Recency–Frequency–Monetary) customer segmentation
* K-Means clustering
* Customer action recommendations
* B2B vs B2C analysis
* Customer lifetime insights

## Revenue Forecasting

* Monthly revenue forecasting by wilaya
* Trend and seasonality decomposition
* Forecast confidence intervals
* Revenue volatility analysis
* Seasonal inventory planning

## Customer Retention

* Logistic Regression retention model
* Customer retention scoring
* Returning customer prediction
* Low-retention customer identification

## Interactive Dashboard

* Executive decision overview
* Sales overview
* Wilaya performance analysis
* Customer analytics
* Product analytics
* Seasonal inventory alerts
* CSV export for business reports

---

# Repository Structure

```
energical-datasci/
│
│
├── notebooks/
│   ├── 01_eda_cleaning.ipynb
│   ├── 02_rfm_segmentation.ipynb
│   ├── 03_loyalty_retention_model.ipynb
│   └── 04_timeseries_forecast.ipynb
│   └── 05_decision_support.ipynb
│
├── dashboard/
│   └── app.py
│
├── report.pdf
├── requirements.txt
└── README.md
```

---

# Methodology

The project follows a sequential analytics pipeline.

### 1. Exploratory Data Analysis

The raw transaction data is cleaned, validated, and enriched before any modeling is performed. Missing values, duplicate records, inconsistent wilaya names, and incomplete transactions are handled to ensure high-quality analytical data.

---

### 2. Customer Segmentation

Customers are segmented using the **RFM framework**:

* **Recency**
* **Frequency**
* **Monetary Value**

K-Means clustering identifies customers with similar purchasing behavior, allowing personalized marketing strategies.

Segments include:

* 🟢 Champions
* 🟡 Occasional Customers
* 🔴 Low-Engagement Customers

---

### 3. Revenue Forecasting

Monthly revenue is modeled separately for each wilaya using time-series analysis.

The workflow includes:

* Trend analysis
* Seasonality detection
* Stationarity testing
* Forecast generation
* Volatility estimation

Forecasts support inventory planning and regional investment decisions.

---

### 4. Customer Retention

Customer loyalty is modeled using **Logistic Regression**, producing a probability that a customer will return.

The analysis estimates:

* Returning customer rate
* Retention score
* Customer value at risk

This enables proactive retention campaigns before customers become inactive.

---

### 5. Decision Support Dashboard

The dashboard combines outputs from all previous analyses into a single interface designed for business users.

Instead of presenting raw statistics, the dashboard provides actionable recommendations for:

* Marketing campaigns
* Customer retention
* Inventory planning
* Regional investment
* Product prioritization

---

# Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* Statsmodels
* Plotly
* Streamlit
* Matplotlib

---

# Business Recommendations

Based on the analyses performed, we recommend the following actions:

* Prioritize **Champions** through VIP programs and personalized offers.
* Increase purchase frequency among **Occasional Customers** using targeted promotions.
* Launch reactivation campaigns for **Low-Engagement Customers** while optimizing marketing expenditure.
* Use seasonal forecasts to anticipate demand and reduce stock shortages.
* Focus commercial campaigns on wilayas combining strong revenue potential with stable demand.
* Continuously retrain forecasting and retention models as new transaction data becomes available.

---

# Dashboard Highlights

The interactive dashboard allows decision-makers to:

* Monitor revenue performance across Algeria
* Compare wilayas and customer segments
* Identify top-performing products
* Visualize seasonal demand patterns
* Track customer retention
* Export customer action lists
* Support inventory and marketing decisions

---

# Installation

Clone the repository:

```bash
git clone https://github.com/serene-b/energical-datasci.git
cd energical-datasci
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

---

# Team

* Belattou fatma zohra Sirine
* Leila Rechoum
* sayah lamis
* ibrahim khalil

---

# Acknowledgements

This project was developed as part of **DataFest 2026 – Challenge 2: ENERGICAL Data Intelligence**. The solution demonstrates how data science techniques can transform historical transactional data into practical commercial intelligence, enabling more informed decisions in sales, marketing, inventory management, and customer relationship management.
