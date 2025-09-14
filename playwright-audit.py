#!/usr/bin/env python3
"""
Mode Landing Page Audit - Playwright Analysis
Captures screenshots and performs technical analysis of MFF vs MMM landing pages
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

class LandingPageAuditor:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(f"audit-screenshots-{self.timestamp}")
        self.output_dir.mkdir(exist_ok=True)
        
        self.urls = {
            "mff": "https://join.modefreefinds.com/mff-signup-affiliate/",
            "mmm": "https://signups.modemobile.com/mm-signup-affv1/"
        }
        
        self.audit_results = {
            "audit_date": datetime.now().isoformat(),
            "pages": {},
            "comparison": {},
            "recommendations": []
        }

    async def audit_page(self, browser, name, url):
        """Comprehensive audit of a single landing page"""
        print(f"🔍 Auditing {name.upper()}: {url}")
        
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate and wait for load
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(2000)  # Allow dynamic content to load
            
            # Desktop screenshots
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.screenshot(path=self.output_dir / f"{name}_desktop_full.png", full_page=True)
            await page.screenshot(path=self.output_dir / f"{name}_desktop_viewport.png")
            
            # Mobile screenshots
            await page.set_viewport_size({"width": 375, "height": 667})  # iPhone SE
            await page.screenshot(path=self.output_dir / f"{name}_mobile_full.png", full_page=True)
            await page.screenshot(path=self.output_dir / f"{name}_mobile_viewport.png")
            
            # Form analysis
            form_data = await self.analyze_form(page)
            
            # Performance metrics
            performance_data = await self.analyze_performance(page)
            
            # Content analysis
            content_data = await self.analyze_content(page)
            
            # Trust signals
            trust_data = await self.analyze_trust_signals(page)
            
            self.audit_results["pages"][name] = {
                "url": url,
                "form_analysis": form_data,
                "performance": performance_data,
                "content": content_data,
                "trust_signals": trust_data,
                "screenshots": {
                    "desktop_full": f"{name}_desktop_full.png",
                    "desktop_viewport": f"{name}_desktop_viewport.png",
                    "mobile_full": f"{name}_mobile_full.png",
                    "mobile_viewport": f"{name}_mobile_viewport.png"
                }
            }
            
            print(f"✅ {name.upper()} audit completed")
            
        except Exception as e:
            print(f"❌ Error auditing {name}: {e}")
            self.audit_results["pages"][name] = {"error": str(e)}
        
        finally:
            await context.close()

    async def analyze_form(self, page):
        """Analyze form structure and friction points"""
        try:
            # Count form fields
            form_fields = await page.locator('input[type="text"], input[type="email"], input[type="tel"], textarea, select').count()
            
            # Check specific field types
            email_fields = await page.locator('input[type="email"]').count()
            phone_fields = await page.locator('input[type="tel"], input[name*="phone"]').count()
            required_fields = await page.locator('input[required]').count()
            
            # CTA button analysis
            cta_buttons = await page.locator('button[type="submit"], input[type="submit"], button:has-text("continue"), button:has-text("submit")').count()
            cta_text = ""
            if cta_buttons > 0:
                cta_element = page.locator('button[type="submit"], input[type="submit"], button:has-text("continue"), button:has-text("submit")').first
                cta_text = await cta_element.text_content() or await cta_element.get_attribute("value") or ""
            
            return {
                "total_fields": form_fields,
                "email_fields": email_fields,
                "phone_fields": phone_fields,
                "required_fields": required_fields,
                "cta_buttons": cta_buttons,
                "cta_text": cta_text.strip()
            }
        except Exception as e:
            return {"error": str(e)}

    async def analyze_performance(self, page):
        """Analyze page performance metrics"""
        try:
            # Get performance timing
            performance = await page.evaluate("""
                () => {
                    const perf = performance.getEntriesByType('navigation')[0];
                    return {
                        load_time: perf.loadEventEnd - perf.loadEventStart,
                        dom_content_loaded: perf.domContentLoadedEventEnd - perf.domContentLoadedEventStart,
                        first_paint: performance.getEntriesByType('paint').find(p => p.name === 'first-paint')?.startTime || 0,
                        largest_contentful_paint: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime || 0
                    }
                }
            """)
            
            # Check for images and their loading
            image_count = await page.locator('img').count()
            
            return {
                "load_time_ms": performance.get("load_time", 0),
                "dom_content_loaded_ms": performance.get("dom_content_loaded", 0),
                "first_paint_ms": performance.get("first_paint", 0),
                "lcp_ms": performance.get("largest_contentful_paint", 0),
                "image_count": image_count
            }
        except Exception as e:
            return {"error": str(e)}

    async def analyze_content(self, page):
        """Analyze content structure and messaging"""
        try:
            # Get title and main heading
            title = await page.title()
            
            # Find main headings
            h1_count = await page.locator('h1').count()
            h1_text = ""
            if h1_count > 0:
                h1_text = await page.locator('h1').first.text_content() or ""
            
            # Check for value proposition keywords
            page_text = await page.locator('body').text_content() or ""
            
            value_prop_keywords = {
                "free": page_text.lower().count("free"),
                "exclusive": page_text.lower().count("exclusive"),
                "daily": page_text.lower().count("daily"),
                "investment": page_text.lower().count("investment"),
                "insight": page_text.lower().count("insight"),
                "deal": page_text.lower().count("deal"),
                "sample": page_text.lower().count("sample")
            }
            
            # Check word count for complexity
            word_count = len(page_text.split())
            
            return {
                "title": title,
                "h1_count": h1_count,
                "h1_text": h1_text.strip(),
                "value_prop_keywords": value_prop_keywords,
                "total_word_count": word_count
            }
        except Exception as e:
            return {"error": str(e)}

    async def analyze_trust_signals(self, page):
        """Analyze trust signals and social proof"""
        try:
            # Look for social proof elements
            facebook_mentions = await page.locator('[href*="facebook"], [src*="facebook"], [alt*="facebook"]').count()
            testimonial_keywords = await page.locator('*:has-text("testimonial"), *:has-text("review"), *:has-text("customer")').count()
            
            # Check for privacy and security mentions
            privacy_mentions = await page.locator('*:has-text("privacy"), *:has-text("secure"), *:has-text("unsubscribe")').count()
            
            # Look for subscriber/follower counts
            page_text = await page.locator('body').text_content() or ""
            has_subscriber_count = any(keyword in page_text.lower() for keyword in ["subscribers", "followers", "members", "users"])
            
            return {
                "facebook_elements": facebook_mentions,
                "testimonial_elements": testimonial_keywords,
                "privacy_mentions": privacy_mentions,
                "has_subscriber_count": has_subscriber_count
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_comparison(self):
        """Generate comparison analysis between MFF and MMM"""
        mff_data = self.audit_results["pages"].get("mff", {})
        mmm_data = self.audit_results["pages"].get("mmm", {})
        
        if not mff_data or not mmm_data:
            return {"error": "Missing data for comparison"}
        
        comparison = {
            "form_friction": {
                "mff_fields": mff_data.get("form_analysis", {}).get("total_fields", 0),
                "mmm_fields": mmm_data.get("form_analysis", {}).get("total_fields", 0),
                "friction_difference": mmm_data.get("form_analysis", {}).get("total_fields", 0) - mff_data.get("form_analysis", {}).get("total_fields", 0)
            },
            "performance": {
                "mff_load_time": mff_data.get("performance", {}).get("load_time_ms", 0),
                "mmm_load_time": mmm_data.get("performance", {}).get("load_time_ms", 0)
            },
            "trust_signals": {
                "mff_facebook": mff_data.get("trust_signals", {}).get("facebook_elements", 0),
                "mmm_facebook": mmm_data.get("trust_signals", {}).get("facebook_elements", 0)
            },
            "messaging_complexity": {
                "mff_words": mff_data.get("content", {}).get("total_word_count", 0),
                "mmm_words": mmm_data.get("content", {}).get("total_word_count", 0)
            }
        }
        
        self.audit_results["comparison"] = comparison
        return comparison

    def generate_recommendations(self):
        """Generate actionable recommendations based on audit findings"""
        mmm_data = self.audit_results["pages"].get("mmm", {})
        mff_data = self.audit_results["pages"].get("mff", {})
        
        recommendations = []
        
        # Form friction recommendations
        mmm_fields = mmm_data.get("form_analysis", {}).get("total_fields", 0)
        mff_fields = mff_data.get("form_analysis", {}).get("total_fields", 0)
        
        if mmm_fields > mff_fields:
            recommendations.append({
                "priority": "HIGH",
                "category": "Form Optimization",
                "issue": f"MMM has {mmm_fields} fields vs MFF's {mff_fields}",
                "recommendation": "Remove unnecessary form fields to match MFF's simplicity",
                "expected_impact": "20-30% conversion improvement"
            })
        
        # Phone field specific check
        mmm_phone = mmm_data.get("form_analysis", {}).get("phone_fields", 0)
        if mmm_phone > 0:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Form Friction",
                "issue": "Phone number field present in MMM",
                "recommendation": "Remove phone number field - major conversion killer",
                "expected_impact": "25-35% conversion improvement"
            })
        
        # Trust signals
        mff_trust = mff_data.get("trust_signals", {}).get("facebook_elements", 0)
        mmm_trust = mmm_data.get("trust_signals", {}).get("facebook_elements", 0)
        
        if mff_trust > mmm_trust:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Trust Building",
                "issue": "MMM lacks social proof elements that MFF has",
                "recommendation": "Add Facebook integration and subscriber count display",
                "expected_impact": "10-15% trust boost"
            })
        
        self.audit_results["recommendations"] = recommendations
        return recommendations

    async def run_audit(self):
        """Execute the complete audit workflow"""
        print("🚀 Starting Mode Landing Page Audit with Playwright")
        print(f"📁 Screenshots will be saved to: {self.output_dir}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Audit both pages
            await self.audit_page(browser, "mff", self.urls["mff"])
            await self.audit_page(browser, "mmm", self.urls["mmm"])
            
            await browser.close()
        
        # Generate analysis
        print("📊 Generating comparison analysis...")
        self.generate_comparison()
        self.generate_recommendations()
        
        # Save results
        results_file = self.output_dir / "audit_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.audit_results, f, indent=2)
        
        print(f"✅ Audit completed! Results saved to: {results_file}")
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print a summary of audit findings"""
        print("\n" + "="*60)
        print("🕵️‍♂️  LANDING PAGE AUDIT SUMMARY")
        print("="*60)
        
        # Form comparison
        mff_form = self.audit_results["pages"].get("mff", {}).get("form_analysis", {})
        mmm_form = self.audit_results["pages"].get("mmm", {}).get("form_analysis", {})
        
        print(f"\n📝 FORM ANALYSIS:")
        print(f"   MFF Fields: {mff_form.get('total_fields', 'N/A')} | Phone: {mff_form.get('phone_fields', 'N/A')}")
        print(f"   MMM Fields: {mmm_form.get('total_fields', 'N/A')} | Phone: {mmm_form.get('phone_fields', 'N/A')}")
        
        # Performance comparison
        mff_perf = self.audit_results["pages"].get("mff", {}).get("performance", {})
        mmm_perf = self.audit_results["pages"].get("mmm", {}).get("performance", {})
        
        print(f"\n⚡ PERFORMANCE:")
        print(f"   MFF Load Time: {mff_perf.get('load_time_ms', 'N/A')}ms")
        print(f"   MMM Load Time: {mmm_perf.get('load_time_ms', 'N/A')}ms")
        
        # Recommendations
        print(f"\n🎯 TOP RECOMMENDATIONS:")
        for rec in self.audit_results.get("recommendations", [])[:3]:
            print(f"   {rec['priority']}: {rec['recommendation']}")
        
        print(f"\n📸 Screenshots saved in: {self.output_dir}")
        print("="*60)

if __name__ == "__main__":
    auditor = LandingPageAuditor()
    asyncio.run(auditor.run_audit()) 