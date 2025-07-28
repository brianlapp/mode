"""
Simple API test script to verify endpoints work
Run this before deploying to Railway
"""

import requests
import json

def test_local_api():
    """Test API endpoints locally"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Mode Popup API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test get campaigns (should be empty initially)
    try:
        response = requests.get(f"{base_url}/api/campaigns")
        print(f"✅ Get campaigns: {response.status_code} - {len(response.json())} campaigns")
    except Exception as e:
        print(f"❌ Get campaigns failed: {e}")
        return False
    
    # Test create campaign
    test_campaign = {
        "name": "Test Tesla Campaign",
        "tune_url": "https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045",
        "logo_url": "https://example.com/tesla-logo.png",
        "main_image_url": "https://example.com/tesla-stock.jpg",
        "description": "Tesla stock alert test campaign"
    }
    
    try:
        response = requests.post(f"{base_url}/api/campaigns", json=test_campaign)
        print(f"✅ Create campaign: {response.status_code} - {response.json()}")
        campaign_id = response.json().get('id')
    except Exception as e:
        print(f"❌ Create campaign failed: {e}")
        return False
    
    # Test property settings
    if campaign_id:
        property_settings = [
            {"property_code": "mff", "visibility_percentage": 75, "active": True},
            {"property_code": "mmm", "visibility_percentage": 50, "active": False}
        ]
        
        try:
            response = requests.post(f"{base_url}/api/campaigns/{campaign_id}/properties", json=property_settings)
            print(f"✅ Set property settings: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ Set property settings failed: {e}")
    
    # Test get campaigns for property
    try:
        response = requests.get(f"{base_url}/api/campaigns/mff")
        campaigns = response.json()
        print(f"✅ Get MFF campaigns: {response.status_code} - {len(campaigns)} campaigns")
        if campaigns:
            print(f"   First campaign: {campaigns[0]['name']} ({campaigns[0]['visibility_percentage']}% visibility)")
    except Exception as e:
        print(f"❌ Get property campaigns failed: {e}")
    
    print("\n🎉 API tests completed!")
    return True

if __name__ == "__main__":
    print("Run 'uvicorn main:app --reload' in another terminal first!")
    input("Press Enter when API is running...")
    test_local_api() 