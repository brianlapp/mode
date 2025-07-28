#!/usr/bin/env python3
"""
Clean database and add Mike's real Tune campaigns
"""

import requests
import json

BASE_URL = "https://mode-dash-production.up.railway.app/api"

# Mike's real campaigns from his email
real_campaigns = [
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
        "description": "Get behind-the-scenes market analysis and investment strategies"
    },
    {
        "name": "Brownstone Research",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/BrownstoneV2.png",
        "main_image_url": "/static/img/financepopupoffers/BrownstoneV2.png",
        "description": "Premium investment research and market intelligence"
    },
    {
        "name": "Hot Sheets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/HotsheetV2.png",
        "main_image_url": "/static/img/financepopupoffers/HotsheetV2.png",
        "description": "Daily hot stock picks and market opportunities"
    },
    {
        "name": "Best Gold Investment",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/Gold300250.png",
        "main_image_url": "/static/img/financepopupoffers/Gold300250.png",
        "description": "Gold investment strategies and precious metals insights"
    },
    {
        "name": "Beat The Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7601&aff_id=43045",
        "logo_url": "/static/img/financepopupoffers/GuyStock_banners_01_300x250.png",
        "main_image_url": "/static/img/financepopupoffers/GuyStock_banners_01_300x250.png",
        "description": "Beat the market with proven investment strategies"
    }
]

def clean_campaigns():
    """Delete all existing campaigns"""
    try:
        # Get all campaigns
        response = requests.get(f"{BASE_URL}/campaigns")
        if response.ok:
            campaigns = response.json()
            print(f"🗑️ Found {len(campaigns)} campaigns to delete...")
            
            # Delete each campaign
            for campaign in campaigns:
                delete_response = requests.delete(f"{BASE_URL}/campaigns/{campaign['id']}")
                if delete_response.ok:
                    print(f"✅ Deleted campaign: {campaign['name']} (ID: {campaign['id']})")
                else:
                    print(f"❌ Failed to delete campaign: {campaign['name']}")
        else:
            print("❌ Failed to fetch campaigns for cleanup")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def add_real_campaigns():
    """Add Mike's real campaigns"""
    print(f"\n🚀 Adding {len(real_campaigns)} real campaigns...")
    
    success_count = 0
    for i, campaign in enumerate(real_campaigns, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/campaigns",
                headers={"Content-Type": "application/json"},
                json=campaign
            )
            
            if response.ok:
                result = response.json()
                print(f"✅ {i}/{len(real_campaigns)} Added: {campaign['name']} (ID: {result.get('id', 'Unknown')})")
                success_count += 1
            else:
                print(f"❌ {i}/{len(real_campaigns)} Failed to add: {campaign['name']} - {response.status_code}")
                
        except Exception as e:
            print(f"❌ {i}/{len(real_campaigns)} Error adding {campaign['name']}: {e}")
    
    return success_count

def verify_campaigns():
    """Verify the final campaign count"""
    try:
        response = requests.get(f"{BASE_URL}/campaigns")
        if response.ok:
            campaigns = response.json()
            print(f"\n📊 Final verification: {len(campaigns)} campaigns in database")
            for campaign in campaigns:
                print(f"   • {campaign['name']} (ID: {campaign['id']})")
            return len(campaigns)
        else:
            print("❌ Failed to verify campaigns")
            return 0
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return 0

if __name__ == "__main__":
    print("🧹 Cleaning up database and adding Mike's real campaigns...")
    
    # Step 1: Clean existing campaigns
    clean_campaigns()
    
    # Step 2: Add real campaigns
    success_count = add_real_campaigns()
    
    # Step 3: Verify
    final_count = verify_campaigns()
    
    print(f"\n🎉 Cleanup complete! Added {success_count} campaigns, final count: {final_count}") 