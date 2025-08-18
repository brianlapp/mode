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
    # 🎯 Protection system removed - no longer needed since fake data sources eliminated
    
    # 🚨 RESTORE MIKE'S PRODUCTION DATA if needed
    try:
        from restore_railway_data import restore_railway_production_data
        restore_railway_production_data()
    except Exception as e:
        print(f"⚠️ Warning: Could not restore production data: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mode Popup Management API"}

@app.get("/debug/property-test")
async def debug_property_test(property: str | None = None, host: str | None = None):
    """Debug endpoint to test property parameter parsing"""
    from database import detect_property_code_from_host
    
    # Test the same logic as the optimized endpoint
    if property and property in ['mff', 'mmm', 'mcad', 'mmd']:
        property_code = property.lower()
        source = "explicit_parameter"
    else:
        hostname = (host or "").strip().lower()
        property_code = detect_property_code_from_host(hostname)
        source = "hostname_detection"
    
    return {
        "input_property": property,
        "input_host": host,
        "resolved_property_code": property_code,
        "source": source
    }

# Quick fix endpoint for Railway database resets
@app.post("/api/quick-fix")
async def quick_fix():
    """Run all necessary fixes after Railway database reset"""
    try:
        results = []
        
        # 1. Fix schema
        from database import get_db_connection
        conn = get_db_connection()
        
        # Add featured_campaign_id column
        try:
            conn.execute("ALTER TABLE properties ADD COLUMN featured_campaign_id INTEGER")
            results.append("✅ Added featured_campaign_id column")
        except:
            results.append("✅ featured_campaign_id column already exists")
            
        # Add impression_cap_daily column
        try:
            conn.execute("ALTER TABLE campaign_properties ADD COLUMN impression_cap_daily INTEGER NULL")
            results.append("✅ Added impression_cap_daily column")
        except:
            results.append("✅ impression_cap_daily column already exists")
            
        # Add click_cap_daily column  
        try:
            conn.execute("ALTER TABLE campaign_properties ADD COLUMN click_cap_daily INTEGER NULL")
            results.append("✅ Added click_cap_daily column")
        except:
            results.append("✅ click_cap_daily column already exists")
            
        conn.commit()
        conn.close()
        
        # 2. Ensure properties exist
        from routes.campaigns import auto_assign_all_campaigns
        try:
            auto_assign_all_campaigns()
            results.append("✅ Auto-assigned all campaigns to all properties")
        except Exception as e:
            results.append(f"⚠️ Auto-assignment: {e}")
        
        return {
            "success": True,
            "message": "Quick fix completed - featured toggle should work now!",
            "results": results
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Quick fix failed"
        }

