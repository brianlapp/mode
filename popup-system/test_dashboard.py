#!/usr/bin/env python3
"""
Test the Mode Dashboard with Playwright to see what's actually happening
"""

from playwright.sync_api import sync_playwright
import time

def test_dashboard():
    with sync_playwright() as p:
        print("🚀 Starting Playwright test of Mode Dashboard...")
        
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set to False so we can see what's happening
        page = browser.new_page()
        
        try:
            # Go to the dashboard
            print("📍 Navigating to dashboard...")
            page.goto("https://mode-dash-production.up.railway.app/admin")
            
            # Wait for page to load
            print("⏳ Waiting for page to load...")
            page.wait_for_timeout(3000)
            
            # Take a screenshot
            print("📸 Taking screenshot...")
            page.screenshot(path="dashboard_test.png")
            
            # Check page title
            title = page.title()
            print(f"📄 Page title: {title}")
            
            # Check if campaigns table exists
            campaigns_table = page.locator("#campaigns-table")
            print(f"🗂️ Campaigns table exists: {campaigns_table.count() > 0}")
            
            # Check if Add Campaign button exists
            add_button = page.locator("#addCampaignBtn")
            print(f"🔘 Add Campaign button exists: {add_button.count() > 0}")
            
            if add_button.count() > 0:
                print(f"🔘 Add Campaign button text: '{add_button.text_content()}'")
            
            # Check table content
            if campaigns_table.count() > 0:
                table_content = campaigns_table.inner_html()
                print(f"📋 Table content preview (first 200 chars): {table_content[:200]}...")
                
                # Count rows
                rows = page.locator("#campaigns-table tr")
                print(f"📊 Number of table rows: {rows.count()}")
                
                # Check if "No campaigns yet" is showing
                if "No campaigns yet" in table_content:
                    print("❌ Table shows 'No campaigns yet' - campaigns not loading!")
                else:
                    print("✅ Table appears to have campaign data")
            
            # Check console logs for JavaScript errors
            print("\n🔍 Checking for JavaScript errors...")
            page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
            
            # Test the Add Campaign button
            if add_button.count() > 0:
                print("\n🔘 Testing Add Campaign button...")
                try:
                    add_button.click()
                    page.wait_for_timeout(1000)
                    
                    # Check if modal opened
                    modal = page.locator("#addCampaignModal")
                    if modal.count() > 0 and modal.is_visible():
                        print("✅ Add Campaign modal opened successfully!")
                    else:
                        print("❌ Add Campaign modal did not open")
                        
                except Exception as e:
                    print(f"❌ Error clicking Add Campaign button: {e}")
            
            # Check API directly from browser
            print("\n🌐 Testing API from browser console...")
            api_test = """
            fetch('/api/campaigns')
                .then(r => r.json())
                .then(data => console.log('API Response:', data))
                .catch(err => console.error('API Error:', err))
            """
            page.evaluate(api_test)
            page.wait_for_timeout(2000)
            
            # Keep browser open for manual inspection
            print("\n👀 Browser will stay open for 10 seconds for manual inspection...")
            page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"❌ Error during test: {e}")
            page.screenshot(path="dashboard_error.png")
            
        finally:
            browser.close()
            print("✅ Test completed")

if __name__ == "__main__":
    test_dashboard() 