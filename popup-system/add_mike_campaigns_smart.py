#!/usr/bin/env python3
"""
Smart Campaign Addition Script
Adds Mike's 6 real Tune campaigns only if they don't already exist.
"""

import requests
import json
import sys

# API Configuration
BASE_URL = "https://mode-dash-production.up.railway.app/api"

# Mike's Real Campaign Data (with tracking IDs extracted from URLs)
MIKE_CAMPAIGNS = [
    {
        "name": "Trading Tips",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045",
        "logo_url": "https://financepopupoffers.s3.amazonaws.com/logos/trading-tips-logo.png",
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/trading-tips-main.jpg",
        "description": "Get exclusive trading tips and market insights delivered daily to your inbox.",
        "cta_text": "Get Trading Tips",
        "offer_id": "6998",
        "aff_id": "43045"
    },
    {
        "name": "Behind The Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045",
        "logo_url": "https://financepopupoffers.s3.amazonaws.com/logos/behind-markets-logo.png",
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/behind-markets-main.jpg",
        "description": "Discover what's really happening behind the financial markets with expert analysis.",
        "cta_text": "Learn More",
        "offer_id": "7521",
        "aff_id": "43045"
    },
    {
        "name": "Brownstone Research",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045",
        "logo_url": "https://financepopupoffers.s3.amazonaws.com/logos/brownstone-logo.png",
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/brownstone-main.jpg",
        "description": "Advanced technology and investment research from Brownstone Research experts.",
        "cta_text": "View Research",
        "offer_id": "7389",
        "aff_id": "43045"
    },
    {
        "name": "Hotsheets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045",
        "logo_url": "https://financepopupoffers.s3.amazonaws.com/logos/hotsheets-logo.png",
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/hotsheets-main.jpg",
        "description": "Daily market hotsheets with the most profitable trading opportunities.",
        "cta_text": "Get Hotsheets",
        "offer_id": "7385",
        "aff_id": "43045"
    },
    {
        "name": "Best Gold",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045",
        "logo_url": "https://financepopupoffers.s3.amazonaws.com/logos/best-gold-logo.png",
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/best-gold-main.jpg",
        "description": "Premium gold investment insights and recommendations from industry experts.",
        "cta_text": "Learn About Gold",
        "offer_id": "7390",
        "aff_id": "43045"
    },
    {
        "name": "Beat the Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7601&aff_id=43045",
        "logo_url": "https://financepopupoffers.s3.amazonaws.com/logos/beat-markets-logo.png",
        "main_image_url": "https://financepopupoffers.s3.amazonaws.com/main/beat-markets-main.jpg",
        "description": "Proven strategies to consistently beat the markets and maximize your returns.",
        "cta_text": "Beat Markets",
        "offer_id": "7601",
        "aff_id": "43045"
    }
]

def get_existing_campaigns():
    """Get all existing campaigns from the API."""
    try:
        response = requests.get(f"{BASE_URL}/campaigns")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching existing campaigns: {e}")
        return []

def campaign_exists(campaign_data, existing_campaigns):
    """Check if a campaign already exists based on offer_id or name."""
    for existing in existing_campaigns:
        # Check by offer_id (most reliable)
        if (campaign_data.get("offer_id") and 
            existing.get("offer_id") == campaign_data["offer_id"]):
            return True
        
        # Check by name (fallback)
        if existing.get("name") == campaign_data["name"]:
            return True
    
    return False

def add_campaign(campaign_data):
    """Add a new campaign via the API."""
    try:
        response = requests.post(f"{BASE_URL}/campaigns", json=campaign_data)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Added campaign: {campaign_data['name']} (ID: {result.get('id')})")
        return True
    except Exception as e:
        print(f"❌ Failed to add {campaign_data['name']}: {e}")
        return False

def main():
    """Main function to smartly add Mike's campaigns."""
    print("🚀 Smart Campaign Addition - Mike's Real Tune Campaigns")
    print("=" * 60)
    
    # Get existing campaigns
    print("📋 Checking existing campaigns...")
    existing_campaigns = get_existing_campaigns()
    print(f"Found {len(existing_campaigns)} existing campaigns")
    
    # Process each of Mike's campaigns
    added_count = 0
    skipped_count = 0
    
    for campaign in MIKE_CAMPAIGNS:
        print(f"\n🔍 Processing: {campaign['name']}")
        
        if campaign_exists(campaign, existing_campaigns):
            print(f"⏭️  SKIPPED - {campaign['name']} already exists")
            skipped_count += 1
        else:
            if add_campaign(campaign):
                added_count += 1
            
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"✅ Added: {added_count} campaigns")
    print(f"⏭️  Skipped: {skipped_count} campaigns (already exist)")
    print(f"📋 Total Mike's campaigns: {len(MIKE_CAMPAIGNS)}")
    
    if added_count > 0:
        print(f"\n🎉 SUCCESS! {added_count} new campaigns added to the dashboard!")
        print("🔗 View them at: https://mode-dash-production.up.railway.app/admin")
    else:
        print(f"\n✨ All of Mike's campaigns are already in the system!")

if __name__ == "__main__":
    main() 