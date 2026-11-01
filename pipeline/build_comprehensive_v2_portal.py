import json
import os

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BASE = os.path.join(PROJECT_ROOT, "data") + "/"
OUT_HTML = os.path.join(PROJECT_ROOT, "index.html")

with open(BASE + "site_finder_bundle_2026.json") as f:
    data_bundle = json.load(f)

data_json_str = json.dumps(data_bundle, separators=(",", ":"))

html_content = r"""<!DOCTYPE html>
<html lang="en" style="color-scheme: light !important; background-color: #ffffff !important;">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light only" />
  <title>Project Connection Site Finder | Independent UK Grid Capacity Screening</title>
  
  <!-- Leaflet & Leaflet.markercluster -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

  <!-- IBM Plex Sans & IBM Plex Mono Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <style>
    :root {
      color-scheme: light !important;
      --bg-page: #ffffff;
      --bg-subtle: #f8fafc;
      --bg-muted: #f1f5f9;
      --bg-active: #e2e8f0;
      --border-subtle: #e2e8f0;
      --border-default: #cbd5e1;
      --border-strong: #94a3b8;
      
      /* WCAG AAA compliant text palette (all text contrast > 5.5:1) */
      --text-main: #090d16;
      --text-muted: #334155;
      --text-sub: #475569;
      --text-soft: #64748b;
      
      /* Brand palette */
      --brand-navy: #0c4a6e;
      --brand-blue: #0369a1;
      --brand-bg: #f0f9ff;
      --brand-border: #bae6fd;
      
      /* Semantic Status Tokens (High Contrast) */
      --status-green-text: #065f46;
      --status-green-bg: #f0fdf4;
      --status-green-border: #86efac;
      
      --status-amber-text: #92400e;
      --status-amber-bg: #fffbeb;
      --status-amber-border: #fde68a;
      
      --status-red-text: #991b1b;
      --status-red-bg: #fef2f2;
      --status-red-border: #fecaca;

      --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      --font-mono: 'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    ::selection {
      background: #bae6fd;
      color: #0c4a6e;
    }

    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #f8fafc;
    }
    ::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }

    html, body {
      background-color: #ffffff !important;
      color: var(--text-main) !important;
      font-family: var(--font-sans);
      font-size: 13.5px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
    }

    /* Top Navigation Bar */
    .portal-nav {
      background: #ffffff;
      border-bottom: 1px solid var(--border-subtle);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 1000;
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .nav-logo {
      width: 32px;
      height: 32px;
      background: #0f172a;
      color: #ffffff;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 13px;
      letter-spacing: 0.05em;
      flex-shrink: 0;
    }

    .nav-titles {
      display: flex;
      align-items: baseline;
      gap: 10px;
    }

    .nav-heading {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
    }

    .nav-desc {
      font-size: 12px;
      color: var(--text-sub);
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .sync-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-family: var(--font-sans);
      font-weight: 600;
      color: #065f46;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      padding: 5px 11px;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.15s ease;
      line-height: 1;
    }

    .sync-status-pill:hover {
      background: #dcfce7;
      border-color: #86efac;
    }

    .sync-status-pill:focus-visible {
      outline: 2px solid #059669;
      outline-offset: 1px;
    }

    .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #16a34a; flex-shrink: 0; }

    .sync-refresh-hint {
      font-size: 12px;
      color: #059669;
      margin-left: 2px;
      opacity: 0.7;
      transition: opacity 0.15s ease;
    }

    .sync-status-pill:hover .sync-refresh-hint {
      opacity: 1;
    }



    
    /* Header Action Buttons (Sleek, unified design) */
    .nav-action-btn {
      height: 32px;
      padding: 0 12px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      transition: all 0.15s ease;
      white-space: nowrap;
      border: 1px solid transparent;
      line-height: 1;
    }

    .nav-action-btn:focus-visible {
      outline: 2px solid #0369a1;
      outline-offset: 1px;
    }

    .nav-back-btn {
      background: #f1f5f9;
      color: #0f172a;
      border-color: #cbd5e1;
    }

    .nav-back-btn:hover {
      background: #e2e8f0;
      border-color: #94a3b8;
    }

    .nav-shortlist-btn {
      background: #ffffff;
      color: #0f172a;
      border-color: #cbd5e1;
    }

    .nav-shortlist-btn:hover {
      background: #f8fafc;
      border-color: #94a3b8;
    }

    .nav-shortlist-btn .star-icon {
      color: #d97706;
      font-size: 14px;
    }

    .shortlist-count-badge {
      font-size: 11px;
      font-weight: 700;
      font-family: var(--font-mono);
      background: #f1f5f9;
      color: #475569;
      padding: 1px 6px;
      border-radius: 9999px;
      min-width: 18px;
      text-align: center;
    }

    .shortlist-count-badge.has-items {
      background: #0369a1;
      color: #ffffff;
    }

    .nav-text-btn {
      background: transparent;
      color: #475569;
    }

    .nav-text-btn:hover {
      background: #f1f5f9;
      color: #0f172a;
    }

    .btn-nav {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 5px 11px;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.12s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .btn-nav:hover {
      background: var(--bg-muted);
      color: var(--text-main);
      border-color: var(--border-default);
    }

    .btn-nav:focus-visible {
      outline: 2px solid var(--brand-blue);
      outline-offset: 1px;
    }

    .btn-nav-primary {
      background: var(--brand-navy) !important;
      color: #ffffff !important;
      border-color: var(--brand-navy) !important;
    }

    .btn-nav-primary:hover {
      background: var(--brand-blue) !important;
      border-color: var(--brand-blue) !important;
    }

    /* Main Container */
    .portal-main {
      max-width: 1760px;
      margin: 0 auto;
      padding: 14px 24px 36px 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    /* 1. Cohesive Search & Preset Ribbon */
    .control-ribbon {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }

    .ribbon-section {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      flex: 1;
    }

    .ribbon-field {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .ribbon-label {
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-sub);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .seg-group {
      display: inline-flex;
      background: var(--bg-subtle);
      border: 1px solid var(--border-default);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }

    .seg-btn {
      padding: 4px 10px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .seg-btn:hover {
      color: var(--text-main);
    }

    .seg-btn.active {
      background: var(--brand-navy);
      color: #ffffff;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
    }

    .capacity-flex-box {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .capacity-box {
      width: 72px;
      padding: 4px 8px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--brand-navy);
      border: 1px solid var(--border-default);
      border-radius: 6px;
      background: #ffffff;
      text-align: right;
    }

    .capacity-slider {
      width: 105px;
      accent-color: var(--brand-navy);
      height: 4px;
      cursor: pointer;
    }

    .preset-pill {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-sub);
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 3px 8px;
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .preset-pill:hover {
      background: var(--brand-bg);
      color: var(--brand-navy);
      border-color: var(--brand-border);
    }

    .preset-pill.active {
      background: var(--brand-navy);
      color: #ffffff;
      border-color: var(--brand-navy);
    }

    .ribbon-sep {
      width: 1px;
      height: 32px;
      background: var(--border-subtle);
      margin: 0 2px;
    }

    .ui-select-sm, .ui-input-sm {
      padding: 5px 8px;
      font-size: 12px;
      color: var(--text-main);
      background: #ffffff;
      border: 1px solid var(--border-default);
      border-radius: 6px;
      outline: none;
    }

    .ui-select-sm:focus, .ui-input-sm:focus {
      border-color: var(--brand-blue);
      box-shadow: 0 0 0 2px var(--brand-bg);
    }

    /* 2. Status Filter Bar & Action Strip */
    .filter-actions-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      padding: 0 2px;
    }

    .status-chips-group {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .chip-filter-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-default);
      background: #ffffff;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .chip-filter-btn:hover {
      background: var(--bg-muted);
      color: var(--text-main);
    }

    .chip-filter-btn.active {
      background: var(--brand-navy);
      color: #ffffff;
      border-color: var(--brand-navy);
    }

    .chip-filter-btn.active .chip-badge {
      background: rgba(255, 255, 255, 0.22);
      color: #ffffff;
    }

    .chip-badge {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 8px;
      background: var(--bg-muted);
      color: var(--text-main);
    }

    .action-tools-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-tool {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      background: #ffffff;
      border: 1px solid var(--border-default);
      border-radius: 5px;
      padding: 4px 9px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.12s ease;
    }

    .btn-tool:hover {
      background: var(--bg-muted);
      color: var(--text-main);
    }

    .btn-tool.has-items {
      background: var(--brand-bg);
      color: var(--brand-navy);
      border-color: var(--brand-border);
      font-weight: 700;
    }

    /* 3. Heroic Two-Column Workspace (Map on Left, Detail + Table on Right) */
    .workspace-grid {
      display: grid;
      grid-template-columns: 40% calc(60% - 18px);
      gap: 18px;
      align-items: start;
    }

    @media (max-width: 1140px) {
      .workspace-grid {
        grid-template-columns: 1fr;
      }
    }

    /* Left Map Canvas */
    .map-container-hero {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
      position: sticky;
      top: 16px;
      height: calc(100vh - 80px);
      min-height: 680px;
    }
    #realMapNode {
      flex: 1;
      width: 100%;
      height: 100%;
    }

    .map-top-bar {
      padding: 8px 14px;
      background: #ffffff;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .map-licence-pills {
      display: flex;
      gap: 3px;
    }

    .licence-btn {
      padding: 3px 8px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid var(--border-subtle);
      background: #ffffff;
      color: var(--text-muted);
      border-radius: 4px;
      cursor: pointer;
    }

    .licence-btn.active {
      background: var(--bg-active);
      color: var(--text-main);
      border-color: var(--border-default);
    }

    #realMapNode {
      width: 100%;
      height: 100%;
      min-height: 580px;
      background: #f8fafc;
      flex: 1;
    }

    /* Map Docked Legend */
    .map-legend-bar {
      padding: 7px 14px;
      background: var(--bg-subtle);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-sub);
      flex-wrap: wrap;
      gap: 8px;
    }

    .legend-symbol-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* MarkerCluster & Custom Status Marker Styling */
    .custom-status-marker {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      cursor: pointer;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .custom-status-marker svg {
      display: block;
      overflow: visible;
      transition: transform 0.12s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .custom-status-marker:hover svg {
      transform: scale(1.3);
    }
    .custom-status-marker.is-selected svg {
      transform: scale(1.15);
    }

    /* MarkerCluster Customization: High-Contrast Solid Fill with White Border Outline */
    .marker-cluster {
      background: transparent !important;
    }
    .marker-cluster div {
      background: #0f172a !important;
      color: #ffffff !important;
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 12px;
      border: 2.5px solid #ffffff !important;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
      border-radius: 50% !important;
      width: 34px !important;
      height: 34px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      margin-left: 3px !important;
      margin-top: 3px !important;
    }
    .marker-cluster-small div {
      background: #0369a1 !important;
    }
    .marker-cluster-medium div {
      background: #0284c7 !important;
    }
    .marker-cluster-large div {
      background: #0f172a !important;
    }

    /* Leaflet Zoom Control High-Contrast Fix (Ensures '+' never looks disabled) */
    .leaflet-control-zoom a {
      color: #090d16 !important;
      font-weight: 700 !important;
      font-size: 17px !important;
      line-height: 28px !important;
      background: #ffffff !important;
      border: none !important;
    }
    .leaflet-control-zoom a:hover {
      background: #f1f5f9 !important;
      color: #0284c7 !important;
    }
    .leaflet-bar {
      border: 1px solid var(--border-default) !important;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12) !important;
      border-radius: 6px !important;
      overflow: hidden !important;
    }

    /* Right Analytical Column */
    .panel-stack {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* Substation Detail Inspector (Collapsible, Typographic, No Nested Boxes) */
    .inspector-card {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
      position: relative;
      transition: all 0.2s ease;
    }

    .inspector-top-row {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
    }

    .sub-title-group {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .sub-name-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 17px;
      font-weight: 700;
      color: var(--text-main);
      flex-wrap: wrap;
    }

    .sub-meta-tags {
      display: flex;
      gap: 10px;
      font-size: 12px;
      color: var(--text-sub);
      flex-wrap: wrap;
    }

    .verdict-box {
      text-align: right;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }

    .verdict-mva {
      font-family: var(--font-mono);
      font-size: 21px;
      font-weight: 700;
      line-height: 1.1;
    }

    .verdict-subtext {
      font-size: 12px;
      color: var(--text-sub);
    }

    /* Verdict Callout Banner (Plain-English summary) */
    .verdict-callout {
      background: var(--bg-subtle);
      border: 1px solid var(--border-default);
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
      font-size: 12px;
      color: var(--text-main);
      line-height: 1.45;
    }

    .verdict-callout.viable {
      background: #f0fdf4;
      border-left-color: #059669;
    }

    .verdict-callout.conditional {
      background: #fffbeb;
      border-left-color: #d97706;
    }

    .verdict-callout.constrained {
      background: #fef2f2;
      border-left-color: #dc2626;
    }

    .verdict-callout.incomplete {
      background: #f8fafc;
      border-left-color: #64748b;
    }

    /* Typographic Stats Row */
    .stats-clean-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      padding: 2px 0;
    }

    @media (max-width: 720px) {
      .stats-clean-row {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    .stat-metric {
      display: flex;
      flex-direction: column;
      gap: 1px;
    }

    .stat-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-sub);
      display: flex;
      align-items: center;
    }

    .stat-number {
      font-family: var(--font-mono);
      font-size: 16.5px;
      font-weight: 700;
      color: var(--brand-navy);
    }

    .stat-desc {
      font-size: 12px;
      color: var(--text-soft);
      line-height: 1.3;
    }

    .not-published-val {
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-soft);
      font-family: var(--font-sans);
    }

    /* Progressive Tooltip (?) */
    .tooltip-help {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: var(--bg-muted);
      color: var(--text-sub);
      font-size: 12px;
      font-family: var(--font-mono);
      font-weight: 700;
      border: 1px solid var(--border-default);
      cursor: help;
      position: relative;
      margin-left: 4px;
      transition: all 0.12s ease;
      flex-shrink: 0;
    }

    .tooltip-help:hover, .tooltip-help:focus-visible {
      background: var(--brand-navy);
      color: #ffffff;
      border-color: var(--brand-navy);
    }

    .tooltip-popover {
      position: absolute;
      bottom: calc(100% + 6px);
      left: 50%;
      transform: translateX(-50%) translateY(4px);
      background: #0f172a;
      color: #ffffff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-family: var(--font-sans);
      font-weight: 400;
      line-height: 1.45;
      white-space: normal;
      width: 280px;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.25);
      pointer-events: none;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.12s ease, transform 0.12s ease;
      z-index: 9999;
    }

    .tooltip-popover::after {
      content: "";
      position: absolute;
      top: 100%;
      left: 50%;
      margin-left: -5px;
      border-width: 5px;
      border-style: solid;
      border-color: #0f172a transparent transparent transparent;
    }

    .tooltip-help:hover .tooltip-popover,
    .tooltip-help:focus-visible .tooltip-popover {
      opacity: 1;
      visibility: visible;
      transform: translateX(-50%) translateY(0);
    }

    .inspector-footer-bar {
      border-top: 1px solid var(--border-subtle);
      padding-top: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 12px;
      color: var(--text-sub);
      flex-wrap: wrap;
    }

    .score-group {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .inspector-actions-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Collapsible State */
    .inspector-card.collapsed .stats-clean-row,
    .inspector-card.collapsed .verdict-callout,
    .inspector-card.collapsed .inspector-footer-bar {
      display: none !important;
    }
    .inspector-card:not(.collapsed) .compact-summary-row {
      display: none !important;
    }
    .inspector-card.collapsed .compact-summary-row {
      display: flex !important;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-top: 8px;
      border-top: 1px solid var(--border-subtle);
      font-size: 12px;
      flex-wrap: wrap;
    }
    .compact-stats {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      color: var(--text-sub);
    }
    .compact-stats strong {
      font-family: var(--font-mono);
      color: var(--text-main);
    }
    .compact-stats .sep {
      color: var(--border-strong);
    }
    .compact-verdict-text {
      color: var(--brand-navy);
      font-weight: 500;
    }
    .compact-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Candidate Table Row Shortlist Button (>=32px Tap Target with Star Icon) */
    .btn-row-shortlist {
      min-height: 32px;
      min-width: 32px;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 4px;
      border: 1px solid var(--border-default);
      background: #ffffff;
      color: var(--text-main);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.12s ease;
    }
    .btn-row-shortlist:hover {
      background: var(--bg-subtle);
      border-color: #0369a1;
      color: #0369a1;
    }
    .btn-row-shortlist .star-icon {
      font-size: 13px;
      color: #94a3b8;
      transition: color 0.12s ease;
    }
    .btn-row-shortlist:hover .star-icon {
      color: #d97706;
    }
    .btn-row-shortlist.is-shortlisted {
      background: #fef3c7;
      border-color: #f59e0b;
      color: #92400e;
    }
    .btn-row-shortlist.is-shortlisted .star-icon {
      color: #d97706;
    }

    /* Unified Capacity & Presets Group CSS */
    .capacity-unified-row {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .capacity-slider-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .capacity-num-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }
    .capacity-unit-tag {
      position: absolute;
      right: 6px;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-soft);
      pointer-events: none;
    }
    .presets-combined-group {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 3px 8px;
    }
    .preset-subgroup {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .preset-subgroup-label {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--text-soft);
    }
    .preset-subgroup-chips {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .preset-divider-vertical {
      width: 1px;
      height: 18px;
      background: var(--border-default);
    }

    /* Ranked Table Surface */
    .table-card {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
      display: flex;
      flex-direction: column;
    }

    .table-header-strip {
      padding: 9px 14px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background: #ffffff;
    }

    .table-count-title {
      font-size: 13.5px;
      font-weight: 700;
      color: var(--text-main);
    }

    .table-scroll-wrap {
      overflow-x: auto;
      max-height: 480px;
    }

    .ranked-data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      text-align: left;
    }

    .ranked-data-table th {
      background: var(--bg-subtle);
      padding: 8px 10px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-sub);
      border-bottom: 1px solid var(--border-default);
      position: sticky;
      top: 0;
      z-index: 5;
      white-space: nowrap;
      cursor: pointer;
      user-select: none;
    }

    .ranked-data-table th:hover {
      color: var(--brand-navy);
      background: var(--bg-muted);
    }

    .ranked-data-table th.sorted-active {
      color: var(--brand-blue);
    }

    .ranked-data-table td {
      padding: 9px 10px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-main);
      vertical-align: middle;
      white-space: nowrap;
    }

    .ranked-data-table tbody tr {
      cursor: pointer;
      transition: background 0.1s ease;
    }

    .ranked-data-table tbody tr:hover {
      background: var(--bg-subtle);
    }

    .ranked-data-table tbody tr.selected {
      background: #eff6ff !important;
      outline: 2px solid #3b82f6;
      font-weight: 600;
    }

    .num-cell {
      font-family: var(--font-mono);
      font-size: 12px;
      text-align: right;
    }

    /* Action Buttons in Table */
    .btn-table-bookmark {
      background: transparent;
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 2px 6px;
      cursor: pointer;
      font-size: 12px;
      color: var(--text-sub);
      transition: all 0.12s ease;
    }

    .btn-table-bookmark:hover {
      background: var(--brand-bg);
      color: var(--brand-navy);
      border-color: var(--brand-border);
    }

    .btn-table-bookmark.bookmarked {
      background: #fef3c7;
      color: #92400e;
      border-color: #fde68a;
      font-weight: 700;
    }

    /* Badges */
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.02em;
    }

    .status-viable {
      background: var(--status-green-bg);
      color: var(--status-green-text);
      border: 1px solid var(--status-green-border);
    }

    .status-conditional {
      background: var(--status-amber-bg);
      color: var(--status-amber-text);
      border: 1px solid var(--status-amber-border);
    }

    .status-constrained {
      background: var(--status-red-bg);
      color: var(--status-red-text);
      border: 1px solid var(--status-red-border);
    }

    .status-incomplete {
      background: var(--bg-muted);
      color: var(--text-sub);
      border: 1px solid var(--border-subtle);
    }

    .badge-subtle {
      display: inline-flex;
      align-items: center;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      background: var(--bg-muted);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }

    .badge-low-conf {
      background: #f1f5f9;
      color: #475569;
      border: 1px solid #cbd5e1;
      font-weight: 600;
      font-size: 12px;
      padding: 1px 5px;
      border-radius: 3px;
    }

    /* Modals & Dialogs */
    .app-dialog {
      border: 1px solid var(--border-default);
      border-radius: 10px;
      background: #ffffff;
      color: var(--text-main);
      max-width: 940px;
      width: 94vw;
      max-height: 90vh;
      padding: 0;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      margin: auto;
    }

    .app-dialog::backdrop {
      background: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(2px);
    }

    .dialog-header {
      padding: 14px 20px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-subtle);
    }

    .dialog-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
    }

    .dialog-body {
      padding: 20px;
      overflow-y: auto;
      max-height: calc(90vh - 100px);
      display: flex;
      flex-direction: column;
      gap: 16px;
      font-size: 12.5px;
      line-height: 1.55;
    }

    /* Compare Grid */
    .compare-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
    }

    .compare-column {
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .compare-cell-title {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-sub);
      text-transform: uppercase;
      margin-top: 4px;
    }

    .compare-cell-val {
      font-size: 13px;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--text-main);
    }

    .portal-footer {
      border-top: 1px solid var(--border-subtle);
      padding: 14px 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-sub);
      flex-wrap: wrap;
      gap: 10px;
    }
  
    /* ---------------------------------------------------------------------- */
    /* FRONT PAGE / GUIDED INTAKE WIZARD STYLES (Impeccable & Accessible)    */
    /* ---------------------------------------------------------------------- */
    /* ---------------------------------------------------------------------- */
    /* ---------------------------------------------------------------------- */
    /* SIMPLIFIED, UNCLUTTERED HOMEPAGE INTAKE (Impeccable & Fast)             */
    /* ---------------------------------------------------------------------- */
    .intake-hero-container {
      max-width: 860px;
      margin: 40px auto 60px auto;
      padding: 0 20px;
    }

    .intake-hero-header {
      text-align: center;
      margin-bottom: 28px;
    }

    .intake-headline {
      font-size: 32px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.03em;
      line-height: 1.25;
      margin: 0 0 10px 0;
    }

    .intake-subheadline {
      font-size: 15px;
      color: var(--text-sub);
      line-height: 1.5;
      max-width: 620px;
      margin: 0 auto;
    }

    /* Single cohesive intake card */
    .intake-card-unified {
      background: #ffffff;
      border: 1px solid var(--border-default);
      border-radius: 12px;
      padding: 24px 28px;
      box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .intake-field-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .intake-field-label {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
      margin: 0 0 4px 0;
      line-height: 1.3;
    }

    /* Tactile compact archetype pills (3x2 or flex) */
    .intake-archetypes-compact {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 8px;
    }

    .archetype-pill {
      background: #ffffff;
      border: 1px solid var(--border-default);
      border-radius: 8px;
      padding: 10px 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: all 0.15s ease;
      text-align: left;
    }

    .archetype-pill:hover {
      border-color: #94a3b8;
      background: #f8fafc;
    }

    .archetype-pill.is-selected {
      border: 1.5px solid #0369a1 !important;
      background: #eff6ff !important;
      box-shadow: 0 0 0 1px #0369a1 !important;
    }

    .archetype-pill.is-selected .archetype-pill-icon {
      background: #0369a1 !important;
      color: #ffffff !important;
    }

    .archetype-pill.is-selected .archetype-pill-name {
      color: #0c4a6e !important;
      font-weight: 700 !important;
    }

    .archetype-pill.is-selected .archetype-pill-cap {
      color: #0369a1 !important;
      font-weight: 600 !important;
    }

    .archetype-pill-icon {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: #f1f5f9;
      color: #0f172a;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .archetype-pill.is-selected .archetype-pill-icon {
      background: #e0f2fe;
      color: #0369a1;
    }

    .archetype-pill-info {
      flex: 1;
      min-width: 0;
    }

    .archetype-pill-name {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-main);
      display: block;
      line-height: 1.25;
    }

    .archetype-pill-cap {
      font-size: 12px;
      color: var(--text-sub);
    }

    .archetype-pill.is-selected .archetype-pill-cap {
      color: #0369a1;
      font-weight: 600;
    }

    /* Two-column parameter row */
    .intake-row-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      padding-top: 6px;
      border-top: 1px solid var(--border-subtle);
    }

    @media (max-width: 680px) {
      .intake-row-grid {
        grid-template-columns: 1fr;
      }
    }

    /* Capacity field */
    .intake-capacity-unified {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .capacity-field-wrap {
      display: inline-flex;
      align-items: center;
      min-height: 38px;
      background: #ffffff;
      border: 1px solid var(--border-default);
      border-radius: 6px;
      padding: 6px 12px;
      gap: 8px;
      box-sizing: border-box;
    }

    .capacity-field-wrap:focus-within {
      border-color: #0369a1;
      outline: 2px solid #0369a1;
      outline-offset: 1px;
    }

    .cap-unit-prefix {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-sub);
    }

    .intake-number-input {
      width: 52px;
      height: 100%;
      border: none;
      outline: none;
      font-family: var(--font-mono);
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      background: transparent;
      text-align: right;
      padding: 0;
    }

    .cap-unit-suffix {
      font-size: 13px;
      font-weight: 700;
      color: var(--brand-navy);
    }

    .intake-slider {
      flex: 1;
      height: 6px;
      accent-color: #0369a1;
      cursor: pointer;
    }

    .intake-quick-pills {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 6px;
      flex-wrap: wrap;
    }

    .intake-pills-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-sub);
      margin-right: 2px;
    }

    /* Target Territory segmented control */
    .intake-region-segmented {
      display: flex;
      background: #f1f5f9;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 4px;
      gap: 4px;
    }

    .region-seg-btn {
      flex: 1;
      height: 32px;
      font-size: 12px;
      font-weight: 600;
      color: #475569;
      background: transparent;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .region-seg-btn:hover {
      color: #0f172a;
    }

    .region-seg-btn.active {
      background: #ffffff;
      color: #0f172a;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
    }

    .intake-sublocation-row {
      display: flex;
      gap: 8px;
      margin-top: 6px;
    }

    .intake-select-sm, .intake-input-sm {
      height: 34px;
      padding: 0 10px;
      border: 1px solid var(--border-default);
      border-radius: 6px;
      font-size: 13px;
      color: var(--text-main);
      background: #ffffff;
      outline: none;
    }

    .intake-select-sm {
      flex: 1;
    }

    .intake-input-sm {
      flex: 1;
    }

    .intake-select-sm:focus, .intake-input-sm:focus {
      border-color: #0369a1;
      outline: 2px solid #0369a1;
      outline-offset: 1px;
    }

    /* Action bar */
    .intake-action-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-top: 10px;
      border-top: 1px solid var(--border-subtle);
      flex-wrap: wrap;
    }

    .intake-action-left {
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }

    .btn-intake-launch {
      height: 42px;
      padding: 0 24px;
      background: #0f172a;
      color: #ffffff;
      border: 1px solid #0f172a;
      border-radius: 8px;
      font-size: 14.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.12);
      transition: background-color 0.15s ease;
    }

    .btn-intake-launch:hover {
      background: #0369a1;
      border-color: #0369a1;
    }

    .intake-counter-preview {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-sub);
    }

    .btn-intake-skip {
      background: transparent;
      border: none;
      color: #475569;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      padding: 8px 12px;
      border-radius: 6px;
    }

    .btn-intake-skip:hover {
      background: #f1f5f9;
      color: #0f172a;
    }

    

  
    /* Toast Notification (Hidden by default, fixed at bottom-left) */
    .toast-msg {
      position: fixed;
      bottom: 24px;
      left: 24px;
      background: #0f172a;
      color: #ffffff;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
      z-index: 99999;
      opacity: 0;
      transform: translateY(12px);
      pointer-events: none;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }

    .toast-msg.show {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }

  
    /* Dashboard Capacity Ribbon Control (Inline, perfectly aligned 32px height) */
    .capacity-clean-row {
      display: inline-flex !important;
      align-items: center !important;
      gap: 10px !important;
      height: 32px !important;
    }

    .capacity-input-pill {
      display: inline-flex !important;
      align-items: center !important;
      height: 32px !important;
      background: #ffffff !important;
      border: 1px solid var(--border-default) !important;
      border-radius: 6px !important;
      padding: 0 8px !important;
      gap: 4px !important;
      box-sizing: border-box !important;
      transition: border-color 0.15s ease, outline 0.15s ease;
    }

    .capacity-input-pill:focus-within {
      border-color: #0369a1 !important;
      outline: 2px solid #0369a1 !important;
      outline-offset: 1px !important;
    }

    .capacity-number-input {
      width: 48px !important;
      height: 100% !important;
      border: none !important;
      outline: none !important;
      background: transparent !important;
      font-family: var(--font-mono) !important;
      font-size: 13.5px !important;
      font-weight: 700 !important;
      color: var(--brand-navy) !important;
      text-align: right !important;
      padding: 0 2px 0 0 !important;
      margin: 0 !important;
      -webkit-appearance: none !important;
      -moz-appearance: textfield !important;
      appearance: none !important;
    }

    .capacity-number-input::-webkit-inner-spin-button,
    .capacity-number-input::-webkit-outer-spin-button {
      -webkit-appearance: none !important;
      margin: 0 !important;
    }

    .capacity-unit-pill-tag {
      font-size: 12px !important;
      font-weight: 700 !important;
      color: var(--text-sub) !important;
      user-select: none !important;
      line-height: 1 !important;
    }

    .capacity-range-slider {
      width: 125px !important;
      height: 6px !important;
      accent-color: #0369a1 !important;
      cursor: pointer !important;
      margin: 0 !important;
    }

  </style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header class="portal-nav">
    <div class="nav-brand">
      <div class="nav-logo">GF</div>
      <div class="nav-titles">
        <h1 class="nav-heading">Project Connection Site Finder</h1>
        <span class="nav-desc">Independent UK Grid Capacity &amp; Headroom Screening Tool</span>
      </div>
    </div>
    <div class="nav-actions">
      <button class="nav-action-btn nav-back-btn" id="btnBackToIntake" type="button" onclick="showIntakeView()" style="display:none;" title="Change archetype, capacity, or location">
        &larr; New Search / Archetypes
      </button>
      <button class="sync-status-pill" id="syncBtn" type="button" onclick="syncLatestData(true)" title="SSEN May 2026 baseline verified. Click to check for updates.">
        <span class="status-dot"></span>
        <span id="syncStatusLabel">Data Synced</span>
        <span class="sync-refresh-hint" aria-hidden="true">&#8635;</span>
      </button>
      <button class="nav-action-btn nav-shortlist-btn" id="btnShortlistNav" type="button" onclick="openCompareModal()" title="View and compare shortlisted substations">
        <span class="star-icon">&#9733;</span>
        <span>Shortlist</span>
        <span class="shortlist-count-badge" id="navShortlistCount">0</span>
      </button>
      <button class="nav-action-btn nav-text-btn" id="openTermsBtn" type="button" onclick="openTermsModal('terms')" title="View technical methodology, formulas, and data sources">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        <span>Formulas &amp; Sources</span>
      </button>
    </div>
  </header>

  <main class="portal-main">

    <!-- FRONT PAGE: Clean, Simplified Project Intake -->
    <section class="intake-hero-container" id="intakeView" aria-label="Project Screening Setup">
      <div class="intake-hero-header">
        <h1 class="intake-headline">Find UK Grid Connection Capacity</h1>
        <p class="intake-subheadline">
          Screen 981 distribution substations across Southern England (SEPD) and Northern Scotland (SHEPD) for available headroom, firm transformer ratings, and transmission curtailment.
        </p>
      </div>

      <div class="intake-card-unified">
        <!-- 1. Archetype Selector -->
        <div class="intake-field-group">
          <h2 class="intake-field-label">1. Select Project Type</h2>
          <div class="intake-archetypes-compact">
            <button type="button" class="archetype-pill is-selected" data-intake-preset="ev_hub" onclick="selectIntakePreset('ev_hub')">
              <div class="archetype-pill-icon" aria-hidden="true">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
              </div>
              <div class="archetype-pill-info">
                <span class="archetype-pill-name">EV Fleet &amp; Depot Hub</span>
                <span class="archetype-pill-cap">Demand &bull; 5.0 MVA</span>
              </div>
            </button>

            <button type="button" class="archetype-pill" data-intake-preset="solar_gen" onclick="selectIntakePreset('solar_gen')">
              <div class="archetype-pill-icon" aria-hidden="true">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
              </div>
              <div class="archetype-pill-info">
                <span class="archetype-pill-name">Solar PV Renewable Farm</span>
                <span class="archetype-pill-cap">Generation &bull; 15.0 MVA</span>
              </div>
            </button>

            <button type="button" class="archetype-pill" data-intake-preset="bess_flex" onclick="selectIntakePreset('bess_flex')">
              <div class="archetype-pill-icon" aria-hidden="true">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="10" x="2" y="7" rx="2" ry="2"/><line x1="22" x2="22" y1="11" y2="13"/><line x1="6" x2="6" y1="11" y2="13"/><line x1="10" x2="10" y1="11" y2="13"/><line x1="14" x2="14" y1="11" y2="13"/></svg>
              </div>
              <div class="archetype-pill-info">
                <span class="archetype-pill-name">Battery Energy Storage (BESS)</span>
                <span class="archetype-pill-cap">Storage &bull; 30.0 MVA</span>
              </div>
            </button>

            <button type="button" class="archetype-pill" data-intake-preset="datacentre" onclick="selectIntakePreset('datacentre')">
              <div class="archetype-pill-icon" aria-hidden="true">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/></svg>
              </div>
              <div class="archetype-pill-info">
                <span class="archetype-pill-name">Data Centre &amp; High-Density</span>
                <span class="archetype-pill-cap">Demand &bull; 25.0 MVA</span>
              </div>
            </button>

            <button type="button" class="archetype-pill" data-intake-preset="industrial" onclick="selectIntakePreset('industrial')">
              <div class="archetype-pill-icon" aria-hidden="true">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/></svg>
              </div>
              <div class="archetype-pill-info">
                <span class="archetype-pill-name">Commercial &amp; Industrial</span>
                <span class="archetype-pill-cap">Demand &bull; 2.5 MVA</span>
              </div>
            </button>

            <button type="button" class="archetype-pill" data-intake-preset="custom" onclick="selectIntakePreset('custom')">
              <div class="archetype-pill-icon" aria-hidden="true">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="21" y2="21"/><line x1="4" x2="20" y1="3" y2="3"/><line x1="12" x2="12" y1="7" y2="17"/><polyline points="8 11 12 7 16 11"/></svg>
              </div>
              <div class="archetype-pill-info">
                <span class="archetype-pill-name">Custom Specification</span>
                <span class="archetype-pill-cap">Custom parameters</span>
              </div>
            </button>
          </div>
        </div>

        <!-- 2. Parameters Two-Column Row -->
        <div class="intake-row-grid">
          <!-- Capacity Column -->
          <div class="intake-field-group">
            <h2 class="intake-field-label">2. Required Capacity</h2>
            <div class="intake-capacity-unified">
              <div class="capacity-field-wrap">
                <span class="cap-unit-prefix">Power:</span>
                <input type="number" id="intakeCapInput" class="intake-number-input" min="0.5" max="100.0" step="0.5" value="5.0" oninput="onIntakeCapInputChange(this.value)" aria-label="Requested capacity in MVA" />
                <span class="cap-unit-suffix">MVA</span>
              </div>
              <input type="range" id="intakeCapSlider" class="intake-slider" min="0" max="100" step="1" value="43" oninput="onIntakeSliderChange(this.value)" aria-label="Capacity slider" />
            </div>

            <!-- Quick Pills -->
            <div class="intake-quick-pills">
              <span class="intake-pills-label">Sizes:</span>
              <button type="button" class="preset-pill cap-pill" onclick="setIntakeCapacity(1.0)">1M</button>
              <button type="button" class="preset-pill cap-pill" onclick="setIntakeCapacity(2.5)">2.5M</button>
              <button type="button" class="preset-pill cap-pill active" id="intakeChip5" onclick="setIntakeCapacity(5.0)">5M</button>
              <button type="button" class="preset-pill cap-pill" id="intakeChip10" onclick="setIntakeCapacity(10.0)">10M</button>
              <button type="button" class="preset-pill cap-pill" id="intakeChip15" onclick="setIntakeCapacity(15.0)">15M</button>
              <button type="button" class="preset-pill cap-pill" id="intakeChip25" onclick="setIntakeCapacity(25.0)">25M</button>
              <button type="button" class="preset-pill cap-pill" id="intakeChip30" onclick="setIntakeCapacity(30.0)">30M</button>
              <button type="button" class="preset-pill cap-pill" id="intakeChip50" onclick="setIntakeCapacity(50.0)">50M</button>
            </div>
          </div>

          <!-- Region Column -->
          <div class="intake-field-group">
            <h2 class="intake-field-label">3. Target Territory &amp; Area</h2>
            <div class="intake-region-segmented">
              <button type="button" class="region-seg-btn active" id="intakeRegionAll" onclick="setIntakeRegion('ALL')">All UK (981)</button>
              <button type="button" class="region-seg-btn" id="intakeRegionSEPD" onclick="setIntakeRegion('SEPD')">SEPD South (478)</button>
              <button type="button" class="region-seg-btn" id="intakeRegionSHEPD" onclick="setIntakeRegion('SHEPD')">SHEPD North (503)</button>
            </div>
            <div class="intake-sublocation-row">
              <select id="intakeGeoAreaSelect" class="intake-select-sm" onchange="onIntakeGeoAreaChange()" aria-label="Select Local Authority">
                <option value="ALL">All Local Authorities</option>
              </select>
              <input type="text" id="intakeSearchInput" class="intake-input-sm" placeholder="Search town..." oninput="updateIntakeCandidateCount()" aria-label="Search town name" />
            </div>
          </div>
        </div>

        <!-- 3. Action Strip -->
        <div class="intake-action-row">
          <div class="intake-action-left">
            <button type="button" class="btn-intake-launch" onclick="launchDashboardFromIntake()">
              Find Available Grid Sites &rarr;
            </button>
            <span class="intake-counter-preview" id="intakeCandidateCount">Screening 981 SSEN distribution assets</span>
          </div>
          <button type="button" class="btn-intake-skip" onclick="launchDashboardFromIntake(true)">
            Browse full map &amp; table &rarr;
          </button>
        </div>
      </div>

      
    </section>

    <div id="dashboardView" style="display:none;">

    <!-- 1. Cohesive Search & Preset Ribbon (All connection parameters unified) -->
    <section class="control-ribbon" aria-label="Project Connection Query">
      <div class="ribbon-section">
        <!-- Type -->
        <div class="ribbon-field">
          <span class="ribbon-label">Type</span>
          <div class="seg-group" role="group" aria-label="Connection Type">
            <button type="button" class="seg-btn active" id="btnTypeDemand" onclick="setProjectType('demand')">Demand</button>
            <button type="button" class="seg-btn" id="btnTypeGen" onclick="setProjectType('generation')">Generation</button>
            <button type="button" class="seg-btn" id="btnTypeBess" onclick="setProjectType('storage')">Storage</button>
          </div>
        </div>

        <div class="ribbon-sep"></div>

        <!-- Required Connection Capacity -->
        <div class="ribbon-field capacity-ribbon-field">
          <span class="ribbon-label">Required Capacity</span>
          <div class="capacity-clean-row">
            <div class="capacity-input-pill">
              <input type="number" id="reqCapInput" class="capacity-number-input" min="0.5" max="100" step="0.5" value="5.0" oninput="onNumberCapChange(this.value)" aria-label="Required Capacity MVA" />
              <span class="capacity-unit-pill-tag">MVA</span>
            </div>
            <input type="range" id="reqCapSlider" class="capacity-range-slider" min="0" max="100" step="1" value="43" oninput="onSliderCapChange(this.value)" aria-label="Capacity slider" />
          </div>
        </div>

        <div class="ribbon-sep"></div>

        <!-- Location (Linked with Licence Area) -->
        <div class="ribbon-field" style="flex:1;min-width:200px;">
          <span class="ribbon-label">Location</span>
          <div style="display:flex;gap:6px;">
            <select id="geoAreaSelect" class="ui-select-sm" onchange="onGeoAreaSelectChange()" style="flex:1;" aria-label="Local Authority Filter">
              <option value="ALL">All Local Authorities</option>
            </select>
            <input type="text" id="geoSearchInput" class="ui-input-sm" placeholder="Search name/town..." oninput="runSiteFinder()" style="width:130px;" aria-label="Search name or town" />
          </div>
        </div>

        <div class="ribbon-sep"></div>

        <!-- Planning Horizon & Tier -->
        <div class="ribbon-field">
          <span class="ribbon-label">Horizon &amp; Tier</span>
          <div style="display:flex;gap:6px;">
            <select id="horizonYearSelect" class="ui-select-sm" onchange="runSiteFinder()" aria-label="Planning Horizon">
              <option value="2026_LTDS" selected>2026/27 (LTDS T3)</option>
              <option value="2027">2027 (NSHR)</option>
              <option value="2028">2028 (NSHR)</option>
              <option value="2030">2030 (NSHR)</option>
              <option value="2035">2035 (RIIO-ED3)</option>
              <option value="2050">2050 (Net Zero)</option>
            </select>
            <select id="subTypeSelect" class="ui-select-sm" onchange="runSiteFinder()" aria-label="Voltage Tier">
              <option value="ALL" selected>All Tiers</option>
              <option value="Primary">Primary (11kV)</option>
              <option value="BSP">BSP (33kV)</option>
              <option value="GSP">GSP (132kV)</option>
            </select>
            <button type="button" class="btn-tool" onclick="resetFilters()">Reset</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Status Filter Bar & Action Strip (Export, Share, Compare) -->
    <section class="filter-actions-bar" aria-label="Feasibility Filters and Export Tools">
      <div class="status-chips-group">
        <button type="button" class="chip-filter-btn active" id="fBtnAll" onclick="setFeasibilityFilter('ALL')">
          <span>All Substations</span>
          <span class="chip-badge" id="countAll">981</span>
        </button>
        <button type="button" class="chip-filter-btn" id="fBtnViable" onclick="setFeasibilityFilter('VIABLE')">
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#059669;"></span>
          <span>Viable</span>
          <span class="chip-badge" id="countViable" style="background:#f0fdf4;color:#065f46;">0</span>
        </button>
        <button type="button" class="chip-filter-btn" id="fBtnCond" onclick="setFeasibilityFilter('CONDITIONAL')">
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#d97706;"></span>
          <span>Conditional</span>
          <span class="chip-badge" id="countCond" style="background:#fffbeb;color:#92400e;">0</span>
        </button>
        <button type="button" class="chip-filter-btn" id="fBtnConst" onclick="setFeasibilityFilter('CONSTRAINED')">
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#dc2626;"></span>
          <span>Constrained</span>
          <span class="chip-badge" id="countConst" style="background:#fef2f2;color:#991b1b;">0</span>
        </button>
      </div>

      <div class="action-tools-group">
        <span id="feasibilityDescriptionText" style="font-size: 12px;color:var(--text-sub);margin-right:6px;"></span>
        <button type="button" class="btn-tool" onclick="exportCSV()" title="Export current results to CSV">
          <span>&darr; Export CSV</span>
        </button>
        <button type="button" class="btn-tool" onclick="copyShareableLink()" title="Copy shareable link with filters">
          <span>&infin; Share Link</span>
        </button>
      </div>
    </section>

    <!-- 3. Two-Column Workspace (Map Left, Inspector + Table Right) -->
    <section class="workspace-grid">

      <!-- Left Heroic Map Column with Clustering & Legend -->
      <aside class="map-container-hero" aria-label="Geographic Network Map">
        <div class="map-top-bar">
          <div style="font-size:12px;font-weight:700;color:var(--text-main);">Spatial Network Coverage</div>
          <!-- Coherent Licence Area Filter -->
          <div class="map-licence-pills">
            <button type="button" class="licence-btn active" id="licenceBtnAll" onclick="setLicenceArea('ALL')">All UK</button>
            <button type="button" class="licence-btn" id="licenceBtnSEPD" onclick="setLicenceArea('SEPD')">SEPD South</button>
            <button type="button" class="licence-btn" id="licenceBtnSHEPD" onclick="setLicenceArea('SHEPD')">SHEPD North</button>
            <button type="button" class="licence-btn" id="btnResetMapView" onclick="resetMapView()" title="Fit map to all filtered candidates">↺ Reset View</button>
          </div>
        </div>

        <div id="realMapNode"></div>

        <!-- On-map Legend with distinct shapes & colors -->
        <div class="map-legend-bar">
          <div class="legend-symbol-item">
            <svg width="14" height="14" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="#059669"/><path d="M6 10l3 3 5-5" stroke="#ffffff" stroke-width="2.5" fill="none"/></svg>
            <span>Viable</span>
          </div>
          <div class="legend-symbol-item">
            <svg width="14" height="14" viewBox="0 0 20 20"><polygon points="10,2 18,10 10,18 2,10" fill="#d97706"/><text x="10" y="14" font-weight="900" font-size="11" fill="#ffffff" text-anchor="middle">!</text></svg>
            <span>Conditional</span>
          </div>
          <div class="legend-symbol-item">
            <svg width="14" height="14" viewBox="0 0 20 20"><rect x="3" y="3" width="14" height="14" rx="2" fill="#dc2626"/><path d="M6 6l8 8M14 6l-8 8" stroke="#ffffff" stroke-width="2" fill="none"/></svg>
            <span>Constrained</span>
          </div>
          <div class="legend-symbol-item">
            <svg width="14" height="14" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="#64748b"/><text x="10" y="14" font-weight="900" font-size="11" fill="#ffffff" text-anchor="middle">?</text></svg>
            <span>Not Published</span>
          </div>
          <div class="legend-symbol-item" style="color:var(--text-soft);">
            <span>Clustering active at low zoom</span>
          </div>
        </div>
      </aside>

      <!-- Right Panel Stack: Inspector Card (Collapsible) + Ranked Candidate Table -->
      <div class="panel-stack">

        <!-- Substation Detail Inspector -->
        <section class="inspector-card collapsed" id="inspectorCard" aria-label="Selected Substation Detail">
          <div class="inspector-top-row">
            <div class="sub-title-group">
              <div class="sub-name-wrap">
                <span id="dosName">Select a Substation</span>
                <span class="status-badge status-viable" id="dosStatusBadge">Viable</span>
                <span class="badge-subtle" id="dosTypeBadge">Primary: 11kV</span>
              </div>
              <div class="sub-meta-tags" id="dosMetaLine">
                <span>Council: None</span>
                <span>GSP: None</span>
                <span>Area: None</span>
              </div>
            </div>

            <div class="verdict-box">
              <div class="verdict-subtext">Post-Project Remaining Headroom</div>
              <div class="verdict-mva" id="dosPostMargin">+0.00 MVA</div>
            </div>
          </div>

          <!-- Plain-English Verdict Callout -->
          <div class="verdict-callout" id="dosVerdictCallout">
            Select any substation on the map or candidate list to inspect connection feasibility.
          </div>

          <!-- 4 Typographic Metrics with On-Demand Hover Tooltips (?) -->
          <div class="stats-clean-row">
            <!-- Stat 1 -->
            <div class="stat-metric">
              <div class="stat-label">
                <span id="metricTitle1">Firm Capacity</span>
                <span class="tooltip-help" tabindex="0" aria-label="Firm Capacity explanation">?
                  <span class="tooltip-popover" id="metricTip1">Maximum continuous load the substation can safely carry under an N-1 single equipment outage.</span>
                </span>
              </div>
              <div class="stat-number" id="metricFirmVal">0.0 MVA</div>
              <div class="stat-desc" id="metricDesc1">N-1 cyclic rating</div>
            </div>

            <!-- Stat 2 -->
            <div class="stat-metric">
              <div class="stat-label">
                <span id="metricTitle2">Peak Demand</span>
                <span class="tooltip-help" tabindex="0" aria-label="Peak Demand explanation">?
                  <span class="tooltip-popover" id="metricTip2">Forecasted peak customer demand in selected planning year.</span>
                </span>
              </div>
              <div class="stat-number" id="metricDemandVal">0.0 MVA</div>
              <div class="stat-desc" id="metricDesc2">Projected winter peak</div>
            </div>

            <!-- Stat 3: Headroom with Contextual Tooltip (?) -->
            <div class="stat-metric">
              <div class="stat-label">
                <span id="metricTitle3">Available Headroom</span>
                <span class="tooltip-help" tabindex="0" aria-label="Available Headroom calculation breakdown">?
                  <span class="tooltip-popover" id="metricTip3">Spare unallocated power capacity before project connection.</span>
                </span>
              </div>
              <div class="stat-number" id="metricHeadroomVal">0.0 MVA</div>
              <div class="stat-desc" id="metricDesc3">Active network limit</div>
            </div>

            <!-- Stat 4 -->
            <div class="stat-metric">
              <div class="stat-label">
                <span id="metricTitle4">Switchgear Margin</span>
                <span class="tooltip-help" tabindex="0" aria-label="Switchgear Fault Margin explanation">?
                  <span class="tooltip-popover" id="metricTip4">Circuit breaker breaking capacity minus short-circuit current. Positive = safe.</span>
                </span>
              </div>
              <div class="stat-number" id="metricFaultVal">0.0 kA</div>
              <div class="stat-desc" id="metricDesc4">Fault current headroom</div>
            </div>
          </div>

          <!-- Compact Summary Row (Visible when collapsed / compact) -->
          <div class="compact-summary-row">
            <div class="compact-stats">
              <span>Headroom: <strong id="dosCompactHeadroom">0.0 MVA</strong></span>
              <span class="sep">•</span>
              <span>Firm: <strong id="dosCompactFirm">0.0 MVA</strong></span>
              <span class="sep">•</span>
              <span>Score: <strong id="dosCompactScore">95/100</strong></span>
              <span class="sep">•</span>
              <span class="compact-verdict-text" id="dosCompactVerdict">Optimal connection candidate.</span>
            </div>
            <div class="compact-actions">
              <button type="button" class="btn-tool" id="btnDetailBookmarkCompact" onclick="toggleCurrentBookmark()">
                <span id="btnDetailBookmarkTextCompact">★ Shortlist</span>
              </button>
              <button type="button" class="btn-tool btn-expand-toggle" onclick="toggleInspectorCollapse()">
                Expand Details ▼
              </button>
            </div>
          </div>

          <!-- Bottom Footer Strip with Collapsible Toggle, Score & Shortlist Action -->
          <div class="inspector-footer-bar">
            <div class="score-group">
              <span>Feasibility:</span>
              <strong style="font-family:var(--font-mono);color:var(--brand-navy);" id="dosSuitabilityScore">95 / 100</strong>
              <span id="dosLowConfidenceBadge"></span>
              <span class="tooltip-help" tabindex="0" aria-label="Score calculation arithmetic">?
                <span class="tooltip-popover" id="dosScoreBreakdownTip">Score arithmetic breakdown.</span>
              </span>
            </div>

            <div id="dosTransmissionNote" style="font-size: 12px;color:var(--text-sub);"></div>

            <div class="inspector-actions-row">
              <button type="button" class="btn-tool" id="btnDetailBookmark" onclick="toggleCurrentBookmark()">
                <span id="btnDetailBookmarkText">★ Shortlist</span>
              </button>
              <button type="button" class="btn-tool" id="btnToggleCollapse" onclick="toggleInspectorCollapse()">
                Compact ▲
              </button>
            </div>
          </div>
        </section>

        <!-- Ranked Candidate Table Surface -->
        <section class="table-card" aria-label="Candidate Substations">
          <div class="table-header-strip">
            <div class="table-count-title" id="tableTitleCount">Candidate Substations (981)</div>
            <div style="font-size: 12px;color:var(--text-sub);">
              <span>Click any row to select &amp; pan map</span>
            </div>
          </div>

          <div class="table-scroll-wrap" id="tableScrollContainer">
            <table class="ranked-data-table">
              <thead>
                <tr>
                  <th onclick="toggleSort('name')" id="thName">Substation <span id="sortArrowName"></span></th>
                  <th>Area / Type</th>
                  <th>Voltage</th>
                  <th class="num-cell" onclick="toggleSort('firm')" id="thFirm">Firm (MVA) <span id="sortArrowFirm"></span></th>
                  <th class="num-cell" onclick="toggleSort('headroom')" id="thHeadroom">Headroom (MVA) <span id="sortArrowHeadroom"></span></th>
                  <th class="num-cell" onclick="toggleSort('margin')" id="thMargin">Margin (MVA) <span id="sortArrowMargin">&darr;</span></th>
                  <th style="text-align:center;">Status</th>
                  <th style="text-align:center;width:115px;">Shortlist</th>
                </tr>
              </thead>
              <tbody id="candidateTableBody">
                <!-- Injected via JavaScript -->
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </section>

    </div><!-- end #dashboardView -->

    <!-- Quiet Footer -->
    <footer class="portal-footer">
      <div>Independent Grid Connection Screening Tool &middot; Not affiliated with or endorsed by SSE plc, SSEN, or National Grid ESO.</div>
      <div style="display:flex;gap:12px;">
        <button type="button" class="btn-tool" onclick="openTermsModal('terms')">Terms &amp; Disclaimer</button>
        <button type="button" class="btn-tool" onclick="openTermsModal('sources')">Data Sources</button>
        <button type="button" class="btn-tool" onclick="openTermsModal('calculations')">Formulas &amp; Methodology</button>
      </div>
    </footer>

  </main>

  <!-- Terms & Methodology Modal Dialog -->
  <dialog id="termsModal" class="app-dialog" aria-labelledby="termsModalTitle">
    <div class="dialog-header">
      <div class="dialog-title" id="termsModalTitle">Terms, Data Sources &amp; Methodology</div>
      <button type="button" class="btn-tool" onclick="closeTermsModal()">Close</button>
    </div>

    <div class="dialog-body">
      <div>
        <h3 style="font-weight:700;font-size:13.5px;margin-bottom:4px;">Independent Build Notice &amp; Disclaimer</h3>
        <p style="color:var(--text-sub);">This portal is an independent engineering screening tool. It is <strong>not affiliated with, endorsed by, or operated by SSE plc, Scottish and Southern Electricity Networks (SSEN Distribution / SSEN Transmission), or National Grid ESO</strong>.</p>
        <p style="color:var(--text-sub);margin-top:6px;">All capacity estimates and feasibility ratings are indicative and for preliminary screening only. They do not constitute a formal Point of Connection (PoC) quote or grid reservation. Formal applications must be submitted directly to SSEN: <a href="https://www.ssen.co.uk/our-services/connections/" target="_blank" rel="noopener" style="color:var(--brand-blue);">ssen.co.uk/our-services/connections/</a>.</p>
      </div>

      <div>
        <h3 style="font-weight:700;font-size:13.5px;margin-bottom:4px;">Regulatory Data Sources</h3>
        <p style="color:var(--text-sub);">All 981 substations are sourced directly from official SSEN open datasets:</p>
        <ul style="margin-left:20px;margin-top:6px;color:var(--text-sub);">
          <li><strong>SSEN May 2026 Generation Availability Heatmaps:</strong> Coordinates, voltages, circuit breaker breaking and fault currents (SEPD: <code>5e44d9db...</code>, SHEPD: <code>9700c765...</code>).</li>
          <li><strong>SSEN May 2026 LTDS Table 3 &amp; 7:</strong> Distribution firm capacities, peak demands, and 5-year forecasts (SEPD: <code>02c9431f...</code>, SHEPD: <code>2bd2c3f3...</code>).</li>
          <li><strong>SSEN May 2026 NSHR Reports:</strong> 2027–2050 multi-scenario headroom envelopes (SEPD: <code>6e1bf42b...</code>, SHEPD: <code>3b368f36...</code>).</li>
          <li><strong>SSEN May 2026 NDR Reports:</strong> GSP transmission reinforcement schemes (Part 2 Table 2).</li>
        </ul>
      </div>

      <div>
        <h3 style="font-weight:700;font-size:13.5px;margin-bottom:4px;">Calculation Methodology</h3>
        <p style="color:var(--text-sub);">Implements SSEN DSO's Network Development Plan (NDP) methodology:</p>
        <ul style="margin-left:20px;margin-top:6px;color:var(--text-sub);">
          <li><strong>Demand Headroom:</strong> Firm Capacity (MVA) &minus; Forecasted Maximum Demand (MVA) [NDP Sec 6.1].</li>
          <li><strong>Generation Headroom:</strong> Reverse Power Flow Rating (MVA) &minus; Minimum Summer Load [NDP Sec 6.2].</li>
          <li><strong>Battery Storage Headroom:</strong> min(Demand Headroom, Generation Headroom) [Dual Constraint].</li>
          <li><strong>Post-Project Margin:</strong> Available Headroom &minus; Requested Capacity.</li>
        </ul>
      </div>
    </div>
  </dialog>

  <!-- Shortlist Compare Modal Dialog -->
  <dialog id="compareModal" class="app-dialog" aria-labelledby="compareModalTitle">
    <div class="dialog-header">
      <div class="dialog-title" id="compareModalTitle">Shortlist Comparison (Side-by-Side)</div>
      <div style="display:flex;gap:8px;">
        <button type="button" class="btn-tool" onclick="clearShortlist()">Clear All</button>
        <button type="button" class="btn-tool" onclick="exportShortlistCSV()">Export Shortlist CSV</button>
        <button type="button" class="btn-tool" onclick="closeCompareModal()">Close</button>
      </div>
    </div>

    <div class="dialog-body" id="compareModalBody">
      <!-- Injected via JavaScript -->
    </div>
  </dialog>

  <!-- Toast Notification -->
  <div id="portalToast" class="toast-msg" role="status" aria-live="polite">
    <span id="toastText">Action completed</span>
  </div>

  <script>
    let PORTAL_DATA = __PORTAL_DATA_JSON__;
    let SUBSTATIONS = PORTAL_DATA.substations || [];
    let BOUNDARIES = PORTAL_DATA.boundaries || {};
    let NDR_HIGHLIGHTS = PORTAL_DATA.ndr_2026_highlights || [];
    const NSHR_YEARS = ["2027", "2028", "2030", "2032", "2035", "2040", "2045", "2050"];

    let state = {
      projectType: "demand",
      reqCapMva: 5.0,
      licenceArea: "ALL", // "ALL", "SEPD", "SHEPD"
      geoArea: "ALL",      // Local authority
      searchQuery: "",
      horizonYear: "2026_LTDS",
      season: "W",
      scenario: "HT",
      subTypeFilter: "ALL",
      feasibilityFilter: "ALL",
      selectedSubId: null,
      sortColumn: "margin", // "margin", "headroom", "firm", "name"
      sortDirection: "desc", // "asc", "desc"
      shortlist: new Set(),
      isCollapsed: true
    };

    let leafletMap = null;
    let clusterGroup = null;
    let substationMarkerMap = new Map();
    let currentEvaluated = [];

    /* Formatting Utilities */
    function fmtNum(val, unit = "") {
      if (val == null || isNaN(val)) return null;
      return Number(val).toLocaleString("en-GB", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + unit;
    }

    function fmtSignedNum(val, unit = "") {
      if (val == null || isNaN(val)) return null;
      const s = val > 0 ? "+" : "";
      return s + Number(val).toLocaleString("en-GB", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + unit;
    }

    /* Logarithmic Slider Utilities */
    function sliderToCap(val) {
      const minCap = 0.5;
      const maxCap = 100.0;
      const normalized = val / 100.0;
      const cap = minCap * Math.pow(maxCap / minCap, normalized);
      return cap < 10 ? Math.round(cap * 10) / 10 : Math.round(cap);
    }

    function capToSlider(cap) {
      const minCap = 0.5;
      const maxCap = 100.0;
      const c = Math.max(minCap, Math.min(maxCap, cap));
      const normalized = Math.log(c / minCap) / Math.log(maxCap / minCap);
      return Math.round(normalized * 100);
    }

    /* Substation Evaluation Engine */
    function evaluateSubstation(sub) {
      let activeFirm = sub.firm_dem_mva;
      let activePeak = sub.forecast_max_dem_2627 ?? sub.obs_max_dem_mva;
      let localDemandHeadroom = (activeFirm != null && activePeak != null) ? (activeFirm - activePeak) : null;
      let availDemandHeadroom = sub.hm_avail_dem_mva ?? localDemandHeadroom;

      let firmGen = sub.firm_gen_mva ?? (sub.firm_dem_mva ? sub.firm_dem_mva * 0.9 : null);
      let availGenHeadroom = sub.hm_avail_gen_mva ?? (firmGen ? firmGen * 0.85 : null);

      let activeHeadroom = null;
      let isGsp = sub.type === "GSP";
      let hasMissingData = (activeFirm == null && availDemandHeadroom == null);

      if (state.projectType === "demand") {
        activeFirm = sub.firm_dem_mva;
        if (state.horizonYear === "2026_LTDS") {
          activeHeadroom = availDemandHeadroom;
        } else {
          const yrIdx = NSHR_YEARS.indexOf(state.horizonYear);
          if (yrIdx !== -1 && sub.nshr_demand && sub.nshr_demand[state.scenario] && sub.nshr_demand[state.scenario][state.season]) {
            activeHeadroom = sub.nshr_demand[state.scenario][state.season][yrIdx];
          }
          if (activeHeadroom == null) activeHeadroom = availDemandHeadroom;
        }
      } else if (state.projectType === "generation") {
        activeFirm = firmGen;
        if (state.horizonYear === "2026_LTDS") {
          activeHeadroom = availGenHeadroom;
        } else {
          const yrIdx = NSHR_YEARS.indexOf(state.horizonYear);
          if (yrIdx !== -1 && sub.nshr_gen && sub.nshr_gen[state.scenario] && sub.nshr_gen[state.scenario][state.season]) {
            activeHeadroom = sub.nshr_gen[state.scenario][state.season][yrIdx];
          }
          if (activeHeadroom == null) activeHeadroom = availGenHeadroom;
        }
      } else {
        // Battery Storage
        if (availDemandHeadroom != null && availGenHeadroom != null) {
          activeHeadroom = Math.min(availDemandHeadroom, availGenHeadroom);
        } else {
          activeHeadroom = availDemandHeadroom ?? availGenHeadroom;
        }
      }

      const req = state.reqCapMva || 1.0;
      let postMargin = activeHeadroom != null ? activeHeadroom - req : null;

      const breaking = sub.breaker_cap_ka;
      const fault = sub.breaker_scc_ka;
      const faultMargin = (breaking != null && fault != null) ? (breaking - fault) : sub.fault_margin_ka;
      const hasFaultRisk = faultMargin != null && faultMargin < 0.5;

      let status = "CONSTRAINED";
      let statusLabel = "Constrained";

      if (hasMissingData) {
        status = "INCOMPLETE";
        statusLabel = "Not Published";
      } else if (postMargin != null && postMargin >= 0) {
        if (hasFaultRisk || postMargin < req * 0.15) {
          status = "CONDITIONAL";
          statusLabel = "Conditional";
        } else {
          status = "VIABLE";
          statusLabel = "Viable";
        }
      } else if (postMargin != null && postMargin > -req * 0.25) {
        status = "CONDITIONAL";
        statusLabel = "Conditional";
      }

      // Transparent Score Arithmetic
      let score = null;
      let scoreBreakdownStr = "";

      if (hasMissingData) {
        score = null;
        scoreBreakdownStr = "Score unavailable: DNO has not published firm rating or headroom for this asset.";
      } else {
        score = 50;
        let parts = ["Base: +50"];
        if (postMargin != null) {
          if (postMargin >= 0) {
            const b = Math.min(35, Math.round(postMargin * 2.5));
            score += b;
            parts.push(`Headroom Surplus: +${b}`);
          } else {
            const p = Math.min(45, Math.round(Math.abs(postMargin) * 1.2));
            score -= p;
            parts.push(`Shortfall Deficit: -${p}`);
          }
        }
        const isUpstreamConstrained = Boolean(sub.upstream_constraint || sub.dem_rag === "Red" || sub.gen_rag === "Red");
        if (isUpstreamConstrained) {
          score -= 10;
          parts.push("Upstream GSP Bottleneck: -10");
        }
        if (faultMargin != null) {
          if (faultMargin >= 2.0) {
            score += 10;
            parts.push("Switchgear Safe: +10");
          } else if (faultMargin < 0.5) {
            score -= 10;
            parts.push("Switchgear Tight: -10");
          }
        }
        score = Math.max(5, Math.min(99, Math.round(score)));
        scoreBreakdownStr = parts.join(" | ") + ` = ${score} / 100`;
      }

      // Plain-English Verdict Summary
      let verdict = "";
      if (hasMissingData) {
        verdict = isGsp 
          ? `Data incomplete. ${sub.name} is a 400kV/132kV National Grid Transmission GSP. Distribution firm ratings are maintained by National Grid ESO (NGET) rather than published by SEPD in LTDS Table 3.`
          : `Data incomplete. DNO has not published firm capacity or peak telemetry figures for ${sub.name} in public LTDS filings.`;
      } else if (status === "VIABLE") {
        verdict = `Immediate capacity available. Substation has sufficient firm headroom for your requested ${req.toFixed(1)} MVA ${state.projectType} connection with safe switchgear fault margins.`;
      } else if (status === "CONDITIONAL") {
        verdict = `Connection possible but requires engineering review. Remaining headroom is tight (<15%) or local ANM flexibility agreement may be required.`;
      } else {
        verdict = `Likely needs reinforcement. Headroom is insufficient for ${req.toFixed(1)} MVA by ${state.horizonYear}. Upstream grid constraints require network reinforcement.`;
      }

      return {
        sub: sub,
        isGsp: isGsp,
        hasMissingData: hasMissingData,
        activeFirm: activeFirm,
        activePeak: activePeak,
        localDemandHeadroom: localDemandHeadroom,
        availDemandHeadroom: availDemandHeadroom,
        availGenHeadroom: availGenHeadroom,
        storageImportHeadroom: availDemandHeadroom,
        storageExportHeadroom: availGenHeadroom,
        activeHeadroom: activeHeadroom != null ? Math.round(activeHeadroom * 100) / 100 : null,
        postMargin: postMargin != null ? Math.round(postMargin * 100) / 100 : null,
        faultMargin: faultMargin != null ? Math.round(faultMargin * 100) / 100 : null,
        status: status,
        statusLabel: statusLabel,
        score: score,
        scoreBreakdownStr: scoreBreakdownStr,
        verdict: verdict,
        isUpstreamConstrained: Boolean(sub.upstream_constraint || sub.dem_rag === "Red" || sub.gen_rag === "Red")
      };
    }

    /* Core Search & Filtering */
    function updateFeasibilityCaption() {
      const cap = document.getElementById("feasibilityDescriptionText");
      if (!cap) return;
      const typeLabel = state.projectType === "demand" ? "Demand" : (state.projectType === "generation" ? "Generation" : "Storage");
      const count = currentEvaluated.length;
      cap.textContent = `Screened ${count} substations for ${state.reqCapMva.toFixed(1)} MVA ${typeLabel}`;
    }

    function runSiteFinder() {
      state.searchQuery = (document.getElementById("geoSearchInput").value || "").trim().toLowerCase();
      state.horizonYear = document.getElementById("horizonYearSelect").value;
      state.subTypeFilter = document.getElementById("subTypeSelect").value;

      const evaluated = [];
      let cntViable = 0;
      let cntCond = 0;
      let cntConst = 0;

      for (let i = 0; i < SUBSTATIONS.length; i++) {
        const s = SUBSTATIONS[i];

        // 1. Licence Area Filter (SEPD / SHEPD / ALL)
        if (state.licenceArea !== "ALL" && s.area !== state.licenceArea) continue;

        // 2. Local Authority Filter
        if (state.geoArea !== "ALL" && s.local_authority !== state.geoArea) continue;

        // 3. Voltage Tier Filter
        if (state.subTypeFilter !== "ALL" && s.type !== state.subTypeFilter) continue;

        // 4. Text Search
        if (state.searchQuery) {
          const q = state.searchQuery;
          const match = (s.name && s.name.toLowerCase().includes(q)) ||
                        (s.local_authority && s.local_authority.toLowerCase().includes(q)) ||
                        (s.gsp && s.gsp.toLowerCase().includes(q));
          if (!match) continue;
        }

        const ev = evaluateSubstation(s);

        if (ev.status === "VIABLE") cntViable++;
        else if (ev.status === "CONDITIONAL") cntCond++;
        else cntConst++;

        // Status Filter
        if (state.feasibilityFilter !== "ALL" && ev.status !== state.feasibilityFilter) continue;

        evaluated.push(ev);
      }

      // Sort evaluated candidates so highest margin / viable candidates appear first
      evaluated.sort((a, b) => {
        let valA, valB;
        if (state.sortColumn === "margin") {
          valA = a.postMargin != null ? a.postMargin : -9999;
          valB = b.postMargin != null ? b.postMargin : -9999;
        } else if (state.sortColumn === "headroom") {
          valA = a.activeHeadroom != null ? a.activeHeadroom : -9999;
          valB = b.activeHeadroom != null ? b.activeHeadroom : -9999;
        } else if (state.sortColumn === "firm") {
          valA = a.activeFirm != null ? a.activeFirm : -9999;
          valB = b.activeFirm != null ? b.activeFirm : -9999;
        } else {
          valA = a.sub.name;
          valB = b.sub.name;
        }

        if (typeof valA === "string") {
          return state.sortDirection === "asc" ? valA.localeCompare(valB) : valB.localeCompare(valA);
        }
        return state.sortDirection === "asc" ? valA - valB : valB - valA;
      });

      currentEvaluated = evaluated;

      // Update Counts
      document.getElementById("countAll").textContent = evaluated.length;
      document.getElementById("countViable").textContent = cntViable;
      document.getElementById("countCond").textContent = cntCond;
      document.getElementById("countConst").textContent = cntConst;
      document.getElementById("tableTitleCount").textContent = `Candidate Substations (${evaluated.length})`;

      updateFeasibilityCaption();
      updateMapMarkers();
      renderTable();

      // Ensure valid selection & update inspector:
      // When first opening or if no selection exists, select the top-ranked viable candidate with full data (e.g. Staines BSP)
      // Never default to incomplete Transmission GSPs like Amersham
      if (currentEvaluated.length > 0) {
        let targetEv = currentEvaluated.find(e => e.sub.id === state.selectedSubId);
        if (!targetEv) {
          targetEv = currentEvaluated.find(e => e.status === "VIABLE" && e.activeFirm != null && e.activeHeadroom != null) || currentEvaluated[0];
          state.selectedSubId = targetEv.sub.id;
        }
        selectSubstation(targetEv.sub.id, false);
      } else {
        renderEmptyState();
      }
    }

    /* Render Candidate Table with Sortable Columns & Bookmark Actions */
    function renderTable() {
      const tbody = document.getElementById("candidateTableBody");
      if (!tbody) return;
      tbody.innerHTML = "";

      if (currentEvaluated.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="8" style="text-align:center;padding:36px;color:var(--text-sub);">
              <div style="font-size:14px;font-weight:700;color:var(--text-main);margin-bottom:4px;">No matching substations found</div>
              <div style="font-size:12px;margin-bottom:12px;">Try selecting "All Local Authorities", reducing your capacity, or resetting filters.</div>
              <button type="button" class="btn-tool" onclick="resetFilters()">Reset All Filters</button>
            </td>
          </tr>
        `;
        return;
      }

      // Sort
      const sorted = [...currentEvaluated].sort((a, b) => {
        let valA, valB;
        if (state.sortColumn === "margin") {
          valA = a.postMargin != null ? a.postMargin : -9999;
          valB = b.postMargin != null ? b.postMargin : -9999;
        } else if (state.sortColumn === "headroom") {
          valA = a.activeHeadroom != null ? a.activeHeadroom : -9999;
          valB = b.activeHeadroom != null ? b.activeHeadroom : -9999;
        } else if (state.sortColumn === "firm") {
          valA = a.activeFirm != null ? a.activeFirm : -9999;
          valB = b.activeFirm != null ? b.activeFirm : -9999;
        } else {
          valA = a.sub.name;
          valB = b.sub.name;
          return state.sortDirection === "asc" ? valA.localeCompare(valB) : valB.localeCompare(valA);
        }
        return state.sortDirection === "asc" ? valA - valB : valB - valA;
      });

      const displayList = sorted.slice(0, 100);

      displayList.forEach(e => {
        const s = e.sub;
        const tr = document.createElement("tr");
        tr.tabIndex = 0;
        tr.setAttribute("role", "row");
        tr.setAttribute("data-sub-id", s.id);
        if (s.id === state.selectedSubId) tr.classList.add("selected");

        let statusClass = "status-constrained";
        if (e.status === "VIABLE") statusClass = "status-viable";
        else if (e.status === "CONDITIONAL") statusClass = "status-conditional";
        else if (e.status === "INCOMPLETE") statusClass = "status-incomplete";

        const isShortlisted = state.shortlist.has(s.id);

        const firmDisplay = e.activeFirm != null ? fmtNum(e.activeFirm) : '<span class="not-published-val">Not pub.</span>';
        const headroomDisplay = e.activeHeadroom != null ? fmtNum(e.activeHeadroom) : '<span class="not-published-val">Not pub.</span>';
        const marginDisplay = e.postMargin != null ? fmtSignedNum(e.postMargin) : '<span class="not-published-val">Not pub.</span>';
        const marginColor = e.postMargin != null ? ((e.postMargin >= 0) ? 'var(--status-green-text)' : 'var(--status-red-text)') : 'var(--text-soft)';

        tr.innerHTML = `
          <td>
            <div style="font-weight:700;">${s.name}</div>
            <div style="font-size: 12px;color:var(--text-sub);">${s.local_authority || 'SSEN Area'}</div>
          </td>
          <td>
            <div>${s.type}</div>
            <div style="font-size: 12px;color:var(--text-sub);">${s.area}</div>
          </td>
          <td class="col-mono">${s.voltage || '11kV'}</td>
          <td class="num-cell">${firmDisplay}</td>
          <td class="num-cell">${headroomDisplay}</td>
          <td class="num-cell" style="font-weight:700;color:${marginColor};">${marginDisplay}</td>
          <td style="text-align:center;">
            <span class="status-badge ${statusClass}">${e.statusLabel}</span>
          </td>
          <td style="text-align:center;">
            <button type="button" class="btn-row-shortlist ${isShortlisted ? 'is-shortlisted' : ''}" onclick="toggleBookmark('${s.id}', event)" aria-label="${isShortlisted ? 'Remove' : 'Add'} ${s.name} from Shortlist">
              <span class="star-icon">★</span> ${isShortlisted ? 'Shortlisted' : 'Shortlist'}
            </button>
          </td>
        `;

        tr.addEventListener("click", () => {
          selectSubstation(s.id, true);
        });

        tr.addEventListener("keydown", (evt) => {
          if (evt.key === "Enter" || evt.key === " ") {
            evt.preventDefault();
            selectSubstation(s.id, true);
          }
        });

        tbody.appendChild(tr);
      });
    }

    function toggleSort(col) {
      if (state.sortColumn === col) {
        state.sortDirection = state.sortDirection === "asc" ? "desc" : "asc";
      } else {
        state.sortColumn = col;
        state.sortDirection = (col === "name") ? "asc" : "desc";
      }

      // Update sort arrow indicators in headers
      ["name", "firm", "headroom", "margin"].forEach(c => {
        const arrow = document.getElementById("sortArrow" + c.charAt(0).toUpperCase() + c.slice(1));
        const th = document.getElementById("th" + c.charAt(0).toUpperCase() + c.slice(1));
        if (arrow) arrow.textContent = (state.sortColumn === c) ? (state.sortDirection === "asc" ? "▲" : "▼") : "";
        if (th) th.classList.toggle("sorted-active", state.sortColumn === c);
      });

      renderTable();
    }

    /* Substation Selection, Marker Highlight, and Scroll-to-Row */
    function selectSubstation(subId, panMap = true) {
      state.selectedSubId = subId;
      const ev = currentEvaluated.find(e => e.sub.id === subId) || SUBSTATIONS.map(evaluateSubstation).find(e => e.sub.id === subId);
      if (!ev) return;

      updateInspector(ev);

      // Highlight row and scroll into view smoothly by exact unique subId
      const rows = document.querySelectorAll("#candidateTableBody tr");
      rows.forEach(r => r.classList.remove("selected"));

      const matchTr = document.querySelector(`#candidateTableBody tr[data-sub-id="${subId}"]`);
      if (matchTr) {
        matchTr.classList.add("selected");
        matchTr.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }

      // Update marker icons dynamically (selected marker enlarges with cyan glow)
      if (substationMarkerMap && currentEvaluated) {
        substationMarkerMap.forEach((m, id) => {
          const subEv = currentEvaluated.find(e => e.sub.id === id);
          if (!subEv) return;
          const isThis = id === subId;
          m.setIcon(createStatusIcon(subEv.status, isThis));
          m.setZIndexOffset(isThis ? 1000 : 0);
        });
      }

      // Pan & Zoom Map to Regional Context (Zoom 12 shows place names, arterial roads & network context)
      if (panMap && leafletMap && ev.sub.lat != null && ev.sub.lon != null) {
        leafletMap.setView([ev.sub.lat, ev.sub.lon], 12, { animate: true });
        const marker = substationMarkerMap.get(subId);
        if (marker) {
          setTimeout(() => {
            marker.openPopup();
          }, 120);
        }
      }
    }

    function updateInspector(ev) {
      const s = ev.sub;
      document.getElementById("dosName").textContent = s.name;
      
      const badge = document.getElementById("dosStatusBadge");
      let statusClass = "status-constrained";
      if (ev.status === "VIABLE") statusClass = "status-viable";
      else if (ev.status === "CONDITIONAL") statusClass = "status-conditional";
      else if (ev.status === "INCOMPLETE") statusClass = "status-incomplete";
      badge.className = "status-badge " + statusClass;
      badge.textContent = ev.statusLabel;

      document.getElementById("dosTypeBadge").textContent = `${s.type}: ${s.voltage || '11kV'}`;
      document.getElementById("dosMetaLine").innerHTML = `
        <span><strong>Council:</strong> ${s.local_authority || 'SSEN Area'}</span>
        <span><strong>GSP:</strong> ${s.gsp || 'Direct Grid'}</span>
        <span><strong>Licence:</strong> ${s.region_label || s.area}</span>
        ${s.lat != null && s.lon != null ? `<span><a href="https://www.google.com/maps/search/?api=1&query=${s.lat},${s.lon}" target="_blank" rel="noopener noreferrer" style="color:#0369a1;text-decoration:none;font-weight:600;display:inline-flex;align-items:center;gap:3px;" title="Open substation coordinates in Google Maps (opens in new tab)">Google Maps &nearr;</a></span>` : ''}
      `;

      // Post-Project Margin or Not published
      const marginEl = document.getElementById("dosPostMargin");
      if (ev.postMargin != null) {
        marginEl.textContent = fmtSignedNum(ev.postMargin, " MVA");
        marginEl.style.color = (ev.postMargin >= 0) ? "var(--status-green-text)" : "var(--status-red-text)";
      } else {
        marginEl.innerHTML = `<span class="not-published-val">Not published</span>`;
      }

      // Plain-English Verdict Callout
      const callout = document.getElementById("dosVerdictCallout");
      callout.className = "verdict-callout " + ev.status.toLowerCase();
      callout.textContent = ev.verdict;

      // 4 Stats with contextual tooltips
      const isMissing = ev.hasMissingData;
      const eisdYear = s.demand_eisd || s.gen_eisd || "TBD";
      const limitFactor = s.dem_limit_factor || s.gen_limit_factor || "Upstream Thermal Capacity";

      // Stat 1
      document.getElementById("metricTitle1").textContent = state.projectType === "generation" ? "Reverse Rating" : "Firm Capacity";
      document.getElementById("metricFirmVal").innerHTML = ev.activeFirm != null ? fmtNum(ev.activeFirm, " MVA") : '<span class="not-published-val">Not published</span>';
      document.getElementById("metricDesc1").textContent = ev.activeFirm != null ? "N-1 cyclic rating" : "Not published in LTDS T3";
      document.getElementById("metricTip1").textContent = ev.activeFirm != null 
        ? `Maximum continuous load the substation can safely carry under an N-1 single equipment outage: ${fmtNum(ev.activeFirm, ' MVA')}.`
        : `SEPD has not published distribution firm capacity for ${s.name} in public LTDS Table 3.`;

      // Stat 2
      document.getElementById("metricTitle2").textContent = state.projectType === "generation" ? "Summer Min Load" : "Peak Demand";
      document.getElementById("metricDemandVal").innerHTML = ev.activePeak != null ? fmtNum(ev.activePeak, " MVA") : '<span class="not-published-val">Not published</span>';
      document.getElementById("metricDesc2").textContent = ev.activePeak != null ? "Forecasted peak" : "Telemetry not published";
      document.getElementById("metricTip2").textContent = ev.activePeak != null 
        ? `Projected peak demand for target planning year: ${fmtNum(ev.activePeak, ' MVA')}.`
        : `Peak load telemetry for ${s.name} is not published in public LTDS filings.`;

      // Stat 3: Headroom
      document.getElementById("metricTitle3").textContent = state.projectType === "storage" ? "Storage Headroom" : "Available Headroom";
      document.getElementById("metricHeadroomVal").innerHTML = ev.activeHeadroom != null ? fmtNum(ev.activeHeadroom, " MVA") : '<span class="not-published-val">Not published</span>';
      document.getElementById("metricDesc3").textContent = ev.activeHeadroom != null ? (ev.isUpstreamConstrained ? "Capped by GSP" : "Active network limit") : "No public rating";

      let tipText = `Available unallocated capacity: ${ev.activeHeadroom != null ? fmtNum(ev.activeHeadroom, ' MVA') : 'Not published'}.`;
      if (ev.isUpstreamConstrained || (ev.activeHeadroom === 0 && (ev.localDemandHeadroom ?? 0) > 0)) {
        tipText = `Why is Available Headroom ${fmtNum(ev.activeHeadroom, ' MVA')} despite ${fmtNum(ev.localDemandHeadroom, ' MVA')} local transformer capacity? While local transformers at ${s.name} have ${fmtNum(ev.localDemandHeadroom, ' MVA')} spare thermal rating, available connection capacity is capped at ${fmtNum(ev.activeHeadroom, ' MVA')} due to an ${limitFactor} bottleneck at ${s.gsp || 'the upstream GSP'} (National Grid Transmission EISD: ${eisdYear}).`;
      }
      document.getElementById("metricTip3").textContent = tipText;

      // Stat 4: Switchgear
      document.getElementById("metricTitle4").textContent = "Switchgear Margin";
      document.getElementById("metricFaultVal").innerHTML = ev.faultMargin != null ? fmtNum(ev.faultMargin, " kA") : '<span class="not-published-val">Safe</span>';
      document.getElementById("metricDesc4").textContent = "Fault current headroom";
      document.getElementById("metricTip4").textContent = `Circuit breaker rating (${fmtNum(s.breaker_cap_ka, ' kA')}) minus prospective short-circuit current (${fmtNum(s.breaker_scc_ka, ' kA')}). Margin: ${fmtNum(ev.faultMargin, ' kA')}.`;

      // Score or Low Confidence Badge
      const scoreEl = document.getElementById("dosSuitabilityScore");
      const lowConfBadge = document.getElementById("dosLowConfidenceBadge");
      const scoreTip = document.getElementById("dosScoreBreakdownTip");

      if (ev.score != null) {
        scoreEl.textContent = `${ev.score} / 100`;
        lowConfBadge.innerHTML = "";
        scoreTip.textContent = ev.scoreBreakdownStr;
      } else {
        scoreEl.textContent = "Data Incomplete";
        lowConfBadge.innerHTML = `<span class="badge-low-conf">Low Confidence</span>`;
        scoreTip.textContent = "A numeric score cannot be calculated because firm capacity or headroom is not published for this asset.";
      }

      // Transmission Note
      const transNote = document.getElementById("dosTransmissionNote");
      if (ev.isUpstreamConstrained) {
        transNote.innerHTML = `<span>GSP Constraint: <strong>${limitFactor}</strong> (EISD: <strong>${eisdYear}</strong>)</span>`;
      } else {
        transNote.innerHTML = `<span>Transmission: <strong style="color:var(--status-green-text);">Unconstrained</strong></span>`;
      }

      // Compact Summary Stats
      document.getElementById("dosCompactHeadroom").textContent = ev.activeHeadroom != null ? fmtNum(ev.activeHeadroom, " MVA") : "Not pub.";
      document.getElementById("dosCompactFirm").textContent = ev.activeFirm != null ? fmtNum(ev.activeFirm, " MVA") : "Not pub.";
      document.getElementById("dosCompactScore").textContent = ev.score != null ? `${ev.score}/100` : "Incomplete";
      document.getElementById("dosCompactVerdict").textContent = ev.verdict;

      // Shortlist Button State in Detail Card (Expanded & Compact)
      const isSaved = state.shortlist.has(s.id);
      const btnBookmarkText = document.getElementById("btnDetailBookmarkText");
      if (btnBookmarkText) {
        btnBookmarkText.textContent = isSaved ? "★ Shortlisted" : "★ Add to Shortlist";
      }
      const btnBookmarkTextCompact = document.getElementById("btnDetailBookmarkTextCompact");
      if (btnBookmarkTextCompact) {
        btnBookmarkTextCompact.textContent = isSaved ? "★ Shortlisted" : "★ Shortlist";
      }
    }

    function toggleInspectorCollapse() {
      const card = document.getElementById("inspectorCard");
      const btn = document.getElementById("btnToggleCollapse");
      state.isCollapsed = !state.isCollapsed;
      card.classList.toggle("collapsed", state.isCollapsed);
      if (btn) btn.innerHTML = state.isCollapsed ? "Expand Details ▼" : "Compact ▲";
    }

    function resetMapView() {
      if (!leafletMap) return;
      const validLatLngs = currentEvaluated
        .filter(e => e.sub.lat != null && e.sub.lon != null)
        .map(e => [e.sub.lat, e.sub.lon]);
      if (validLatLngs.length > 0) {
        leafletMap.fitBounds(L.latLngBounds(validLatLngs), { padding: [30, 30], maxZoom: 11 });
      } else {
        leafletMap.setView([54.5, -3.5], 6);
      }
    }

    /* Interactive Leaflet Map with Custom Status SVG Icons & MarkerCluster */
    function createStatusIcon(status, isSelected) {
      let symbol = "";

      if (status === "VIABLE") {
        // High-contrast emerald green circle with white checkmark
        symbol = `
          <circle cx="10" cy="10" r="8.5" fill="#059669" stroke="#ffffff" stroke-width="2"/>
          <path d="M6 10l3 3 5-5" stroke="#ffffff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        `;
      } else if (status === "CONDITIONAL") {
        // High-contrast amber diamond with bold white exclamation mark
        symbol = `
          <polygon points="10,1.5 18.5,10 10,18.5 1.5,10" fill="#d97706" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
          <text x="10" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="11" fill="#ffffff" text-anchor="middle">!</text>
        `;
      } else if (status === "INCOMPLETE") {
        // High-contrast slate circle with white question mark
        symbol = `
          <circle cx="10" cy="10" r="8.5" fill="#64748b" stroke="#ffffff" stroke-width="2"/>
          <text x="10" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="11" fill="#ffffff" text-anchor="middle">?</text>
        `;
      } else {
        // High-contrast red rounded-square with bold white cross
        symbol = `
          <rect x="2" y="2" width="16" height="16" rx="4" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>
          <path d="M6.5 6.5l7 7M13.5 6.5l-7 7" stroke="#ffffff" stroke-width="2.2" fill="none" stroke-linecap="round"/>
        `;
      }

      const baseSize = isSelected ? 28 : 20;
      const filterStyle = isSelected
        ? "filter: drop-shadow(0 0 6px #0284c7) drop-shadow(0 0 3px #0284c7) drop-shadow(0 2px 4px rgba(0,0,0,0.4));"
        : "filter: drop-shadow(0 2px 3px rgba(0,0,0,0.35));";

      const svgHtml = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" width="${baseSize}" height="${baseSize}" style="display:block;overflow:visible;${filterStyle}">${symbol}</svg>`;

      return L.divIcon({
        className: "custom-status-marker" + (isSelected ? " is-selected" : ""),
        html: svgHtml,
        iconSize: [baseSize, baseSize],
        iconAnchor: [baseSize / 2, baseSize / 2],
        popupAnchor: [0, -baseSize / 2]
      });
    }

    function initMap() {
      leafletMap = L.map("realMapNode", {
        center: [54.5, -3.5],
        zoom: 6,
        zoomControl: true,
        attributionControl: false
      });

      L.control.attribution({ position: "bottomright", prefix: false }).addTo(leafletMap);

      const esriStreets = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 18,
        attribution: "Tiles &copy; Esri"
      });

      const esriCanvas = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 16,
        attribution: "Tiles &copy; Esri"
      });

      const osmHot = L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap"
      });

      esriStreets.addTo(leafletMap);

      const baseMaps = {
        "UK Infrastructure Streets": esriStreets,
        "Clean Light Canvas": esriCanvas,
        "Humanitarian Detail": osmHot
      };

      L.control.layers(baseMaps, null, { position: "topright" }).addTo(leafletMap);

      // Initialize Cluster Group
      clusterGroup = L.markerClusterGroup({
        showCoverageOnHover: false,
        maxClusterRadius: 40,
        disableClusteringAtZoom: 12,
        spiderfyOnMaxZoom: true,
        zoomToBoundsOnClick: true,
        spiderfyDistanceMultiplier: 1.5,
        removeOutsideVisibleBounds: true,
        animate: true
      });
      leafletMap.addLayer(clusterGroup);
    }

    function updateMapMarkers() {
      if (!leafletMap || !clusterGroup) return;
      clusterGroup.clearLayers();
      substationMarkerMap.clear();

      const validLatLngs = [];

      currentEvaluated.forEach(e => {
        const s = e.sub;
        if (s.lat == null || s.lon == null) return;

        validLatLngs.push([s.lat, s.lon]);
        const isSel = s.id === state.selectedSubId;

        const icon = createStatusIcon(e.status, isSel);
        const marker = L.marker([s.lat, s.lon], { icon: icon, zIndexOffset: isSel ? 1000 : 0 });

        marker.bindPopup(`
          <div style="font-family:var(--font-sans);line-height:1.4;min-width:180px;">
            <div style="font-weight:700;font-size:13px;color:var(--text-main);">${s.name}</div>
            <div style="font-size: 12px;color:var(--text-sub);margin-bottom:4px;">${s.local_authority || 'SSEN Area'} | ${s.type} (${s.voltage})</div>
            <div style="font-family:var(--font-mono);font-size: 12px;">Headroom: <strong>${e.activeHeadroom != null ? fmtNum(e.activeHeadroom, ' MVA') : 'Not pub.'}</strong></div>
            <div style="font-family:var(--font-mono);font-size: 12px;">Post-Project: <strong style="color:${(e.postMargin ?? -1) >= 0 ? 'var(--status-green-text)' : 'var(--status-red-text)'};">${e.postMargin != null ? fmtSignedNum(e.postMargin, ' MVA') : 'Not pub.'}</strong></div>
            <div style="margin-top:8px;padding-top:6px;border-top:1px solid #e2e8f0;display:flex;align-items:center;justify-content:space-between;gap:8px;">
              <span class="status-badge ${e.status === 'VIABLE' ? 'status-viable' : (e.status === 'CONDITIONAL' ? 'status-conditional' : (e.status === 'INCOMPLETE' ? 'status-incomplete' : 'status-constrained'))}">${e.statusLabel}</span>
              ${s.lat != null && s.lon != null ? `<a href="https://www.google.com/maps/search/?api=1&query=${s.lat},${s.lon}" target="_blank" rel="noopener noreferrer" style="font-size:12px;color:#0369a1;text-decoration:none;font-weight:600;display:inline-flex;align-items:center;gap:2px;" title="Open location in Google Maps (opens in new tab)">Google Maps &nearr;</a>` : ''}
            </div>
          </div>
        `);

        marker.on("click", () => {
          selectSubstation(s.id, false);
        });

        clusterGroup.addLayer(marker);
        substationMarkerMap.set(s.id, marker);
      });

      // Always fit map bounds to current filtered substations if map container is visible
      const mapContainerNode = document.getElementById("realMapNode");
      if (mapContainerNode && mapContainerNode.offsetWidth > 0 && mapContainerNode.offsetHeight > 0) {
        if (validLatLngs.length > 1) {
          leafletMap.fitBounds(L.latLngBounds(validLatLngs), { padding: [35, 35], maxZoom: 12 });
        } else if (validLatLngs.length === 1) {
          leafletMap.setView(validLatLngs[0], 12);
        }
      }
    }

    /* Coherent Filter: Region Pills + Location Dropdown */
    function setLicenceArea(area) {
      state.licenceArea = area;
      state.geoArea = "ALL"; // Reset council filter when changing region

      document.getElementById("licenceBtnAll").classList.toggle("active", area === "ALL");
      document.getElementById("licenceBtnSEPD").classList.toggle("active", area === "SEPD");
      document.getElementById("licenceBtnSHEPD").classList.toggle("active", area === "SHEPD");

      // Scope Location Dropdown to the selected licence area
      populateGeoAreaOptions();
      runSiteFinder();

      // Zoom to area bounds
      if (area === "SEPD") {
        leafletMap.setView([51.3, -1.3], 8, { animate: true });
      } else if (area === "SHEPD") {
        leafletMap.setView([57.4, -4.2], 7, { animate: true });
      } else {
        leafletMap.setView([54.5, -3.5], 6, { animate: true });
      }
    }

    function onGeoAreaSelectChange() {
      const selectedCouncil = document.getElementById("geoAreaSelect").value;
      state.geoArea = selectedCouncil;

      // Auto-set licence area based on the council
      if (selectedCouncil !== "ALL") {
        const sampleSub = SUBSTATIONS.find(s => s.local_authority === selectedCouncil);
        if (sampleSub && sampleSub.area) {
          state.licenceArea = sampleSub.area;
          document.getElementById("licenceBtnAll").classList.toggle("active", state.licenceArea === "ALL");
          document.getElementById("licenceBtnSEPD").classList.toggle("active", state.licenceArea === "SEPD");
          document.getElementById("licenceBtnSHEPD").classList.toggle("active", state.licenceArea === "SHEPD");
        }
      }

      runSiteFinder();

      // Fit bounds to selected council's substations
      const councilSubs = currentEvaluated.filter(e => e.sub.local_authority === selectedCouncil && e.sub.lat && e.sub.lon);
      if (councilSubs.length > 0) {
        const bounds = L.latLngBounds(councilSubs.map(e => [e.sub.lat, e.sub.lon]));
        leafletMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 12 });
      }
    }

    function populateGeoAreaOptions() {
      const select = document.getElementById("geoAreaSelect");
      if (!select) return;

      const councils = new Set();
      SUBSTATIONS.forEach(s => {
        if (state.licenceArea === "ALL" || s.area === state.licenceArea) {
          if (s.local_authority) councils.add(s.local_authority);
        }
      });

      const sorted = Array.from(councils).sort();
      const areaLabel = state.licenceArea === "ALL" ? "All UK" : (state.licenceArea === "SEPD" ? "SEPD South" : "SHEPD North");
      select.innerHTML = `<option value="ALL">All Local Authorities (${areaLabel})</option>`;
      sorted.forEach(la => {
        const opt = document.createElement("option");
        opt.value = la;
        opt.textContent = la;
        if (la === state.geoArea) opt.selected = true;
        select.appendChild(opt);
      });
    }

    /* Capacity Handlers with Logarithmic Slider */
    function setCapacity(cap) {
      state.reqCapMva = cap;
      document.getElementById("reqCapInput").value = cap.toFixed(1);
      document.getElementById("reqCapSlider").value = capToSlider(cap);
      updateCapacityPillUI(cap);
      syncActivePresetUI();
      runSiteFinder();
    }

    function onNumberCapChange(val) {
      let cap = parseFloat(val);
      if (isNaN(cap) || cap <= 0) cap = 0.5;
      state.reqCapMva = cap;
      document.getElementById("reqCapSlider").value = capToSlider(cap);
      updateCapacityPillUI(cap);
      runSiteFinder();
    }

    function onSliderCapChange(sliderVal) {
      const cap = sliderToCap(parseFloat(sliderVal));
      state.reqCapMva = cap;
      document.getElementById("reqCapInput").value = cap.toFixed(1);
      updateCapacityPillUI(cap);
      runSiteFinder();
    }

    function updateCapacityPillUI(cap) {
      [1.0, 5.0, 20.0, 50.0].forEach(p => {
        const pill = document.getElementById("chipCap" + Math.round(p));
        if (pill) pill.classList.toggle("active", Math.abs(cap - p) < 0.2);
      });
    }

    function setProjectType(type) {
      state.projectType = type;
      document.getElementById("btnTypeDemand").classList.toggle("active", type === "demand");
      document.getElementById("btnTypeGen").classList.toggle("active", type === "generation");
      document.getElementById("btnTypeBess").classList.toggle("active", type === "storage");
      syncActivePresetUI();
      runSiteFinder();
    }

    function setFeasibilityFilter(f) {
      state.feasibilityFilter = f;
      document.getElementById("fBtnAll").classList.toggle("active", f === "ALL");
      document.getElementById("fBtnViable").classList.toggle("active", f === "VIABLE");
      document.getElementById("fBtnCond").classList.toggle("active", f === "CONDITIONAL");
      document.getElementById("fBtnConst").classList.toggle("active", f === "CONSTRAINED");
      runSiteFinder();
    }

    function applyPreset(code) {
      let targetType = "demand";
      let targetCap = 5.0;

      if (code === "ev_hub") {
        targetType = "demand";
        targetCap = 5.0;
      } else if (code === "solar_gen") {
        targetType = "generation";
        targetCap = 15.0;
      } else if (code === "datacentre") {
        targetType = "demand";
        targetCap = 25.0;
      } else if (code === "bess_flex") {
        targetType = "storage";
        targetCap = 30.0;
      }

      // 1. Update internal state atomically
      state.projectType = targetType;
      state.reqCapMva = targetCap;

      // 2. Update Connection Type UI Buttons
      document.getElementById("btnTypeDemand").classList.toggle("active", targetType === "demand");
      document.getElementById("btnTypeGen").classList.toggle("active", targetType === "generation");
      document.getElementById("btnTypeBess").classList.toggle("active", targetType === "storage");

      // 3. Update Capacity Input & Slider
      document.getElementById("reqCapInput").value = targetCap.toFixed(1);
      document.getElementById("reqCapSlider").value = capToSlider(targetCap);
      updateCapacityPillUI(targetCap);

      // 4. Update preset pill active states
      syncActivePresetUI(code);

      // 5. Run evaluation and UI refresh immediately in one single pass
      runSiteFinder();
    }

    function syncActivePresetUI(activeCode = null) {
      const presets = ["ev_hub", "solar_gen", "datacentre", "bess_flex"];
      presets.forEach(p => {
        const btn = document.querySelector(`.preset-pill[data-preset="${p}"]`);
        if (!btn) return;
        if (activeCode) {
          btn.classList.toggle("active", p === activeCode);
        } else {
          let matches = false;
          if (p === "ev_hub" && state.projectType === "demand" && Math.abs(state.reqCapMva - 5.0) < 0.1) matches = true;
          if (p === "solar_gen" && state.projectType === "generation" && Math.abs(state.reqCapMva - 15.0) < 0.1) matches = true;
          if (p === "datacentre" && state.projectType === "demand" && Math.abs(state.reqCapMva - 25.0) < 0.1) matches = true;
          if (p === "bess_flex" && state.projectType === "storage" && Math.abs(state.reqCapMva - 30.0) < 0.1) matches = true;
          btn.classList.toggle("active", matches);
        }
      });
    }

    function resetFilters() {
      state.licenceArea = "ALL";
      state.geoArea = "ALL";
      state.searchQuery = "";
      state.horizonYear = "2026_LTDS";
      state.subTypeFilter = "ALL";
      state.feasibilityFilter = "ALL";

      document.getElementById("geoSearchInput").value = "";
      document.getElementById("horizonYearSelect").value = "2026_LTDS";
      document.getElementById("subTypeSelect").value = "ALL";
      document.getElementById("licenceBtnAll").classList.add("active");
      document.getElementById("licenceBtnSEPD").classList.remove("active");
      document.getElementById("licenceBtnSHEPD").classList.remove("active");

      setFeasibilityFilter("ALL");
      setProjectType("demand");
      setCapacity(5.0);
      populateGeoAreaOptions();
    }

    /* Shortlist and Compare System */
    function toggleBookmark(subId, event) {
      if (event) event.stopPropagation();
      if (state.shortlist.has(subId)) {
        state.shortlist.delete(subId);
        showToast("Removed from shortlist.");
      } else {
        if (state.shortlist.size >= 4) {
          showToast("Shortlist maximum of 4 substations reached.");
          return;
        }
        state.shortlist.add(subId);
        showToast("Added to shortlist! Open comparison above.");
      }
      updateShortlistUI();
      renderTable();
      if (state.selectedSubId === subId) {
        const ev = currentEvaluated.find(e => e.sub.id === subId);
        if (ev) updateInspector(ev);
      }
    }

    function toggleCurrentBookmark() {
      if (state.selectedSubId) {
        toggleBookmark(state.selectedSubId);
      }
    }

    function updateShortlistUI() {
      const countEl = document.getElementById("navShortlistCount");
      const btnEl = document.getElementById("btnShortlistNav");
      if (countEl) countEl.textContent = state.shortlist.size;
      if (btnEl) btnEl.classList.toggle("has-items", state.shortlist.size > 0);
    }

    function openCompareModal() {
      if (state.shortlist.size === 0) {
        showToast("No substations shortlisted yet. Click '+ Bookmark' on any row.");
        return;
      }

      const body = document.getElementById("compareModalBody");
      const shortlistedSubs = Array.from(state.shortlist).map(id => {
        const s = SUBSTATIONS.find(sub => sub.id === id);
        return s ? evaluateSubstation(s) : null;
      }).filter(Boolean);

      let html = `<div class="compare-grid">`;
      shortlistedSubs.forEach(e => {
        const s = e.sub;
        html += `
          <div class="compare-column">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
              <div>
                <strong style="font-size:14px;color:var(--text-main);">${s.name}</strong>
                <div style="font-size: 12px;color:var(--text-sub);">${s.local_authority} (${s.type})</div>
              </div>
              <button type="button" class="btn-tool" onclick="removeCompareItem('${s.id}')">&times;</button>
            </div>
            
            <div class="compare-cell-title">Feasibility Verdict</div>
            <div><span class="status-badge ${e.status === 'VIABLE' ? 'status-viable' : (e.status === 'CONDITIONAL' ? 'status-conditional' : (e.status === 'INCOMPLETE' ? 'status-incomplete' : 'status-constrained'))}">${e.statusLabel}</span></div>

            <div class="compare-cell-title">Post-Project Margin</div>
            <div class="compare-cell-val" style="color:${(e.postMargin ?? -1) >= 0 ? 'var(--status-green-text)' : 'var(--status-red-text)'};">${e.postMargin != null ? fmtSignedNum(e.postMargin, ' MVA') : 'Not pub.'}</div>

            <div class="compare-cell-title">Available Headroom</div>
            <div class="compare-cell-val">${e.activeHeadroom != null ? fmtNum(e.activeHeadroom, ' MVA') : 'Not pub.'}</div>

            <div class="compare-cell-title">Firm Capacity</div>
            <div class="compare-cell-val">${e.activeFirm != null ? fmtNum(e.activeFirm, ' MVA') : 'Not pub.'}</div>

            <div class="compare-cell-title">Switchgear Margin</div>
            <div class="compare-cell-val">${e.faultMargin != null ? fmtNum(e.faultMargin, ' kA') : 'Safe'}</div>

            <div class="compare-cell-title">Feasibility Score</div>
            <div class="compare-cell-val">${e.score != null ? e.score + ' / 100' : 'Incomplete'}</div>
          </div>
        `;
      });
      html += `</div>`;
      body.innerHTML = html;

      const modal = document.getElementById("compareModal");
      if (modal && typeof modal.showModal === "function") modal.showModal();
    }

    function closeCompareModal() {
      const modal = document.getElementById("compareModal");
      if (modal && typeof modal.close === "function") modal.close();
    }

    function removeCompareItem(id) {
      state.shortlist.delete(id);
      updateShortlistUI();
      renderTable();
      if (state.shortlist.size === 0) {
        closeCompareModal();
      } else {
        openCompareModal();
      }
    }

    function clearShortlist() {
      state.shortlist.clear();
      updateShortlistUI();
      renderTable();
      closeCompareModal();
      showToast("Shortlist cleared.");
    }

    /* Export CSV & Share Link */
    function exportCSV(useShortlistOnly = false) {
      const targets = useShortlistOnly && state.shortlist.size > 0
        ? Array.from(state.shortlist).map(id => {
            const s = SUBSTATIONS.find(sub => sub.id === id);
            return s ? evaluateSubstation(s) : null;
          }).filter(Boolean)
        : currentEvaluated;

      if (targets.length === 0) {
        showToast("No substations to export.");
        return;
      }

      const rows = [
        ["Substation Name", "Type", "Area", "Local Authority", "Voltage", "Firm Capacity (MVA)", "Peak Demand (MVA)", "Available Headroom (MVA)", "Post-Project Margin (MVA)", "Switchgear Margin (kA)", "EISD", "Feasibility Status", "Feasibility Score"]
      ];

      targets.forEach(e => {
        const s = e.sub;
        rows.push([
          `"${s.name}"`,
          s.type,
          s.area,
          `"${s.local_authority || ''}"`,
          `"${s.voltage || ''}"`,
          e.activeFirm != null ? e.activeFirm : "Not Published",
          e.activePeak != null ? e.activePeak : "Not Published",
          e.activeHeadroom != null ? e.activeHeadroom : "Not Published",
          e.postMargin != null ? e.postMargin : "Not Published",
          e.faultMargin != null ? e.faultMargin : "Safe",
          s.demand_eisd || s.gen_eisd || "None",
          e.statusLabel,
          e.score != null ? e.score : "Incomplete"
        ]);
      });

      const csvContent = "data:text/csv;charset=utf-8," + rows.map(r => r.join(",")).join("\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `grid_finder_export_${state.projectType}_${state.reqCapMva}MVA.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast("CSV export initiated.");
    }

    function exportShortlistCSV() {
      exportCSV(true);
    }

    function copyShareableLink() {
      const params = new URLSearchParams();
      params.set("type", state.projectType);
      params.set("cap", state.reqCapMva);
      params.set("licence", state.licenceArea);
      params.set("geo", state.geoArea);
      params.set("horizon", state.horizonYear);
      params.set("tier", state.subTypeFilter);
      if (state.selectedSubId) params.set("sub", state.selectedSubId);

      const shareUrl = window.location.origin + window.location.pathname + "#" + params.toString();
      navigator.clipboard.writeText(shareUrl).then(() => {
        showToast("Shareable search link copied to clipboard!");
      }).catch(() => {
        prompt("Copy this search URL:", shareUrl);
      });
    }

    function loadStateFromHash() {
      if (!window.location.hash || window.location.hash.length < 2) return;
      try {
        const hashStr = window.location.hash.substring(1);
        const params = new URLSearchParams(hashStr);
        if (params.has("type")) state.projectType = params.get("type");
        if (params.has("cap")) state.reqCapMva = parseFloat(params.get("cap"));
        if (params.has("licence")) state.licenceArea = params.get("licence");
        if (params.has("geo")) state.geoArea = params.get("geo");
        if (params.has("horizon")) state.horizonYear = params.get("horizon");
        if (params.has("tier")) state.subTypeFilter = params.get("tier");
        if (params.has("sub")) state.selectedSubId = params.get("sub");
      } catch (e) {}
    }

    /* Modal Dialog Controls */
    function openTermsModal(tab) {
      const m = document.getElementById("termsModal");
      if (m && typeof m.showModal === "function") m.showModal();
    }

    function closeTermsModal() {
      const m = document.getElementById("termsModal");
      if (m && typeof m.close === "function") m.close();
    }

    const termsModalNode = document.getElementById("termsModal");
    if (termsModalNode) {
      termsModalNode.addEventListener("click", e => {
        if (e.target === termsModalNode) termsModalNode.close();
      });
    }

    const compareModalNode = document.getElementById("compareModal");
    if (compareModalNode) {
      compareModalNode.addEventListener("click", e => {
        if (e.target === compareModalNode) compareModalNode.close();
      });
    }

    /* Toast Notification */
    let toastTimer = null;
    function showToast(msg) {
      const toast = document.getElementById("portalToast");
      const txt = document.getElementById("toastText");
      if (!toast || !txt) return;
      txt.textContent = msg;
      toast.classList.add("show");
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove("show"), 3200);
    }

    /* Live Data Refresh & Sync */
    async function syncLatestData(manual = false) {
      const btn = document.getElementById("syncBtn");
      const label = document.getElementById("syncStatusLabel");
      if (label) label.textContent = "Syncing...";
      if (btn) btn.disabled = true;

      let updated = false;
      const paths = [
        "./site_finder_bundle_2026.json?t=" + Date.now(),
        "./scratch/site_finder_bundle_2026.json?t=" + Date.now()
      ];

      for (const p of paths) {
        try {
          const res = await fetch(p, { cache: "no-store" });
          if (res.ok) {
            const fresh = await res.json();
            if (fresh && fresh.substations && fresh.substations.length > 0) {
              SUBSTATIONS = fresh.substations;
              populateGeoAreaOptions();
              runSiteFinder();
              if (label) label.textContent = "Data Synced";
              if (manual) showToast("Live refresh: 981 substations reloaded from latest bundle.");
              updated = true;
              break;
            }
          }
        } catch (e) {}
      }

      if (!updated) {
        runSiteFinder();
        if (label) label.textContent = "Data Synced";
        if (manual) showToast("Verified data bundle active.");
      }

      if (btn) btn.disabled = false;
    }

    /* Initialize Application */
    
    /* ---------------------------------------------------------------------- */
    /* FRONT PAGE INTAKE CONTROLLER LOGIC                                      */
    /* ---------------------------------------------------------------------- */
    const intakeState = {
      preset: "ev_hub",
      projectType: "demand",
      capacity: 5.0,
      licenceArea: "ALL",
      geoArea: "ALL",
      searchQuery: ""
    };

    const ARCHETYPE_CONFIG = {
      ev_hub: {
        type: "demand",
        cap: 5.0,
        tip: "5.0 MVA provides ~5,000 kVA, suitable for ~25x 150kW ultra-rapid chargers or an electrified commercial bus depot."
      },
      solar_gen: {
        type: "generation",
        cap: 15.0,
        tip: "15.0 MVA provides ~15MW export capacity, suitable for a 40–60 acre utility solar farm generating ~14GWh/year."
      },
      bess_flex: {
        type: "storage",
        cap: 30.0,
        tip: "30.0 MVA battery energy storage (BESS) requires co-located import charging capacity and export discharging capacity."
      },
      datacentre: {
        type: "demand",
        cap: 25.0,
        tip: "25.0 MVA provides high-density firm dual-circuit supply for hyperscale compute, AI processing, and edge facilities."
      },
      industrial: {
        type: "demand",
        cap: 10.0,
        tip: "10.0 MVA provides heavy manufacturing, refrigerated logistics, and electrified process heating capacity."
      },
      custom: {
        type: "demand",
        cap: 5.0,
        tip: "Specify custom import, export, or storage capacities across your desired network tiers."
      }
    };

    function selectIntakePreset(code) {
      intakeState.preset = code;
      const config = ARCHETYPE_CONFIG[code] || ARCHETYPE_CONFIG.ev_hub;
      intakeState.projectType = config.type;
      
      // Update UI buttons across both selector classes
      document.querySelectorAll(".archetype-pill, .intake-archetype-card").forEach(c => {
        const isMatch = c.getAttribute("data-intake-preset") === code;
        c.classList.toggle("is-selected", isMatch);
      });

      if (code !== "custom") {
        setIntakeCapacity(config.cap);
      }
      const guidance = document.getElementById("intakeGuidanceText");
      if (guidance) guidance.textContent = config.tip;
      updateIntakeCandidateCount();
    }

    function setIntakeCapacity(cap) {
      intakeState.capacity = cap;
      document.getElementById("intakeCapInput").value = cap.toFixed(1);
      document.getElementById("intakeCapSlider").value = capToSlider(cap);
      
      // Update quick size pills
      document.querySelectorAll(".intake-quick-pills .cap-pill").forEach(pill => {
        const raw = pill.textContent.replace("MVA", "").replace("M", "").trim();
        const pVal = parseFloat(raw);
        pill.classList.toggle("active", !isNaN(pVal) && Math.abs(pVal - cap) < 0.2);
      });

      updateIntakeCandidateCount();
    }

    function onIntakeCapInputChange(val) {
      let cap = parseFloat(val);
      if (isNaN(cap) || cap < 0.5) cap = 0.5;
      if (cap > 100.0) cap = 100.0;
      intakeState.capacity = cap;
      document.getElementById("intakeCapSlider").value = capToSlider(cap);
      updateIntakeCandidateCount();
    }

    function onIntakeSliderChange(sliderVal) {
      const cap = sliderToCap(parseFloat(sliderVal));
      intakeState.capacity = cap;
      document.getElementById("intakeCapInput").value = cap.toFixed(1);
      updateIntakeCandidateCount();
    }

    function setIntakeRegion(area) {
      intakeState.licenceArea = area;
      intakeState.geoArea = "ALL";

      document.getElementById("intakeRegionAll").classList.toggle("active", area === "ALL");
      document.getElementById("intakeRegionSEPD").classList.toggle("active", area === "SEPD");
      document.getElementById("intakeRegionSHEPD").classList.toggle("active", area === "SHEPD");

      populateIntakeCouncils();
      updateIntakeCandidateCount();
    }

    function populateIntakeCouncils() {
      const select = document.getElementById("intakeGeoAreaSelect");
      if (!select) return;
      select.innerHTML = '<option value="ALL">All Local Authorities in Selected Area</option>';

      let filteredSubs = SUBSTATIONS;
      if (intakeState.licenceArea !== "ALL") {
        filteredSubs = SUBSTATIONS.filter(s => s.area === intakeState.licenceArea);
      }

      const councils = Array.from(new Set(filteredSubs.map(s => s.local_authority).filter(Boolean))).sort();
      councils.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        select.appendChild(opt);
      });
    }

    function onIntakeGeoAreaChange() {
      const sel = document.getElementById("intakeGeoAreaSelect").value;
      intakeState.geoArea = sel;
      if (sel !== "ALL") {
        const sample = SUBSTATIONS.find(s => s.local_authority === sel);
        if (sample && sample.area) {
          intakeState.licenceArea = sample.area;
          document.getElementById("intakeRegionAll").classList.toggle("active", intakeState.licenceArea === "ALL");
          document.getElementById("intakeRegionSEPD").classList.toggle("active", intakeState.licenceArea === "SEPD");
          document.getElementById("intakeRegionSHEPD").classList.toggle("active", intakeState.licenceArea === "SHEPD");
        }
      }
      updateIntakeCandidateCount();
    }

    function updateIntakeCandidateCount() {
      const searchQ = (document.getElementById("intakeSearchInput").value || "").trim().toLowerCase();
      let matchCount = 0;

      for (let i = 0; i < SUBSTATIONS.length; i++) {
        const s = SUBSTATIONS[i];
        if (intakeState.licenceArea !== "ALL" && s.area !== intakeState.licenceArea) continue;
        if (intakeState.geoArea !== "ALL" && s.local_authority !== intakeState.geoArea) continue;
        if (searchQ) {
          const match = (s.name && s.name.toLowerCase().includes(searchQ)) ||
                        (s.local_authority && s.local_authority.toLowerCase().includes(searchQ));
          if (!match) continue;
        }
        matchCount++;
      }

      const countEl = document.getElementById("intakeCandidateCount");
      if (countEl) {
        countEl.textContent = `Screening ${matchCount} SSEN distribution assets`;
      }
    }

    function launchDashboardFromIntake(skipToAll = false) {
      if (!skipToAll) {
        // Transfer intake state into dashboard state
        state.projectType = intakeState.projectType;
        state.reqCapMva = intakeState.capacity;
        state.licenceArea = intakeState.licenceArea;
        state.geoArea = intakeState.geoArea;
        state.searchQuery = (document.getElementById("intakeSearchInput").value || "").trim();

        // Sync dashboard ribbon controls
        document.getElementById("reqCapInput").value = state.reqCapMva.toFixed(1);
        document.getElementById("reqCapSlider").value = capToSlider(state.reqCapMva);
        updateCapacityPillUI(state.reqCapMva);

        document.getElementById("btnTypeDemand").classList.toggle("active", state.projectType === "demand");
        document.getElementById("btnTypeGen").classList.toggle("active", state.projectType === "generation");
        document.getElementById("btnTypeBess").classList.toggle("active", state.projectType === "storage");

        document.getElementById("licenceBtnAll").classList.toggle("active", state.licenceArea === "ALL");
        document.getElementById("licenceBtnSEPD").classList.toggle("active", state.licenceArea === "SEPD");
        document.getElementById("licenceBtnSHEPD").classList.toggle("active", state.licenceArea === "SHEPD");

        populateGeoAreaOptions();
        document.getElementById("geoAreaSelect").value = state.geoArea;
        document.getElementById("geoSearchInput").value = state.searchQuery;

        syncActivePresetUI(intakeState.preset);
      }

      // Hide Intake View and Show Dashboard
      document.getElementById("intakeView").style.display = "none";
      document.getElementById("dashboardView").style.display = "block";
      document.getElementById("btnBackToIntake").style.display = "inline-flex";

      // Force synchronous layout recalculation so #realMapNode has valid non-zero dimensions
      const mapNode = document.getElementById("realMapNode");
      if (mapNode) {
        void mapNode.offsetWidth;
        void mapNode.offsetHeight;
      }

      // Initialize map on visible container if not yet created, or invalidate size
      if (!leafletMap) {
        initMap();
      } else {
        leafletMap.invalidateSize({ animate: false });
      }

      // Refresh candidate evaluation and table/markers
      runSiteFinder();

      // Fit map bounds to filtered set of substations once layout is fully painted
      setTimeout(() => {
        if (leafletMap) {
          leafletMap.invalidateSize({ animate: false });
          const validLatLngs = currentEvaluated
            .filter(e => e.sub.lat != null && e.sub.lon != null)
            .map(e => [e.sub.lat, e.sub.lon]);

          if (validLatLngs.length > 1) {
            leafletMap.fitBounds(L.latLngBounds(validLatLngs), { padding: [35, 35], maxZoom: 12 });
          } else if (validLatLngs.length === 1) {
            leafletMap.setView(validLatLngs[0], 12);
          }
        }
      }, 120);

      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function showIntakeView() {
      document.getElementById("dashboardView").style.display = "none";
      document.getElementById("intakeView").style.display = "block";
      document.getElementById("btnBackToIntake").style.display = "none";
      populateIntakeCouncils();
      updateIntakeCandidateCount();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function initPortal() {
      populateGeoAreaOptions();
      populateIntakeCouncils();
      updateShortlistUI();
      syncLatestData(false);

      // If URL has direct parameters (e.g. from share link #type=...), launch dashboard directly
      if (window.location.hash && window.location.hash.length > 2) {
        loadStateFromHash();
        launchDashboardFromIntake();
      } else {
        // Fresh visit: Show Front Page Intake Screen
        showIntakeView();
      }
    }

    window.addEventListener("DOMContentLoaded", initPortal);
  </script>
</body>
</html>
"""

final_html = html_content.replace("__PORTAL_DATA_JSON__", data_json_str)

with open(OUT_HTML, "w") as f:
    f.write(final_html)

print(f"Generated comprehensive V2 portal successfully: {OUT_HTML} ({len(final_html) // 1024} KB)")
