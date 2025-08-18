"""
Manual script to add Mike's campaigns directly to the database
Run this if the dashboard isn't working
"""

import requests
import json

# Railway API URL
BASE_URL = "https://mode-dash-production.up.railway.app/api"

# Mike's real campaigns
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
        "logo_url": "/static/img/financepopupoffers/300x250ElonAI.png",
        "main_image_url": "/static/img/financepopupoffers/300x250ElonAI.png",
        "description": "Uncover what is really happening behind the markets with Elon insights"
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

def add_all_campaigns():
    """Add all campaigns via API"""
    print("🚀 Adding Mike's campaigns to the database...")
    
    for i, campaign in enumerate(campaigns, 1):
        try:
            response = requests.post(f"{BASE_URL}/campaigns", json=campaign)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {i}/6 Added: {campaign['name']} (ID: {result.get('id')})")
            else:
                print(f"❌ {i}/6 Failed to add {campaign['name']}: {response.text}")
        except Exception as e:
            print(f"❌ {i}/6 Error adding {campaign['name']}: {e}")
    
    print("\n📊 Checking final campaign count...")
    try:
        response = requests.get(f"{BASE_URL}/campaigns")
        if response.status_code == 200:
            campaigns_list = response.json()
            print(f"✅ Total campaigns in database: {len(campaigns_list)}")
        else:
            print(f"❌ Failed to check campaigns: {response.text}")
    except Exception as e:
        print(f"❌ Error checking campaigns: {e}")

if __name__ == "__main__":
    add_all_campaigns() 