#!/usr/bin/env python3
"""
Read-only backup of production campaign configuration via public API.
Captures: campaigns, properties schema/data, featured per property, and
campaign lists per property. Does NOT modify production.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://mode-dash-production.up.railway.app"

def get(path: str, params: dict | None = None):
    url = f"{BASE_URL}{path}"
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(__file__).resolve().parents[1] / "backups"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"remote_config_backup_{timestamp}.json"

    snapshot: dict = {
        "backup_timestamp": timestamp,
        "base_url": BASE_URL,
        "properties": {},
    }

    # Campaigns (all)
    snapshot["campaigns_all"] = get("/api/campaigns")

    # Properties schema + full table
    try:
        snapshot["properties_schema"] = get("/api/db/properties-schema")
    except Exception as e:
        snapshot["properties_schema_error"] = str(e)

    # Per property featured + campaigns
    for code in ["mff", "mmm", "mcad", "mmd"]:
        try:
            featured = get(f"/api/properties/{code}/featured")
        except Exception as e:
            featured = {"error": str(e)}
        try:
            campaigns = get(f"/api/properties/{code}/campaigns")
        except Exception as e:
            campaigns = {"error": str(e)}
        snapshot["properties"][code] = {
            "featured": featured,
            "campaigns": campaigns,
        }

    with open(out_file, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"✅ Remote config backup saved: {out_file}")

if __name__ == "__main__":
    main()


