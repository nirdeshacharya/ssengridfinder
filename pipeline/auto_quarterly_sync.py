#!/usr/bin/env python3
"""
SSEN Automated Sync Runner
Orchestrates the entire update pipeline:
1. Queries SSEN CKAN API for updates
2. Re-extracts & validates substation data
3. Rebuilds index.html
Can be run on-demand or scheduled via cron.
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def run_step(cmd_desc, script_name):
    print(f"\n========================================================")
    print(f"▶ {cmd_desc}...")
    print(f"========================================================")
    script_path = os.path.join(SCRIPT_DIR, script_name)
    res = subprocess.run([sys.executable, script_path], cwd=PROJECT_ROOT)
    if res.returncode != 0:
        print(f"❌ Error executing {script_name} (exit code {res.returncode})")
        sys.exit(res.returncode)
    print(f"✓ {cmd_desc} completed successfully.")

def main():
    print("Starting Automated SSEN Grid Connection Sync...")
    run_step("1/3 Checking SSEN CKAN API for new releases", "fetch_ssen_live_updates.py")
    run_step("2/3 Processing Substation Datasets & Engineering Metrics", "build_site_finder_data.py")
    run_step("3/3 Rebuilding Web Portal Application (index.html)", "build_comprehensive_v2_portal.py")
    print("\n🎉 Full quarterly sync completed successfully!")
    print(f"Updated application ready at: {os.path.join(PROJECT_ROOT, 'index.html')}")

if __name__ == "__main__":
    main()
