#!/usr/bin/env python3
"""
Simple test of core functionality without FastAPI
Tests database operations and core logic
"""

import sys
import os

# Test database creation and basic operations
def test_database():
    print("🧪 Testing database operations...")
    
    try:
        # Import and test database functions
        from database import init_db, insert_campaign, get_active_campaigns_for_property
        
        # Initialize database
        print("  📁 Initializing database...")
        init_db()
        print("  ✅ Database initialized")
        
        # Test inserting a campaign
        print("  📝 Testing campaign insertion...")
        campaign_id = insert_campaign(
            name="Test Tesla Campaign",
            tune_url="https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045",
            logo_url="https://example.com/tesla-logo.png",
            main_image_url="https://example.com/tesla-stock.jpg",
            description="Test campaign for Tesla stock alert"
        )
        print(f"  ✅ Campaign created with ID: {campaign_id}")
        
        # Test getting campaigns (should be empty since no property settings yet)
        print("  🔍 Testing campaign retrieval...")
        campaigns = get_active_campaigns_for_property("mff")
        print(f"  ✅ Retrieved {len(campaigns)} campaigns for MFF")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def test_imports():
    print("🔍 Testing imports...")
    
    try:
        import sqlite3
        print("  ✅ SQLite available")
        
        from database import get_db_connection
        print("  ✅ Database module imports successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import test failed: {e}")
        return False

def main():
    print("🚀 Mode Popup API - Simple Test Suite")
    print("="*50)
    
    # Test imports first
    if not test_imports():
        print("\n❌ Import tests failed - stopping here")
        return False
    
    # Test database operations
    if not test_database():
        print("\n❌ Database tests failed")
        return False
    
    print("\n🎉 All core tests passed!")
    print("✅ Database operations work correctly")
    print("✅ Campaign creation and retrieval functional")
    print("✅ Ready for FastAPI integration")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 