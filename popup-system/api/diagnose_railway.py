#!/usr/bin/env python3
"""
🔍 RAILWAY VOLUME MOUNT DIAGNOSTIC SCRIPT
Debug exactly what's happening with Railway volume mounts
"""

import os
import sqlite3
from database import get_db_path

def diagnose_railway_setup():
    """Diagnose Railway volume mount and database path"""
    print("🔍 RAILWAY VOLUME MOUNT DIAGNOSTIC")
    print("=" * 50)
    
    # Check volume paths
    volume_paths = [
        "/app/popup-system/api/data",
        "/app/api/data", 
        "/app/data"
    ]
    
    print("\n📁 VOLUME PATH CHECK:")
    for path in volume_paths:
        exists = os.path.exists(path)
        writable = False
        if exists:
            try:
                test_file = os.path.join(path, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                writable = True
            except:
                writable = False
        
        print(f"   {path}: {'✅ EXISTS' if exists else '❌ MISSING'}, {'✅ WRITABLE' if writable else '❌ READ-ONLY' if exists else ''}")
    
    # Check actual database path
    db_path = get_db_path()
    print(f"\n📊 DATABASE PATH: {db_path}")
    
    # Check if database exists and has data
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            
            # Check impressions count
            cursor = conn.execute("SELECT COUNT(*) FROM impressions")
            impression_count = cursor.fetchone()[0]
            
            # Check clicks count  
            cursor = conn.execute("SELECT COUNT(*) FROM clicks")
            click_count = cursor.fetchone()[0]
            
            # Check campaigns count
            cursor = conn.execute("SELECT COUNT(*) FROM campaigns")
            campaign_count = cursor.fetchone()[0]
            
            print(f"   📊 Impressions: {impression_count:,}")
            print(f"   🖱️  Clicks: {click_count:,}")
            print(f"   📈 Campaigns: {campaign_count}")
            
            # Check data freshness
            cursor = conn.execute("SELECT MAX(timestamp) FROM impressions")
            last_impression = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT MAX(timestamp) FROM clicks")
            last_click = cursor.fetchone()[0]
            
            print(f"   🕒 Last impression: {last_impression}")
            print(f"   🕒 Last click: {last_click}")
            
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Database error: {e}")
    else:
        print("   ❌ Database file does not exist")
    
    # Check environment
    print(f"\n🌍 ENVIRONMENT:")
    print(f"   Working directory: {os.getcwd()}")
    print(f"   Railway: {'✅' if os.environ.get('RAILWAY_ENVIRONMENT') else '❌'}")
    print(f"   Volume mount: {'✅' if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH') else '❌'}")

if __name__ == "__main__":
    diagnose_railway_setup()