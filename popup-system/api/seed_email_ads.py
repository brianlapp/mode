"""
Seed Email Ads Data
Populates the database with default email ads for each property
"""

import sqlite3
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import get_db_connection
except ImportError:
    # Fallback if import fails
    def get_db_connection():
        conn = sqlite3.connect('popup_campaigns.db')
        conn.row_factory = sqlite3.Row
        return conn

def seed_email_ads():
    """Create default email ads for each property"""
    conn = get_db_connection()

    # Default email ads data
    email_ads_data = [
        # ModeFreeFinds (MFF) Email Ads
        {
            'property_code': 'mff',
            'name': 'Free Samples Newsletter Ad',
            'desktop_image_url': 'https://via.placeholder.com/600x200/F7007C/FFFFFF?text=ModeFreeFinds+Newsletter+Banner',
            'mobile_image_url': 'https://via.placeholder.com/320x200/F7007C/FFFFFF?text=MFF+Mobile+Banner',
            'click_url': 'https://modefinds.com/newsletter-signup?utm_source=email&utm_medium=banner&utm_campaign=newsletter',
            'description': 'Newsletter signup banner for free samples and deals',
            'visibility_percentage': 100,
            'active': True
        },
        {
            'property_code': 'mff',
            'name': 'Daily Deals Email Banner',
            'desktop_image_url': 'https://via.placeholder.com/600x200/07C8F7/FFFFFF?text=MFF+Daily+Deals+Banner',
            'mobile_image_url': 'https://via.placeholder.com/320x200/07C8F7/FFFFFF?text=MFF+Daily+Deals+Mobile',
            'click_url': 'https://modefinds.com/deals?utm_source=email&utm_medium=banner&utm_campaign=daily_deals',
            'description': 'Daily deals promotion banner for email campaigns',
            'visibility_percentage': 80,
            'active': True
        },
        {
            'property_code': 'mff',
            'name': 'Lifestyle Offers Email Ad',
            'desktop_image_url': 'https://via.placeholder.com/600x200/9f7aea/FFFFFF?text=MFF+Lifestyle+Offers',
            'mobile_image_url': 'https://via.placeholder.com/320x200/9f7aea/FFFFFF?text=MFF+Lifestyle+Mobile',
            'click_url': 'https://modefinds.com/lifestyle?utm_source=email&utm_medium=banner&utm_campaign=lifestyle',
            'description': 'Lifestyle and wellness offers promotional banner',
            'visibility_percentage': 60,
            'active': True
        },

        # ModeMarketMunchies (MMM) Email Ads
        {
            'property_code': 'mmm',
            'name': 'Trading Tips Email Banner',
            'desktop_image_url': 'https://via.placeholder.com/600x200/00FF7F/000000?text=Trading+Tips+Newsletter',
            'mobile_image_url': 'https://via.placeholder.com/320x200/00FF7F/000000?text=Trading+Tips+Mobile',
            'click_url': 'https://modemarketmunchies.com/trading-tips?utm_source=email&utm_medium=banner&utm_campaign=trading_tips',
            'description': 'Weekly trading tips and market insights newsletter banner',
            'visibility_percentage': 100,
            'active': True
        },
        {
            'property_code': 'mmm',
            'name': 'Financial Newsletter Ad',
            'desktop_image_url': 'https://via.placeholder.com/600x200/3B82F6/FFFFFF?text=Financial+Newsletter+MMM',
            'mobile_image_url': 'https://via.placeholder.com/320x200/3B82F6/FFFFFF?text=Financial+Newsletter+Mobile',
            'click_url': 'https://modemarketmunchies.com/financial-newsletter?utm_source=email&utm_medium=banner&utm_campaign=financial_newsletter',
            'description': 'Daily financial newsletter subscription banner',
            'visibility_percentage': 90,
            'active': True
        },
        {
            'property_code': 'mmm',
            'name': 'Stock Broker Comparison Ad',
            'desktop_image_url': 'https://via.placeholder.com/600x200/EF4444/FFFFFF?text=Best+Stock+Brokers+2025',
            'mobile_image_url': 'https://via.placeholder.com/320x200/EF4444/FFFFFF?text=Best+Brokers+Mobile',
            'click_url': 'https://modemarketmunchies.com/broker-comparison?utm_source=email&utm_medium=banner&utm_campaign=broker_comparison',
            'description': 'Stock broker comparison and recommendation banner',
            'visibility_percentage': 70,
            'active': True
        },

        # ModeClearanceDeals (MCAD) Email Ads
        {
            'property_code': 'mcad',
            'name': 'Clearance Deals Newsletter',
            'desktop_image_url': 'https://via.placeholder.com/600x200/10B981/FFFFFF?text=Clearance+Deals+Newsletter',
            'mobile_image_url': 'https://via.placeholder.com/320x200/10B981/FFFFFF?text=Clearance+Mobile',
            'click_url': 'https://modeclearancedeals.com/newsletter?utm_source=email&utm_medium=banner&utm_campaign=clearance_newsletter',
            'description': 'Weekly clearance deals and discount alerts banner',
            'visibility_percentage': 100,
            'active': True
        },
        {
            'property_code': 'mcad',
            'name': 'Flash Sale Email Banner',
            'desktop_image_url': 'https://via.placeholder.com/600x200/F59E0B/FFFFFF?text=Flash+Sale+Alert',
            'mobile_image_url': 'https://via.placeholder.com/320x200/F59E0B/FFFFFF?text=Flash+Sale+Mobile',
            'click_url': 'https://modeclearancedeals.com/flash-sale?utm_source=email&utm_medium=banner&utm_campaign=flash_sale',
            'description': 'Limited time flash sale promotional banner',
            'visibility_percentage': 85,
            'active': True
        },

        # ModeMarketDeals (MMD) Email Ads
        {
            'property_code': 'mmd',
            'name': 'Market Deals Newsletter',
            'desktop_image_url': 'https://via.placeholder.com/600x200/8B5CF6/FFFFFF?text=Market+Deals+Newsletter',
            'mobile_image_url': 'https://via.placeholder.com/320x200/8B5CF6/FFFFFF?text=Market+Deals+Mobile',
            'click_url': 'https://modemarketdeals.com/newsletter?utm_source=email&utm_medium=banner&utm_campaign=market_newsletter',
            'description': 'Daily market deals and opportunities newsletter banner',
            'visibility_percentage': 100,
            'active': True
        },
        {
            'property_code': 'mmd',
            'name': 'Investment Opportunities Banner',
            'desktop_image_url': 'https://via.placeholder.com/600x200/EC4899/FFFFFF?text=Investment+Opportunities',
            'mobile_image_url': 'https://via.placeholder.com/320x200/EC4899/FFFFFF?text=Investment+Mobile',
            'click_url': 'https://modemarketdeals.com/investments?utm_source=email&utm_medium=banner&utm_campaign=investments',
            'description': 'Investment opportunities and recommendations banner',
            'visibility_percentage': 75,
            'active': True
        }
    ]

    try:
        # Clear existing email ads (for fresh seed)
        print("🧹 Clearing existing email ads...")
        conn.execute("DELETE FROM email_ads")
        conn.execute("DELETE FROM email_ad_impressions")
        conn.execute("DELETE FROM email_ad_clicks")

        # Insert seed data
        print("📧 Inserting seed email ads...")
        for i, ad_data in enumerate(email_ads_data):
            conn.execute("""
                INSERT INTO email_ads (
                    property_code, name, desktop_image_url, mobile_image_url,
                    click_url, description, visibility_percentage, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ad_data['property_code'],
                ad_data['name'],
                ad_data['desktop_image_url'],
                ad_data['mobile_image_url'],
                ad_data['click_url'],
                ad_data['description'],
                ad_data['visibility_percentage'],
                ad_data['active']
            ))
            print(f"  ✅ Created: {ad_data['name']} ({ad_data['property_code'].upper()})")

        conn.commit()
        print(f"✅ Successfully seeded {len(email_ads_data)} email ads")

        # Show summary
        cursor = conn.execute("""
            SELECT property_code, COUNT(*) as count
            FROM email_ads
            GROUP BY property_code
            ORDER BY property_code
        """)

        print("\n📊 Email Ads Summary:")
        for row in cursor.fetchall():
            print(f"  {row[0].upper()}: {row[1]} email ads")

        return True

    except Exception as e:
        print(f"❌ Failed to seed email ads: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def verify_email_ads():
    """Verify the seeded email ads"""
    conn = get_db_connection()

    try:
        print("\n🔍 Verifying email ads setup...")

        # Check total count
        cursor = conn.execute("SELECT COUNT(*) FROM email_ads")
        total_count = cursor.fetchone()[0]
        print(f"  Total email ads: {total_count}")

        # Check by property
        cursor = conn.execute("""
            SELECT property_code, COUNT(*) as count,
                   COUNT(CASE WHEN active = 1 THEN 1 END) as active_count
            FROM email_ads
            GROUP BY property_code
            ORDER BY property_code
        """)

        print("  By property:")
        for row in cursor.fetchall():
            print(f"    {row[0].upper()}: {row[1]} total, {row[2]} active")

        # Test ad serving endpoints
        print("\n🧪 Testing email ad serving...")
        for prop in ['mff', 'mmm', 'mcad', 'mmd']:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM email_ads
                WHERE property_code = ? AND active = 1
            """, (prop,))
            active_count = cursor.fetchone()[0]

            if active_count > 0:
                print(f"  ✅ {prop.upper()}: {active_count} active email ads ready")
            else:
                print(f"  ❌ {prop.upper()}: No active email ads found")

        return True

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Seeding Email Ads Database...")
    print("=" * 50)

    success = seed_email_ads()

    if success:
        verify_email_ads()
        print("\n" + "=" * 50)
        print("✅ Email ads seeding completed successfully!")
        print("\n🌐 Test the API endpoints:")
        print("  • GET /api/email-ads/ - List all email ads")
        print("  • GET /api/email-ads/ad.png?property=mff - Serve MFF email ad")
        print("  • GET /api/email-ads/ad.png?property=mmm - Serve MMM email ad")
        print("  • GET /api/email-ads/analytics/summary - View analytics")
        print("\n📋 Admin Dashboard:")
        print("  • Visit /admin and click 'Email Ads' tab")
        print("  • Test CRUD operations, filtering, and previews")
    else:
        print("\n" + "=" * 50)
        print("❌ Email ads seeding failed!")
        exit(1)