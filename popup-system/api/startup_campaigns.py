#!/usr/bin/env python3
"""
🛡️ MIKE'S REVENUE MACHINE PROTECTION SYSTEM
Ensures only real campaigns exist - NO MORE TEST CAMPAIGN ZOMBIES!
"""

import sqlite3
from database import get_db_connection, insert_campaign

# Mike's 5 REAL campaigns - THE ONLY ONES THAT SHOULD EXIST
MIKES_REAL_CAMPAIGNS = [
    {
        "name": "Trading Tips",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045",
        "logo_url": "https://i.imgur.com/lHn301q.png",
        "main_image_url": "https://i.imgur.com/ZVGOktR.png",
        "description": "Get exclusive trading tips and market insights delivered daily to your inbox.",
        "cta_text": "Get Trading Tips",
        "offer_id": "6998",
        "aff_id": "43045"
    },
    {
        "name": "Behind The Markets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045",
        "logo_url": "https://i.imgur.com/O3iEVP7.jpeg",
        "main_image_url": "https://i.imgur.com/NA0o7iJ.png",
        "description": "Discover what's really happening behind the financial markets with expert analysis.",
        "cta_text": "Learn More",
        "offer_id": "7521",
        "aff_id": "43045"
    },
    {
        "name": "Brownstone Research",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045",
        "logo_url": "https://i.imgur.com/3KVDcV7.jpeg",
        "main_image_url": "https://i.imgur.com/vzoiVpd.png",
        "description": "Advanced technology and investment research from Brownstone Research experts.",
        "cta_text": "View Research",
        "offer_id": "7389",
        "aff_id": "43045"
    },
    {
        "name": "Hotsheets",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045",
        "logo_url": "https://i.imgur.com/4JoGdZr.png",
        "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg",
        "description": "Daily market hotsheets with the most profitable trading opportunities.",
        "cta_text": "Get Hotsheets",
        "offer_id": "7385",
        "aff_id": "43045"
    },
    {
        "name": "Best Gold",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045",
        "logo_url": "https://i.imgur.com/5Yb0LJn.png",
        "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg",
        "description": "Premium gold investment insights and recommendations from industry experts.",
        "cta_text": "Learn About Gold",
        "offer_id": "7390",
        "aff_id": "43045"
    }
]

def is_real_campaign(campaign_name):
    """Check if a campaign is one of Mike's real campaigns"""
    real_names = [c["name"] for c in MIKES_REAL_CAMPAIGNS]
    return campaign_name in real_names

def clean_database():
    """Remove any campaigns that aren't Mike's real ones"""
    conn = get_db_connection()
    try:
        # Get all current campaigns
        cursor = conn.execute("SELECT id, name FROM campaigns")
        campaigns = cursor.fetchall()
        
        deleted_count = 0
        for campaign in campaigns:
            campaign_id, campaign_name = campaign[0], campaign[1]
            
            # If it's not one of Mike's real campaigns, DELETE IT
            if not is_real_campaign(campaign_name):
                print(f"🗑️  DELETING FAKE CAMPAIGN: {campaign_name} (ID: {campaign_id})")
                conn.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
                deleted_count += 1
        
        conn.commit()
        print(f"🧹 Cleaned {deleted_count} fake campaigns from database")
        return deleted_count
        
    finally:
        conn.close()

def ensure_real_campaigns_exist():
    """Make sure all of Mike's real campaigns exist in the database"""
    conn = get_db_connection()
    try:
        # Get existing campaign names
        cursor = conn.execute("SELECT name FROM campaigns")
        existing_names = [row[0] for row in cursor.fetchall()]
        
        added_count = 0
        for campaign in MIKES_REAL_CAMPAIGNS:
            if campaign["name"] not in existing_names:
                print(f"➕ ADDING MISSING CAMPAIGN: {campaign['name']}")
                insert_campaign(
                    name=campaign["name"],
                    tune_url=campaign["tune_url"],
                    logo_url=campaign["logo_url"],
                    main_image_url=campaign["main_image_url"],
                    description=campaign["description"],
                    cta_text=campaign["cta_text"],
                    offer_id=campaign["offer_id"],
                    aff_id=campaign["aff_id"]
                )
                added_count += 1
            else:
                print(f"✅ REAL CAMPAIGN EXISTS: {campaign['name']}")
        
        print(f"🚀 Added {added_count} missing real campaigns")
        return added_count
        
    finally:
        conn.close()

def protect_mikes_revenue_machine():
    """
    🛡️ PROTECTION SYSTEM - DISABLED TEMPORARILY
    ⚠️  DATA LOSS PREVENTION: Do not clean database until missing campaigns are restored!
    """
    print("⚠️  PROTECTION SYSTEM DISABLED - PREVENTING FURTHER DATA LOSS")
    print("=" * 60)
    print("🚨 URGENT: 4 campaigns were lost in recent deployment")
    print("🛡️  Database cleaning is DISABLED until manual restoration")
    print("📋 Currently allowing all campaigns to prevent further deletions")
    
    # ONLY ensure real campaigns exist - DO NOT DELETE anything
    added = ensure_real_campaigns_exist()
    
    # Step 3: Report current state WITHOUT cleaning
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns")
        total_campaigns = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT name, offer_id FROM campaigns ORDER BY name")
        campaigns = cursor.fetchall()
        
        print(f"\n🎯 CURRENT DATABASE STATE:")
        print(f"   📊 Total campaigns: {total_campaigns}")
        print(f"   ➕ Added missing protected campaigns: {added}")
        print(f"   📋 All campaigns in database:")
        for name, offer_id in campaigns:
            print(f"      📍 {name} (offer_id: {offer_id})")
        
        print(f"\n⚠️  NEXT STEPS:")
        print(f"   1. Restore 4 missing campaigns manually")
        print(f"   2. Update MIKES_REAL_CAMPAIGNS list to include all 9")
        print(f"   3. Re-enable protection system")
        
        return True
            
    finally:
        conn.close()

if __name__ == "__main__":
    success = protect_mikes_revenue_machine()
    if not success:
        exit(1) 