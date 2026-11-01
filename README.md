# SSEN Grid Connection Site Finder (2026 Baseline)

An independent, interactive engineering portal to screen 981 distribution substations across Scottish & Southern Electricity Networks (SEPD South & SHEPD North) for project connection feasibility, firm transformer ratings, and transmission curtailment.

---

## Architecture Overview: How It Works

This project is split into two complementary layers:

```
┌────────────────────────────────────────────────────────┐
│  1. PYTHON DATA PIPELINE (Data Extraction & Analysis)  │
│  - Downloads & parses official SSEN Excel / JSON files │
│  - Cleans, disambiguates, and validates 981 assets     │
│  - Computes N-1 cyclic ratings, reverse power limits   │
│  - Outputs: site_finder_bundle_2026.json & index.html  │
└──────────────────────────┬─────────────────────────────┘
                           │ Embeds / Synchronizes
                           ▼
┌────────────────────────────────────────────────────────┐
│  2. CLIENT-SIDE WEB DASHBOARD (Interactive Real-Time)   │
│  - Runs 100% in the user's browser (zero server lag)   │
│  - User moves capacity slider or switches archetypes   │
│  - JavaScript recalculates headroom & ranks candidates │
│  - Instant Leaflet map clustering & filter sync        │
└────────────────────────────────────────────────────────┘
```