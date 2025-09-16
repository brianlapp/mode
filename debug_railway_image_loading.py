#!/usr/bin/env python3
"""
Debug script to see exactly what's happening with image loading on Railway
"""

import urllib.request
import json

def debug_railway_image_loading():
    """Debug Railway image loading issue"""
    print("🔍 DEBUGGING RAILWAY IMAGE LOADING")
    print("=" * 50)
    
    # Test the debug endpoint to see what's happening
    debug_url = "https://mode-dash-production.up.railway.app/api/email/ad.debug?property=mff"
    
    try:
        with urllib.request.urlopen(debug_url, timeout=10) as response:
            debug_data = json.loads(response.read().decode())
            
        print("📊 DEBUG INFO:")
        print(f"   System: {debug_data.get('SYSTEM', 'N/A')}")
        print(f"   PIL Available: {debug_data.get('pil_available', 'N/A')}")
        print(f"   Active Campaigns: {debug_data.get('active_campaigns', 'N/A')}")
        
        campaign = debug_data.get('campaign')
        if campaign:
            print(f"\n🎯 CAMPAIGN INFO:")
            print(f"   Name: {campaign.get('name', 'N/A')}")
            print(f"   Image URL: {campaign.get('main_image_url', 'N/A')}")
            
            # Test if we can fetch this image URL directly
            image_url = campaign.get('main_image_url')
            if image_url:
                print(f"\n🔗 TESTING IMAGE URL: {image_url}")
                
                # Fix imgur URL if needed
                fixed_url = image_url
                if "imgur.com/" in fixed_url and not fixed_url.startswith("https://i.imgur.com/"):
                    fixed_url = fixed_url.replace("imgur.com/", "i.imgur.com/")
                    if not fixed_url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                        fixed_url += '.jpg'
                    print(f"   Fixed URL: {fixed_url}")
                
                try:
                    req = urllib.request.Request(fixed_url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                    
                    with urllib.request.urlopen(req, timeout=10) as img_response:
                        if img_response.status == 200:
                            content_length = len(img_response.read())
                            print(f"   ✅ Image accessible: {content_length} bytes")
                        else:
                            print(f"   ❌ HTTP {img_response.status}")
                            
                except Exception as e:
                    print(f"   ❌ Image fetch error: {e}")
        else:
            print("❌ No campaign data found")
            
        # Check if there's any image_loading debug info
        if 'image_loading' in debug_data:
            print(f"\n🖼️ IMAGE LOADING DEBUG: {debug_data['image_loading']}")
        else:
            print("\n⚠️ NO IMAGE LOADING DEBUG INFO - This means the image loading code isn't running!")
            
    except Exception as e:
        print(f"❌ Debug request failed: {e}")

if __name__ == "__main__":
    debug_railway_image_loading()
