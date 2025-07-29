#!/usr/bin/env python3
"""
Hard delete inactive campaigns using the new hard-delete endpoint
This permanently removes campaigns IDs 1-8 from the database
"""

import requests
import json
import time

# API endpoint
API_BASE = "https://mode-dash-production.up.railway.app/api"

def hard_delete_inactive_campaigns():
    """Permanently delete all inactive campaigns"""
    try:
        print("🧹 Fetching all campaigns...")
        response = requests.get(f"{API_BASE}/campaigns")
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch campaigns: {response.status_code}")
            return False
        
        campaigns = response.json()
        
        # Filter for inactive campaigns
        inactive_campaigns = [c for c in campaigns if not c.get('active', True)]
        active_campaigns = [c for c in campaigns if c.get('active', True)]
        
        print(f"📊 Status:")
        print(f"   ✅ Active campaigns: {len(active_campaigns)}")
        print(f"   🗑️  Inactive campaigns: {len(inactive_campaigns)}")
        
        if not inactive_campaigns:
            print("✅ No inactive campaigns found!")
            return True
        
        print(f"\n🗑️  INACTIVE CAMPAIGNS TO PERMANENTLY DELETE:")
        for campaign in inactive_campaigns:
            print(f"   ❌ ID {campaign['id']}: {campaign['name']}")
        
        print(f"\n🚀 Hard deleting {len(inactive_campaigns)} inactive campaigns...")
        
        deleted_count = 0
        
        for campaign in inactive_campaigns:
            campaign_id = campaign['id']
            name = campaign['name']
            
            print(f"🗑️  Deleting: {name} (ID: {campaign_id})")
            
            # Use the new hard-delete endpoint
            delete_response = requests.delete(f"{API_BASE}/campaigns/{campaign_id}/hard-delete")
            
            if delete_response.status_code == 200:
                print(f"✅ Permanently deleted {name}")
                deleted_count += 1
            else:
                print(f"⚠️  Failed to delete {name}: {delete_response.status_code} - {delete_response.text}")
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.5)
        
        print(f"\n🎉 HARD DELETE COMPLETE! Deleted {deleted_count}/{len(inactive_campaigns)} campaigns")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during hard delete: {str(e)}")
        return False

def verify_cleanup():
    """Verify cleanup was successful"""
    try:
        print("\n🔍 Verifying cleanup...")
        response = requests.get(f"{API_BASE}/campaigns")
        
        if response.status_code != 200:
            print(f"❌ Failed to verify: {response.status_code}")
            return
        
        campaigns = response.json()
        active_campaigns = [c for c in campaigns if c.get('active', True)]
        inactive_campaigns = [c for c in campaigns if not c.get('active', True)]
        
        print(f"📊 Final status:")
        print(f"   ✅ Active campaigns: {len(active_campaigns)}")
        print(f"   ❌ Inactive campaigns: {len(inactive_campaigns)}")
        print(f"   📋 Total campaigns: {len(campaigns)}")
        
        if len(campaigns) == 6 and len(active_campaigns) == 6 and len(inactive_campaigns) == 0:
            print("🎉 PERFECT! Only Mike's 6 active campaigns remain!")
            
            print("\n📋 REMAINING CAMPAIGNS:")
            for campaign in sorted(active_campaigns, key=lambda x: x['id']):
                print(f"   • ID {campaign['id']}: {campaign['name']} (offer_id: {campaign.get('offer_id', 'N/A')})")
                
        else:
            print("⚠️  Check results manually.")
            
            if inactive_campaigns:
                print("\n🗑️  REMAINING INACTIVE CAMPAIGNS:")
                for campaign in inactive_campaigns:
                    print(f"   ❌ ID {campaign['id']}: {campaign['name']}")
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")

def main():
    print("🎯 Mode Popup System - Hard Delete Inactive Campaigns")
    print("=" * 60)
    
    if hard_delete_inactive_campaigns():
        verify_cleanup()
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. 🖼️  Dashboard: https://mode-dash-production.up.railway.app/admin")
        print(f"2. 👀 Test Edit button (should work now)")
        print(f"3. 🎨 Add real images to campaigns")
        print(f"4. 🚀 Test Properties modal")

if __name__ == "__main__":
    main() 