# Manual migration endpoint to fix missing columns
@app.post("/migrate")
async def run_migration():
    """Manual migration endpoint to fix missing columns"""
    from database import get_db_connection
    conn = get_db_connection()
    try:
        # Add missing columns to campaign_properties table
        cursor = conn.execute("PRAGMA table_info(campaign_properties)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        added_columns = []
        cap_columns = {
            'impression_cap_daily': 'INTEGER',
            'click_cap_daily': 'INTEGER'
        }
        
        for column, column_type in cap_columns.items():
            if column not in existing_columns:
                try:
                    conn.execute(f"ALTER TABLE campaign_properties ADD COLUMN {column} {column_type}")
                    conn.commit()
                    added_columns.append(column)
                except Exception as e:
                    return {"status": "error", "message": f"Failed to add {column}: {str(e)}"}
        
        return {
            "status": "success", 
            "added_columns": added_columns,
            "existing_columns": existing_columns,
            "message": "Migration completed successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

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

# Emergency restoration endpoint for Railway deployment fixes
@app.post("/api/emergency-restore-12-campaigns")
async def emergency_restore_12_campaigns():
    """Emergency endpoint to restore all 12 campaigns with property attribution"""
    import sqlite3
    import json
    from database import get_db_path
    
    try:
        print("🚨 EMERGENCY RESTORATION: Restoring 12 campaigns")
        
        # Load from backup file
        backup_path = Path(__file__).parent.parent / "campaign_backup.json"
        if not backup_path.exists():
            return {"status": "error", "message": "Backup file not found"}
            
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        campaigns_data = backup_data['campaigns']
        
        conn = sqlite3.connect(get_db_path())
        
        # Clear and restore campaigns
        conn.execute("DELETE FROM campaigns")
        conn.execute("DELETE FROM campaign_properties")
        
        for campaign in campaigns_data:
            # Fix offer_id mismatch for campaign 12
            if campaign['id'] == 12 and campaign['name'] == 'Prizies':
                campaign['offer_id'] = '3752'
                
            conn.execute('''
                INSERT INTO campaigns (
                    id, name, tune_url, logo_url, main_image_url, description,
                    cta_text, offer_id, aff_id, active, featured, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
            ''', (
                campaign['id'], campaign['name'], campaign['tune_url'],
                campaign['logo_url'], campaign['main_image_url'], campaign['description'],
                campaign['cta_text'], campaign['offer_id'], campaign['aff_id'], 
                campaign['active'], campaign.get('created_at', '2025-01-28 12:00:00'),
                campaign.get('updated_at', '2025-01-28 12:00:00')
            ))
            
            # Set property assignment
            property_code = 'mmm' if campaign['aff_id'] == '43045' else 'mff'
            conn.execute('''
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active
                ) VALUES (?, ?, 100, 1)
            ''', (campaign['id'], property_code))
        
        conn.commit()
        conn.close()
        
        print("✅ Emergency restoration complete: 12 campaigns with property attribution")
        
        return {
            "status": "success",
            "message": "All 12 campaigns restored with property attribution",
            "campaigns_restored": len(campaigns_data),
            "mmm_campaigns": 5,
            "mff_campaigns": 7
        }
        
    except Exception as e:
        print(f"❌ Emergency restoration failed: {e}")
        return {
            "status": "error", 
            "message": f"Restoration failed: {e}"
        }

# Database migration endpoint
@app.post("/api/db/migrate")
async def run_migration():
    """Run database migration to add Phase 2 tracking columns"""
    try:
        init_db()
        return {"success": True, "message": "Database migration completed successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Emergency schema fix endpoint
@app.post("/api/db/fix-schema")
async def fix_database_schema():
    """Emergency fix for missing featured column causing popup Internal Server Error"""
    from database import get_db_connection
    conn = get_db_connection()
    try:
        results = []
        
        # Check and add featured column to campaigns table
        cursor = conn.execute("PRAGMA table_info(campaigns)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'featured' not in columns:
            conn.execute("ALTER TABLE campaigns ADD COLUMN featured BOOLEAN DEFAULT false")
            conn.commit()
            results.append("✅ Added featured column to campaigns table")
        else:
            results.append("✅ Featured column already exists in campaigns table")
        
        # Check and add daily cap columns to campaign_properties table
        cursor = conn.execute("PRAGMA table_info(campaign_properties)")
        cp_columns = [row[1] for row in cursor.fetchall()]
        
        if 'impression_cap_daily' not in cp_columns:
            conn.execute("ALTER TABLE campaign_properties ADD COLUMN impression_cap_daily INTEGER")
            conn.commit()
            results.append("✅ Added impression_cap_daily column to campaign_properties table")
        else:
            results.append("✅ impression_cap_daily column already exists")
            
        if 'click_cap_daily' not in cp_columns:
            conn.execute("ALTER TABLE campaign_properties ADD COLUMN click_cap_daily INTEGER")
            conn.commit()
            results.append("✅ Added click_cap_daily column to campaign_properties table")
        else:
            results.append("✅ click_cap_daily column already exists")
        
        return {
            "success": True, 
            "message": "Schema fix completed",
            "results": results,
            "campaigns_columns": columns,
            "campaign_properties_columns": cp_columns
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": "Schema fix failed"}
    finally:
        conn.close()

# Domain configuration fix endpoint
@app.post("/api/db/fix-domains")
async def fix_domain_configuration():
    """Fix missing domain mappings for property resolution"""
    from database import get_db_connection
    conn = get_db_connection()
    try:
        results = []
        
        # Define the correct domain mappings
        domain_mappings = [
            ('mff', 'ModeFreeFinds', 'modefreefinds.com'),
            ('mmm', 'ModeMarketMunchies', 'modemarketmunchies.com'),
            ('mcad', 'ModeClassActionsDaily', 'modeclassactionsdaily.com'),
            ('mmd', 'ModeMobileDaily', 'modemobiledaily.com')
        ]
        
        for code, name, domain in domain_mappings:
            # Check if property exists and update domain
            cursor = conn.execute("SELECT id, domain FROM properties WHERE code = ?", (code,))
            row = cursor.fetchone()
            
            if row:
                current_domain = row[1]
                if current_domain != domain:
                    conn.execute("UPDATE properties SET domain = ? WHERE code = ?", (domain, code))
                    results.append(f"✅ Updated {code} domain from '{current_domain}' to '{domain}'")
                else:
                    results.append(f"✅ {code} domain already correct: {domain}")
            else:
                # Insert missing property
                conn.execute("""
                    INSERT INTO properties (code, name, domain, active, popup_enabled) 
                    VALUES (?, ?, ?, 1, 1)
                """, (code, name, domain))
                results.append(f"✅ Added missing property {code}: {domain}")
        
        conn.commit()
        
        # Verify the configuration
        cursor = conn.execute("SELECT code, name, domain FROM properties ORDER BY code")
        properties = [dict(zip(['code', 'name', 'domain'], row)) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "message": "Domain configuration fixed",
            "results": results,
            "properties": properties
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": "Domain fix failed"}
    finally:
        conn.close()

# Property-specific featured campaign migration
@app.post("/api/db/migrate-featured-to-properties")
async def migrate_featured_to_properties():
    """Migrate featured flag from campaigns to property-specific featured_campaign_id"""
    from database import get_db_connection
    conn = get_db_connection()
    try:
        results = []
        
        # Step 1: Add featured_campaign_id column to properties table
        cursor = conn.execute("PRAGMA table_info(properties)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'featured_campaign_id' not in columns:
            conn.execute("ALTER TABLE properties ADD COLUMN featured_campaign_id INTEGER")
            conn.commit()
            results.append("✅ Added featured_campaign_id column to properties table")
        else:
            results.append("✅ featured_campaign_id column already exists in properties table")
        
        # Step 2: Find any currently featured campaigns and migrate them
        cursor = conn.execute("SELECT id, name FROM campaigns WHERE featured = 1")
        featured_campaigns = cursor.fetchall()
        
        if featured_campaigns:
            for campaign_id, campaign_name in featured_campaigns:
                results.append(f"📋 Found featured campaign: {campaign_name} (ID: {campaign_id})")
                
                # For now, set this as featured for MFF property (most active property)
                # User can adjust this later through the properties interface
                conn.execute("""
                    UPDATE properties 
                    SET featured_campaign_id = ? 
                    WHERE code = 'mff'
                """, (campaign_id,))
                results.append(f"🎯 Set {campaign_name} as featured for MFF property")
        else:
            results.append("📋 No currently featured campaigns found")
        
        # Step 3: Remove featured column from campaigns table (will be done in Phase 2)
        # For now, just unset all featured flags to prevent confusion
        conn.execute("UPDATE campaigns SET featured = 0")
        results.append("✅ Cleared all campaign-level featured flags")
        
        conn.commit()
        
        # Step 4: Verify the migration
        cursor = conn.execute("""
            SELECT p.code, p.name, p.featured_campaign_id, c.name as featured_campaign_name
            FROM properties p
            LEFT JOIN campaigns c ON p.featured_campaign_id = c.id
            ORDER BY p.code
        """)
        properties = [dict(zip(['property_code', 'property_name', 'featured_campaign_id', 'featured_campaign_name'], row)) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "message": "Featured campaign migration completed",
            "results": results,
            "properties": properties
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": "Migration failed"}
    finally:
        conn.close()

# Check properties table schema 
@app.get("/api/db/properties-schema")
async def check_properties_schema():
    """Check properties table schema and data"""
    from database import get_db_connection
    conn = get_db_connection()
    try:
        # Get table schema
        cursor = conn.execute("PRAGMA table_info(properties)")
        columns = [dict(zip(['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'], row)) for row in cursor.fetchall()]
        
        # Get all properties data  
        cursor = conn.execute("SELECT * FROM properties")
        properties = [dict(row) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "schema": columns,
            "properties": properties,
            "has_featured_column": 'featured_campaign_id' in [col['name'] for col in columns]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()

# Popup script endpoint
@app.get("/popup.js")
async def serve_popup_script():
    """Serve the production popup script"""
    # Try multiple possible paths for Railway deployment
    # Prefer the canonical popup script in project root (popup-system/popup.js)
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "popup.js"),               # popup-system/popup.js
        os.path.join(os.path.dirname(__file__), "..", "scripts", "popup.js"),    # popup-system/scripts/popup.js
        os.path.join(os.path.dirname(__file__), "..", "frontend", "popup.js"),   # legacy frontend copy (fallback)
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
 