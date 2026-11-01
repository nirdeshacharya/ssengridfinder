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

---

## Project Structure

```
ssen_grid_finder/
│
├── index.html                   # Deployable web application (Embedded data + Leaflet + UI)
├── site_finder_bundle_2026.json # Raw processed JSON dataset of 981 substations
│
├── pipeline/
│   ├── build_site_finder_data.py       # Python pipeline: processes raw SSEN files into JSON
│   └── build_comprehensive_v2_portal.py # Python pipeline: builds/updates index.html
│
└── data/
    └── site_finder_bundle_2026.json    # Source dataset backup
```

---

## When & How to Use the Python Pipeline

### When to run Python:
- When SSEN publishes new Long Term Development Statements (LTDS), Network Development Plans (NDP), or updated Heatmap spreadsheets.
- When you want to modify backend engineering formulas or add new substation attributes.

### How to re-run the pipeline:
1. Run the data extraction script:
   ```bash
   python3 pipeline/build_site_finder_data.py
   ```
   *(This parses official spreadsheets and updates `site_finder_bundle_2026.json`)*

2. Rebuild the web dashboard:
   ```bash
   python3 pipeline/build_comprehensive_v2_portal.py
   ```
   *(This embeds the updated dataset and outputs a fresh, standalone `index.html`)*

---

## How the Web Dashboard Works

- **Zero Backend Required for Users:** When hosting on GitHub Pages, Netlify, or Vercel, users do not need Python or a database. The entire screening algorithm runs inside their browser in under 10ms.
- **Data Sync Button:** In the top navigation, the `● Data Synced ↺` pill checks if a new `site_finder_bundle_2026.json` has been uploaded to the web host. If yes, it updates the in-memory data live without requiring a hard browser refresh.

---

## Deployment (100% Free)

- **Netlify Drop:** Drag and drop this folder onto [app.netlify.com/drop](https://app.netlify.com/drop).
- **GitHub Pages:** Push this repository to GitHub and enable GitHub Pages on the `main` branch.
- **Cloudflare Pages / Vercel:** Connect your GitHub repo for instant global CDN deployment.

---

## Automated Quarterly Sync (Every Few Months)

### Method A: Automated in the Cloud (GitHub Actions - Recommended)
A workflow has been configured in `.github/workflows/ssen_quarterly_sync.yml`.
- **Automatic Schedule**: Runs at 04:00 UTC on the 1st of every 3rd month (Jan, Apr, Jul, Oct).
- **Zero Local Maintenance**: Runs on GitHub's cloud servers for free.
- **Auto-Deploy**: When SSEN publishes new quarterly data, GitHub Actions pulls the updates, runs the analysis pipeline, commits the new `index.html`, and deploys it live.
- **Manual Trigger**: You can also trigger an update at any time under the **Actions** tab in your GitHub repository.

### Method B: Automated Locally via Terminal / Cron
You can run the all-in-one sync script on your own computer:
```bash
python3 pipeline/auto_quarterly_sync.py
```
To run it automatically every 3 months on macOS/Linux via crontab:
```bash
# Add to crontab (crontab -e):
0 4 1 */3 * cd /path/to/ssen_grid_finder && python3 pipeline/auto_quarterly_sync.py
```
