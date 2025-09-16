#!/usr/bin/env python3
"""
Image URL Diagnostic Script
Tests all campaign image URLs to identify broken ones
"""

import requests
import sqlite3
import json
from urllib.parse import urlparse
from pathlib import Path

def test_image_url(url):
    """Test if an image URL is working"""
    if not url:
        return "Empty URL"
    
    try:
        # Fix common imgur issues
        if "imgur.com/" in url and not url.startswith("https://i.imgur.com/"):
            url = url.replace("imgur.com/", "i.imgur.com/")
            if not url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                url += '.jpg'
        
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache'
        })
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                return f"✅ OK ({len(response.content)} bytes, {content_type})"
            else:
                return f"❌ Not an image: {content_type}"
        elif response.status_code == 404:
            return "❌ HTTP 404 - Not Found"
        elif response.status_code == 429:
            return "⚠️ HTTP 429 - Rate Limited"
        else:
            return f"❌ HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return "⏱️ Timeout"
    except requests.exceptions.ConnectionError:
        return "🔌 Connection Error"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def test_campaign_images():
    """Test all campaign image URLs"""
    db_path = Path(__file__).parent / "popup_campaigns.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return []
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, main_image_url, logo_url FROM campaigns WHERE active = 1")
        campaigns = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return []
    finally:
        conn.close()
    
    results = []
    print(f"\n🔍 Testing {len(campaigns)} active campaigns...\n")
    
    for campaign in campaigns:
        id, name, main_url, logo_url = campaign
        
        print(f"📋 Campaign: {name} (ID: {id})")
        
        # Test main image
        main_status = test_image_url(main_url)
        print(f"   📸 Main Image: {main_status}")
        if main_url:
            print(f"      URL: {main_url}")
        
        # Test logo
        logo_status = test_image_url(logo_url) if logo_url else "No logo URL"
        if logo_url:
            print(f"   🏷️ Logo: {logo_status}")
            print(f"      URL: {logo_url}")
        else:
            print(f"   🏷️ Logo: {logo_status}")
        
        results.append({
            "id": id,
            "campaign": name,
            "main_image": {"url": main_url, "status": main_status},
            "logo": {"url": logo_url, "status": logo_status}
        })
        print()
    
    return results

def generate_report(results):
    """Generate summary report"""
    total = len(results)
    main_working = sum(1 for r in results if "✅ OK" in r['main_image']['status'])
    logo_working = sum(1 for r in results if r['logo']['url'] and "✅ OK" in r['logo']['status'])
    
    print("=" * 60)
    print("📊 SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Campaigns: {total}")
    print(f"Main Images Working: {main_working}/{total} ({main_working/total*100:.1f}%)")
    print(f"Logo Images Working: {logo_working}/{total} ({logo_working/total*100:.1f}%)")
    print()
    
    # Show broken campaigns
    broken_main = [r for r in results if "✅ OK" not in r['main_image']['status']]
    if broken_main:
        print("🚨 CAMPAIGNS WITH BROKEN MAIN IMAGES:")
        for r in broken_main:
            print(f"   • {r['campaign']}: {r['main_image']['status']}")
        print()
    
    broken_logo = [r for r in results if r['logo']['url'] and "✅ OK" not in r['logo']['status']]
    if broken_logo:
        print("⚠️ CAMPAIGNS WITH BROKEN LOGOS:")
        for r in broken_logo:
            print(f"   • {r['campaign']}: {r['logo']['status']}")
        print()
    
    # Save detailed results
    report_file = Path(__file__).parent / "image_test_results.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Detailed results saved to: {report_file}")

if __name__ == "__main__":
    print("🖼️ Campaign Image URL Diagnostic Tool")
    print("=" * 50)
    
    results = test_campaign_images()
    if results:
        generate_report(results)
    else:
        print("❌ No results to analyze")
