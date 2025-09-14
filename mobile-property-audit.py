#!/usr/bin/env python3
"""
Mobile Property Visual Audit Script
Captures mobile screenshots of Mode properties for visual optimization analysis
"""

import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime
import json

# Property URLs to audit
PROPERTIES = {
    "ModeFreeFinds": {
        "landing_page": "https://modefreefinds.com",
        "signup_flow": "https://join.modefreefinds.com/mff-meta-dgbcpcthanks",
        "thank_you": "https://join.modefreefinds.com/mff-ty-meta-dgbcpcthanks/?email=test@example.com",
        "status": "live",
        "description": "Free Stuff Content Site - $25k-$35k monthly"
    },
    "ModeMarketMunchies": {
        "landing_page": "https://modemarketmunchies.com",
        "signup_flow": None,  # No monetization yet
        "thank_you": None,
        "status": "launched",
        "description": "Finance Content Site - Just launched"
    },
    "ModeMobileDaily": {
        "landing_page": "https://modemobiledaily.com",
        "signup_flow": None,
        "thank_you": None,
        "status": "development",
        "description": "Viral News Site - In development"
    },
    "ModeClassActionsDaily": {
        "landing_page": "https://modeclassactionsdaily.com",
        "signup_flow": None,
        "thank_you": None,
        "status": "development", 
        "description": "Class Action Awareness - In development"
    }
}

async def capture_mobile_screenshots():
    """Capture mobile screenshots of all Mode properties"""
    
    # Create screenshots directory
    screenshots_dir = "property-screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_results = {
        "timestamp": timestamp,
        "properties": {},
        "mobile_device": "iPhone 12 Pro"
    }
    
    async with async_playwright() as p:
        # Launch browser with mobile emulation
        browser = await p.chromium.launch(headless=True)
        
        # iPhone 12 Pro mobile viewport
        context = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
        )
        
        page = await context.new_page()
        
        for property_name, property_data in PROPERTIES.items():
            print(f"\n📱 Capturing {property_name}...")
            
            property_dir = os.path.join(screenshots_dir, property_name.lower().replace(' ', '-'))
            os.makedirs(property_dir, exist_ok=True)
            
            property_results = {
                "status": property_data["status"],
                "description": property_data["description"],
                "screenshots": {},
                "page_info": {}
            }
            
            # Capture landing page
            if property_data["landing_page"]:
                try:
                    print(f"  📄 Landing page: {property_data['landing_page']}")
                    await page.goto(property_data["landing_page"], wait_until="networkidle", timeout=30000)
                    await page.wait_for_timeout(3000)  # Wait for dynamic content
                    
                    # Capture full page screenshot
                    screenshot_path = os.path.join(property_dir, f"landing-page-mobile-{timestamp}.png")
                    await page.screenshot(path=screenshot_path, full_page=True)
                    
                    # Get page info
                    title = await page.title()
                    url = page.url
                    
                    property_results["screenshots"]["landing_page"] = screenshot_path
                    property_results["page_info"]["landing_page"] = {
                        "title": title,
                        "url": url,
                        "accessible": True
                    }
                    
                    print(f"    ✅ Screenshot saved: {screenshot_path}")
                    print(f"    📋 Title: {title}")
                    
                except Exception as e:
                    print(f"    ❌ Error capturing landing page: {e}")
                    property_results["page_info"]["landing_page"] = {
                        "accessible": False,
                        "error": str(e)
                    }
            
            # Capture signup flow (if exists)
            if property_data["signup_flow"]:
                try:
                    print(f"  📝 Signup flow: {property_data['signup_flow']}")
                    await page.goto(property_data["signup_flow"], wait_until="networkidle", timeout=30000)
                    await page.wait_for_timeout(3000)
                    
                    screenshot_path = os.path.join(property_dir, f"signup-flow-mobile-{timestamp}.png")
                    await page.screenshot(path=screenshot_path, full_page=True)
                    
                    title = await page.title()
                    property_results["screenshots"]["signup_flow"] = screenshot_path
                    property_results["page_info"]["signup_flow"] = {
                        "title": title,
                        "url": property_data["signup_flow"],
                        "accessible": True
                    }
                    
                    print(f"    ✅ Screenshot saved: {screenshot_path}")
                    
                except Exception as e:
                    print(f"    ❌ Error capturing signup flow: {e}")
                    property_results["page_info"]["signup_flow"] = {
                        "accessible": False,
                        "error": str(e)
                    }
            
            # Capture thank you page (if exists)
            if property_data["thank_you"]:
                try:
                    print(f"  🎉 Thank you page: {property_data['thank_you']}")
                    await page.goto(property_data["thank_you"], wait_until="networkidle", timeout=30000)
                    await page.wait_for_timeout(5000)  # Extra wait for Thanks.co popup
                    
                    screenshot_path = os.path.join(property_dir, f"thank-you-page-mobile-{timestamp}.png")
                    await page.screenshot(path=screenshot_path, full_page=True)
                    
                    title = await page.title()
                    property_results["screenshots"]["thank_you"] = screenshot_path
                    property_results["page_info"]["thank_you"] = {
                        "title": title,
                        "url": property_data["thank_you"],
                        "accessible": True
                    }
                    
                    print(f"    ✅ Screenshot saved: {screenshot_path}")
                    
                except Exception as e:
                    print(f"    ❌ Error capturing thank you page: {e}")
                    property_results["page_info"]["thank_you"] = {
                        "accessible": False,
                        "error": str(e)
                    }
            
            audit_results["properties"][property_name] = property_results
        
        await browser.close()
    
    # Save audit results
    results_file = f"mobile-audit-results-{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(audit_results, f, indent=2)
    
    print(f"\n📊 Audit complete! Results saved to {results_file}")
    return audit_results

async def main():
    """Main execution function"""
    print("🚀 Starting Mode Properties Mobile Visual Audit")
    print("📱 Device: iPhone 12 Pro (390x844)")
    print("=" * 60)
    
    results = await capture_mobile_screenshots()
    
    print("\n" + "=" * 60)
    print("📊 AUDIT SUMMARY")
    print("=" * 60)
    
    for prop_name, prop_data in results["properties"].items():
        print(f"\n🏢 {prop_name}")
        print(f"   Status: {prop_data['status']}")
        print(f"   Screenshots: {len(prop_data['screenshots'])} captured")
        
        for page_type, screenshot_path in prop_data["screenshots"].items():
            print(f"   📱 {page_type}: {screenshot_path}")
    
    print(f"\n✅ Complete audit saved: mobile-audit-results-{results['timestamp']}.json")

if __name__ == "__main__":
    asyncio.run(main()) 