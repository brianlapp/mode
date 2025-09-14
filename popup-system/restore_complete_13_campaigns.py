#!/usr/bin/env python3
"""
🎯 COMPLETE 13-CAMPAIGN RESTORATION 
Restore all campaigns including the missing UpLevelRewards as Mike specified
"""

import sqlite3
import json
import os
from datetime import datetime

def restore_complete_campaigns():
    """Restore all 13 campaigns (5 MMM + 8 MFF) from updated backup"""
    
    # Load backup data with UpLevelRewards
    backup_path = os.path.join(os.path.dirname(__file__), 'campaign_backup.json')
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup file not found: {backup_path}")
        return False
        
    with open(backup_path, 'r') as f:
        backup_data = json.load(f)
    
    campaigns = backup_data['campaigns']
    print(f"🔄 Restoring {len(campaigns)} campaigns from backup...")
    print(f"📊 Expected: 5 MMM Finance + 7 MFF Lifestyle (+ 1 duplicate Prizies)")
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(__file__), 'api', 'popup_campaigns.db')
    conn = sqlite3.connect(db_path)
    
    try:
        # Clear existing campaigns and properties
        conn.execute("DELETE FROM campaigns")
        conn.execute("DELETE FROM campaign_properties")
        print("🧹 Cleared existing campaign data")
        
        mmm_count = 0
        mff_count = 0
        
        # Restore campaigns
        for campaign in campaigns:
            # Fix offer_id mismatch for campaign 12 (Prizies)
            if campaign['id'] == 12 and campaign['name'] == 'Prizies':
                campaign['offer_id'] = '3752'
                
            conn.execute('''
                INSERT INTO campaigns (
                    id, name, tune_url, logo_url, main_image_url, description,
                    cta_text, offer_id, aff_id, active, featured, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
            ''', (
                campaign['id'], campaign['name'], campaign['tune_url'],
                campaign['logo_url'], campaign['main_image_url'], campaign['description'],
                campaign['cta_text'], campaign['offer_id'], campaign['aff_id'], 
                campaign['active'], 
                campaign.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                campaign.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ))
            
            # Set property assignment based on aff_id (per Mike's specification)
            if campaign['aff_id'] == '43045':
                property_code = 'mmm'  # MMM Finance
                mmm_count += 1
            else:
                property_code = 'mff'  # MFF Lifestyle
                mff_count += 1
                
            conn.execute('''
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active
                ) VALUES (?, ?, 100, 1)
            ''', (campaign['id'], property_code))
            
            print(f"✅ Restored: {campaign['name']} (ID: {campaign['id']}, Property: {property_code.upper()})")
        
        conn.commit()
        
        # Verify restoration
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        active_campaigns = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT COUNT(*) FROM campaign_properties WHERE active = 1")
        property_assignments = cursor.fetchone()[0]
        
        print(f"\n🎉 COMPLETE RESTORATION SUCCESS!")
        print(f"📊 Active campaigns: {active_campaigns}")
        print(f"🏠 Property assignments: {property_assignments}")
        print(f"💰 MMM Finance campaigns: {mmm_count}")
        print(f"🎁 MFF Lifestyle campaigns: {mff_count}")
        print(f"✅ UpLevelRewards now included as requested")
        print(f"🛡️ No protection system - campaigns can be managed normally")
        
        return active_campaigns == 13 and property_assignments == 13
        
    except Exception as e:
        print(f"❌ Restoration failed: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🎯 COMPLETE 13-CAMPAIGN RESTORATION")
    print("=" * 60)
    
    success = restore_complete_campaigns()
    
    if success:
        print("\n✅ SUCCESS: All 13 campaigns restored with proper assignments")
        print("🚀 Mike's revenue machine is fully operational!")
        print("📈 MMM: Finance offers | MFF: Lifestyle offers")
    else:
        print("\n❌ RESTORATION FAILED")
        print("📋 Check backup file and database permissions")
