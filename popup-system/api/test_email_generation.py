#!/usr/bin/env python3
"""
Test email PNG generation with actual campaign images
"""

import sys
import os
from main import create_popup_style_email_ad
from database import get_db_connection

def test_email_generation():
    """Test email generation with real campaign data"""
    print("🧪 Testing Email PNG Generation")
    print("=" * 50)
    
    # Get a sample campaign
    conn = get_db_connection()
    cur = conn.execute("""
        SELECT name, description, main_image_url, logo_url, cta_text 
        FROM campaigns 
        WHERE active = 1 AND name != 'Prizies'
        ORDER BY RANDOM() 
        LIMIT 1
    """)
    campaign = cur.fetchone()
    conn.close()
    
    if not campaign:
        print("❌ No campaigns found")
        return
    
    campaign_data = {
        'name': campaign[0],
        'description': campaign[1],
        'main_image_url': campaign[2],
        'logo_url': campaign[3],
        'cta_text': campaign[4]
    }
    
    print(f"📋 Selected Campaign: {campaign_data['name']}")
    print(f"🔗 Image URL: {campaign_data['main_image_url']}")
    
    # Test different sizes
    test_sizes = [
        (600, 400, "mff"),
        (600, 400, "mmm")
    ]
    
    for width, height, property_name in test_sizes:
        print(f"\n🎨 Generating {width}x{height} for {property_name.upper()}")
        
        try:
            png_bytes, debug_info = create_popup_style_email_ad(property_name, width, height, campaign_data)
            
            # Save test file
            filename = f"test_email_{property_name}_{width}x{height}.png"
            with open(filename, 'wb') as f:
                f.write(png_bytes)
            
            print(f"✅ Generated: {filename} ({len(png_bytes)} bytes)")
            
            # Print debug info
            if debug_info.get('image_loading'):
                print(f"🖼️ Image Loading: {debug_info['image_loading']}")
            if debug_info.get('errors'):
                print(f"⚠️ Errors: {debug_info['errors']}")
                
        except Exception as e:
            print(f"❌ Error generating {property_name}: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_email_generation()