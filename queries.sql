-- Create Table: advertising_data
CREATE TABLE IF NOT EXISTS advertising_data (
    TV REAL,
    Radio REAL,
    Newspaper REAL,
    Sales REAL
);

-- Query 1: Total Advertising Spend and Total Sales
SELECT 
    SUM(TV) AS total_tv_spend,
    SUM(Radio) AS total_radio_spend,
    SUM(Newspaper) AS total_newspaper_spend,
    SUM(Sales) AS total_sales
FROM advertising_data;

-- Query 2: Average Spend and Average Sales
SELECT 
    AVG(TV) AS avg_tv_spend,
    AVG(Radio) AS avg_radio_spend,
    AVG(Newspaper) AS avg_newspaper_spend,
    AVG(Sales) AS avg_sales
FROM advertising_data;

-- Query 3: TV Spend vs. Sales (Ordered by TV Spend)
SELECT TV, Sales 
FROM advertising_data
ORDER BY TV;

-- Query 4: ROI Calculation for Each Medium (TV, Radio, Newspaper)
SELECT 
    TV, Sales, 
    CASE WHEN TV != 0 THEN Sales / TV ELSE 0 END AS tv_roi,
    Radio, 
    CASE WHEN Radio != 0 THEN Sales / Radio ELSE 0 END AS radio_roi,
    Newspaper, 
    CASE WHEN Newspaper != 0 THEN Sales / Newspaper ELSE 0 END AS newspaper_roi
FROM advertising_data;
