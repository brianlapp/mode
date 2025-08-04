"""
Mode Popup Management System - Main API
Simple campaign management dashboard + embeddable popup script
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
import uvicorn
import os
from pathlib import Path

# Import our route modules (will create these next)
from routes.campaigns import router as campaigns_router
from routes.properties import router as properties_router
from database import init_db

# Create FastAPI app
app = FastAPI(
    title="Mode Popup Management API",
    description="Campaign management dashboard + embeddable popup script for Mike's Tune CPL campaigns",
    version="1.0.0"
)

# CORS middleware for admin dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for admin dashboard
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "assets")), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup():
    # 🛡️ ENSURE RAILWAY VOLUME MOUNT - Critical for data persistence
    try:
        from ensure_volume import ensure_railway_volume
        if not ensure_railway_volume():
            print("🚨 CRITICAL: Volume mount failed - data will not persist!")
    except Exception as e:
        print(f"⚠️ Warning: Volume check failed: {e}")
    
    init_db()
    # 🛡️ PROTECT MIKE'S REVENUE MACHINE - Ensure only real campaigns exist
    try:
        from startup_campaigns import protect_mikes_revenue_machine
        protect_mikes_revenue_machine()
    except Exception as e:
        print(f"⚠️ Warning: Could not run campaign protection: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mode Popup Management API"}

# Admin dashboard routes
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Mode Popup Management</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: linear-gradient(135deg, #F7007C 0%, #07C8F7 100%); color: white; }
                .container { background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; backdrop-filter: blur(10px); }
                a { color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px; display: inline-block; margin: 10px; }
                a:hover { background: rgba(255,255,255,0.3); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Mode Popup Management System</h1>
                <p>Campaign management dashboard for Mike's Tune CPL campaigns</p>
                <a href="/admin">📊 Admin Dashboard</a>
                <a href="/admin/integration">🚀 Integration Guide</a>
                <a href="/api/docs">📖 API Documentation</a>
                <a href="/health">🔍 Health Check</a>
            </div>
        </body>
    </html>
    """

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    """Serve the admin dashboard"""
    admin_file = frontend_path / "admin" / "index.html"
    if not admin_file.exists():
        raise HTTPException(status_code=404, detail="Admin dashboard not found")
    return FileResponse(admin_file)

@app.get("/integration-guide", response_class=HTMLResponse)
async def integration_guide():
    """Serve the integration guide page"""
    integration_file = frontend_path / "admin" / "integration.html"
    if not integration_file.exists():
        raise HTTPException(status_code=404, detail="Integration guide not found")
    return FileResponse(integration_file)

@app.get("/admin/add-campaign", response_class=HTMLResponse)
async def add_campaign_modal():
    """Serve the add campaign modal HTML"""
    modal_file = frontend_path / "admin" / "add-campaign.html"
    if not modal_file.exists():
        raise HTTPException(status_code=404, detail="Add campaign modal not found")
    return FileResponse(modal_file)

@app.get("/test-tracking.html", response_class=HTMLResponse)
async def test_tracking_dashboard():
    """Serve the Phase 2 tracking test dashboard"""
    test_file = Path(__file__).parent.parent / "test-tracking.html"
    if not test_file.exists():
        raise HTTPException(status_code=404, detail="Test tracking dashboard not found")
    return FileResponse(test_file)

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_dashboard():
    """Serve the Phase 2 analytics dashboard for Mike"""
    dashboard_file = Path(__file__).parent.parent / "phase2-analytics-dashboard.html"
    if not dashboard_file.exists():
        raise HTTPException(status_code=404, detail="Analytics dashboard not found")
    return FileResponse(dashboard_file)

@app.get("/property-colors-test.html", response_class=HTMLResponse)
async def property_colors_test():
    """Serve the property-specific reward pill test page"""
    test_file = Path(__file__).parent.parent / "frontend" / "property-colors-test.html"
    if not test_file.exists():
        raise HTTPException(status_code=404, detail="Property colors test page not found")
    return FileResponse(test_file)

# Include API routes
app.include_router(campaigns_router, prefix="/api", tags=["campaigns"])
app.include_router(properties_router, prefix="/api", tags=["properties"])

# Database migration endpoint
@app.post("/api/db/migrate")
async def run_migration():
    """Run database migration to add Phase 2 tracking columns"""
    try:
        init_db()
        return {"success": True, "message": "Database migration completed successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Popup script endpoint
@app.get("/popup.js")
async def serve_popup_script():
    """Serve the production popup script"""
    # Try multiple possible paths for Railway deployment
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "frontend", "popup.js"),
        os.path.join(os.path.dirname(__file__), "..", "scripts", "popup.js"),
        os.path.join(os.path.dirname(__file__), "..", "popup.js"),
        os.path.join(os.path.dirname(__file__), "scripts", "popup.js"),
        "popup-system/scripts/popup.js",
        "scripts/popup.js"
    ]
    
    for script_path in possible_paths:
        if os.path.exists(script_path):
            return FileResponse(script_path, media_type="application/javascript")
    
    # If file not found, return error info for debugging
    return PlainTextResponse(f"// Popup script not found. Checked paths: {possible_paths}", media_type="application/javascript")

@app.get("/popup.min.js")
async def serve_popup_script_minified():
    """Serve the minified popup script"""
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "popup.min.js")
    if os.path.exists(script_path):
        return FileResponse(script_path, media_type="application/javascript")
    else:
        return PlainTextResponse("// Minified popup script not found", media_type="application/javascript")

@app.get("/popup-styles.css")
async def serve_popup_styles():
    """Serve the popup CSS styles"""
    css_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "popup-styles.css")
    if os.path.exists(css_path):
        return FileResponse(css_path, media_type="text/css")
    else:
        return PlainTextResponse("/* Popup styles not found */", media_type="text/css")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    ) # Force deployment trigger
 