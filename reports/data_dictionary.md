# Data Dictionary

## Project Overview

This document defines all major datasets, columns, data types, and business meanings used in the Bluestock Mutual Fund Analytics Capstone Project.

---

# 1. dim_fund

Source File:
`01_fund_master.csv`

Description:
Master dimension table containing metadata for all mutual fund schemes.

| Column Name        | Data Type | Description                           |
| ------------------ | --------- | ------------------------------------- |
| amfi_code          | TEXT      | Unique AMFI mutual fund scheme code   |
| fund_house         | TEXT      | Asset Management Company (AMC) name   |
| scheme_name        | TEXT      | Full official scheme name             |
| category           | TEXT      | Fund category (Equity/Debt/Hybrid)    |
| sub_category       | TEXT      | Large Cap, Mid Cap, Small Cap, etc.   |
| plan               | TEXT      | Direct or Regular plan                |
| launch_date        | DATE      | Fund launch date                      |
| benchmark          | TEXT      | Benchmark index                       |
| expense_ratio_pct  | REAL      | Annual expense ratio percentage       |
| exit_load_pct      | REAL      | Exit load charged on redemption       |
| fund_manager       | TEXT      | Primary fund manager                  |
| risk_category      | TEXT      | SEBI risk category                    |
| sebi_category_code | TEXT      | Internal category classification code |

---

# 2. fact_nav

Source File:
`02_nav_history.csv`

Description:
Stores historical daily NAV values for all mutual fund schemes.

| Column Name | Data Type | Description                   |
| ----------- | --------- | ----------------------------- |
| amfi_code   | TEXT      | Foreign key to dim_fund       |
| date        | DATE      | NAV reporting date            |
| nav         | REAL      | Net Asset Value of the scheme |

Derived Fields:

* Daily return %
* Rolling averages
* CAGR
* Volatility metrics

---

# 3. fact_transactions

Source File:
`08_investor_transactions.csv`

Description:
Contains investor-level SIP, Lumpsum, and Redemption transactions.

| Column Name        | Data Type | Description                          |
| ------------------ | --------- | ------------------------------------ |
| investor_id        | TEXT      | Unique investor identifier           |
| transaction_date   | DATE      | Transaction date                     |
| amfi_code          | TEXT      | Mutual fund scheme code              |
| transaction_type   | TEXT      | SIP / Lumpsum / Redemption           |
| amount_inr         | REAL      | Transaction amount in INR            |
| state              | TEXT      | Investor state                       |
| city               | TEXT      | Investor city                        |
| city_tier          | TEXT      | T30 or B30 classification            |
| age_group          | TEXT      | Investor age bracket                 |
| gender             | TEXT      | Male / Female                        |
| annual_income_lakh | REAL      | Annual income in lakh INR            |
| payment_mode       | TEXT      | UPI / Net Banking / Mandate / Cheque |
| kyc_status         | TEXT      | Verified or Pending KYC              |

---

# 4. fact_performance

Source File:
`07_scheme_performance.csv`

Description:
Stores fund performance and risk metrics computed using NAV history and benchmark data.

| Column Name        | Data Type | Description                         |
| ------------------ | --------- | ----------------------------------- |
| amfi_code          | TEXT      | Mutual fund scheme code             |
| return_1yr_pct     | REAL      | 1-year return percentage            |
| return_3yr_pct     | REAL      | 3-year CAGR percentage              |
| return_5yr_pct     | REAL      | 5-year CAGR percentage              |
| benchmark_3yr_pct  | REAL      | Benchmark 3-year CAGR               |
| alpha              | REAL      | Excess return above benchmark       |
| beta               | REAL      | Market sensitivity metric           |
| sharpe_ratio       | REAL      | Risk-adjusted return ratio          |
| sortino_ratio      | REAL      | Downside-risk adjusted return ratio |
| std_dev_ann_pct    | REAL      | Annualised standard deviation       |
| max_drawdown_pct   | REAL      | Worst peak-to-trough decline        |
| morningstar_rating | INTEGER   | Simulated 1-5 star rating           |

---

# 5. fact_aum

Source File:
`03_aum_by_fund_house.csv`

Description:
Quarterly Assets Under Management (AUM) values for major fund houses.

| Column Name | Data Type | Description                          |
| ----------- | --------- | ------------------------------------ |
| fund_house  | TEXT      | AMC name                             |
| quarter     | TEXT      | Quarter period                       |
| aum_crore   | REAL      | Assets Under Management in crore INR |

---

# 6. monthly_sip_inflows

Source File:
`04_monthly_sip_inflows.csv`

Description:
Monthly SIP industry statistics published by AMFI.

| Column Name               | Data Type | Description                          |
| ------------------------- | --------- | ------------------------------------ |
| month                     | TEXT      | YYYY-MM format                       |
| sip_inflow_crore          | REAL      | Monthly SIP inflow in crore INR      |
| active_sip_accounts_crore | REAL      | Active SIP accounts in crore         |
| new_sip_accounts_lakh     | REAL      | New SIP registrations in lakh        |
| sip_aum_lakh_crore        | REAL      | SIP assets under management          |
| yoy_growth_pct            | REAL      | Year-over-year SIP growth percentage |

---

# 7. category_inflows

Source File:
`05_category_inflows.csv`

Description:
Monthly category-wise mutual fund inflows and outflows.

| Column Name      | Data Type | Description                    |
| ---------------- | --------- | ------------------------------ |
| month            | TEXT      | Reporting month                |
| category         | TEXT      | Fund category                  |
| net_inflow_crore | REAL      | Net inflow amount in crore INR |

---

# 8. industry_folio_count

Source File:
`06_industry_folio_count.csv`

Description:
Industry-level folio count statistics across fund segments.

| Column Name       | Data Type | Description               |
| ----------------- | --------- | ------------------------- |
| date              | DATE      | Reporting date            |
| segment           | TEXT      | Equity / Debt / Hybrid    |
| folio_count_crore | REAL      | Number of folios in crore |

---

# 9. portfolio_holdings

Source File:
`09_portfolio_holdings.csv`

Description:
Top equity holdings for mutual fund schemes.

| Column Name  | Data Type | Description                     |
| ------------ | --------- | ------------------------------- |
| amfi_code    | TEXT      | Mutual fund scheme code         |
| stock_symbol | TEXT      | Equity stock ticker             |
| company_name | TEXT      | Company name                    |
| sector       | TEXT      | Industry sector                 |
| weight_pct   | REAL      | Portfolio allocation percentage |

---

# 10. benchmark_indices

Source File:
`10_benchmark_indices.csv`

Description:
Daily benchmark index closing values used for fund comparison.

| Column Name | Data Type | Description               |
| ----------- | --------- | ------------------------- |
| date        | DATE      | Trading date              |
| index_name  | TEXT      | Benchmark index name      |
| close_value | REAL      | Daily closing index value |

---

# Data Quality Checks Performed

1. Removed duplicate rows
2. Converted dates to datetime format
3. Validated NAV values greater than zero
4. Standardised transaction types
5. Validated expense ratio ranges
6. Validated KYC status values
7. Forward-filled missing NAV values for weekends and holidays
8. Converted numerical columns to correct datatypes

---

# Technologies Used

* Python
* Pandas
* NumPy
* SQLite
* SQLAlchemy
* Jupyter Notebook
* Power BI
* Plotly
* Matplotlib
* Seaborn
