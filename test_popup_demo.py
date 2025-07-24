import asyncio
from playwright.async_api import async_playwright
import time

async def test_popup_demo():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # headless=False to see what's happening
        page = await browser.new_page()
        
        try:
            print("🚀 Testing Mode Dashboard Popup Demo...")
            
            # Navigate to the dashboard
            await page.goto("https://modedash.streamlit.app/")
            
            # Wait for page to load
            await page.wait_for_timeout(3000)
            print("✅ Dashboard loaded")
            
            # Look for the Properties Portfolio navigation
            print("🔍 Looking for Properties Portfolio button...")
            properties_button = page.locator("text=Properties Portfolio")
            if await properties_button.count() > 0:
                await properties_button.click()
                print("✅ Clicked Properties Portfolio")
                await page.wait_for_timeout(2000)
            
            # Look for the Thanks.co Analysis tab
            print("🔍 Looking for Thanks.co Analysis tab...")
            thanks_tab = page.locator("text=Thanks.co Analysis")
            if await thanks_tab.count() > 0:
                await thanks_tab.click()
                print("✅ Clicked Thanks.co Analysis tab")
                await page.wait_for_timeout(2000)
            
            # Look for the Custom Concept tab
            print("🔍 Looking for Custom Concept tab...")
            custom_tab = page.locator("text=Custom Concept")
            if await custom_tab.count() > 0:
                await custom_tab.click()
                print("✅ Clicked Custom Concept tab")
                await page.wait_for_timeout(2000)
            
            # Look for the Launch Custom Popup Demo button
            print("🔍 Looking for Launch Custom Popup Demo button...")
            demo_button = page.locator("text=Launch Custom Popup Demo")
            if await demo_button.count() > 0:
                print("✅ Found Launch Custom Popup Demo button")
                await demo_button.click()
                print("🎬 Clicked Launch Custom Popup Demo button")
                await page.wait_for_timeout(2000)
                
                # Check if popup appeared
                popup_overlay = page.locator("#modePopupOverlay")
                if await popup_overlay.count() > 0:
                    print("✅ Popup overlay element found in DOM")
                    
                    # Check if popup is visible
                    is_visible = await popup_overlay.is_visible()
                    print(f"👀 Popup visible: {is_visible}")
                    
                    if is_visible:
                        print("🎉 SUCCESS: Popup is working!")
                        
                        # Test the close button
                        close_button = page.locator("#modePopupOverlay button:has-text('×')")
                        if await close_button.count() > 0:
                            print("✅ Close button found - testing...")
                            await close_button.click()
                            await page.wait_for_timeout(1000)
                            
                            is_still_visible = await popup_overlay.is_visible()
                            print(f"🔄 Popup after close: {is_still_visible}")
                    else:
                        print("❌ ISSUE: Popup element exists but is not visible")
                        # Check the display style
                        display_style = await popup_overlay.get_attribute("style")
                        print(f"📝 Popup style: {display_style}")
                else:
                    print("❌ ISSUE: Popup overlay element not found in DOM")
            else:
                print("❌ ISSUE: Launch Custom Popup Demo button not found")
                
                # List all available buttons for debugging
                all_buttons = await page.locator("button").all()
                print(f"🔍 Found {len(all_buttons)} buttons on page:")
                for i, button in enumerate(all_buttons[:10]):  # Show first 10
                    text = await button.text_content()
                    if text and text.strip():
                        print(f"  {i+1}. '{text.strip()}'")
            
            # Take a screenshot for debugging
            await page.screenshot(path="popup_test_screenshot.png")
            print("📸 Screenshot saved as popup_test_screenshot.png")
            
            # Keep browser open for 10 seconds to see the result
            print("⏳ Keeping browser open for 10 seconds...")
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"❌ Error during test: {e}")
            await page.screenshot(path="error_screenshot.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_popup_demo()) 