#!/usr/bin/env python3
"""
🚨 EMERGENCY PRIZIES CLEANUP FOR RAILWAY
=========================================
Forces cleanup of Prizies and restores exactly 12 good campaigns
"""

import requests
import json
import time

def test_api_connection():
    """Test if we can connect to the API"""
    try:
        response = requests.get("https://mode-dash-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            print("✅ API connection successful")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def get_current_campaigns():
    """Get current campaign list"""
    try:
        response = requests.get("https://mode-dash-production.up.railway.app/api/campaigns", timeout=10)
        if response.status_code == 200:
            campaigns = response.json()
            print(f"📊 Current campaigns: {len(campaigns)}")
            
            prizies_campaigns = [c for c in campaigns if c.get('name') == 'Prizies']
            print(f"🗑️ Prizies campaigns found: {len(prizies_campaigns)}")
            
            return campaigns
        else:
            print(f"❌ Failed to get campaigns: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting campaigns: {e}")
        return None

def force_emergency_restore():
    """Force emergency restore with clean data"""
    try:
        print("🔄 Running emergency restore...")
        response = requests.post("https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Emergency restore result: {result}")
            return True
        else:
            print(f"❌ Emergency restore failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Emergency restore error: {e}")
        return False

def manual_prizies_cleanup():
    """Manually delete Prizies campaigns via API calls"""
    try:
        # Get current campaigns
        campaigns = get_current_campaigns()
        if not campaigns:
            return False
            
        # Find Prizies campaigns
        prizies_campaigns = [c for c in campaigns if c.get('name') == 'Prizies']
        
        if not prizies_campaigns:
            print("✅ No Prizies campaigns found")
            return True
            
        print(f"🗑️ Found {len(prizies_campaigns)} Prizies campaigns to delete")
        
        # Since we don't have a direct delete endpoint deployed yet,
        # we'll use the emergency restore which should exclude Prizies
        return force_emergency_restore()
        
    except Exception as e:
        print(f"❌ Manual cleanup error: {e}")
        return False

def verify_final_state():
    """Verify the final state after cleanup"""
    try:
        campaigns = get_current_campaigns()
        if not campaigns:
            return False
            
        # Check for Prizies
        prizies_campaigns = [c for c in campaigns if c.get('name') == 'Prizies']
        if prizies_campaigns:
            print(f"❌ CLEANUP FAILED: {len(prizies_campaigns)} Prizies campaigns still exist")
            return False
            
        # Check campaign count
        if len(campaigns) != 12:
            print(f"⚠️ Campaign count is {len(campaigns)}, expected 12")
            
        print("📋 Final campaign list:")
        for campaign in sorted(campaigns, key=lambda x: x.get('name', '')):
            print(f"   - {campaign.get('name')}")
            
        print("✅ CLEANUP VERIFICATION COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def main():
    """Main cleanup process"""
    print("🚨 EMERGENCY PRIZIES CLEANUP FOR RAILWAY")
    print("=" * 50)
    
    # Step 1: Test connection
    if not test_api_connection():
        print("❌ Cannot connect to API - aborting")
        return False
    
    # Step 2: Get current state
    print("\n📊 CURRENT STATE:")
    get_current_campaigns()
    
    # Step 3: Force cleanup
    print("\n🗑️ FORCING CLEANUP:")
    if not manual_prizies_cleanup():
        print("❌ Cleanup failed")
        return False
    
    # Step 4: Wait and verify
    print("\n⏳ Waiting for changes to take effect...")
    time.sleep(5)
    
    print("\n✅ VERIFICATION:")
    success = verify_final_state()
    
    if success:
        print("\n🎉 SUCCESS: Prizies eliminated from Railway!")
        print("   Email ads will now show professional campaigns only")
    else:
        print("\n❌ CLEANUP INCOMPLETE - manual intervention may be needed")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
