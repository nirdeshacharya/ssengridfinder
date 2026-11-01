import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BASE = os.path.join(PROJECT_ROOT, "data") + "/"
ROOT_BUNDLE = os.path.join(PROJECT_ROOT, "site_finder_bundle_2026.json")

def norm_name(s, keep_kv=False):
    if not s:
        return ""
    s = str(s).upper().strip()
    if keep_kv:
        s = re.sub(r'\b(PRIMARY|BSP|GSP|SUBSTATION|S/S)\b', '', s)
    else:
        s = re.sub(r'\b(PRIMARY|BSP|GSP|SUBSTATION|S/S|11KV|33KV|6\.6KV|132KV|275KV|400KV)\b', '', s)
    s = re.sub(r'[^A-Z0-9]', '', s)
    return s

def safe_float(v, default=None):
    if v is None or v == "" or v == "N/A" or v == "NA":
        return default
    try:
        f = float(v)
        if math.isnan(f) or math.isinf(f):
            return default
        return round(f, 2)
    except Exception:
        return default

def osgb_to_latlon(gridref):
    if not gridref or not isinstance(gridref, str):
        return None, None
    s = re.sub(r'\s+', '', gridref.upper())
    m = re.match(r'^([A-Z]{2})(\d+)$', s)
    if not m:
        return None, None
    letters, digits = m.group(1), m.group(2)
    if len(digits) % 2 != 0 or len(digits) < 4:
        return None, None
    l1 = ord(letters[0]) - ord('A')
    l2 = ord(letters[1]) - ord('A')
    if l1 > 7:
        l1 -= 1
    if l2 > 7:
        l2 -= 1
    e100k = ((l1 - 2) % 5) * 5 + (l2 % 5)
    n100k = (19 - (l1 // 5) * 5) - (l2 // 5)
    if e100k < 0 or e100k > 6 or n100k < 0 or n100k > 12:
        return None, None
    half = len(digits) // 2
    scale = 10 ** (5 - half)
    e = e100k * 100000 + int(digits[:half]) * scale
    n = n100k * 100000 + int(digits[half:]) * scale

    a, b = 6377563.396, 6356256.909
    F0 = 0.9996012717
    lat0 = math.radians(49.0)
    lon0 = math.radians(-2.0)
    N0, E0 = -100000.0, 400000.0
    e2 = 1 - (b * b) / (a * a)
    n_val = (a - b) / (a + b)
    n2, n3 = n_val * n_val, n_val ** 3

    lat = lat0
    M = 0.0
    for _ in range(12):
        lat = (n - N0 - M) / (a * F0) + lat
        Ma = (1 + n_val + 1.25 * n2 + 1.25 * n3) * (lat - lat0)
        Mb = (3 * n_val + 3 * n2 + 2.625 * n3) * math.sin(lat - lat0) * math.cos(lat + lat0)
        Mc = (1.875 * n2 + 1.875 * n3) * math.sin(2 * (lat - lat0)) * math.cos(2 * (lat + lat0))
        Md = (35.0 / 24.0) * n3 * math.sin(3 * (lat - lat0)) * math.cos(3 * (lat + lat0))
        M = b * F0 * (Ma - Mb + Mc - Md)
        if abs(n - N0 - M) < 0.01:
            break

    cosLat, sinLat, tanLat = math.cos(lat), math.sin(lat), math.tan(lat)
    nu = a * F0 / math.sqrt(1 - e2 * sinLat * sinLat)
    rho = a * F0 * (1 - e2) / ((1 - e2 * sinLat * sinLat) ** 1.5)
    eta2 = nu / rho - 1
    tan2, tan4, tan6 = tanLat * tanLat, tanLat ** 4, tanLat ** 6
    secLat = 1.0 / cosLat
    nu3, nu5, nu7 = nu ** 3, nu ** 5, nu ** 7
    VII = tanLat / (2 * rho * nu)
    VIII = tanLat / (24 * rho * nu3) * (5 + 3 * tan2 + eta2 - 9 * tan2 * eta2)
    IX = tanLat / (720 * rho * nu5) * (61 + 90 * tan2 + 45 * tan4)
    X = secLat / nu
    XI = secLat / (6 * nu3) * (nu / rho + 2 * tan2)
    XII = secLat / (120 * nu5) * (5 + 28 * tan2 + 24 * tan4)
    XIIA = secLat / (5040 * nu7) * (61 + 662 * tan2 + 1320 * tan4 + 720 * tan6)

    dE = e - E0
    lat_osgb = lat - VII * (dE ** 2) + VIII * (dE ** 4) - IX * (dE ** 6)
    lon_osgb = lon0 + X * dE - XI * (dE ** 3) + XII * (dE ** 5) - XIIA * (dE ** 7)
    lat_deg = math.degrees(lat_osgb) + 0.0005
    lon_deg = math.degrees(lon_osgb) - 0.0012
    return round(lat_deg, 5), round(lon_deg, 5)

def read_xlsx_sheet(path, sheet_idx):
    with zipfile.ZipFile(path, "r") as z:
        ss = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
                texts = [t.text or "" for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")]
                ss.append("".join(texts))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rel_map = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        sheets = wb.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheets")
        s = list(sheets)[sheet_idx]
        name = s.attrib["name"]
        rid = s.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        target = "xl/" + rel_map[rid]
        sroot = ET.fromstring(z.read(target))
        rows = []
        for row in sroot.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"):
            rdict = {}
            for c in row:
                ref = c.attrib.get("r", "")
                col = "".join(ch for ch in ref if ch.isalpha())
                t = c.attrib.get("t", "")
                v = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                val = v.text if v is not None else ""
                if t == "s" and val != "":
                    val = ss[int(val)]
                rdict[col] = val
            rows.append(rdict)
        return name, rows

with open(BASE + "ssen_bundle_v2.json") as f:
    bundle = json.load(f)
with open(BASE + "sepd_heatmap_may2026.json") as f:
    sepd_hm = json.load(f)
with open(BASE + "shepd_heatmap_may2026.json") as f:
    shepd_hm = json.load(f)

# 1. Local Authority Reference (NSHR 2026)
_, sepd_lep_rows = read_xlsx_sheet(BASE + "sepd_nshr_2026.xlsx", 6)
_, shepd_la_rows = read_xlsx_sheet(BASE + "shepd_nshr_2026.xlsx", 4)

la_by_sub = {}
la_by_bsp = defaultdict(list)
la_by_gsp = defaultdict(list)

for r in sepd_lep_rows[2:]:
    la = r.get("B", "").strip()
    gsp = r.get("C", "").strip()
    bsp = r.get("D", "").strip()
    prim = r.get("E", "").strip()
    if not la:
        continue
    if prim:
        la_by_sub[("SEPD", norm_name(prim))] = la
    if bsp and la not in la_by_bsp[("SEPD", norm_name(bsp))]:
        la_by_bsp[("SEPD", norm_name(bsp))].append(la)
    if gsp and la not in la_by_gsp[("SEPD", norm_name(gsp))]:
        la_by_gsp[("SEPD", norm_name(gsp))].append(la)

for r in shepd_la_rows[1:]:
    la = r.get("B", "").strip()
    gsp = r.get("C", "").strip()
    prim = r.get("D", "").strip()
    if not la or la == "Local Authority":
        continue
    if prim:
        la_by_sub[("SHEPD", norm_name(prim))] = la
    if gsp and la not in la_by_gsp[("SHEPD", norm_name(gsp))]:
        la_by_gsp[("SHEPD", norm_name(gsp))].append(la)

# 2. EISD from NSHR 2026
_, sepd_eisd_rows = read_xlsx_sheet(BASE + "sepd_nshr_2026.xlsx", 7)
_, shepd_eisd_rows = read_xlsx_sheet(BASE + "shepd_nshr_2026.xlsx", 5)
eisd_by_gsp = {}
for area, rows in [("SEPD", sepd_eisd_rows[2:]), ("SHEPD", shepd_eisd_rows[2:])]:
    for r in rows:
        gsp = r.get("B", "").strip()
        if not gsp:
            continue
        dem_eisd = r.get("C", "").strip()
        gen_eisd = r.get("E", "").strip()
        eisd_by_gsp[(area, norm_name(gsp))] = {
            "demand_eisd": dem_eisd if dem_eisd and dem_eisd != "NA" else None,
            "gen_eisd": gen_eisd if gen_eisd and gen_eisd != "NA" else None,
            "status": (r.get("D", "").strip() or r.get("F", "").strip())
        }

# 3. May 2026 LTDS Table 3 & Table 7
_, sepd_t3 = read_xlsx_sheet(BASE + "sepd_ltds_may2026.xlsx", 3)
_, shepd_t3 = read_xlsx_sheet(BASE + "shepd_ltds_may2026.xlsx", 2)

ltds_t3_by_sub = {}
for area, rows in [("SEPD", sepd_t3[3:]), ("SHEPD", shepd_t3[3:])]:
    for r in rows:
        gsp = r.get("A", "").strip()
        ss = r.get("B", "").strip()
        kv = r.get("C", "").strip()
        if not ss or ss.isdigit():
            continue
        t3_entry = {
            "gsp": gsp,
            "name": ss,
            "kv": kv,
            "firm_mva": safe_float(r.get("L")),
            "actual_2425": safe_float(r.get("D")),
            "pf": safe_float(r.get("E"), 0.98),
            "f_2526": safe_float(r.get("G")),
            "f_2627": safe_float(r.get("H")),
            "f_2728": safe_float(r.get("I")),
            "f_2829": safe_float(r.get("J")),
            "f_2930": safe_float(r.get("K")),
        }
        ltds_t3_by_sub[(area, norm_name(ss, keep_kv=True))] = t3_entry
        if (area, norm_name(ss)) not in ltds_t3_by_sub:
            ltds_t3_by_sub[(area, norm_name(ss))] = t3_entry

_, sepd_t7 = read_xlsx_sheet(BASE + "sepd_ltds_may2026.xlsx", 8)
_, shepd_t7 = read_xlsx_sheet(BASE + "shepd_ltds_may2026.xlsx", 6)
ltds_t7_by_gsp = {}
for area, rows in [("SEPD", sepd_t7[3:]), ("SHEPD", shepd_t7[2:])]:
    for r in rows:
        gsp = r.get("A", "").strip()
        if not gsp:
            continue
        pf = safe_float(r.get("D"), 0.98) or 0.98
        # Convert MW to MVA via pf
        def mw_to_mva(val):
            v = safe_float(val)
            return round(v / pf, 2) if v is not None else None
        ltds_t7_by_gsp[(area, norm_name(gsp))] = {
            "kv": r.get("B", "").strip(),
            "actual_2425": mw_to_mva(r.get("C")),
            "pf": pf,
            "f_2526": mw_to_mva(r.get("E")),
            "f_2627": mw_to_mva(r.get("F")),
            "f_2728": mw_to_mva(r.get("G")),
            "f_2829": mw_to_mva(r.get("H")),
            "f_2930": mw_to_mva(r.get("I")),
        }

# 4. NSHR 2026 Headroom sheets
def parse_nshr_sheet(rows, is_shepd=False):
    out = {}
    if not is_shepd:
        w_cols = {"2027": "J", "2028": "K", "2030": "M", "2032": "O", "2035": "R", "2040": "S", "2045": "T", "2050": "U"}
        s_cols = {"2027": "W", "2028": "X", "2030": "Z", "2032": "AB", "2035": "AE", "2040": "AF", "2045": "AG", "2050": "AH"}
        a_cols = {"2027": "AJ", "2028": "AK", "2030": "AM", "2032": "AO", "2035": "AR", "2040": "AS", "2045": "AT", "2050": "AU"}
    else:
        w_cols = {"2027": "I", "2028": "J", "2030": "L", "2032": "N", "2035": "Q", "2040": "S", "2045": "T", "2050": "U"}
        s_cols = {"2027": "W", "2028": "X", "2030": "Z", "2032": "AB", "2035": "AE", "2040": "AG", "2045": "AH", "2050": "AI"}
        a_cols = {"2027": "AK", "2028": "AL", "2030": "AN", "2032": "AP", "2035": "AS", "2040": "AU", "2045": "AV", "2050": "AW"}

    for r in rows[2:]:
        if not is_shepd:
            sub_raw = r.get("D", "").strip() or r.get("C", "").strip()
            scen = r.get("E", "").strip()
            gsp = r.get("B", "").strip()
            bsp = r.get("C", "").strip()
            gref = r.get("F", "").strip()
            stx = r.get("G", "").strip()
            upstr = r.get("H", "").strip()
            contr = safe_float(r.get("I"))
        else:
            sub_raw = r.get("C", "").strip()
            scen = r.get("D", "").strip()
            gsp = r.get("B", "").strip()
            bsp = ""
            gref = r.get("E", "").strip()
            stx = r.get("F", "").strip()
            upstr = r.get("G", "").strip()
            contr = safe_float(r.get("H"))

        if not sub_raw or not scen:
            continue
        key = norm_name(sub_raw)
        if not key:
            continue
        if key not in out:
            out[key] = {
                "raw_name": sub_raw,
                "gsp": gsp,
                "bsp": bsp,
                "grid_ref": gref,
                "single_tx": stx == "YES",
                "upstream_constraint": upstr == "YES",
                "contracted_mva": contr,
                "scenarios": {}
            }
        else:
            if gsp and not out[key]["gsp"]:
                out[key]["gsp"] = gsp
            if bsp and not out[key]["bsp"]:
                out[key]["bsp"] = bsp
            if gref and not out[key]["grid_ref"]:
                out[key]["grid_ref"] = gref
            if contr is not None and out[key]["contracted_mva"] is None:
                out[key]["contracted_mva"] = contr

        scen_code = "MIN" if "MINIMUM" in scen.upper() else scen.upper()
        out[key]["scenarios"][scen_code] = {
            "W": [safe_float(r.get(col)) for _, col in w_cols.items()],
            "S": [safe_float(r.get(col)) for _, col in s_cols.items()],
            "A": [safe_float(r.get(col)) for _, col in a_cols.items()],
        }
    return out

_, sepd_p_dem = read_xlsx_sheet(BASE + "sepd_nshr_2026.xlsx", 2)
_, sepd_p_gen = read_xlsx_sheet(BASE + "sepd_nshr_2026.xlsx", 3)
_, sepd_b_dem = read_xlsx_sheet(BASE + "sepd_nshr_2026.xlsx", 4)
_, sepd_b_gen = read_xlsx_sheet(BASE + "sepd_nshr_2026.xlsx", 5)
_, shepd_p_dem = read_xlsx_sheet(BASE + "shepd_nshr_2026.xlsx", 2)
_, shepd_p_gen = read_xlsx_sheet(BASE + "shepd_nshr_2026.xlsx", 3)

nshr_sepd_dem = parse_nshr_sheet(sepd_p_dem, is_shepd=False)
nshr_sepd_dem.update(parse_nshr_sheet(sepd_b_dem, is_shepd=False))
nshr_sepd_gen = parse_nshr_sheet(sepd_p_gen, is_shepd=False)
nshr_sepd_gen.update(parse_nshr_sheet(sepd_b_gen, is_shepd=False))

nshr_shepd_dem = parse_nshr_sheet(shepd_p_dem, is_shepd=True)
nshr_shepd_gen = parse_nshr_sheet(shepd_p_gen, is_shepd=True)

# 5. March 2026 Headroom Dashboard Data (from bundle["substations"])
dash_by_sub = {}
for s in bundle.get("substations", []):
    area = "SEPD" if "Southern" in s.get("region", "") or s.get("area") == "SEPD" else "SHEPD"
    dash_by_sub[(area, norm_name(s.get("name", "")))] = s

# 6. Merge all substations from May 2026 Heatmap JSONs + NSHR 2026
unified = []
seen_keys = set()

all_hm_subs = []
for s in sepd_hm.get("Substations", []):
    s["_area"] = "SEPD"
    all_hm_subs.append(s)
for s in shepd_hm.get("Substations", []):
    s["_area"] = "SHEPD"
    all_hm_subs.append(s)

for hm in all_hm_subs:
    area = hm["_area"]
    raw_name = hm.get("name", "").strip()
    key = norm_name(raw_name)
    if not key:
        continue
    seen_keys.add((area, key))

    stype = hm.get("type", "Primary")
    gsp_raw = hm.get("GSP") if hm.get("GSP") not in (None, "Not Applicable") else (raw_name if stype == "GSP" else "")
    bsp_raw = hm.get("BSP") if hm.get("BSP") not in (None, "Not Applicable") else (raw_name if stype == "BSP" else "")

    dash = dash_by_sub.get((area, key), {})
    t3 = ltds_t3_by_sub.get((area, norm_name(raw_name, keep_kv=True))) or ltds_t3_by_sub.get((area, key), {})
    t7 = ltds_t7_by_gsp.get((area, key), {}) if stype == "GSP" else {}
    ndem = (nshr_sepd_dem if area == "SEPD" else nshr_shepd_dem).get(key, {})
    ngen = (nshr_sepd_gen if area == "SEPD" else nshr_shepd_gen).get(key, {})

    if not gsp_raw and ndem.get("gsp"):
        gsp_raw = ndem["gsp"]
    if not gsp_raw and t3.get("gsp"):
        gsp_raw = t3["gsp"]
    if not bsp_raw and ndem.get("bsp"):
        bsp_raw = ndem["bsp"]

    # Local Authority lookup
    la = la_by_sub.get((area, key))
    if not la and stype == "BSP":
        las = la_by_bsp.get((area, key), [])
        la = las[0] if las else None
    if not la and gsp_raw:
        las = la_by_gsp.get((area, norm_name(gsp_raw)), [])
        la = las[0] if las else None
    if not la and stype == "GSP":
        las = la_by_gsp.get((area, key), [])
        la = las[0] if las else None

    # Voltages
    vols = hm.get("voltages") or []
    vols_clean = sorted([int(v) if float(v).is_integer() else float(v) for v in vols if v], reverse=True)
    voltage_str = "/".join(f"{v}kV" for v in vols_clean) if vols_clean else (f"{t3.get('kv')}kV" if t3.get("kv") else "11kV")

    # Coordinates
    lat = safe_float(hm.get("latitude"), 5)
    lon = safe_float(hm.get("longitude"), 5)
    if (lat is None or lon is None) and ndem.get("grid_ref"):
        lat, lon = osgb_to_latlon(ndem["grid_ref"])

    # Firm Capacity & Forecasted Maximum Demand (2026 NDP Formula: Demand Headroom = Firm Capacity - Forecasted Max Demand)
    firm_dem = safe_float(hm.get("demandFirmCapacity"))
    if firm_dem is None:
        firm_dem = t3.get("firm_mva")
    if firm_dem is None:
        firm_dem = safe_float(dash.get("firm_cap"))

    obs_max_dem = safe_float(hm.get("demandMaximum"))
    if obs_max_dem is None:
        obs_max_dem = t3.get("actual_2425") or t7.get("actual_2425") or safe_float(dash.get("peak_dem"))

    # Forecasted Maximum Demand for 2026/27 (and multi-year LTDS series 25/26..29/30)
    f_2526 = t3.get("f_2526") if t3.get("f_2526") is not None else t7.get("f_2526")
    f_2627 = t3.get("f_2627") if t3.get("f_2627") is not None else t7.get("f_2627")
    f_2728 = t3.get("f_2728") if t3.get("f_2728") is not None else t7.get("f_2728")
    f_2829 = t3.get("f_2829") if t3.get("f_2829") is not None else t7.get("f_2829")
    f_2930 = t3.get("f_2930") if t3.get("f_2930") is not None else t7.get("f_2930")

    # If LTDS forecast 26/27 is not present, derive from Firm Capacity - NSHR 2027 HT Winter Headroom (since Demand Headroom = Firm Capacity - Forecasted Maximum Demand!)
    ht_w_arr = ndem.get("scenarios", {}).get("HT", {}).get("W") or []
    ht_w_2027 = ht_w_arr[0] if ht_w_arr else None
    if f_2627 is None and firm_dem is not None and ht_w_2027 is not None:
        f_2627 = round(max(0.0, firm_dem - ht_w_2027), 2)
    if f_2627 is None and obs_max_dem is not None:
        f_2627 = obs_max_dem

    # Compute Formula Demand Headroom (2026/27 baseline) = Firm Capacity - Forecasted Max Demand
    formula_dem_hdrm = None
    if firm_dem is not None and f_2627 is not None:
        formula_dem_hdrm = round(firm_dem - f_2627, 2)

    hm_avail_dem = safe_float(hm.get("demandAvailableCapacity"))
    dash_dem_hdrm = safe_float(dash.get("dem_hdrm"))

    # Generation Firm / Nameplate Rating & Headroom
    firm_gen = safe_float(hm.get("generationFirmCapacity")) or safe_float(hm.get("reversePowerFlowTotalCapacity"))
    hm_avail_gen = safe_float(hm.get("generationAvailableCapacity"))
    dash_gen_hdrm = safe_float(dash.get("gen_hdrm"))
    ht_gen_w_arr = ngen.get("scenarios", {}).get("HT", {}).get("W") or []
    ht_gen_w_2027 = ht_gen_w_arr[0] if ht_gen_w_arr else None

    # Connected & Contracted Demands / Generators / Storage from Heatmap JSON
    dem_conn = sum(safe_float(d.get("demandConnectedCapacity"), 0) for d in hm.get("Demands", []))
    dem_contr = sum(safe_float(d.get("demandContractedCapacity"), 0) for d in hm.get("Demands", []))
    if not dem_contr and ndem.get("contracted_mva"):
        dem_contr = ndem["contracted_mva"]

    gen_conn = sum(safe_float(g.get("generationConnectedCapacity"), 0) for g in hm.get("Generators", []))
    gen_contr = sum(safe_float(g.get("generationContractedCapacity"), 0) for g in hm.get("Generators", []))
    if not gen_contr and ngen.get("contracted_mva"):
        gen_contr = ngen["contracted_mva"]

    stor_conn = sum(safe_float(st.get("generationConnectedCapacity"), 0) for st in hm.get("Storage", []))
    stor_contr = sum(safe_float(st.get("generationContractedCapacity"), 0) for st in hm.get("Storage", []))

    # Past Connection Activity (2025/26)
    pca = (hm.get("PastConnectionActivity") or [{}])[0]
    offers_load_made_cnt = int(pca.get("loadConnectionOffersMadeCount") or 0)
    offers_load_made_mva = safe_float(pca.get("loadConnectionOffersMadeCapacity"), 0.0)
    offers_load_acc_cnt = int(pca.get("loadConnectionOffersAcceptedCount") or 0)
    offers_load_acc_mva = safe_float(pca.get("loadConnectionOffersAcceptedCapacity"), 0.0)
    offers_gen_made_cnt = int(pca.get("generationConnectionOffersMadeCount") or 0)
    offers_gen_made_mva = safe_float(pca.get("generationConnectionOffersMadeCapacity"), 0.0)
    offers_gen_acc_cnt = int(pca.get("generationConnectionOffersAcceptedCount") or 0)
    offers_gen_acc_mva = safe_float(pca.get("generationConnectionOffersAcceptedCapacity"), 0.0)

    # Fault Level (Breaker Rating vs Short Circuit Current)
    brk_cap = safe_float(hm.get("breakerBreakingCapacity"))
    brk_scc = safe_float(hm.get("breakerShortCircuitCurrent"))
    fault_margin_ka = round(brk_cap - brk_scc, 2) if (brk_cap is not None and brk_scc is not None) else None
    fault_pct = round((brk_scc / brk_cap) * 100, 1) if (brk_cap and brk_scc is not None and brk_cap > 0) else None

    # EISD
    eisd_info = eisd_by_gsp.get((area, norm_name(gsp_raw or raw_name)), {})

    # Additional Constraints notes
    constraint_notes = [c.get("description") for c in (hm.get("Constraint") or []) if c.get("description")]
    single_tx = bool(ndem.get("single_tx") or ngen.get("single_tx") or any("single transformer" in str(n).lower() for n in constraint_notes))
    upstream_constr = bool(ndem.get("upstream_constraint") or ngen.get("upstream_constraint") or "Upstream" in str(hm.get("demandConstraintLimitingFactor") or ""))

    unified.append({
        "id": f"{area}_{key}",
        "name": raw_name,
        "type": stype,
        "area": area,
        "region_label": "Southern England (SEPD)" if area == "SEPD" else "North Scotland (SHEPD)",
        "local_authority": la or ("Southern England (Unassigned BSP/GSP)" if area == "SEPD" else "North Scotland (Unassigned GSP)"),
        "gsp": gsp_raw or raw_name,
        "bsp": bsp_raw or "",
        "voltage": voltage_str,
        "max_kv": vols_clean[0] if vols_clean else 11,
        "min_kv": vols_clean[-1] if vols_clean else 11,
        "lat": round(hm["latitude"], 5) if hm.get("latitude") is not None else lat,
        "lon": round(hm["longitude"], 5) if hm.get("longitude") is not None else lon,
        "grid_ref": ndem.get("grid_ref") or ngen.get("grid_ref") or "",
        "single_tx": single_tx,
        "upstream_constraint": upstream_constr,
        # 2026 NDP Demand Metrics
        "firm_dem_mva": firm_dem,
        "obs_max_dem_mva": obs_max_dem,
        "forecast_max_dem_2627": f_2627,
        "ltds_demand_forecast": {
            "2024/25": obs_max_dem,
            "2025/26": f_2526,
            "2026/27": f_2627,
            "2027/28": f_2728,
            "2028/29": f_2829,
            "2029/30": f_2930,
        },
        "formula_dem_hdrm_mva": formula_dem_hdrm,
        "hm_avail_dem_mva": hm_avail_dem,
        "dash_dem_hdrm_mva": dash_dem_hdrm,
        "dem_rag": hm.get("demandConstraint") or dash.get("dem_rag") or "Green",
        "dem_limit_factor": hm.get("demandConstraintLimitingFactor") or ("Upstream Constraint" if upstream_constr else "None"),
        # 2026 NDP Generation Metrics
        "firm_gen_mva": firm_gen,
        "hm_avail_gen_mva": hm_avail_gen,
        "dash_gen_hdrm_mva": dash_gen_hdrm,
        "gen_rag": hm.get("generationConstraint") or dash.get("gen_rag") or "Green",
        "gen_limit_factor": hm.get("generationConstraintLimitingFactor") or "None",
        # Fault Level / Switchgear
        "breaker_cap_ka": brk_cap,
        "breaker_scc_ka": brk_scc,
        "fault_margin_ka": fault_margin_ka,
        "fault_util_pct": fault_pct,
        # Connected & Contracted Queue
        "dem_connected_mva": round(dem_conn, 2),
        "dem_contracted_mva": round(dem_contr, 2),
        "gen_connected_mva": round(gen_conn, 2),
        "gen_contracted_mva": round(gen_contr, 2),
        "stor_connected_mva": round(stor_conn, 2),
        "stor_contracted_mva": round(stor_contr, 2),
        "lct_mpans": dash.get("total_mpans") or 0,
        # 2025/26 Connection Activity
        "activity_2526": {
            "load_offers_made_cnt": offers_load_made_cnt,
            "load_offers_made_mva": offers_load_made_mva,
            "load_offers_acc_cnt": offers_load_acc_cnt,
            "load_offers_acc_mva": offers_load_acc_mva,
            "gen_offers_made_cnt": offers_gen_made_cnt,
            "gen_offers_made_mva": offers_gen_made_mva,
            "gen_offers_acc_cnt": offers_gen_acc_cnt,
            "gen_offers_acc_mva": offers_gen_acc_mva,
        },
        # Reinforcement & Transmission EISD
        "reinforcement_work": dash.get("reinf_work") or "",
        "reinforcement_year": dash.get("reinf_yr") or "",
        "demand_eisd": eisd_info.get("demand_eisd"),
        "gen_eisd": eisd_info.get("gen_eisd"),
        "constraint_notes": constraint_notes,
        # NSHR 2026 Multi-Scenario Trajectory (2027-2050)
        "nshr_demand": ndem.get("scenarios", {}),
        "nshr_gen": ngen.get("scenarios", {}),
    })

print(f"Total unified substations from May 2026 Heatmap + NSHR + LTDS: {len(unified)}")

# Fill any missing Local Authorities using nearest substation in same area with known LA
known_la_subs = [u for u in unified if u["lat"] and u["lon"] and "Unassigned" not in u["local_authority"]]
for u in unified:
    if "Unassigned" in u["local_authority"] and u["lat"] and u["lon"]:
        best_d = 999999
        best_la = None
        for k in known_la_subs:
            if k["area"] != u["area"]:
                continue
            d = (k["lat"] - u["lat"]) ** 2 + (k["lon"] - u["lon"]) ** 2
            if d < best_d:
                best_d = d
                best_la = k["local_authority"]
        if best_la:
            u["local_authority"] = best_la

# Check summary statistics
with_nshr = sum(1 for u in unified if u["nshr_demand"] or u["nshr_gen"])
with_firm = sum(1 for u in unified if u["firm_dem_mva"] is not None)
with_la = sum(1 for u in unified if "Unassigned" not in u["local_authority"])
print(f"Stats: with_nshr={with_nshr}, with_firm={with_firm}, with_la={with_la}")

# Save to scratch JSON
out_data = {
    "substations": unified,
    "boundaries": bundle.get("boundaries"),
    "gsp_intelligence": bundle.get("gsp_intelligence"),
    "ndr_2026_highlights": [
        {"area": "SEPD", "gsp": "fleet-bramley", "project": "Fleet-Bramley & Pyestock 132kV/33kV Reinforcement", "driver": "Data Centre & LCT Demand Growth", "existing_mva": 114.0, "released_mva": 60.0, "completion": "2028/29"},
        {"area": "SEPD", "gsp": "iver", "project": "Slough / Iver 132kV & 33kV Data Centre Corridor Upgrade", "driver": "Hyperscale Data Centres & Industrial Electrification", "existing_mva": 240.0, "released_mva": 90.0, "completion": "2028–2031"},
        {"area": "SEPD", "gsp": "mannington", "project": "Bournemouth & Alderney 33kV/11kV Thermal Upgrade", "driver": "EV & Heat Pump Demand Headroom", "existing_mva": 38.0, "released_mva": 16.5, "completion": "2027/28"},
        {"area": "SEPD", "gsp": "lovedean", "project": "Chichester & Hunston BSP 132/33kV Transformer Reinforcement", "driver": "Demand & Solar Generation Headroom", "existing_mva": 90.0, "released_mva": 45.0, "completion": "2028"},
        {"area": "SEPD", "gsp": "cowley", "project": "Oxfordshire (Cowley / Yarnton / Witney) 33kV Capacity Release", "driver": "Science Park Demand & LCT Uptake", "existing_mva": 120.0, "released_mva": 48.0, "completion": "2027–2029"},
        {"area": "SHEPD", "gsp": "clayhills", "project": "Aberdeen City (Clayhills / Craigiebuckler) 33/11kV Reinforcement", "driver": "Port Electrification, District Heat & EV Hubs", "existing_mva": 68.0, "released_mva": 24.0, "completion": "2027/28"},
        {"area": "SHEPD", "gsp": "burghmuir", "project": "Perth & Burghmuir 33kV Primary Transformer Upgrade", "driver": "Commercial Demand & Heat Electrification", "existing_mva": 42.4, "released_mva": 20.0, "completion": "2028"},
        {"area": "SHEPD", "gsp": "alness", "project": "Cromarty Firth / Alness Green Freeport 33kV Reinforcement", "driver": "Industrial Hydrogen / Electrolyser & Port Load", "existing_mva": 30.5, "released_mva": 28.0, "completion": "2027/28"},
        {"area": "SHEPD", "gsp": "beauly", "project": "Inverness & Beauly 33kV Network Reinforcement", "driver": "Highland LCT Demand & Embedded Generation", "existing_mva": 26.6, "released_mva": 40.0, "completion": "2028/29"},
        {"area": "SHEPD", "gsp": "dudhope", "project": "Dundee (Dudhope / Charleston / Milton of Craigie) 33/11kV Upgrade", "driver": "Urban Heat & EV Charging Infrastructure", "existing_mva": 96.0, "released_mva": 32.0, "completion": "2027–2029"}
    ]
}

with open(BASE + "site_finder_bundle_2026.json", "w") as f:
    json.dump(out_data, f, separators=(",", ":"))
with open(ROOT_BUNDLE, "w") as f:
    json.dump(out_data, f, separators=(",", ":"))
print("Wrote site_finder_bundle_2026.json to both data/ and root successfully!")
