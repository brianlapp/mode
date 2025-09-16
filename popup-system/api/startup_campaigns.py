#!/usr/bin/env python3
"""
🛡️ MIKE'S REVENUE MACHINE PROTECTION SYSTEM
Ensures only real campaigns exist - NO MORE TEST CAMPAIGN ZOMBIES!
"""

import sqlite3
from database import get_db_connection, insert_campaign

# Mike's CORE campaigns - used for bootstrap/recovery only (not for deletion validation)
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
    },
    # 🎯 MISSING MFF CAMPAIGNS - RESTORED FROM BACKUP
    {
        "name": "UpLevel - Amazon Mystery Box",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks",
        "logo_url": "https://imgur.com/Xmb1P8t.jpg",
        "main_image_url": "https://imgur.com/tA8fYBO.jpg",
        "description": "Grab an Amazon Mystery Box!",
        "cta_text": "Get Box!",
        "offer_id": "4689",
        "aff_id": "42946"
    },
    {
        "name": "Hulu - Hit Movies, TV and More!",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946&aff_sub2=perks",
        "logo_url": "https://imgur.com/RHRuCvk.jpg",
        "main_image_url": "https://imgur.com/SEu1NtW.jpg",
        "description": "Exclusive Offers from Hulu!",
        "cta_text": "Get Hulu!",
        "offer_id": "5555",
        "aff_id": "42946"
    },
    {
        "name": "Paramount",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946&aff_sub2=perks",
        "logo_url": "https://imgur.com/2IpSLaY.jpg",
        "main_image_url": "https://imgur.com/p8o0YSR.jpg",
        "description": "Exclusive Offers from Paramount+!",
        "cta_text": "Get Paramount+!",
        "offer_id": "5172",
        "aff_id": "42946"
    },
    {
        "name": "Trend'n Daily",
        "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks",
        "logo_url": "https://imgur.com/Xmb1P8t.jpg",
        "main_image_url": "https://imgur.com/tA8fYBO.jpg",
        "description": "Grab an Amazon Mystery Box!",
        "cta_text": "Get Box!",
        "offer_id": "4689",
        "aff_id": "42946"
    },
]

def is_legitimate_campaign(campaign_data):
    """
    Smart campaign validation - checks multiple criteria instead of hardcoded names
    """
    campaign_id, campaign_name, offer_id, aff_id = campaign_data
    
    # Criteria 1: Must have valid affiliate ID (Mike's two properties)
    valid_aff_ids = ["43045", "42946"]  # MMM and MFF
    if str(aff_id) not in valid_aff_ids:
        print(f"❌ Invalid aff_id: {campaign_name} has aff_id {aff_id}")
        return False
    
    # Criteria 2: Must have valid offer_id (not empty, not test values)
    if not offer_id or offer_id in ["0", "999", "test", "demo"]:
        print(f"❌ Invalid offer_id: {campaign_name} has offer_id '{offer_id}'")
        return False
    
    # Criteria 3: Must have reasonable campaign name (not test/debug names)
    test_names = ["test", "debug", "demo", "sample", "fake", "temp"]
    if any(test_word in campaign_name.lower() for test_word in test_names):
        print(f"❌ Test campaign name: {campaign_name}")
        return False
    
    print(f"✅ Legitimate campaign: {campaign_name} (aff_id: {aff_id}, offer_id: {offer_id})")
    return True

def clean_database():
    """Remove campaigns that don't meet legitimacy criteria (smart validation)"""
    conn = get_db_connection()
    try:
        # Get all current campaigns with full data for validation
        cursor = conn.execute("SELECT id, name, offer_id, aff_id FROM campaigns")
        campaigns = cursor.fetchall()
        
        deleted_count = 0
        for campaign_data in campaigns:
            campaign_id = campaign_data[0]
            campaign_name = campaign_data[1]
            
            # Use smart validation instead of hardcoded names
            if not is_legitimate_campaign(campaign_data):
                print(f"🗑️  DELETING ILLEGITIMATE CAMPAIGN: {campaign_name} (ID: {campaign_id})")
                conn.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
                deleted_count += 1
        
        conn.commit()
        print(f"🧹 Cleaned {deleted_count} illegitimate campaigns from database")
        return deleted_count
        
    finally:
        conn.close()

def ensure_core_campaigns_exist():
    """Bootstrap: ensure core campaigns exist if database is empty/corrupted"""
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
    🛡️ SMART PROTECTION SYSTEM - PROTECT LEGITIMATE CAMPAIGNS
    ✅ Uses intelligent validation instead of hardcoded lists
    ✅ Future-proof: works with any number of legitimate campaigns
    """
    print("🛡️ MIKE'S REVENUE DATA PROTECTION (SMART MODE)")
    print("=" * 60)
    
    # Step 1: Ensure core campaigns exist (bootstrap if empty)
    added = ensure_core_campaigns_exist()
    
    # Step 2: Clean illegitimate campaigns using smart criteria
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