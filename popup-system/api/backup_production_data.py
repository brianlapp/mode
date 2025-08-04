#!/usr/bin/env python3
"""
🚨 EMERGENCY DATA PRESERVATION SCRIPT
Backup Mike's production analytics data before it gets lost again
"""

import sqlite3
import json
from datetime import datetime

def backup_production_data():
    """Extract and save all tracking data"""
    conn = sqlite3.connect('popup_campaigns.db')
    
    backup_data = {
        'backup_timestamp': datetime.now().isoformat(),
        'impressions': [],
        'clicks': [],
        'campaigns': []
    }
    
    # Backup impressions
    cursor = conn.execute("""
        SELECT campaign_id, property_code, session_id, placement, 
               user_agent, timestamp, source, subsource, utm_campaign, 
               referrer, landing_page
        FROM impressions
    """)
    
    for row in cursor.fetchall():
        backup_data['impressions'].append({
            'campaign_id': row[0],
            'property_code': row[1], 
            'session_id': row[2],
            'placement': row[3],
            'user_agent': row[4],
            'timestamp': row[5],
            'source': row[6],
            'subsource': row[7],
            'utm_campaign': row[8],
            'referrer': row[9],
            'landing_page': row[10]
        })
    
    # Backup clicks
    cursor = conn.execute("""
        SELECT campaign_id, property_code, session_id, placement,
               user_agent, timestamp, revenue_estimate, conversion_tracked,
               source, subsource, utm_campaign, referrer, landing_page
        FROM clicks
    """)
    
    for row in cursor.fetchall():
        backup_data['clicks'].append({
            'campaign_id': row[0],
            'property_code': row[1],
            'session_id': row[2], 
            'placement': row[3],
            'user_agent': row[4],
            'timestamp': row[5],
            'revenue_estimate': row[6],
            'conversion_tracked': row[7],
            'source': row[8],
            'subsource': row[9],
            'utm_campaign': row[10],
            'referrer': row[11],
            'landing_page': row[12]
        })
    
    # Backup campaign info
    cursor = conn.execute("SELECT * FROM campaigns")
    columns = [description[0] for description in cursor.description]
    
    for row in cursor.fetchall():
        campaign_dict = dict(zip(columns, row))
        backup_data['campaigns'].append(campaign_dict)
    
    conn.close()
    
    # Save backup
    backup_filename = f"mike_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"✅ Backed up {len(backup_data['impressions'])} impressions")
    print(f"✅ Backed up {len(backup_data['clicks'])} clicks") 
    print(f"✅ Backed up {len(backup_data['campaigns'])} campaigns")
    print(f"📁 Saved to: {backup_filename}")
    
    return backup_filename

if __name__ == "__main__":
    backup_production_data()