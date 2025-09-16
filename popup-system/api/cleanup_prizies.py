#!/usr/bin/env python3
"""
🗑️ PRIZIES CLEANUP TOOL
=======================
Permanently removes Prizies campaigns from database and all backup files
"""

import sqlite3
import json
import os
import glob
from pathlib import Path

def get_db_path():
    """Get database path"""
    # Check Railway production paths first
    paths = [
        "/app/popup-system/api/data/popup_campaigns.db",
        "/app/api/data/popup_campaigns.db",
        "popup_campaigns.db"
    ]
    
    for path in paths:
        if os.path.exists(path):
            return path
    
    return "popup_campaigns.db"

def cleanup_database():
    """Remove Prizies from database"""
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            print(f"❌ Database not found: {db_path}")
            return False
            
        conn = sqlite3.connect(db_path)
        
        # Delete Prizies campaigns
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns WHERE name = 'Prizies'")
        prizies_count = cursor.fetchone()[0]
        
        if prizies_count > 0:
            print(f"🗑️ Found {prizies_count} Prizies campaigns - deleting...")
            
            # Get IDs first
            cursor = conn.execute("SELECT id FROM campaigns WHERE name = 'Prizies'")
            prizies_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete from campaign_properties first (foreign key constraint)
            for campaign_id in prizies_ids:
                conn.execute("DELETE FROM campaign_properties WHERE campaign_id = ?", (campaign_id,))
            
            # Delete campaigns
            conn.execute("DELETE FROM campaigns WHERE name = 'Prizies'")
            
            conn.commit()
            print(f"✅ Deleted {prizies_count} Prizies campaigns")
        else:
            print("✅ No Prizies campaigns found in database")
            
        # Verify final count
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        final_count = cursor.fetchone()[0]
        print(f"📊 Final campaign count: {final_count}")
        
        # List remaining campaigns
        cursor = conn.execute("SELECT name FROM campaigns WHERE active = 1 ORDER BY name")
        campaigns = [row[0] for row in cursor.fetchall()]
        print("📋 Remaining campaigns:")
        for campaign in campaigns:
            print(f"   - {campaign}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database cleanup failed: {e}")
        return False

def cleanup_backup_files():
    """Remove Prizies from backup files"""
    try:
        backup_dir = Path(__file__).parent.parent / "backups"
        if not backup_dir.exists():
            print("📁 No backup directory found")
            return True
            
        # Find JSON backup files
        json_files = list(backup_dir.glob("*.json"))
        cleaned_files = 0
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Check if it has campaigns array
                if 'campaigns' in data and isinstance(data['campaigns'], list):
                    original_count = len(data['campaigns'])
                    # Remove Prizies campaigns
                    data['campaigns'] = [c for c in data['campaigns'] if c.get('name') != 'Prizies']
                    new_count = len(data['campaigns'])
                    
                    if original_count != new_count:
                        # Update the file
                        data['total_campaigns'] = new_count
                        data['campaign_count'] = new_count
                        
                        with open(json_file, 'w') as f:
                            json.dump(data, f, indent=2)
                        
                        print(f"🧹 Cleaned {json_file.name}: {original_count} → {new_count} campaigns")
                        cleaned_files += 1
                        
            except Exception as e:
                print(f"⚠️ Could not process {json_file.name}: {e}")
        
        print(f"✅ Cleaned {cleaned_files} backup files")
        return True
        
    except Exception as e:
        print(f"❌ Backup cleanup failed: {e}")
        return False

def main():
    """Main cleanup function"""
    print("🗑️ PRIZIES CLEANUP TOOL")
    print("=" * 30)
    
    # Step 1: Clean database
    print("\n1. Cleaning database...")
    db_success = cleanup_database()
    
    # Step 2: Clean backup files
    print("\n2. Cleaning backup files...")
    backup_success = cleanup_backup_files()
    
    # Summary
    print("\n🎯 CLEANUP SUMMARY:")
    print(f"   Database: {'✅ Success' if db_success else '❌ Failed'}")
    print(f"   Backups:  {'✅ Success' if backup_success else '❌ Failed'}")
    
    if db_success and backup_success:
        print("\n🎉 PRIZIES ELIMINATED PERMANENTLY!")
        print("   No more placeholder campaigns will appear in emails")
        return True
    else:
        print("\n❌ CLEANUP INCOMPLETE - some issues occurred")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
