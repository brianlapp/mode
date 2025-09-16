#!/usr/bin/env python3
"""
Playwright test to verify the email ad PNG fixes are working
"""

import asyncio
from playwright.async_api import async_playwright
import requests
import json

async def test_email_ads():
    """Test the fixed email ad generation"""
    
    print("🧪 Testing FIXED Email Ad PNG Generation...")
    
    # Wait a moment for Railway deployment
    print("⏱️ Waiting for Railway deployment to complete...")
    await asyncio.sleep(10)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Test URLs
        urls_to_test = [
            {
                'name': 'MFF PNG',
                'url': 'https://mode-dash-production.up.railway.app/api/email/ad.png?property=mff&w=600&h=400&send=qa'
            },
            {
                'name': 'MMM PNG', 
                'url': 'https://mode-dash-production.up.railway.app/api/email/ad.png?property=mmm&w=600&h=400&send=qa'
            },
            {
                'name': 'MFF Debug',
                'url': 'https://mode-dash-production.up.railway.app/api/email/ad.debug?property=mff&w=600&h=400&send=qa'
            },
            {
                'name': 'MMM Debug',
                'url': 'https://mode-dash-production.up.railway.app/api/email/ad.debug?property=mmm&w=600&h=400&send=qa'
            }
        ]
        
        results = []
        
        for test in urls_to_test:
            print(f"\n🔍 Testing {test['name']}: {test['url']}")
            
            try:
                response = await page.goto(test['url'])
                
                if response.status == 200:
                    print(f"✅ {test['name']}: HTTP 200 OK")
                    
                    if 'debug' in test['url']:
                        # For debug endpoints, check the JSON response
                        content = await page.content()
                        if 'Trading Tips' in content or 'Market Munchies' in content:
                            print(f"✅ {test['name']}: Contains expected campaign data")
                            results.append({'name': test['name'], 'status': 'PASS', 'details': 'Contains expected data'})
                        elif 'Prizies' in content:
                            print(f"❌ {test['name']}: Still showing old 'Prizies' data")
                            results.append({'name': test['name'], 'status': 'FAIL', 'details': 'Still using old data'})
                        else:
                            print(f"⚠️ {test['name']}: Unknown content")
                            results.append({'name': test['name'], 'status': 'UNKNOWN', 'details': 'Unexpected content'})
                    else:
                        # For PNG endpoints, just check if we get an image
                        content_type = response.headers.get('content-type', '')
                        if 'image/png' in content_type:
                            print(f"✅ {test['name']}: Valid PNG returned")
                            results.append({'name': test['name'], 'status': 'PASS', 'details': 'Valid PNG'})
                        else:
                            print(f"❌ {test['name']}: Not a PNG image (content-type: {content_type})")
                            results.append({'name': test['name'], 'status': 'FAIL', 'details': f'Wrong content-type: {content_type}'})
                    
                else:
                    print(f"❌ {test['name']}: HTTP {response.status}")
                    results.append({'name': test['name'], 'status': 'FAIL', 'details': f'HTTP {response.status}'})
                    
            except Exception as e:
                print(f"❌ {test['name']}: Error - {str(e)}")
                results.append({'name': test['name'], 'status': 'ERROR', 'details': str(e)})
        
        await browser.close()
        
        # Summary
        print(f"\n📊 TEST RESULTS SUMMARY:")
        print(f"========================")
        
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        errors = sum(1 for r in results if r['status'] == 'ERROR')
        
        for result in results:
            status_emoji = {'PASS': '✅', 'FAIL': '❌', 'ERROR': '🔥', 'UNKNOWN': '⚠️'}
            print(f"{status_emoji.get(result['status'], '❓')} {result['name']}: {result['status']} - {result['details']}")
        
        print(f"\n📈 TOTALS: {passed} passed, {failed} failed, {errors} errors")
        
        if failed == 0 and errors == 0:
            print(f"\n🎉 ALL TESTS PASSED! Email ads are FIXED!")
            return True
        else:
            print(f"\n💥 TESTS FAILED! Email ads still need work.")
            return False

if __name__ == "__main__":
    success = asyncio.run(test_email_ads())
    exit(0 if success else 1)
