#!/usr/bin/env python3
"""
Test the frontend admin dashboard editable aff_id functionality
"""

from playwright.sync_api import sync_playwright
import time

def test_frontend_editable_aff_id():
    with sync_playwright() as p:
        print("🚀 Testing Frontend Editable AFF_ID Functionality...")
        
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Visual test
        page = browser.new_page()
        
        try:
            # Go to the admin dashboard
            print("📍 Navigating to admin dashboard...")
            page.goto("https://mode-dash-production.up.railway.app/admin")
            
            # Wait for page to load
            print("⏳ Waiting for dashboard to load...")
            page.wait_for_timeout(5000)
            
            # Take screenshot of dashboard
            print("📸 Taking dashboard screenshot...")
            page.screenshot(path="frontend_test_dashboard.png")
            
            # Look for campaigns table
            campaigns_exist = page.locator("#campaigns-table").count() > 0
            print(f"🗂️ Campaigns table exists: {campaigns_exist}")
            
            if campaigns_exist:
                # Look for Edit buttons
                edit_buttons = page.locator("button:has-text('Edit')")
                edit_count = edit_buttons.count()
                print(f"✏️ Edit buttons found: {edit_count}")
                
                if edit_count > 0:
                    print("🎯 Testing editable aff_id functionality...")
                    
                    # Click first Edit button
                    edit_buttons.first.click()
                    print("✅ Clicked Edit button")
                    
                    # Wait for modal to appear
                    page.wait_for_timeout(2000)
                    
                    # Look for editable aff_id field
                    aff_id_field = page.locator("#edit_aff_id")
                    if aff_id_field.count() > 0:
                        print("✅ Found editable aff_id field!")
                        
                        # Check if field is editable (not readonly)
                        is_readonly = aff_id_field.get_attribute("readonly")
                        print(f"🔒 AFF_ID field readonly: {is_readonly}")
                        
                        if not is_readonly:
                            # Get current value
                            current_value = aff_id_field.input_value()
                            print(f"📝 Current aff_id value: {current_value}")
                            
                            # Test editing (but don't save)
                            aff_id_field.fill("TEST_EDIT")
                            new_value = aff_id_field.input_value()
                            print(f"✏️ After test edit: {new_value}")
                            
                            # Restore original value
                            aff_id_field.fill(current_value)
                            restored_value = aff_id_field.input_value()
                            print(f"↩️ Restored to: {restored_value}")
                            
                            print("🎉 EDITABLE AFF_ID FUNCTIONALITY CONFIRMED!")
                        else:
                            print("❌ AFF_ID field is readonly - feature not working")
                    else:
                        print("❌ Editable aff_id field not found")
                    
                    # Take screenshot of edit modal
                    print("📸 Taking edit modal screenshot...")
                    page.screenshot(path="frontend_test_edit_modal.png")
                    
                else:
                    print("❌ No Edit buttons found")
            else:
                print("❌ Campaigns table not found")
            
            print("✅ Frontend test completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            page.screenshot(path="frontend_test_error.png")
        
        finally:
            browser.close()

if __name__ == "__main__":
    test_frontend_editable_aff_id()

