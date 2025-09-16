#!/usr/bin/env python3
"""
🛡️ BULLETPROOF BACKUP & RESTORE SYSTEM
=====================================
Automatically backs up and restores campaign data to prevent Railway resets
"""

import sqlite3
import json
import os
import glob
from pathlib import Path
from datetime import datetime

def get_db_path():
    """Get database path with persistent volume support"""
    # Railway production path
    volume_path = "/app/popup-system/api/data"
    if os.path.exists(volume_path):
        return os.path.join(volume_path, "popup_campaigns.db")
    
    # Fallback path
    fallback_path = "/app/api/data"
    if os.path.exists(fallback_path):
        return os.path.join(fallback_path, "popup_campaigns.db")
    
    # Local development
    return os.path.join(os.path.dirname(__file__), "popup_campaigns.db")

def create_backup():
    """Create a backup of the current database"""
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            print(f"❌ Database not found: {db_path}")
            return False
            
        # Create backups directory
        backup_dir = Path(__file__).parent.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export campaigns to JSON for easy restore
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Get campaigns
        cursor = conn.execute("""
            SELECT c.*, cp.property_code
            FROM campaigns c
            LEFT JOIN campaign_properties cp ON c.id = cp.campaign_id
            WHERE c.active = 1
            ORDER BY c.id
        """)
        campaigns = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Save backup
        backup_file = backup_dir / f"campaigns_backup_{timestamp}.json"
        backup_data = {
            "timestamp": timestamp,
            "campaign_count": len(campaigns),
            "campaigns": campaigns
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
            
        print(f"✅ Backup created: {backup_file}")
        print(f"   📊 Campaigns backed up: {len(campaigns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def get_latest_backup():
    """Get the most recent backup file"""
    backup_dir = Path(__file__).parent.parent / "backups"
    if not backup_dir.exists():
        return None
        
    # Look for campaign backup files
    backup_files = list(backup_dir.glob("campaigns_backup_*.json"))
    if not backup_files:
        return None
        
    # Return the most recent
    return max(backup_files, key=lambda p: p.stat().st_mtime)

def restore_from_backup(backup_file=None):
    """Restore campaigns from backup file"""
    try:
        if backup_file is None:
            backup_file = get_latest_backup()
            
        if not backup_file or not backup_file.exists():
            print("❌ No backup file found")
            return False
            
        print(f"🔄 Restoring from backup: {backup_file}")
        
        # Load backup data
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
            
        campaigns = backup_data.get('campaigns', [])
        if not campaigns:
            print("❌ No campaigns in backup file")
            return False
            
        # Filter out Prizies campaigns
        good_campaigns = [c for c in campaigns if c.get('name') != 'Prizies']
        print(f"📊 Filtering: {len(campaigns)} → {len(good_campaigns)} campaigns (removed Prizies)")
        
        # Restore to database
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        
        # Clear existing data
        conn.execute("DELETE FROM campaign_properties")
        conn.execute("DELETE FROM campaigns")
        
        # Restore campaigns
        for campaign in good_campaigns:
            # Insert campaign
            conn.execute('''
                INSERT INTO campaigns (
                    id, name, tune_url, logo_url, main_image_url, description,
                    cta_text, offer_id, aff_id, active, featured, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                campaign.get('id'),
                campaign.get('name'),
                campaign.get('tune_url'),
                campaign.get('logo_url'),
                campaign.get('main_image_url'),
                campaign.get('description'),
                campaign.get('cta_text', 'View Offer'),
                campaign.get('offer_id'),
                campaign.get('aff_id'),
                campaign.get('active', 1),
                campaign.get('featured', 0),
                campaign.get('created_at', '2025-01-28 12:00:00'),
                campaign.get('updated_at', '2025-01-28 12:00:00')
            ))
            
            # Set property assignment
            property_code = campaign.get('property_code')
            if not property_code:
                # Determine property from affiliate ID
                finance_affiliates = {"43045", "43092"}
                property_code = 'mmm' if str(campaign.get('aff_id', '')) in finance_affiliates else 'mff'
                
            conn.execute('''
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active
                ) VALUES (?, ?, 100, 1)
            ''', (campaign.get('id'), property_code))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Restore complete: {len(good_campaigns)} campaigns restored")
        return True
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def auto_backup_and_restore():
    """Main function: backup if data exists, restore if empty"""
    try:
        db_path = get_db_path()
        
        # Check if database exists and has campaigns
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
            campaign_count = cursor.fetchone()[0]
            conn.close()
            
            if campaign_count > 0:
                print(f"✅ Database healthy: {campaign_count} campaigns")
                # Create backup of current state
                create_backup()
                return True
            else:
                print("🚨 Database empty - attempting restore...")
                return restore_from_backup()
        else:
            print("🚨 Database missing - attempting restore...")
            # Initialize database first
            from database import init_db
            init_db()
            return restore_from_backup()
            
    except Exception as e:
        print(f"❌ Auto backup/restore failed: {e}")
        return False

if __name__ == "__main__":
    print("🛡️ BACKUP & RESTORE SYSTEM")
    print("=" * 40)
    auto_backup_and_restore()
