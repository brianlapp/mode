#!/usr/bin/env python3
"""
🧹 EMERGENCY CLEANUP SCRIPT - Remove Inactive Campaigns
Removes all inactive campaigns to prevent fallback issues and reduce payload size
"""
import requests
import json

BASE_URL = "https://mode-dash-production.up.railway.app/api"

def get_all_campaigns():
    """Get all campaigns from API"""
    response = requests.get(f"{BASE_URL}/campaigns")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get campaigns: {response.status_code}")
        return []

def delete_campaign(campaign_id):
    """Delete a campaign by ID"""
    response = requests.delete(f"{BASE_URL}/campaigns/{campaign_id}")
    if response.status_code == 200:
        return True
    else:
        print(f"❌ Failed to delete campaign {campaign_id}: {response.status_code}")
        return False

def main():
    print("🧹 EMERGENCY CLEANUP - Removing Inactive Campaigns")
    print("=" * 50)
    
    # Get all campaigns
    campaigns = get_all_campaigns()
    if not campaigns:
        print("❌ No campaigns found")
        return
    
    print(f"📊 Found {len(campaigns)} total campaigns")
    
    # Find inactive campaigns
    inactive_campaigns = [c for c in campaigns if not c.get('active', True)]
    active_campaigns = [c for c in campaigns if c.get('active', True)]
    
    print(f"✅ Active campaigns: {len(active_campaigns)}")
    print(f"❌ Inactive campaigns: {len(inactive_campaigns)}")
    
    if not inactive_campaigns:
        print("🎉 No inactive campaigns to remove!")
        return
    
    print("\n🗑️  INACTIVE CAMPAIGNS TO DELETE:")
    for campaign in inactive_campaigns:
        print(f"   - ID {campaign['id']}: {campaign['name']} (created: {campaign.get('created_at', 'unknown')})")
    
    # Confirm deletion
    confirm = input(f"\n⚠️  Delete {len(inactive_campaigns)} inactive campaigns? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Cleanup cancelled")
        return
    
    # Delete inactive campaigns
    deleted_count = 0
    for campaign in inactive_campaigns:
        if delete_campaign(campaign['id']):
            print(f"✅ Deleted: {campaign['name']} (ID: {campaign['id']})")
            deleted_count += 1
        else:
            print(f"❌ Failed to delete: {campaign['name']} (ID: {campaign['id']})")
    
    print(f"\n🎉 CLEANUP COMPLETE!")
    print(f"   - Deleted: {deleted_count} inactive campaigns")
    print(f"   - Remaining: {len(active_campaigns)} active campaigns")
    print(f"   - Payload reduction: ~{(deleted_count/(deleted_count+len(active_campaigns)))*100:.1f}%")

if __name__ == "__main__":
    main() 