# Map Customisations - countries_map.json

## 1. Western Sahara → Morocco border fix
**Date:** 2026-03-10  
**Script:** `../powerbi/fix_morocco_wsahara.py`  
**File modified:** `powerbi/countries_map.json`

**Problem:** W. Sahara appeared as a separate, uncoloured region next to Morocco,
creating a visual gap in the Power BI map since it has no HDI value in the dataset.

**Fix:** Merged W. Sahara geometry (id 732) into Morocco (id 504) by replacing
the shared border arc with W. Sahara's outer boundary arcs.
