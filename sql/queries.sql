-- 1. Top 5 funds by AUM

SELECT *
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month

SELECT
    strftime('%Y-%m', date) AS month,
    AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. SIP transactions YoY

SELECT
    strftime('%Y', transaction_date) AS year,
    SUM(amount_inr) AS sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year;

-- 4. Transactions by state

SELECT
    state,
    COUNT(*) AS transaction_count
FROM fact_transactions
GROUP BY state
ORDER BY transaction_count DESC;

-- 5. Funds with expense ratio below 1%

SELECT
    scheme_name,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1;

-- 6. Top 10 funds by Sharpe ratio

SELECT
    amfi_code,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;

-- 7. Average return by category

SELECT
    d.category,
    AVG(f.return_3yr_pct) AS avg_return
FROM fact_performance f
JOIN dim_fund d
ON f.amfi_code = d.amfi_code
GROUP BY d.category;

-- 8. Redemption amount by state

SELECT
    state,
    SUM(amount_inr) AS redemption_amount
FROM fact_transactions
WHERE transaction_type = 'REDEMPTION'
GROUP BY state
ORDER BY redemption_amount DESC;

-- 9. Gender-wise investment amount

SELECT
    gender,
    SUM(amount_inr) AS total_investment
FROM fact_transactions
GROUP BY gender;

-- 10. Risk category distribution

SELECT
    risk_category,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY risk_category;

