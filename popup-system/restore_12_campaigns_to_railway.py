#!/usr/bin/env python3
"""
🚨 EMERGENCY RESTORATION: Deploy 12 campaigns to Railway
This script restores all campaigns and property settings to Railway production
"""

import requests
import json
import time

# Load our complete campaign backup
with open('campaign_backup.json', 'r') as f:
    backup_data = json.load(f)

campaigns = backup_data['campaigns']

print("🚨 EMERGENCY RESTORATION OF 12 CAMPAIGNS TO RAILWAY")
print("=" * 60)
print(f"📊 Restoring {len(campaigns)} campaigns with property attribution")

# Railway API endpoint (update with actual Railway URL)
RAILWAY_API_BASE = "https://mode-production.up.railway.app"  # Update this!

# Restoration data
restoration_data = {
    "campaigns": campaigns,
    "campaign_properties": [
        # MMM Finance campaigns (aff_id 43045)
        {"campaign_id": 1, "property_code": "mmm", "visibility_percentage": 100, "active": True},
        {"campaign_id": 2, "property_code": "mmm", "visibility_percentage": 100, "active": True},
        {"campaign_id": 3, "property_code": "mmm", "visibility_percentage": 100, "active": True},
        {"campaign_id": 4, "property_code": "mmm", "visibility_percentage": 100, "active": True},
        {"campaign_id": 5, "property_code": "mmm", "visibility_percentage": 100, "active": True},
        
        # MFF Lifestyle campaigns (aff_id 42946)
        {"campaign_id": 6, "property_code": "mff", "visibility_percentage": 100, "active": True},
        {"campaign_id": 7, "property_code": "mff", "visibility_percentage": 100, "active": True},
        {"campaign_id": 8, "property_code": "mff", "visibility_percentage": 100, "active": True},
        {"campaign_id": 9, "property_code": "mff", "visibility_percentage": 100, "active": True},
        {"campaign_id": 10, "property_code": "mff", "visibility_percentage": 100, "active": True},
        {"campaign_id": 11, "property_code": "mff", "visibility_percentage": 100, "active": True},
        {"campaign_id": 12, "property_code": "mff", "visibility_percentage": 100, "active": True},
    ]
}

def restore_to_railway():
    """Send restoration data to Railway"""
    try:
        # Try to post the restoration data
        response = requests.post(
            f"{RAILWAY_API_BASE}/api/emergency-restore",
            json=restoration_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Railway restoration successful!")
            return True
        else:
            print(f"❌ Railway restoration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Could not connect to Railway: {e}")
        return False

def verify_restoration():
    """Verify all campaigns are live"""
    try:
        # Check MFF campaigns
        mff_response = requests.get(f"{RAILWAY_API_BASE}/api/campaigns/mff", timeout=10)
        mmm_response = requests.get(f"{RAILWAY_API_BASE}/api/campaigns/mmm", timeout=10)
        
        if mff_response.status_code == 200 and mmm_response.status_code == 200:
            mff_campaigns = mff_response.json()
            mmm_campaigns = mmm_response.json()
            
            print(f"🎁 MFF campaigns live: {len(mff_campaigns)}")
            print(f"🏦 MMM campaigns live: {len(mmm_campaigns)}")
            print(f"📈 Total live: {len(mff_campaigns) + len(mmm_campaigns)}")
            
            return len(mff_campaigns) == 7 and len(mmm_campaigns) == 5
        else:
            print("❌ Could not verify restoration")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("⏱️ Waiting for Railway hotfix to deploy (30 seconds)...")
    time.sleep(30)
    
    print("🚀 Attempting Railway restoration...")
    success = restore_to_railway()
    
    if success:
        print("✅ Restoration sent - verifying...")
        time.sleep(5)
        verified = verify_restoration()
        
        if verified:
            print("🎉 RAILWAY RESTORATION COMPLETE!")
            print("✅ All 12 campaigns are now live with proper domain attribution")
        else:
            print("⚠️ Restoration may need manual verification")
    else:
        print("❌ Railway restoration failed - may need manual intervention")
        print("\n📋 MANUAL RESTORATION STEPS:")
        print("1. Access Railway console")
        print("2. Run database restoration manually")
        print("3. Verify campaign_properties table is populated")
