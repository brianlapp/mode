#!/usr/bin/env python3
"""
🔄 DATA RESTORATION SCRIPT  
Restore Mike's backed up analytics data to fix the reset issue
"""

import sqlite3
import json
import sys
import os

def restore_data_from_backup(backup_file):
    """Restore tracking data from JSON backup"""
    
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return False
        
    with open(backup_file, 'r') as f:
        backup_data = json.load(f)
    
    conn = sqlite3.connect('popup_campaigns.db')
    
    try:
        # Restore impressions
        for impression in backup_data['impressions']:
            conn.execute("""
                INSERT OR IGNORE INTO impressions 
                (campaign_id, property_code, session_id, placement, user_agent, 
                 timestamp, source, subsource, utm_campaign, referrer, landing_page)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                impression['campaign_id'], impression['property_code'],
                impression['session_id'], impression['placement'], 
                impression['user_agent'], impression['timestamp'],
                impression['source'], impression['subsource'],
                impression['utm_campaign'], impression['referrer'],
                impression['landing_page']
            ))
        
        # Restore clicks  
        for click in backup_data['clicks']:
            conn.execute("""
                INSERT OR IGNORE INTO clicks
                (campaign_id, property_code, session_id, placement, user_agent,
                 timestamp, revenue_estimate, conversion_tracked, source, 
                 subsource, utm_campaign, referrer, landing_page)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                click['campaign_id'], click['property_code'],
                click['session_id'], click['placement'],
                click['user_agent'], click['timestamp'],
                click['revenue_estimate'], click['conversion_tracked'],
                click['source'], click['subsource'], 
                click['utm_campaign'], click['referrer'],
                click['landing_page']
            ))
        
        conn.commit()
        
        # Verify restoration
        cursor = conn.execute("SELECT COUNT(*) FROM impressions")
        impression_count = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT COUNT(*) FROM clicks") 
        click_count = cursor.fetchone()[0]
        
        print(f"✅ Restored {impression_count} impressions")
        print(f"✅ Restored {click_count} clicks")
        print(f"🎉 Data restoration complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Restoration failed: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python restore_production_data.py <backup_file.json>")
        sys.exit(1)
        
    backup_file = sys.argv[1]
    success = restore_data_from_backup(backup_file)
    
    if not success:
        sys.exit(1)