# Data Dictionary: HDI Cross-Country Analysis (2022)
                   A Multi-Source Data Pipeline & Integrity Audit

---

## 1. `processed_data/master_dataset.csv`
**Primary Analytical Dataset.** Built by merging five source files via ISO alpha-3 identifiers.  
**Dimensions:** 186 rows × 11 columns · **Reference Year:** 2022

| Column | Type | Description | Source | Missing |
| :--- | :--- | :--- | :--- | :--- |
| `country_code` | string | ISO alpha-3 identifier (e.g., `MAR`, `USA`) | World Bank | 0 |
| `country` | string | Official country name | UNDP | 0 |
| `hdi` | float | **Target Variable:** Human Development Index (0–1). | UNDP HDR | 0 |
| `gdp_per_capita` | float | **Strategic Proxy:** GDP per capita (PPP, current intl. $). Used as a high-density proxy for GNI. Signal audit confirmed a logarithmic alignment of $r = 0.95$ with HDI (linear $r = 0.72$), validating the log-transformation and confirming GDP per capita as a high-fidelity proxy. | World Bank | 0 |
| `mean_years_schooling` | float | Average years of schooling for adults (25+). | UNDP HDR | 0 |
| `education_expenditure_pct_gdp` | float | Gov. expenditure on education as % of GDP. | World Bank | 34 |
| `health_expenditure_per_capita` | float | Current health expenditure per capita (USD). | World Bank | 0 |
| `government_effectiveness` | float | WGI Score (−2.5 to +2.5). Perceptions of public service quality. | World Bank | 0 |
| `gii` | float | Gender Inequality Index (0–1). Higher = more unequal. | UNDP HDR | 23 |
| `region` | string | World Bank geographic classification (7 categories). | World Bank | 0 |
| `income_level` | string | World Bank income classification (4 categories). | World Bank | 2 |

### **Methodological & Missing Value Notes**

| Column | Missing | Technical Justification & Handling |
| :--- | :--- | :--- |
<<<<<<< HEAD
| **`gdp_per_capita`** | 0 | **Proxy Decision:** While the official HDI uses GNI, GDP (PPP) was selected to maximise overlap with World Bank Governance and Health indicators. Signal audit confirmed a logarithmic alignment of $r = 0.95$ with HDI (linear $r = 0.72$), validating the proxy selection. |
| **`education_expenditure`** | 34 | Data density insufficient for 2022 cycle. Retained as `NaN` in master; excluded from regression to maintain statistical power. |
=======
| **`gdp_per_capita`** | 0 | **Proxy Decision:** While the official HDI uses GNI, GDP (PPP) was utilized to ensure 100% overlap with World Bank Governance and Health indicators. Signal audit confirmed a 0.95 correlation with target. |
| **`education_expenditure`** | 34 | Data density insufficient for 2022 cycle. Retained as `NaN` in master; **excluded from regression** to maintain statistical power. |
>>>>>>> 1698cf8405ce618745f7622c4af77879836df2da
| **`gii`** | 23 | Not published by UNDP for these specific territories. Preserved via Left Join to maintain core country list. |
| **`income_level`** | 2 | ETH & VEN unclassified in 2022. Logically mapped to `"Unclassified"` for BI downstream consistency. |

---

## 2. `processed_data/std_coef.csv`
**Standardized Regression Output.** Generated from the pipeline integrity validation notebook (`04_statistical_analysis.ipynb`).

| Column | Type | Description |
| :--- | :--- | :--- |
| `variable` | string | Predictor name (includes `log_gdp_per_capita`). |
| `std_coefficient` | float | **Beta ($\beta^*$):** Change in HDI (SD units) per 1 SD change in predictor. Enables direct signal comparison. |
| `p_value` | float | Significance test. Threshold used: $p < 0.05$. |

### **Model Specifications**
- **GDP Transformation:** Logarithmic layer applied ($log\_gdp = \ln(gdp)$) to linearize the signal and satisfy homoscedasticity.
- **Integrity Check:** Multicollinearity managed via VIF audit.
- **Key validated signals ($p < 0.001$):** `log_gdp_per_capita` ($\beta^* = 0.540$), `mean_years_schooling` ($\beta^* = 0.325$), `gii` ($\beta^* = -0.240$).

---

## 3. MySQL — `hdi.hdi_master` Table
**Production-Ready Warehouse Table.** Loaded via SQLAlchemy (`05_load_to_mysql.ipynb`).

| View Name | Technical Logic | Analytical Purpose |
| :--- | :--- | :--- |
| **`v_hdi_overview`** | Joins metrics with `income_group` cleaning. | Primary source for Power BI Map and Table visuals. |
| **`v_income_groups`** | Aggregates HDI/GDP stats by WB classification. | Powers "Development by Income Tier" bar charts. |
| **`v_development_efficiency`** | Classifies countries by performance pattern (Actual vs. Expected HDI). | Identifies Overperformers relative to economic baseline. |

---

## 4. Source File Reference

| Level | Location | Filename | Description |
| :--- | :--- | :--- | :--- |
| **Raw** | `raw_data/` | `worldbank_raw.csv` | Initial WDI pull (798 rows). |
<<<<<<< HEAD
| **Raw** | `raw_data/` | `wgi_government_effectiveness_raw.zip` | Raw Excel export from Worldwide Governance Indicators. |
| **Processed** | `processed_data/` | `master_dataset.csv` | Final audited analytical dataset. |
| **Output** | `processed_data/` | `std_coef.csv` | Validation output for visualization in Power BI. |
=======
| **Raw** | `raw_data/` | `wgi_gov_eff.zip` | Raw Excel export from Worldwide Governance Indicators. |
| **Processed** | `processed_data/` | `master_dataset.csv` | Final audited analytical dataset for modeling. |
| **Output** | `processed_data/` | `std_coef.csv` | Model results for visualization in Power BI. |
>>>>>>> 1698cf8405ce618745f7622c4af77879836df2da
