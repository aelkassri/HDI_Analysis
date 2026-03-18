-- Active: 1772988847585@@127.0.0.1@3306@hdi
-------------- HDI: Analytical Queries -------------- 
-- Database: hdi
-- Table: hdi_master
-- Reference year: 2022

USE hdi;

-- Query 1: Top 10 Countries with Highest HDI score 
SELECT 
    country_code,
    country,
    hdi,
    gdp_per_capita,
    mean_years_schooling
FROM hdi_master
ORDER BY hdi DESC
LIMIT 10;

-- Query 2: 10 Countries with Lowest HDI score 
SELECT 
    country_code,
    country,
    hdi,
    gdp_per_capita,
    mean_years_schooling
FROM hdi_master
ORDER BY hdi ASC
LIMIT 10;

-- Query 3: HDI by income group
/* Aggregates HDI, schooling and GII by official World Bank income classification
   to reveal the development ladder pattern across economic groups. */
SELECT 
    COALESCE(income_level, 'Unclassified')  AS income_group,
    COUNT(*)                                AS country_count,
    ROUND(AVG(hdi), 3)                      AS avg_hdi,
    ROUND(AVG(mean_years_schooling), 2)     AS avg_schooling,
    ROUND(AVG(gii), 3)                      AS avg_gii
FROM hdi_master
GROUP BY income_level
ORDER BY avg_hdi DESC;

-- Note: Income group thresholds are approximations based on GDP per capita.
-- Official World Bank classifications use GNI per capita with different cutoffs.

-- Query 4: HDI overperformers 
/* Countries achieving high HDI (>0.75) despite low GDP (<5000)
   Highlights cases where education and gender equity compensate 
   for limited economic resources*/
SELECT
    country_code,
    country,
    hdi,
    ROUND(gdp_per_capita, 0) AS gdp_per_capita,
    mean_years_schooling,
    ROUND(gii, 3) AS gii
FROM hdi_master
WHERE gdp_per_capita < 5000 AND hdi > 0.75
ORDER BY hdi DESC;

-- Query 5: HDI underperformers
/* Countries with high GDP (>15000) but low HDI (<0.75)
   Reveals where economic wealth has not translated into 
   human development outcomes */
SELECT
    country_code,
    country,
    hdi,
    ROUND(gdp_per_capita, 0) AS gdp_per_capita,
    mean_years_schooling,
    ROUND(gii, 3) AS gii
FROM hdi_master
WHERE gdp_per_capita > 15000 AND hdi < 0.75
ORDER BY hdi ASC;