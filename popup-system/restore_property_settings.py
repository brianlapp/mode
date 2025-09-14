#!/usr/bin/env python3
"""
Emergency Property Settings Restoration Script
Created after Mike lost his property visibility settings
"""

import sqlite3
import json
import sys

def restore_property_settings():
    """Restore Mike's property settings from backup"""
    
    backup_file = 'CRITICAL_BACKUP_BEFORE_AFFID_FIX_20250818_110452.json'
    
    try:
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        conn = sqlite3.connect('api/popup_campaigns.db')
        
        # Clear existing property settings
        conn.execute('DELETE FROM campaign_properties')
        print("🗑️ Cleared existing property settings")
        
        # Restore from backup
        restored_count = 0
        for prop_setting in backup_data['campaign_properties']:
            conn.execute("""
                INSERT INTO campaign_properties 
                (campaign_id, property_code, active, visibility_percentage, impression_cap_daily, click_cap_daily)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                prop_setting['campaign_id'],
                prop_setting['property_code'], 
                prop_setting['active'],
                prop_setting['visibility_percentage'],
                prop_setting.get('impression_cap_daily'),
                prop_setting.get('click_cap_daily')
            ))
            restored_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Restored {restored_count} property settings successfully!")
        print("Mike's property visibility settings are back!")
        
    except Exception as e:
        print(f"❌ Error restoring property settings: {e}")
        sys.exit(1)

if __name__ == "__main__":
    restore_property_settings()
