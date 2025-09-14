#!/usr/bin/env python3
"""
🎯 CLEAN CAMPAIGN RESTORATION
Restore all 12 legitimate campaigns without protection system interference
"""

import sqlite3
import json
import os
from datetime import datetime

def restore_campaigns_from_backup():
    """Restore all 12 campaigns from verified backup"""
    
    # Load backup data
    backup_path = os.path.join(os.path.dirname(__file__), 'campaign_backup.json')
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup file not found: {backup_path}")
        return False
        
    with open(backup_path, 'r') as f:
        backup_data = json.load(f)
    
    campaigns = backup_data['campaigns']
    print(f"🔄 Restoring {len(campaigns)} campaigns from backup...")
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(__file__), 'api', 'popup_campaigns.db')
    conn = sqlite3.connect(db_path)
    
    try:
        # Clear existing campaigns and properties
        conn.execute("DELETE FROM campaigns")
        conn.execute("DELETE FROM campaign_properties")
        print("🧹 Cleared existing campaign data")
        
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
            
            # Set property assignment based on aff_id
            property_code = 'mmm' if campaign['aff_id'] == '43045' else 'mff'
            conn.execute('''
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active
                ) VALUES (?, ?, 100, 1)
            ''', (campaign['id'], property_code))
            
            print(f"✅ Restored: {campaign['name']} (ID: {campaign['id']}, Property: {property_code})")
        
        conn.commit()
        
        # Verify restoration
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        active_campaigns = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT COUNT(*) FROM campaign_properties WHERE active = 1")
        property_assignments = cursor.fetchone()[0]
        
        print(f"\n🎉 RESTORATION COMPLETE!")
        print(f"📊 Active campaigns: {active_campaigns}")
        print(f"🏠 Property assignments: {property_assignments}")
        print(f"🛡️ No protection system - campaigns can be added/managed normally")
        
        return active_campaigns == 12 and property_assignments == 12
        
    except Exception as e:
        print(f"❌ Restoration failed: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🎯 CLEAN CAMPAIGN RESTORATION")
    print("=" * 50)
    
    success = restore_campaigns_from_backup()
    
    if success:
        print("\n✅ SUCCESS: All 12 campaigns restored")
        print("🚀 Mike's revenue machine is operational!")
        print("➕ Future campaigns can be added without protection interference")
    else:
        print("\n❌ RESTORATION FAILED")
        print("📋 Check backup file and database permissions")
