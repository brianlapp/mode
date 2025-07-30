#!/usr/bin/env python3
"""
🛡️ ULTIMATE BACKUP SCRIPT - MIKE'S COMPLETE CAMPAIGN SYSTEM
✅ All 6 real campaigns with final image URLs
✅ Complete tracking data (offer_id, aff_id)
✅ One-click restore capability
"""

import requests
import json
import sys

# API Configuration
BASE_URL = "https://mode-dash-production.up.railway.app/api"

# 🔥 MIKE'S COMPLETE CAMPAIGN DATA - FINAL VERSION
# Updated with real image URLs from user on 2025-01-28
COMPLETE_CAMPAIGNS = [
    {
        "name": "Trading Tips",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045",
        "logo_url": "https://i.imgur.com/lHn301q.png",  # Real user-provided URL
        "main_image_url": "https://i.imgur.com/ZVGOktR.png",  # Real user-provided URL
        "description": "Get exclusive trading tips and market insights delivered daily to your inbox.",
        "cta_text": "Get Trading Tips",
        "offer_id": "6998",
        "aff_id": "43045"
    },
    {
        "name": "Behind The Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045",
        "logo_url": "https://i.imgur.com/O3iEVP7.jpeg",  # Real user-provided URL
        "main_image_url": "https://i.imgur.com/NA0o7iJ.png",  # Real user-provided URL
        "description": "Discover what's really happening behind the financial markets with expert analysis.",
        "cta_text": "Learn More",
        "offer_id": "7521",
        "aff_id": "43045"
    },
    {
        "name": "Brownstone Research",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045",
        "logo_url": "https://i.imgur.com/3KVDcV7.jpeg",  # Updated to working Imgur URL
        "main_image_url": "https://i.imgur.com/vzoiVpd.png",  # Updated to working Imgur URL
        "description": "Advanced technology and investment research from Brownstone Research experts.",
        "cta_text": "View Research",
        "offer_id": "7389",
        "aff_id": "43045"
    },
    {
        "name": "Hotsheets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045",
        "logo_url": "https://i.imgur.com/4JoGdZr.png",  # Updated to working Imgur URL
        "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg",  # Updated to working Imgur URL
        "description": "Daily market hotsheets with the most profitable trading opportunities.",
        "cta_text": "Get Hotsheets",
        "offer_id": "7385",
        "aff_id": "43045"
    },
    {
        "name": "Best Gold",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045",
        "logo_url": "https://i.imgur.com/5Yb0LJn.png",  # Updated to working Imgur URL
        "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg",  # Updated to working Imgur URL
        "description": "Premium gold investment insights and recommendations from industry experts.",
        "cta_text": "Learn About Gold",
        "offer_id": "7390",
        "aff_id": "43045"
    },
    {
        "name": "Beat the Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7601&aff_id=43045",
        "logo_url": "https://i.imgur.com/lHn301q.png",  # Using Trading Tips logo (user preference)
        "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg",  # Using Best Gold image as placeholder
        "description": "Proven strategies to consistently beat the markets and maximize your returns.",
        "cta_text": "Beat Markets",
        "offer_id": "7601",
        "aff_id": "43045"
    }
]

def get_campaigns():
    """Get all current campaigns"""
    try:
        response = requests.get(f"{BASE_URL}/campaigns")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error getting campaigns: {e}")
        return []

def hard_delete_campaign(campaign_id):
    """Permanently delete a campaign"""
    try:
        response = requests.delete(f"{BASE_URL}/campaigns/{campaign_id}/hard-delete")
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to delete campaign {campaign_id}: {e}")
        return False

def add_campaign(campaign_data):
    """Add a campaign"""
    try:
        response = requests.post(f"{BASE_URL}/campaigns", json=campaign_data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to add campaign {campaign_data['name']}: {e}")
        return False

def backup_current_system():
    """Create a backup of the current system"""
    print("📋 CREATING SYSTEM BACKUP...")
    print("=" * 50)
    
    campaigns = get_campaigns()
    
    if not campaigns:
        print("❌ No campaigns found to backup!")
        return None
    
    print(f"✅ Found {len(campaigns)} campaigns to backup")
    
    # Save to backup file
    backup_data = {
        "timestamp": "2025-01-28T00:00:00Z",
        "total_campaigns": len(campaigns),
        "campaigns": campaigns
    }
    
    with open("campaign_backup.json", "w") as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"💾 Backup saved to: campaign_backup.json")
    return backup_data

