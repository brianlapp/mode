#!/usr/bin/env python3
"""
Clean up inactive campaigns (duplicates from IDs 1-8)
This removes only the inactive campaigns, keeping the active ones
"""

import requests
import json

# API endpoint
API_BASE = "https://mode-dash-production.up.railway.app/api"

def cleanup_inactive_campaigns():
    """Delete all inactive campaigns"""
    try:
        print("🧹 Fetching all campaigns...")
        response = requests.get(f"{API_BASE}/campaigns")
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch campaigns: {response.status_code}")
            return False
        
        campaigns = response.json()
        print(f"📋 Found {len(campaigns)} total campaigns")
        
        # Filter for inactive campaigns
        inactive_campaigns = [c for c in campaigns if not c.get('active', True)]
        active_campaigns = [c for c in campaigns if c.get('active', True)]
        
        print(f"🎯 Active campaigns: {len(active_campaigns)}")
        print(f"🗑️  Inactive campaigns to delete: {len(inactive_campaigns)}")
        
        if not inactive_campaigns:
            print("✅ No inactive campaigns found!")
            return True
        
        print("\n📋 ACTIVE CAMPAIGNS (will keep):")
        for campaign in active_campaigns:
            print(f"   ✅ ID {campaign['id']}: {campaign['name']} (offer_id: {campaign.get('offer_id', 'N/A')})")
        
        print(f"\n🗑️  INACTIVE CAMPAIGNS (will delete):")
        for campaign in inactive_campaigns:
            print(f"   ❌ ID {campaign['id']}: {campaign['name']} (offer_id: {campaign.get('offer_id', 'N/A')})")
        
        print(f"\n🚀 Deleting {len(inactive_campaigns)} inactive campaigns...")
        
        deleted_count = 0
        
        for campaign in inactive_campaigns:
            campaign_id = campaign['id']
            name = campaign['name']
            
            print(f"🗑️  Deleting: {name} (ID: {campaign_id})")
            delete_response = requests.delete(f"{API_BASE}/campaigns/{campaign_id}")
            
            if delete_response.status_code == 200:
                print(f"✅ Deleted {name}")
                deleted_count += 1
            else:
                print(f"⚠️  Failed to delete {name}: {delete_response.status_code}")
        
        print(f"\n🎉 CLEANUP COMPLETE! Deleted {deleted_count}/{len(inactive_campaigns)} inactive campaigns")
        print(f"📊 Remaining active campaigns: {len(active_campaigns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during cleanup: {str(e)}")
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
        
        if len(active_campaigns) == 6 and len(inactive_campaigns) == 0:
            print("🎉 PERFECT! Only Mike's 6 active campaigns remain!")
            
            print("\n📋 REMAINING CAMPAIGNS:")
            for campaign in sorted(active_campaigns, key=lambda x: x['id']):
                print(f"   • ID {campaign['id']}: {campaign['name']} (offer_id: {campaign.get('offer_id', 'N/A')})")
                
        else:
            print("⚠️  Unexpected results. Check manually.")
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")

def main():
    print("🎯 Mode Popup System - Cleanup Inactive Campaigns")
    print("=" * 55)
    
    if cleanup_inactive_campaigns():
        verify_cleanup()
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. 🖼️  Dashboard: https://mode-dash-production.up.railway.app/admin")
        print(f"2. 👀 Test Edit button functionality")
        print(f"3. 🎨 Add real images to campaigns")

if __name__ == "__main__":
    main() 