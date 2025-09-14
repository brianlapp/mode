#!/usr/bin/env python3
"""
Playwright test to verify demo navigation works correctly
Tests that clicking "View Thanks.co Demo" from homepage navigates to the demo tab and shows popup
"""

import asyncio
from playwright.async_api import async_playwright
import time

async def test_demo_navigation():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()
        
        try:
            print("🚀 Starting demo navigation test...")
            
            # Navigate to the dashboard
            print("📍 Navigating to dashboard...")
            await page.goto("http://localhost:8501")
            
            # Wait for page to load
            await page.wait_for_timeout(3000)
            
            # Take initial screenshot
            await page.screenshot(path="test_screenshots/01_homepage.png")
            print("📸 Screenshot: Homepage loaded")
            
            # Look for and click the demo link button
            print("🔍 Looking for 'View Thanks.co Demo' button...")
            demo_button = page.get_by_text("🔗 View Thanks.co Demo")
            
            if await demo_button.count() > 0:
                print("✅ Found demo button - clicking it...")
                await demo_button.click()
                
                # Wait for navigation
                await page.wait_for_timeout(2000)
                
                # Take screenshot after navigation
                await page.screenshot(path="test_screenshots/02_after_demo_click.png")
                print("📸 Screenshot: After clicking demo button")
                
                # Check if we're on Properties Hub page
                properties_hub_text = page.get_by_text("🏢 Mode Properties Hub")
                if await properties_hub_text.count() > 0:
                    print("✅ Successfully navigated to Properties Hub!")
                    
                    # Check if we're on the DEMO tab (first tab)
                    demo_tab = page.get_by_text("🎬 DEMO")
                    if await demo_tab.count() > 0:
                        print("✅ DEMO tab is visible!")
                        
                        # Check if the popup demo content is visible
                        demo_content = page.get_by_text("Interactive Custom Popup Demo")
                        if await demo_content.count() > 0:
                            print("✅ Demo content is loaded!")
                            
                            # Look for the popup demo itself
                            popup_overlay = page.locator("#modePopupOverlay")
                            if await popup_overlay.count() > 0:
                                print("✅ Popup demo is present on page!")
                                
                                # Check if popup is visible (should auto-show)
                                is_visible = await popup_overlay.is_visible()
                                if is_visible:
                                    print("🎉 SUCCESS: Popup is auto-displayed!")
                                else:
                                    print("⚠️  Popup exists but not visible - might need to click Launch Demo")
                                    
                                    # Try clicking Launch Demo button
                                    launch_button = page.get_by_text("🎬 Launch Interactive Demo")
                                    if await launch_button.count() > 0:
                                        await launch_button.click()
                                        await page.wait_for_timeout(1000)
                                        
                                        is_visible_after_click = await popup_overlay.is_visible()
                                        if is_visible_after_click:
                                            print("🎉 SUCCESS: Popup displayed after clicking Launch Demo!")
                                        else:
                                            print("❌ Popup still not visible after clicking")
                            else:
                                print("❌ Popup overlay not found")
                        else:
                            print("❌ Demo content not found")
                    else:
                        print("❌ DEMO tab not found")
                else:
                    print("❌ Not on Properties Hub page")
            else:
                print("❌ Demo button not found on homepage")
            
            # Take final screenshot
            await page.screenshot(path="test_screenshots/03_final_state.png")
            print("📸 Screenshot: Final state")
            
            # Keep browser open for manual inspection
            print("\n🔍 Browser will stay open for 10 seconds for manual inspection...")
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            await page.screenshot(path="test_screenshots/error_screenshot.png")
        
        finally:
            await browser.close()
            print("🔚 Test completed!")

if __name__ == "__main__":
    # Create screenshots directory
    import os
    os.makedirs("test_screenshots", exist_ok=True)
    
    # Run the test
    asyncio.run(test_demo_navigation()) 