def restore_complete_system():
    """🔥 NUCLEAR OPTION: Complete system restore"""
    print("🚨 COMPLETE SYSTEM RESTORE")
    print("=" * 50)
    print("⚠️  This will DELETE ALL current campaigns and restore Mike's 6 real campaigns")
    
    # Get current campaigns
    current_campaigns = get_campaigns()
    
    if current_campaigns:
        print(f"🗑️  Deleting {len(current_campaigns)} existing campaigns...")
        deleted_count = 0
        
        for campaign in current_campaigns:
            if hard_delete_campaign(campaign['id']):
                deleted_count += 1
                print(f"   ✅ Deleted: {campaign['name']}")
            else:
                print(f"   ❌ Failed: {campaign['name']}")
        
        print(f"🧹 Cleanup complete: {deleted_count}/{len(current_campaigns)} deleted")
    
    # Add Mike's complete campaigns
    print(f"\n🚀 Adding {len(COMPLETE_CAMPAIGNS)} Mike's campaigns...")
    added_count = 0
    
    for campaign in COMPLETE_CAMPAIGNS:
        if add_campaign(campaign):
            added_count += 1
            print(f"   ✅ Added: {campaign['name']}")
            print(f"      📸 Logo: {campaign['logo_url'][:50]}...")
            print(f"      🖼️  Main: {campaign['main_image_url'][:50]}...")
        else:
            print(f"   ❌ Failed: {campaign['name']}")
    
    print("=" * 50)
    print(f"🎉 RESTORE COMPLETE: {added_count}/{len(COMPLETE_CAMPAIGNS)} campaigns restored")
    return added_count

def smart_update_images_only():
    """🎯 SMART UPDATE: Only update images for existing campaigns"""
    print("🎯 SMART IMAGE UPDATE")
    print("=" * 50)
    
    current_campaigns = get_campaigns()
    if not current_campaigns:
        print("❌ No campaigns found!")
        return 0
    
    updated_count = 0
    
    # Create lookup by name
    image_lookup = {campaign["name"]: campaign for campaign in COMPLETE_CAMPAIGNS}
    
    for campaign in current_campaigns:
        name = campaign.get('name')
        if name in image_lookup:
            # Update only images
            update_data = {
                "logo_url": image_lookup[name]["logo_url"],
                "main_image_url": image_lookup[name]["main_image_url"]
            }
            
            try:
                response = requests.put(f"{BASE_URL}/campaigns/{campaign['id']}", json=update_data)
                response.raise_for_status()
                updated_count += 1
                print(f"✅ Updated images for: {name}")
                print(f"   📸 Logo: {update_data['logo_url'][:50]}...")
                print(f"   🖼️  Main: {update_data['main_image_url'][:50]}...")
            except Exception as e:
                print(f"❌ Failed to update {name}: {e}")
        else:
            print(f"⏭️  Skipping {name} (not in backup data)")
    
    print("=" * 50)
    print(f"🎨 IMAGE UPDATE COMPLETE: {updated_count} campaigns updated")
    return updated_count

def validate_system():
    """🔍 Validate the current system"""
    print("🔍 SYSTEM VALIDATION")
    print("=" * 50)
    
    campaigns = get_campaigns()
    if not campaigns:
        print("❌ No campaigns found!")
        return False
    
    print(f"📊 System Status:")
    print(f"   Total Campaigns: {len(campaigns)}")
    print(f"   Active Campaigns: {sum(1 for c in campaigns if c.get('active', True))}")
    
    # Check Mike's campaigns
    expected_names = {c["name"] for c in COMPLETE_CAMPAIGNS}
    current_names = {c["name"] for c in campaigns}
    
    missing = expected_names - current_names
    extra = current_names - expected_names
    
    if missing:
        print(f"❌ Missing campaigns: {', '.join(missing)}")
    
    if extra:
        print(f"⚠️  Extra campaigns: {', '.join(extra)}")
    
    if not missing and not extra:
        print("✅ All Mike's campaigns present!")
    
    # Check image URLs
    print(f"\n🖼️  Image Status:")
    for campaign in campaigns:
        name = campaign.get('name')
        if name in expected_names:
            logo_ok = campaign.get('logo_url', '').startswith(('https://i.imgur.com', 'https://financepopupoffers'))
            main_ok = campaign.get('main_image_url', '').startswith(('https://i.imgur.com', 'https://financepopupoffers'))
            status = "✅" if logo_ok and main_ok else "❌"
            print(f"   {status} {name}: Logo={logo_ok}, Main={main_ok}")
    
    return len(missing) == 0

def main():
    """Main menu for backup/restore operations"""
    print("🛡️  MIKE'S CAMPAIGN BACKUP & RESTORE SYSTEM")
    print("=" * 50)
    print("Options:")
    print("1. 📋 Backup Current System")
    print("2. 🔥 Complete System Restore (NUCLEAR)")
    print("3. 🎯 Smart Image Update Only")
    print("4. 🔍 Validate System")
    print("5. 🚪 Exit")
    print("=" * 50)
    
    try:
        choice = input("Select option (1-5): ").strip()
        
        if choice == "1":
            backup_current_system()
        elif choice == "2":
            confirm = input("⚠️  Type 'RESTORE' to confirm complete system restore: ")
            if confirm == "RESTORE":
                restore_complete_system()
            else:
                print("❌ Restore cancelled")
        elif choice == "3":
            smart_update_images_only()
        elif choice == "4":
            validate_system()
        elif choice == "5":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main() 