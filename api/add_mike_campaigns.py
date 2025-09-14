"""
Script to add Mike's real Tune campaigns to the database
"""
import requests
import json

# API base URL
BASE_URL = "https://mode-dash-production.up.railway.app/api"

# Mike's campaigns data
campaigns = [
    {
        "name": "Trading Tips",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/TradingTipsbanner.jpg",
        "main_image_url": "/static/img/financepopupoffers/TradingTipsbanner.jpg",
        "description": "Expert trading tips and market insights for smart investors"
    },
    {
        "name": "Behind The Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/300x250ElonAI (1).png",
        "main_image_url": "/static/img/financepopupoffers/300x250ElonAI (1).png",
        "description": "Uncover what's really happening behind the markets with Elon's insights"
    },
    {
        "name": "Brownstone Research",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/BrownstoneV2.png",
        "main_image_url": "/static/img/financepopupoffers/BrownstoneV2.png",
        "description": "Independent research and investment insights from Brownstone"
    },
    {
        "name": "Hot Sheets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/HotsheetV2.png",
        "main_image_url": "/static/img/financepopupoffers/HotsheetV2.png",
        "description": "Get the hottest stock picks and market opportunities"
    },
    {
        "name": "Best Gold Investment",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/Gold300250.png",
        "main_image_url": "/static/img/financepopupoffers/Gold300250.png",
        "description": "Smart gold investment strategies for wealth protection"
    },
    {
        "name": "Beat The Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7601&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/GuyStock_banners_01_300x250.png",
        "main_image_url": "/static/img/financepopupoffers/GuyStock_banners_01_300x250.png",
        "description": "Professional strategies to consistently beat the market"
    }
]

def add_campaigns():
    """Add all campaigns to the database via API"""
    for campaign in campaigns:
        try:
            response = requests.post(f"{BASE_URL}/campaigns", json=campaign)
            if response.status_code == 200:
                print(f"✅ Added: {campaign['name']}")
            else:
                print(f"❌ Failed to add {campaign['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Error adding {campaign['name']}: {e}")

if __name__ == "__main__":
    print("Adding Mike's campaigns to the database...")
    add_campaigns()
    print("Done!") 