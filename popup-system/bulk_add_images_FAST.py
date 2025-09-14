#!/usr/bin/env python3
"""
EMERGENCY BULK IMAGE UPDATER
Quickly add images to all campaigns for Mike's meeting
"""

import requests
import json

# API Configuration
BASE_URL = "https://mode-dash-production.up.railway.app/api"

# Quick image updates for each campaign
CAMPAIGN_IMAGES = {
    "Trading Tips": {
        "logo_url": "https://via.placeholder.com/56x56/F7007C/FFFFFF?text=TT",
        "main_image_url": "https://via.placeholder.com/280x220/F7007C/FFFFFF?text=Trading+Tips"
    },
    "Behind The Markets": {
        "logo_url": "https://via.placeholder.com/56x56/07C8F7/FFFFFF?text=BM", 
        "main_image_url": "https://via.placeholder.com/280x220/07C8F7/FFFFFF?text=Behind+Markets"
    },
    "Brownstone Research": {
        "logo_url": "https://via.placeholder.com/56x56/8B5CF6/FFFFFF?text=BR",
        "main_image_url": "https://via.placeholder.com/280x220/8B5CF6/FFFFFF?text=Brownstone"
    },
    "Hotsheets": {
        "logo_url": "https://via.placeholder.com/56x56/F59E0B/FFFFFF?text=HS",
        "main_image_url": "https://via.placeholder.com/280x220/F59E0B/FFFFFF?text=Hotsheets"
    },
    "Best Gold": {
        "logo_url": "https://via.placeholder.com/56x56/EAB308/FFFFFF?text=BG",
        "main_image_url": "https://via.placeholder.com/280x220/EAB308/FFFFFF?text=Best+Gold"
    },
    "Beat the Markets": {
        "logo_url": "https://via.placeholder.com/56x56/10B981/FFFFFF?text=BTM",
        "main_image_url": "https://via.placeholder.com/280x220/10B981/FFFFFF?text=Beat+Markets"
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
    print("🚨 EMERGENCY BULK IMAGE UPDATE")
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
            print(f"🖼️  Updating {name} (ID: {campaign_id})...")
            
            if update_campaign_images(campaign_id, CAMPAIGN_IMAGES[name]):
                print(f"✅ Updated {name}")
                updated_count += 1
            else:
                print(f"❌ Failed {name}")
        else:
            print(f"⏭️  Skipping {name} (no images defined)")
    
    print("=" * 50)
    print(f"🎉 COMPLETE! Updated {updated_count} campaigns")
    print("🔗 Check: https://mode-dash-production.up.railway.app/admin")
    
    if updated_count > 0:
        print("🚀 READY FOR YOUR MEETING!")

if __name__ == "__main__":
    main() 