"""
Emergency restoration endpoint for Railway
Add this to main.py to allow immediate campaign restoration
"""

@app.post("/api/emergency-restore-12-campaigns")
async def emergency_restore_12_campaigns():
    """Emergency endpoint to restore all 12 campaigns with property attribution"""
    import sqlite3
    import json
    from database import get_db_path
    
    try:
        print("🚨 EMERGENCY RESTORATION: Restoring 12 campaigns")
        
        # Campaign data to restore
        campaigns_data = [
            # MMM Finance campaigns (aff_id 43045)
            {"id": 1, "name": "Trading Tips", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips", "logo_url": "https://i.imgur.com/lHn301q.png", "main_image_url": "https://i.imgur.com/ZVGOktR.png", "description": "Get exclusive trading tips and market insights delivered daily to your inbox.", "cta_text": "Get Trading Tips", "offer_id": "6998", "aff_id": "43045", "active": True},
            {"id": 2, "name": "Behind The Markets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045&aff_sub5=popup_behindMarkets", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Discover what's really happening behind the financial markets with expert analysis.", "cta_text": "Learn More", "offer_id": "7521", "aff_id": "43045", "active": True},
            {"id": 3, "name": "Brownstone Research", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045&aff_sub5=popup_brownstone", "logo_url": "https://i.imgur.com/3KVDcV7.jpeg", "main_image_url": "https://i.imgur.com/vzoiVpd.png", "description": "Advanced technology and investment research from Brownstone Research experts.", "cta_text": "View Research", "offer_id": "7389", "aff_id": "43045", "active": True},
            {"id": 4, "name": "Hotsheets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045&aff_sub5=popup_hotsheets", "logo_url": "https://i.imgur.com/4JoGdZr.png", "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg", "description": "Daily market hotsheets with the most profitable trading opportunities.", "cta_text": "Get Hotsheets", "offer_id": "7385", "aff_id": "43045", "active": True},
            {"id": 5, "name": "Best Gold", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045&aff_sub5=popup_bestGold", "logo_url": "https://i.imgur.com/5Yb0LJn.png", "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg", "description": "Premium gold investment insights and recommendations from industry experts.", "cta_text": "Learn About Gold", "offer_id": "7390", "aff_id": "43045", "active": True},
            
            # MFF Lifestyle campaigns (aff_id 42946)
            {"id": 6, "name": "Daily Goodie Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946&aff_sub2=perks", "logo_url": "https://i.imgur.com/DH7Tp4A.jpeg", "main_image_url": "https://i.imgur.com/JpKD9AX.png", "description": "Get your daily goodie box filled with amazing free samples and deals.", "cta_text": "Claim Now!", "offer_id": "6571", "aff_id": "42946", "active": True},
            {"id": 7, "name": "Free Samples Guide", "tune_url": "https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946&aff_sub2=perks", "logo_url": "https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png", "main_image_url": "https://i.imgur.com/vbgSfMi.jpeg", "description": "Get your comprehensive free samples guide with exclusive offers.", "cta_text": "Claim Now!", "offer_id": "3907", "aff_id": "42946", "active": True},
            {"id": 8, "name": "Prizies", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7774&aff_id=42946&aff_sub2=perks", "logo_url": "https://imgur.com/QEt3znb.jpg", "main_image_url": "https://imgur.com/KCp0xqn.jpg", "description": "Win $1,000 Cashapp!", "cta_text": "Win Now!", "offer_id": "7774", "aff_id": "42946", "active": True},
            {"id": 9, "name": "Hulu - Hit Movies, TV and More!", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946&aff_sub2=perks", "logo_url": "https://imgur.com/RHRuCvk.jpg", "main_image_url": "https://imgur.com/SEu1NtW.jpg", "description": "Exclusive Offers from Hulu!", "cta_text": "Get Hulu!", "offer_id": "5555", "aff_id": "42946", "active": True},
            {"id": 10, "name": "Paramount", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946&aff_sub2=perks", "logo_url": "https://imgur.com/2IpSLaY.jpg", "main_image_url": "https://imgur.com/p8o0YSR.jpg", "description": "Exclusive Offers from Paramount+!", "cta_text": "Get Paramount+!", "offer_id": "5172", "aff_id": "42946", "active": True},
            {"id": 11, "name": "Trend'n Daily", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks", "logo_url": "https://imgur.com/Xmb1P8t.jpg", "main_image_url": "https://imgur.com/tA8fYBO.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "active": True},
            {"id": 12, "name": "Prizies", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7774&aff_id=42946&aff_sub2=perks", "logo_url": "https://imgur.com/QEt3znb.jpg", "main_image_url": "https://imgur.com/KCp0xqn.jpg", "description": "Win $1,000 Cashapp!", "cta_text": "Win!", "offer_id": "3752", "aff_id": "42946", "active": True}
        ]
        
        conn = sqlite3.connect(get_db_path())
        
        # Clear and restore campaigns
        conn.execute("DELETE FROM campaigns")
        conn.execute("DELETE FROM campaign_properties")
        
        for campaign in campaigns_data:
            conn.execute('''
                INSERT INTO campaigns (
                    id, name, tune_url, logo_url, main_image_url, description,
                    cta_text, offer_id, aff_id, active, featured
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            ''', (
                campaign['id'], campaign['name'], campaign['tune_url'],
                campaign['logo_url'], campaign['main_image_url'], campaign['description'],
                campaign['cta_text'], campaign['offer_id'], campaign['aff_id'], campaign['active']
            ))
            
            # Set property assignment
            property_code = 'mmm' if campaign['aff_id'] == '43045' else 'mff'
            conn.execute('''
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active
                ) VALUES (?, ?, 100, 1)
            ''', (campaign['id'], property_code))
        
        conn.commit()
        conn.close()
        
        print("✅ Emergency restoration complete: 12 campaigns with property attribution")
        
        return {
            "status": "success",
            "message": "All 12 campaigns restored with property attribution",
            "campaigns_restored": len(campaigns_data),
            "mmm_campaigns": 5,
            "mff_campaigns": 7
        }
        
    except Exception as e:
        print(f"❌ Emergency restoration failed: {e}")
        return {
            "status": "error", 
            "message": f"Restoration failed: {e}"
        }
