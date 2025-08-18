#!/usr/bin/env python3
"""
Update existing campaigns with Tune tracking IDs (offer_id, aff_id)
This adds the missing tracking fields to campaigns already in the database
"""

import requests
import json
import re

# API endpoint
API_BASE = "https://mode-dash-production.up.railway.app/api"

# Extract tracking IDs from Tune URLs
def extract_tracking_ids(tune_url):
    """Extract offer_id and aff_id from Tune URL"""
    offer_match = re.search(r'offer_id=(\d+)', tune_url)
    aff_match = re.search(r'aff_id=(\d+)', tune_url)
    
    offer_id = offer_match.group(1) if offer_match else ""
    aff_id = aff_match.group(1) if aff_match else ""
    
    return offer_id, aff_id

def update_campaign_tracking():
    """Update all campaigns with tracking IDs extracted from their Tune URLs"""
    try:
        # Get all campaigns
        print("🔍 Fetching existing campaigns...")
        response = requests.get(f"{API_BASE}/campaigns")
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch campaigns: {response.status_code}")
            return
        
        campaigns = response.json()
        print(f"📋 Found {len(campaigns)} campaigns to update")
        
        updated_count = 0
        
        for campaign in campaigns:
            campaign_id = campaign['id']
            tune_url = campaign['tune_url']
            name = campaign['name']
            
            # Extract tracking IDs
            offer_id, aff_id = extract_tracking_ids(tune_url)
            
            if not offer_id or not aff_id:
                print(f"⚠️  {name}: Missing tracking IDs in URL {tune_url}")
                continue
            
            print(f"🔧 Updating {name}: offer_id={offer_id}, aff_id={aff_id}")
            
            # Update campaign via API (we'll call the database directly)
            # Note: This is a simplified update - in a full system we'd use the API
            import sqlite3
            
            # Direct database update (simpler for this script)
            conn = sqlite3.connect('popup_campaigns.db')
            try:
                conn.execute("""
                    UPDATE campaigns 
                    SET offer_id = ?, aff_id = ? 
                    WHERE id = ?
                """, (offer_id, aff_id, campaign_id))
                conn.commit()
                print(f"✅ Updated {name} successfully")
                updated_count += 1
            except Exception as e:
                print(f"❌ Failed to update {name}: {str(e)}")
            finally:
                conn.close()
        
        print(f"\n🎉 COMPLETE! Updated {updated_count}/{len(campaigns)} campaigns")
        
        if updated_count > 0:
            print("\n🎯 IMPRESSION PIXEL TESTING:")
            print("You can now test impression pixels at:")
            for campaign in campaigns:
                if campaign['id'] <= updated_count + 2:  # Rough estimate
                    offer_id, aff_id = extract_tracking_ids(campaign['tune_url'])
                    if offer_id and aff_id:
                        print(f"   • {campaign['name']}: https://mode-dash-production.up.railway.app/api/campaigns/{campaign['id']}/impression-pixel")
                        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    update_campaign_tracking() 