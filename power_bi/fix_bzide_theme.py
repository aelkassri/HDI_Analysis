import json

path = r"E:\Portfolio\projects\hdi_project\power_bi\HDI_Theme.json"

with open(path, "r", encoding="utf-8-sig") as f:
    theme = json.load(f)

fixes_applied = []

def fix_node(obj, parent_key=None):
    if isinstance(obj, dict):

        # ── 1. Remove ALL _comment keys ────────────────────────────────────────
        for k in [k for k in list(obj.keys()) if k == "_comment"]:
            del obj[k]
            fixes_applied.append("Removed _comment key")

        # ── 20. Fix capital-R "Responsive" key → "responsive" ──────────────────
        if "Responsive" in obj:
            obj["responsive"] = obj.pop("Responsive")
            fixes_applied.append('Renamed "Responsive" → "responsive"')

        for k in list(obj.keys()):
            v = obj[k]

            # ── 2 & 19. position: context-aware fix ────────────────────────────
            if k == "position" and isinstance(v, str):
                if parent_key == "dropShadow" and v.lower() == "outside":
                    obj[k] = "Outer"              # dropShadow: "Outside" → "Outer"
                    fixes_applied.append('dropShadow position "Outside" → "Outer"')
                elif parent_key == "dropShadow" and v.lower() == "inner":
                    pass                           # "Inner" is valid — keep it
                elif parent_key not in ("dropShadow",) and v[0].islower():
                    obj[k] = v.capitalize()        # e.g. "left" → "Left"
                    fixes_applied.append(f'position "{v}" → "{v.capitalize()}"')

            # ── 3 & 4. axisType: "Continuous" / "Continous" → "Scalar" ─────────
            elif k == "axisType" and isinstance(v, str):
                if v.lower() in ("continuous", "continous"):
                    obj[k] = "Scalar"
                    fixes_applied.append(f'axisType "{v}" → "Scalar"')
                elif v.lower() == "categorical":
                    obj[k] = "Categorical"
                    fixes_applied.append(f'axisType "{v}" → "Categorical"')

            # ── 5. legendMarkerRendering ────────────────────────────────────────
            elif k == "legendMarkerRendering" and isinstance(v, str):
                mapping = {
                    "markers only":   "markerOnly",
                    "markeronly":     "markerOnly",
                    "lineonly":       "lineOnly",
                    "lineandmarker":  "lineAndMarker",
                }
                fixed = mapping.get(v.lower().replace(" ", ""))
                if fixed and fixed != v:
                    obj[k] = fixed
                    fixes_applied.append(f'legendMarkerRendering "{v}" → "{fixed}"')

            # ── 6 & 7. labelPrecision / secLabelPrecision: "Auto"/"auto" → 0 ───
            elif k in ("labelPrecision", "secLabelPrecision"):
                if isinstance(v, str):
                    obj[k] = 0
                    fixes_applied.append(f'{k} "{v}" (string) → 0')
                elif isinstance(v, float):
                    obj[k] = int(v)
                    fixes_applied.append(f'{k} {v} (float) → {int(v)}')

            # ── 8. textSize: float → int ────────────────────────────────────────
            elif k == "textSize" and isinstance(v, float):
                obj[k] = int(round(v))
                fixes_applied.append(f'textSize {v} → {int(round(v))}')

            # ── 9. labelDisplayUnits: "auto" → 0 ───────────────────────────────
            elif k == "labelDisplayUnits" and isinstance(v, str):
                valid = ["0", "1", "1000", "1000000", "1000000000", "1000000000000", "-1"]
                if v not in valid:
                    obj[k] = 0
                    fixes_applied.append(f'labelDisplayUnits "{v}" → 0')

            # ── 10. markerColor: plain string → solid color object ───────────────
            elif k == "markerColor" and isinstance(v, str):
                color = v if v.startswith("#") else f"#{v}"
                obj[k] = {"solid": {"color": color}}
                fixes_applied.append(f'markerColor "{v}" → solid color object')

            # ── 11. mapTheme: "light" → "canvasLight" ───────────────────────────
            elif k == "mapTheme" and isinstance(v, str):
                valid_themes = ["aerial", "canvasDark", "canvasLight", "grayscale", "road"]
                if v not in valid_themes:
                    obj[k] = "canvasLight"
                    fixes_applied.append(f'mapTheme "{v}" → "canvasLight"')

            # ── 12. relativeRange: "" → "Last" ───────────────────────────────────
            elif k == "relativeRange" and v == "":
                obj[k] = "Last"
                fixes_applied.append('relativeRange "" → "Last"')

            # ── 13. relativePeriod: "" → "None" ──────────────────────────────────
            elif k == "relativePeriod" and v == "":
                obj[k] = "None"
                fixes_applied.append('relativePeriod "" → "None"')

            # ── 14. aiMode: "Absolute" → "absolute" ──────────────────────────────
            elif k == "aiMode" and isinstance(v, str):
                lower = v.lower()
                if v != lower:
                    obj[k] = lower
                    fixes_applied.append(f'aiMode "{v}" → "{lower}"')

            # ── 15. dataBarScalingType: "levelMAximum" → "levelMaximum" ──────────
            elif k == "dataBarScalingType" and isinstance(v, str):
                if v.lower() == "levelmaximum" and v != "levelMaximum":
                    obj[k] = "levelMaximum"
                    fixes_applied.append(f'dataBarScalingType "{v}" → "levelMaximum"')

            # ── 16. connectorType: "Default" → "curve" ────────────────────────────
            elif k == "connectorType" and isinstance(v, str):
                if v not in ("curve", "round"):
                    obj[k] = "curve"
                    fixes_applied.append(f'connectorType "{v}" → "curve"')

            # ── 17. density: "Default" → "default" ────────────────────────────────
            elif k == "density" and isinstance(v, str):
                lower = v.lower()
                if v != lower:
                    obj[k] = lower
                    fixes_applied.append(f'density "{v}" → "{lower}"')

            # ── 18. labelStyle: "Data, percent of total" fix ──────────────────────
            elif k == "labelStyle" and isinstance(v, str):
                if v == "Data, percent of total":
                    obj[k] = "Data value, percent of total"
                    fixes_applied.append('labelStyle "Data, percent of total" → "Data value, percent of total"')

            else:
                fix_node(v, parent_key=k)

    elif isinstance(obj, list):
        for item in obj:
            fix_node(item, parent_key=parent_key)

fix_node(theme)

with open(path, "w", encoding="utf-8-sig") as f:
    json.dump(theme, f, indent=2)

print(f"\n✅  HDI_Theme.json fixed and saved.")
print(f"   {len(fixes_applied)} corrections applied:\n")
for i, fix in enumerate(fixes_applied, 1):
    print(f"   {i:>3}. {fix}")
print("\nRe-import the file in Power BI — the validation banner should be gone.")
