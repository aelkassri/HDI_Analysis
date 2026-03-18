"""
build_hdi_map.py
================
Builds the final countries_map.json for the HDI Power BI dashboard.

WHAT THIS DOES (in order):
  1. Merges W. Sahara into Morocco (clean southern border)
  2. Removes all non-UN territories and unrecognised states
  3. Replaces all numeric ISO IDs with ISO alpha-3 codes
  4. Documents all changes in a change_log

TERRITORIES REMOVED:
  - W. Sahara          (732) → merged into Morocco (Moroccan territory, no separate HDI data available)
  - Fr. S. Antarctic   (260) → French overseas territory
  - Puerto Rico        (630) → US territory
  - Falkland Islands   (238) → British territory
  - Greenland          (304) → Danish territory
  - New Caledonia      (540) → French territory
  - Antarctica         (010) → Not a country
  - Taiwan             (158) → Not a UN member state
  - Kosovo             (None)→ Partially recognised
  - Somaliland         (None)→ Not recognised
  - N. Cyprus          (None)→ Not recognised

USAGE:
  1. Run fix_morocco_wsahara.py first (or use the original JSON as input)
  2. python build_hdi_map.py
  Edit INPUT_PATH below to match your file location.
"""

import json
from pathlib import Path
from datetime import datetime

# ── CONFIGURE PATH ────────────────────────────────────────────────────────────
INPUT_PATH  = Path(r"E:\Portfolio\projects\hdi_project\power_bi\map_data\countries_map.json")
OUTPUT_PATH = INPUT_PATH
# ─────────────────────────────────────────────────────────────────────────────

# Numeric ISO → Alpha-3
NUM_TO_A3 = {
    "004":"AFG","008":"ALB","012":"DZA","024":"AGO","032":"ARG","036":"AUS",
    "040":"AUT","031":"AZE","044":"BHS","050":"BGD","112":"BLR","056":"BEL",
    "084":"BLZ","204":"BEN","064":"BTN","068":"BOL","070":"BIH","072":"BWA",
    "076":"BRA","096":"BRN","100":"BGR","854":"BFA","108":"BDI","116":"KHM",
    "120":"CMR","124":"CAN","140":"CAF","148":"TCD","152":"CHL","156":"CHN",
    "170":"COL","180":"COD","178":"COG","188":"CRI","384":"CIV","191":"HRV",
    "192":"CUB","196":"CYP","203":"CZE","208":"DNK","262":"DJI","214":"DOM",
    "218":"ECU","818":"EGY","222":"SLV","226":"GNQ","232":"ERI","233":"EST",
    "748":"SWZ","231":"ETH","242":"FJI","246":"FIN","250":"FRA","266":"GAB",
    "270":"GMB","268":"GEO","276":"DEU","288":"GHA","300":"GRC","320":"GTM",
    "324":"GIN","624":"GNB","328":"GUY","332":"HTI","340":"HND","348":"HUN",
    "352":"ISL","356":"IND","360":"IDN","364":"IRN","368":"IRQ","372":"IRL",
    "376":"ISR","380":"ITA","388":"JAM","392":"JPN","400":"JOR","398":"KAZ",
    "404":"KEN","408":"PRK","410":"KOR","414":"KWT","417":"KGZ","418":"LAO",
    "428":"LVA","422":"LBN","426":"LSO","430":"LBR","434":"LBY","440":"LTU",
    "442":"LUX","450":"MDG","454":"MWI","458":"MYS","466":"MLI","478":"MRT",
    "484":"MEX","498":"MDA","496":"MNG","499":"MNE","504":"MAR","508":"MOZ",
    "104":"MMR","516":"NAM","524":"NPL","528":"NLD","554":"NZL","558":"NIC",
    "562":"NER","566":"NGA","807":"MKD","578":"NOR","512":"OMN","586":"PAK",
    "591":"PAN","598":"PNG","600":"PRY","604":"PER","608":"PHL","616":"POL",
    "620":"PRT","634":"QAT","642":"ROU","643":"RUS","646":"RWA","682":"SAU",
    "686":"SEN","688":"SRB","694":"SLE","702":"SGP","703":"SVK","705":"SVN",
    "706":"SOM","710":"ZAF","728":"SSD","724":"ESP","144":"LKA","729":"SDN",
    "740":"SUR","752":"SWE","756":"CHE","760":"SYR","762":"TJK","834":"TZA",
    "764":"THA","626":"TLS","768":"TGO","780":"TTO","788":"TUN","792":"TUR",
    "795":"TKM","800":"UGA","804":"UKR","784":"ARE","826":"GBR","840":"USA",
    "858":"URY","860":"UZB","862":"VEN","704":"VNM","275":"PSE","887":"YEM",
    "894":"ZMB","716":"ZWE","132":"CPV","174":"COM","462":"MDV","470":"MLT",
    "480":"MUS","678":"STP","690":"SYC","548":"VUT","090":"SLB","882":"WSM",
    "776":"TON","052":"BRB","051":"ARM",
    "260":"ATF",  # Fr. S. Antarctic Lands — grey (no HDI data)
    "630":"PRI",  # Puerto Rico            — grey (no HDI data)
    "238":"FLK",  # Falkland Islands       — grey (no HDI data)
    "304":"GRL",  # Greenland              — grey (no HDI data)
    "540":"NCL",  # New Caledonia          — grey (no HDI data)
    "010":"ATA",  # Antarctica             — grey (no HDI data)
    "158":"TWN",  # Taiwan                 — grey (no HDI data)
}

