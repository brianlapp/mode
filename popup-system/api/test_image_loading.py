#!/usr/bin/env python3
"""
Test script for image loading functionality
"""

import sys
import os
sys.path.append('utils')

from utils.image_loader import load_campaign_image, create_fallback_image
from database import get_db_connection

def test_image_loading():
    """Test loading campaign images"""
    print("🧪 Testing Image Loading Functionality")
    print("=" * 50)
    
    # Get a sample campaign
    conn = get_db_connection()
    cur = conn.execute("SELECT name, main_image_url FROM campaigns WHERE active = 1 LIMIT 3")
    campaigns = cur.fetchall()
    conn.close()
    
    for name, image_url in campaigns:
        print(f"\n📋 Campaign: {name}")
        print(f"🔗 URL: {image_url}")
        
        # Test image loading
        try:
            campaign_image = load_campaign_image(image_url, (280, 120))
            if campaign_image:
                print(f"✅ Successfully loaded image: {campaign_image.size}")
                
                # Save test image
                test_file = f"test_{name.replace(' ', '_').lower()}.png"
                campaign_image.save(test_file)
                print(f"💾 Saved test image: {test_file}")
            else:
                print("❌ Failed to load image")
                
                # Create fallback
                fallback = create_fallback_image((280, 120), f"FAILED: {name}")
                fallback_file = f"fallback_{name.replace(' ', '_').lower()}.png"
                fallback.save(fallback_file)
                print(f"🔄 Created fallback: {fallback_file}")
                
        except Exception as e:
            print(f"💥 Error: {str(e)}")

if __name__ == "__main__":
    test_image_loading()
