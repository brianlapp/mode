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
    },
    {
        "name": "Daily Goodie Box",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946",
        "logo_url": "https://i.imgur.com/DH7Tp4A.jpeg",
        "main_image_url": "https://i.imgur.com/JpKD9AX.png",
        "description": "Get your daily goodie box filled with amazing free samples and deals.",
        "cta_text": "Claim Now!",
        "offer_id": "6571",
        "aff_id": "42946"
    },
    {
        "name": "Free Samples Guide",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946",
        "logo_url": "https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png",
        "main_image_url": "https://i.imgur.com/vbgSfMi.jpeg",
        "description": "Get your comprehensive free samples guide with exclusive offers.",
        "cta_text": "Claim Now!",
        "offer_id": "3907",
        "aff_id": "42946"
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
    🛡️ PROTECTION SYSTEM - PERMANENTLY PROTECT 7 CAMPAIGNS
    ✅ Updated with all 7 real campaigns including recovered ones
    """
    print("🛡️ MIKE'S REVENUE DATA PROTECTION")
    print("=" * 60)
    
    # Step 1: Ensure all 7 real campaigns exist
    added = ensure_real_campaigns_exist()
    
    # Step 2: Clean any fake campaigns (re-enabled protection)
    deleted = clean_database()
    
    # Step 3: Report final state
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns")
        total_campaigns = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT name, offer_id FROM campaigns ORDER BY name")
        campaigns = cursor.fetchall()
        
        print(f"\n🎯 FINAL DATABASE STATE:")
        print(f"   📊 Total campaigns: {total_campaigns}")
        print(f"   ➕ Added missing campaigns: {added}")
        print(f"   🗑️  Removed fake campaigns: {deleted}")
        print(f"   📋 Protected campaigns:")
        for name, offer_id in campaigns:
            print(f"      📍 {name} (offer_id: {offer_id})")
        
        print(f"\n🎉 PROTECTION SYSTEM ACTIVE!")
        print(f"✅ Your data is now BULLETPROOF against resets!")
        
        # Auto-assign all campaigns to all properties
        from routes.campaigns import auto_assign_all_campaigns
        try:
            auto_assign_all_campaigns()
            print(f"✅ All campaigns auto-assigned to all properties!")
        except Exception as e:
            print(f"⚠️  Auto-assignment failed: {e}")
        
        return True
            
    finally:
        conn.close()

if __name__ == "__main__":
    success = protect_mikes_revenue_machine()
    if not success:
        exit(1) 