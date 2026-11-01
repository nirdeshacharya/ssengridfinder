#!/usr/bin/env python3
"""
SSEN Open Data CKAN API Query & Update Check
Connects directly to SSEN's official CKAN Open Data Portal API (https://ckan-prod.sse.datopian.com)
to discover and verify published grid capacity datasets, maps, and LTDS updates.
"""

import json
import os
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

TARGET_PACKAGES = [
    "generation-and-network-availability-maps",
    "generation-availability-and-network-capacity",
    "grid-supply-point-gsp-bulk-supply-point-bsp-electricity-supply-area-datasets",
    "embedded_capacity_register",
    "low-carbon-technology-connections"
]

def check_ssen_portal():
    print("Connecting to SSEN Open Data Portal API (https://ckan-prod.sse.datopian.com)...")
    for pkg in TARGET_PACKAGES:
        url = f"https://ckan-prod.sse.datopian.com/api/3/action/package_show?id={pkg}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                if data.get("success"):
                    res = data["result"]
                    title = res.get("title", pkg)
                    modified = res.get("metadata_modified", "Unknown")[:10]
                    resources = res.get("resources", [])
                    print(f"\n[SSEN Official] {title}")
                    print(f"  Modified: {modified} | Resources: {len(resources)}")
                    for r in resources[:2]:
                        r_name = r.get("name") or r.get("description") or "File"
                        r_fmt = r.get("format", "")
                        r_url = r.get("url", "")
                        print(f"   ↳ {r_name} ({r_fmt}): {r_url[:80]}...")
        except Exception as e:
            print(f"Error checking {pkg}: {e}")

if __name__ == "__main__":
    check_ssen_portal()
