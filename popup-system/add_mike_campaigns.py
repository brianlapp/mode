#!/usr/bin/env python3
"""
Add Mike's Real Tune Campaigns to the Popup System
This script adds the 6 real campaigns with proper tracking URLs and impression pixels
"""

import requests
import json

# API endpoint
API_BASE = "https://mode-dash-production.up.railway.app/api"

# Mike's real campaigns with proper offer_id and aff_id extraction
campaigns = [
    {
        "name": "Trading Tips",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045",
        "offer_id": "6998",
        "aff_id": "43045",
        "description": "Get exclusive trading tips and market insights from financial experts.",
        "cta_text": "Get Trading Tips"
    },
    {
        "name": "Behind The Markets", 
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045",
        "offer_id": "7521", 
        "aff_id": "43045",
        "description": "Discover what's really happening behind the financial markets.",
        "cta_text": "See Market Secrets"
    },
    {
        "name": "Brownstone",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045", 
        "offer_id": "7389",
        "aff_id": "43045",
        "description": "Premium financial research and investment insights.",
        "cta_text": "Access Research"
    },
    {
        "name": "Hotsheets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045",
        "offer_id": "7385",
        "aff_id": "43045", 
        "description": "Hot stock picks and market opportunities delivered daily.",
        "cta_text": "Get Hot Picks"
    },
    {
        "name": "Best Gold",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045",
        "offer_id": "7390",
        "aff_id": "43045",
        "description": "Gold investment strategies and precious metals insights.",
        "cta_text": "Invest in Gold"
    },
    {
        "name": "Beat the Markets", 
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7601&aff_id=43045",
        "offer_id": "7601",
        "aff_id": "43045",
        "description": "Learn proven strategies to consistently beat market performance.",
        "cta_text": "Beat Markets"
    }
]

def add_campaign(campaign_data):
    """Add a single campaign via API"""
    # Prepare API payload
    payload = {
        "name": campaign_data["name"],
        "tune_url": campaign_data["tune_url"], 
        "logo_url": "https://via.placeholder.com/56/F7007C/FFFFFF?text=" + campaign_data["name"][:2],
        "main_image_url": "https://via.placeholder.com/280x220/F7007C/FFFFFF?text=" + campaign_data["name"].replace(" ", "+"),
        "description": campaign_data["description"],
        "cta_text": campaign_data["cta_text"],
        "offer_id": campaign_data["offer_id"],
        "aff_id": campaign_data["aff_id"]
    }
    
    try:
        print(f"🚀 Adding campaign: {campaign_data['name']}")
        response = requests.post(f"{API_BASE}/campaigns", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Campaign ID: {result.get('id')}")
            
            # Store offer_id and aff_id for impression pixel reference
            campaign_data['api_id'] = result.get('id')
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding {campaign_data['name']}: {str(e)}")
        return False

def main():
    """Add all campaigns"""
    print("🎯 Adding Mike's 6 Real Tune Campaigns to Mode Popup System")
    print("=" * 60)
    
    success_count = 0
    
    for campaign in campaigns:
        if add_campaign(campaign):
            success_count += 1
        print("-" * 40)
    
    print(f"\n🎉 COMPLETE! Added {success_count}/{len(campaigns)} campaigns successfully")
    
    if success_count > 0:
        print("\n📝 NEXT STEPS FOR MIKE:")
        print("1. 🖼️  Open admin dashboard: https://mode-dash-production.up.railway.app/admin")
        print("2. 👁️  Click 'Edit' on any campaign to see live preview")
        print("3. 🎨  Add logo_url and main_image_url using the form")
        print("4. ⚙️  Click 'Properties' to set visibility per site (MFF, MMM, etc.)")
        print("5. 🚀  Ready for popup.js integration on thank you pages!")
        
        print("\n🎯 IMPRESSION PIXEL INFO:")
        print("Each campaign will automatically generate impression pixels like:")
        for campaign in campaigns:
            if 'api_id' in campaign:
                print(f"   • {campaign['name']}: https://track.modemobile.com/aff_i?offer_id={campaign['offer_id']}&aff_id={campaign['aff_id']}")

if __name__ == "__main__":
    main() 