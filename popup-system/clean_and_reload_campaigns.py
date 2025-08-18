#!/usr/bin/env python3
"""
Clean existing campaigns and reload Mike's 6 real campaigns with tracking IDs
"""

import requests
import json

# API endpoint
API_BASE = "https://mode-dash-production.up.railway.app/api"

def clean_existing_campaigns():
    """Delete all existing campaigns"""
    try:
        print("🧹 Fetching existing campaigns to clean...")
        response = requests.get(f"{API_BASE}/campaigns")
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch campaigns: {response.status_code}")
            return False
        
        campaigns = response.json()
        print(f"📋 Found {len(campaigns)} campaigns to delete")
        
        for campaign in campaigns:
            campaign_id = campaign['id']
            name = campaign['name']
            
            print(f"🗑️  Deleting: {name} (ID: {campaign_id})")
            delete_response = requests.delete(f"{API_BASE}/campaigns/{campaign_id}")
            
            if delete_response.status_code == 200:
                print(f"✅ Deleted {name}")
            else:
                print(f"⚠️  Failed to delete {name}: {delete_response.status_code}")
        
        print("🎉 Cleanup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during cleanup: {str(e)}")
        return False

def add_mike_campaigns():
    """Add Mike's campaigns with tracking IDs"""
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
    
    print("\n🚀 Adding Mike's 6 Real Tune Campaigns with Tracking IDs")
    print("=" * 60)
    
    success_count = 0
    
    for campaign_data in campaigns:
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
            print(f"🚀 Adding campaign: {campaign_data['name']} (offer_id: {campaign_data['offer_id']})")
            response = requests.post(f"{API_BASE}/campaigns", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Campaign ID: {result.get('id')}")
                success_count += 1
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error adding {campaign_data['name']}: {str(e)}")
        
        print("-" * 40)
    
    print(f"\n🎉 COMPLETE! Added {success_count}/{len(campaigns)} campaigns successfully")
    return success_count

def main():
    print("🎯 Mode Popup System - Clean & Reload Campaigns")
    print("=" * 50)
    
    # Step 1: Clean existing campaigns
    if clean_existing_campaigns():
        print("\n" + "="*50)
        
        # Step 2: Add Mike's campaigns with tracking
        success_count = add_mike_campaigns()
        
        if success_count > 0:
            print("\n🎯 IMPRESSION PIXEL TESTING:")
            print("Test impression pixels at:")
            campaigns = [
                ("Trading Tips", "6998", "43045"),
                ("Behind The Markets", "7521", "43045"),
                ("Brownstone", "7389", "43045"),
                ("Hotsheets", "7385", "43045"),
                ("Best Gold", "7390", "43045"),
                ("Beat the Markets", "7601", "43045")
            ]
            
            for i, (name, offer_id, aff_id) in enumerate(campaigns, 1):
                if i <= success_count:
                    print(f"   • {name}: {API_BASE}/campaigns/{i+8}/impression-pixel")
                    print(f"     Direct: https://track.modemobile.com/aff_i?offer_id={offer_id}&aff_id={aff_id}")
            
            print(f"\n📝 NEXT: Open admin dashboard to add images!")
            print(f"🖼️  Dashboard: {API_BASE.replace('/api', '/admin')}")

if __name__ == "__main__":
    main() 