# W. Sahara only — merged into Morocco, not shown separately
REMOVE_BY_ID   = {"732"}
REMOVE_BY_NAME = set()  # All other territories kept (show as grey — no HDI data)

# ── STEP 1: MERGE W. SAHARA INTO MOROCCO ─────────────────────────────────────
def merge_wsahara(geometries):
    morocco  = next((g for g in geometries if g.get("id") == "504"), None)
    wsahara  = next((g for g in geometries if g.get("id") == "732"), None)

    if not morocco or not wsahara:
        print("⚠️  Morocco or W. Sahara not found — skipping merge")
        return geometries

    ws_ring  = wsahara["arcs"][0]           # [11, 12, 13, 14]
    mor_ring = morocco["arcs"][0]           # [-341, -15, 573]

    shared_encoded = -15
    shared_arc     = 14
    outer_ws       = [a for a in ws_ring if a != shared_arc]  # [11, 12, 13]

    pos          = mor_ring.index(shared_encoded)
    new_ring     = mor_ring[:pos] + outer_ws + mor_ring[pos + 1:]
    morocco["arcs"][0] = new_ring

    print(f"✅ Merged W. Sahara into Morocco")
    print(f"   Morocco arcs: {mor_ring} → {new_ring}")
    return geometries

# ── STEP 2: REMOVE NON-UN TERRITORIES ────────────────────────────────────────
def remove_territories(geometries):
    before = len(geometries)
    kept   = []
    removed = []

    for g in geometries:
        gid  = g.get("id", "")
        name = g["properties"].get("name", "")
        if gid in REMOVE_BY_ID or name in REMOVE_BY_NAME:
            removed.append(f"  {gid:>5}  {name}")
        else:
            kept.append(g)

    print(f"\n✅ Removed {len(removed)} non-UN territories:")
    for r in removed:
        print(r)
    print(f"   Geometries: {before} → {len(kept)}")
    return kept

# ── STEP 3: REPLACE NUMERIC IDS WITH ALPHA-3 ─────────────────────────────────
def update_ids(geometries):
    updated = []
    skipped = []

    for g in geometries:
        old_id = g.get("id")
        name   = g["properties"].get("name", "")
        if old_id is None:
            continue
        if old_id in NUM_TO_A3:
            g["id"] = NUM_TO_A3[old_id]
            updated.append(f"  {old_id:>5} → {g['id']}  ({name})")
        else:
            skipped.append(f"  {old_id:>5}  ({name})")

    print(f"\n✅ Updated {len(updated)} numeric IDs to alpha-3")
    if skipped:
        print(f"⚠️  {len(skipped)} IDs not mapped:")
        for s in skipped:
            print(s)
    return geometries

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print(f"Reading: {INPUT_PATH}\n")
    with open(INPUT_PATH, encoding="utf-8") as f:
        topo = json.load(f)

    geometries = topo["objects"]["countries"]["geometries"]

    geometries = merge_wsahara(geometries)
    geometries = remove_territories(geometries)
    geometries = update_ids(geometries)

    topo["objects"]["countries"]["geometries"] = geometries

    # ── CHANGE LOG ────────────────────────────────────────────────────────────
    if "change_log" not in topo:
        topo["change_log"] = []

    topo["change_log"].append({
        "date"   : datetime.now().strftime("%Y-%m-%d"),
        "author" : "HDI Project — build_hdi_map.py",
        "changes": [
            {
                "step"   : "1 — Morocco / W. Sahara merge",
                "detail" : "Arc -15 (shared border) replaced with W. Sahara outer arcs [11,12,13]. Morocco now covers the full territory."
            },
            {
                "step"   : "2 — Non-UN territories removed",
                "removed": sorted(list(REMOVE_BY_ID)) + sorted(list(REMOVE_BY_NAME)),
                "reason" : "These territories have no HDI values and are not UN member states. Removing them produces a clean map aligned with the UNDP dataset."
            },
            {
                "step"   : "3 — Numeric IDs → ISO alpha-3",
                "reason" : "Power BI Shaped Map Location field uses country_code (alpha-3). Updating IDs allows direct matching without any DAX or Power Query workarounds."
            }
        ]
    })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(topo, f, separators=(",", ":"))

    print(f"\n✅ Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()