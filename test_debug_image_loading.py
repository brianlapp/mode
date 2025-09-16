#!/usr/bin/env python3
"""
Test script to verify image loading debug information on Railway
"""

import requests
import json

def test_debug_image_loading():
    """Test debug endpoint to verify image loading is working"""
    print("🧪 Testing Railway Image Loading Debug")
    print("=" * 50)
    
    # Test both properties
    properties = ['mff', 'mmm']
    
    for prop in properties:
        print(f"\n📋 Testing {prop.upper()} property:")
        
        # Get debug info (this doesn't actually generate images but tests the function)
        debug_url = f"https://mode-dash-production.up.railway.app/api/email/ad.debug?property={prop}"
        
        try:
            response = requests.get(debug_url, timeout=10)
            if response.status_code == 200:
                debug_data = response.json()
                
                print(f"✅ Debug endpoint working")
                print(f"📊 Active campaigns: {debug_data.get('active_campaigns', 'N/A')}")
                
                campaign = debug_data.get('campaign')
                if campaign:
                    print(f"🎯 Selected campaign: {campaign.get('name', 'N/A')}")
                    print(f"🔗 Image URL: {campaign.get('main_image_url', 'N/A')}")
                else:
                    print("❌ No campaign data in debug")
                    
            else:
                print(f"❌ Debug endpoint failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Now test actual PNG generation with a single request to see debug info
    print(f"\n🎨 Testing actual PNG generation:")
    png_url = "https://mode-dash-production.up.railway.app/api/email/ad.png?property=mff&w=600&h=400"
    
    try:
        response = requests.get(png_url, timeout=15)
        if response.status_code == 200:
            print(f"✅ PNG generated successfully ({len(response.content)} bytes)")
            
            # Check if it's a proper PNG
            if response.content.startswith(b'\x89PNG'):
                print("✅ Valid PNG file format")
            else:
                print("❌ Not a valid PNG file")
                print(f"First 50 bytes: {response.content[:50]}")
        else:
            print(f"❌ PNG generation failed: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error generating PNG: {e}")

if __name__ == "__main__":
    test_debug_image_loading()
