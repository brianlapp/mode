"""
Mode Popup Management System - Main API
Simple campaign management dashboard + embeddable popup script
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
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
    init_db()

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

@app.get("/admin/add-campaign", response_class=HTMLResponse)
async def add_campaign_modal():
    """Serve the add campaign modal HTML"""
    modal_file = frontend_path / "admin" / "add-campaign.html"
    if not modal_file.exists():
        raise HTTPException(status_code=404, detail="Add campaign modal not found")
    return FileResponse(modal_file)

# Include API routes
app.include_router(campaigns_router, prefix="/api", tags=["campaigns"])
app.include_router(properties_router, prefix="/api", tags=["properties"])

# Popup script endpoint (future)
@app.get("/popup.js")
async def get_popup_script():
    """Serve the embeddable popup script"""
    return {
        "message": "Popup script coming in Phase 3!",
        "usage": "Include this script on your thank you pages",
        "example": '<script src="https://your-domain.railway.app/popup.js"></script>'
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    ) 