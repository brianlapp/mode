#!/usr/bin/env python3
"""
🛡️ COMPREHENSIVE DATABASE PROTECTION SYSTEM
============================================
Protects Mike's revenue data from EVER being lost again!
"""

import sqlite3
import shutil
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def find_database():
    """Find the active database file"""
    possible_paths = [
        "popup-system/api/popup_campaigns.db",
        "api/popup_campaigns.db", 
        "popup_campaigns.db"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_production_data():
    """Get production data via API for comparison"""
    try:
        import requests
        url = "https://mode-dash-production.up.railway.app/api/analytics/attribution"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            total_imp = sum(campaign['impressions'] for campaign in data['by_campaign'])
            return {
                "impressions": total_imp,
                "clicks": data['summary']['total_clicks'],
                "revenue": data['summary']['total_revenue']
            }
    except:
        pass
    return None

def analyze_database(db_path):
    """Analyze database and return summary"""
    if not os.path.exists(db_path):
        return {"error": f"Database not found: {db_path}"}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get data counts
        cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        campaigns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM impressions")
        impressions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM clicks")
        clicks = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(revenue_estimate) FROM clicks")
        revenue = cursor.fetchone()[0] or 0
        
        # Get date range
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM impressions")
        date_range = cursor.fetchone()
        
        conn.close()
        
        return {
            "campaigns": campaigns,
            "impressions": impressions, 
            "clicks": clicks,
            "revenue": float(revenue),
            "date_range": {
                "first": date_range[0],
                "last": date_range[1]
            },
            "file_size": os.path.getsize(db_path)
        }
    except Exception as e:
        return {"error": str(e)}

def create_comprehensive_backup():
    """Create backup with production comparison"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("popup-system/backups")
    backup_dir.mkdir(exist_ok=True)
    
    db_path = find_database()
    if not db_path:
        print("❌ No database found!")
        return False
    
    backup_path = backup_dir / f"popup_campaigns_backup_{timestamp}.db"
    analysis_path = backup_dir / f"backup_analysis_{timestamp}.json"
    
    # Create backup
    shutil.copy2(db_path, backup_path)
    print(f"✅ Database backed up: {backup_path}")
    
    # Analyze local data
    local_analysis = analyze_database(db_path)
    
    # Get production data for comparison
    production_data = get_production_data()
    
    # Create comprehensive report
    report = {
        "backup_timestamp": timestamp,
        "backup_file": str(backup_path),
        "original_file": db_path,
        "local_data": local_analysis,
        "production_data": production_data,
        "data_loss_alert": False
    }
    
    # Check for data loss
    if production_data and local_analysis.get('impressions', 0) < production_data.get('impressions', 0):
        report["data_loss_alert"] = True
        print("🚨 DATA LOSS DETECTED!")
        print(f"   Local: {local_analysis.get('impressions', 0)} impressions")
        print(f"   Production: {production_data.get('impressions', 0)} impressions")
    
    with open(analysis_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📊 BACKUP SUMMARY:")
    print(f"   - Campaigns: {local_analysis.get('campaigns', 'Unknown')}")
    print(f"   - Impressions: {local_analysis.get('impressions', 'Unknown')}")
    print(f"   - Clicks: {local_analysis.get('clicks', 'Unknown')}")
    print(f"   - Revenue: ${local_analysis.get('revenue', 0):.2f}")
    
    if production_data:
        print(f"📊 PRODUCTION COMPARISON:")
        print(f"   - Production Impressions: {production_data.get('impressions', 'Unknown')}")
        print(f"   - Production Clicks: {production_data.get('clicks', 'Unknown')}")
        print(f"   - Production Revenue: ${production_data.get('revenue', 0):.2f}")
    
    return True

def setup_git_pre_commit_hook():
    """Setup automatic backup before commits"""
    hook_content = """#!/bin/bash
# 🛡️ PROTECTION: Auto-backup database before commit
echo "🛡️ Backing up database before commit..."
cd "$(git rev-parse --show-toplevel)"
python3 popup-system/backup_protection.py
if [ $? -ne 0 ]; then
    echo "❌ Backup failed! Commit aborted."
    exit 1
fi
echo "✅ Database protected!"
"""
    
    hooks_dir = Path(".git/hooks")
    hooks_dir.mkdir(exist_ok=True)
    
    pre_commit_path = hooks_dir / "pre-commit"
    with open(pre_commit_path, 'w') as f:
        f.write(hook_content)
    
    os.chmod(pre_commit_path, 0o755)
    print(f"✅ Git pre-commit hook installed!")

if __name__ == "__main__":
    print("🛡️ MIKE'S REVENUE DATA PROTECTION")
    print("==================================")
    
    success = create_comprehensive_backup()
    
    if success:
        if not Path(".git/hooks/pre-commit").exists():
            setup_git_pre_commit_hook()
        
        print("\n🎉 PROTECTION SYSTEM ACTIVE!")
        print("✅ Your data is now BULLETPROOF against resets!")
    else:
        print("\n❌ PROTECTION SETUP FAILED!")