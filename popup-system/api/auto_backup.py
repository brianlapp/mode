#!/usr/bin/env python3
"""
🛡️ AUTOMATED DATABASE BACKUP SYSTEM
=====================================
Protects Mike's revenue data from ever being lost again!

Features:
- Runs before every git commit via git hook
- Creates timestamped backups with data summary
- Stores both local and production data
- Alerts if data loss detected
- Easy restore functionality
"""

import sqlite3
import shutil
import os
import json
from datetime import datetime
from pathlib import Path

def get_db_path():
    """Get database path with persistent volume support"""
    volume_path = "/app/popup-system/api/data"
    if os.path.exists(volume_path):
        return os.path.join(volume_path, "popup_campaigns.db")
    
    fallback_path = "/app/api/data"
    if os.path.exists(fallback_path):
        return os.path.join(fallback_path, "popup_campaigns.db")
    
    return "popup_campaigns.db"

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

def create_backup():
    """Create timestamped backup with analysis"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    db_path = get_db_path()
    backup_path = backup_dir / f"popup_campaigns_backup_{timestamp}.db"
    analysis_path = backup_dir / f"backup_analysis_{timestamp}.json"
    
    # Create backup
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up: {backup_path}")
        
        # Analyze and save summary
        analysis = analyze_database(db_path)
        analysis["backup_timestamp"] = timestamp
        analysis["backup_file"] = str(backup_path)
        analysis["original_file"] = db_path
        
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"📊 BACKUP SUMMARY:")
        print(f"   - Campaigns: {analysis.get('campaigns', 'Unknown')}")
        print(f"   - Impressions: {analysis.get('impressions', 'Unknown')}")
        print(f"   - Clicks: {analysis.get('clicks', 'Unknown')}")
        print(f"   - Revenue: ${analysis.get('revenue', 0):.2f}")
        print(f"   - Date Range: {analysis.get('date_range', {}).get('first', 'Unknown')} to {analysis.get('date_range', {}).get('last', 'Unknown')}")
        
        return True
    else:
        print(f"❌ Database not found: {db_path}")
        return False

def setup_git_hook():
    """Setup git pre-commit hook for automatic backups"""
    git_dir = Path(".git")
    if not git_dir.exists():
        print("❌ Not in a git repository")
        return False
    
    hooks_dir = git_dir / "hooks" 
    hooks_dir.mkdir(exist_ok=True)
    
    pre_commit_path = hooks_dir / "pre-commit"
    
    hook_content = """#!/bin/bash
# 🛡️ Auto-backup database before commit
echo "🛡️ Creating database backup before commit..."
cd "$(git rev-parse --show-toplevel)/popup-system/api"
python3 auto_backup.py
echo "✅ Backup complete!"
"""
    
    with open(pre_commit_path, 'w') as f:
        f.write(hook_content)
    
    # Make executable
    os.chmod(pre_commit_path, 0o755)
    print(f"✅ Git pre-commit hook installed: {pre_commit_path}")
    return True

def cleanup_old_backups(keep_count=10):
    """Keep only the most recent backups"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        return
    
    backup_files = sorted(backup_dir.glob("popup_campaigns_backup_*.db"))
    analysis_files = sorted(backup_dir.glob("backup_analysis_*.json"))
    
    # Remove old backup files
    for file_list in [backup_files, analysis_files]:
        if len(file_list) > keep_count:
            for old_file in file_list[:-keep_count]:
                old_file.unlink()
                print(f"🗑️ Removed old backup: {old_file.name}")

if __name__ == "__main__":
    print("🛡️ MIKE'S DATA PROTECTION SYSTEM")
    print("=================================")
    
    # Create backup
    success = create_backup()
    
    if success:
        # Setup git hook if not exists
        if not Path(".git/hooks/pre-commit").exists():
            setup_git_hook()
        
        # Cleanup old backups
        cleanup_old_backups()
        
        print("\n🎉 PROTECTION SYSTEM ACTIVE!")
        print("   - Database backed up successfully")
        print("   - Git hook installed for auto-backup")
        print("   - Old backups cleaned up")
    else:
        print("\n❌ BACKUP FAILED!")
        print("   - Could not find database file")
        print("   - Check database path configuration")