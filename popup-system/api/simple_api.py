#!/usr/bin/env python3
"""
Simplified FastAPI app for testing core endpoints
"""

import sys
import os

# Try to import FastAPI with proper error handling
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError as e:
    print(f"FastAPI not available: {e}")
    FASTAPI_AVAILABLE = False

if FASTAPI_AVAILABLE:
    # Import our database functions
    from database import init_db, insert_campaign, get_active_campaigns_for_property
    
    app = FastAPI(title="Mode Popup API - Simple Test")
    
    @app.on_event("startup")
    async def startup():
        init_db()
    
    @app.get("/")
    async def root():
        return {"status": "healthy", "message": "Mode Popup API Simple Test"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "popup-api-test"}
    
    @app.get("/test-campaign")
    async def test_campaign():
        """Create a test campaign and return it"""
        try:
            campaign_id = insert_campaign(
                name="API Test Tesla Campaign",
                tune_url="https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045",
                logo_url="https://example.com/tesla-logo.png",
                main_image_url="https://example.com/tesla-stock.jpg",
                description="API test campaign for Tesla stock alert"
            )
            return {"success": True, "campaign_id": campaign_id, "message": "Test campaign created"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/campaigns/{property_code}")
    async def get_campaigns(property_code: str):
        """Get campaigns for a property"""
        if property_code not in ['mff', 'mmm', 'mcad', 'mmd']:
            raise HTTPException(status_code=400, detail="Invalid property code")
        
        campaigns = get_active_campaigns_for_property(property_code)
        return {"property": property_code, "campaigns": campaigns}

    if __name__ == "__main__":
        print("🚀 Starting Simple Mode Popup API...")
        print("Available at: http://127.0.0.1:8000")
        print("Health check: http://127.0.0.1:8000/health")
        print("Test campaign: http://127.0.0.1:8000/test-campaign")
        uvicorn.run(app, host="127.0.0.1", port=8000)

else:
    print("❌ FastAPI not available - cannot start API server")
    sys.exit(1) 