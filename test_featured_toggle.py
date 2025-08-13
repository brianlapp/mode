#!/usr/bin/env python3
"""
Test featured campaign toggle functionality with Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import json

async def test_featured_toggle():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Listen to console messages and network requests
        console_messages = []
        network_requests = []
        
        page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))
        page.on("request", lambda req: network_requests.append(f"{req.method} {req.url}"))
        page.on("response", lambda resp: print(f"Response: {resp.status} {resp.url}"))
        
        try:
            print("🚀 Testing featured campaign toggle...")
            
            # Go to admin dashboard
            await page.goto("https://mode-dash-production.up.railway.app/admin")
            await page.wait_for_timeout(2000)
            
            print("📋 Looking for Properties button...")
            
            # Find and click the first Properties button
            properties_button = page.locator('button:has-text("Properties")').first
            if await properties_button.count() > 0:
                await properties_button.click()
                print("✅ Clicked Properties button")
                await page.wait_for_timeout(1000)
                
                # Find featured toggle checkbox
                featured_toggle = page.locator('input[id*="featured_"]').first
                if await featured_toggle.count() > 0:
                    print("🌟 Found featured toggle, clicking...")
                    await featured_toggle.click()
                    await page.wait_for_timeout(3000)  # Wait for API call
                    
                    print("📊 Console messages:")
                    for msg in console_messages[-10:]:  # Last 10 messages
                        print(f"  {msg}")
                        
                    print("🌐 Recent network requests:")
                    for req in network_requests[-5:]:  # Last 5 requests
                        print(f"  {req}")
                        
                else:
                    print("❌ Featured toggle not found")
            else:
                print("❌ Properties button not found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_featured_toggle())
