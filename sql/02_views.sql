-- View 1: HDI Overview
/* Main dashboard view for Power BI.
   Uses official World Bank income_level classifications from hdi_master. */
CREATE OR REPLACE VIEW v_hdi_overview AS
SELECT 
    country_code,
    country,
    hdi,
    ROUND(gdp_per_capita, 0)                    AS gdp_per_capita,
    mean_years_schooling,
    ROUND(education_expenditure_pct_gdp, 3)     AS education_expenditure_pct_gdp,
    ROUND(health_expenditure_per_capita, 0)     AS health_expenditure_per_capita,
    ROUND(government_effectiveness, 3)          AS government_effectiveness,
    ROUND(gii, 3)                               AS gii,
    region,
    COALESCE(income_level, 'Unclassified')      AS income_group
FROM hdi_master
ORDER BY hdi DESC;

-- View 2: Income Group Aggregations
/* Aggregated view using official World Bank income classifications. */
CREATE OR REPLACE VIEW v_income_groups AS
SELECT 
    COALESCE(income_level, 'Unclassified')      AS income_group,
    COUNT(*)                                    AS country_count,
    ROUND(AVG(hdi), 3)                          AS avg_hdi,
    ROUND(AVG(mean_years_schooling), 2)         AS avg_schooling,
    ROUND(AVG(gii), 3)                          AS avg_gii,
    ROUND(AVG(government_effectiveness), 3)     AS avg_gov_effectiveness
FROM hdi_master
GROUP BY income_level
ORDER BY avg_hdi DESC;

/*
View 3: Development Efficiency
Creates a derived classification comparing countries’ Human Development Index (HDI) to their
economic capacity (GDP per capita). Countries are labeled as:

- Overperformer: GDP per capita < 5000 and HDI > 0.75
- Underperformer: GDP per capita > 15000 and HDI < 0.75
- Expected: All other cases

This view consolidates HDI, GDP per capita, education, gender inequality, region, and income group
to support cross-country benchmarking of development efficiency.
*/

CREATE OR REPLACE VIEW v_development_efficiency AS
SELECT
    country_code,
    country,
    hdi,
    ROUND(gdp_per_capita, 0)        AS gdp_per_capita,
    mean_years_schooling,
    ROUND(gii, 3)                   AS gii,
    region,
    COALESCE(income_level, 'Unclassified') AS income_group,
    CASE
        WHEN gdp_per_capita < 5000  AND hdi > 0.75 THEN 'Overperformer'
        WHEN gdp_per_capita > 15000 AND hdi < 0.75 THEN 'Underperformer'
        ELSE 'Expected'
    END                             AS development_status
FROM hdi_master
ORDER BY hdi DESC;