#!/usr/bin/env python3
"""
REAL CAMPAIGN IMAGES - MIKE'S EXACT CREATIVES
Emergency update for meeting
"""

import requests
import json

# API Configuration
BASE_URL = "https://mode-dash-production.up.railway.app/api"

# MIKE'S REAL CAMPAIGN IMAGES
CAMPAIGN_IMAGES = {
    "Trading Tips": {
        "logo_url": "https://i.imgur.com/lHn301q.png",
        "main_image_url": "https://i.imgur.com/ZVGOktR.png"
    },
    "Behind The Markets": {
        "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", 
        "main_image_url": "https://i.imgur.com/NA0o7iJ.png"
    },
    "Brownstone Research": {
        "logo_url": "https://i.imgur.com/lHn301q.png",  # Use trading tips logo for now
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/BrownstoneV2.png"
    },
    "Best Gold": {
        "logo_url": "https://i.imgur.com/lHn301q.png",  # Use trading tips logo for now
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/Gold300250.png"
    },
    "Beat the Markets": {
        "logo_url": "https://i.imgur.com/lHn301q.png",  # Use trading tips logo for now
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/GuyStock_banners_01_300x250.png"
    },
    "Hotsheets": {
        "logo_url": "https://i.imgur.com/lHn301q.png",  # Use trading tips logo for now
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/HotsheetV2.png"
    }
}

def get_campaigns():
    """Get all campaigns"""
    try:
        response = requests.get(f"{BASE_URL}/campaigns")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting campaigns: {e}")
        return []

def update_campaign_images(campaign_id, images):
    """Update campaign with images"""
    try:
        response = requests.put(f"{BASE_URL}/campaigns/{campaign_id}", json=images)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to update campaign {campaign_id}: {e}")
        return False

def main():
    print("🚨 REAL CAMPAIGN IMAGES UPDATE")
    print("=" * 50)
    
    campaigns = get_campaigns()
    if not campaigns:
        print("❌ No campaigns found!")
        return
    
    updated_count = 0
    
    for campaign in campaigns:
        name = campaign.get('name')
        campaign_id = campaign.get('id')
        
        if name in CAMPAIGN_IMAGES:
            print(f"🎯 Updating {name} with REAL images...")
            
            if update_campaign_images(campaign_id, CAMPAIGN_IMAGES[name]):
                print(f"✅ {name} - REAL IMAGES ADDED")
                updated_count += 1
            else:
                print(f"❌ Failed {name}")
        else:
            print(f"⏭️  Skipping {name}")
    
    print("=" * 50)
    print(f"🎉 REAL IMAGES COMPLETE! Updated {updated_count} campaigns")
    print("🔗 Check: https://mode-dash-production.up.railway.app/admin")
    
    if updated_count > 0:
        print("🚀 MEETING READY WITH REAL CREATIVES!")

if __name__ == "__main__":
    main() 