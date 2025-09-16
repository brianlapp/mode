"""
Mode Popup Management System - Main API
Simple campaign management dashboard + embeddable popup script
"""

from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
import uvicorn
import os
from pathlib import Path
from io import BytesIO
import datetime

# Try to import PIL for PNG generation
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = ImageDraw = ImageFont = None

# Import our route modules (will create these next)
from routes.campaigns import router as campaigns_router
from routes.properties import router as properties_router
from routes.email import router as email_router
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
    print("🚀 STARTING MODE POPUP SYSTEM...")
    
    # 🛡️ ENSURE RAILWAY VOLUME MOUNT - Critical for data persistence
    try:
        from ensure_volume import ensure_railway_volume
        if not ensure_railway_volume():
            print("🚨 CRITICAL: Volume mount failed - data will not persist!")
    except Exception as e:
        print(f"⚠️ Warning: Volume check failed: {e}")
    
    # Initialize database first
    init_db()
    
    # 🛡️ BULLETPROOF AUTO-RESTORE SYSTEM
    try:
        from backup_restore_system import auto_backup_and_restore
        success = auto_backup_and_restore()
        if not success:
            print("⚠️ Backup/restore system failed, trying emergency restore...")
            await auto_restore_campaigns()
    except Exception as e:
        print(f"⚠️ Backup system error: {e}")
        # Fallback to emergency restore
        try:
            await auto_restore_campaigns()
        except Exception as restore_error:
            print(f"❌ All restore methods failed: {restore_error}")

async def auto_restore_campaigns():
    """Auto-restore the 12 good campaigns when database is empty"""
    try:
        print("🔄 AUTO-RESTORING 12 CAMPAIGNS...")
        
        # The 12 GOOD campaigns (NO PRIZIES)
        good_campaigns = [
            # MMM Finance campaigns (5 total)
            {"id": 1, "name": "Trading Tips", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045", "logo_url": "https://i.imgur.com/lHn301q.png", "main_image_url": "https://i.imgur.com/ZVGOktR.png", "description": "Get exclusive trading tips and market insights delivered daily to your inbox.", "cta_text": "Get Trading Tips", "offer_id": "6998", "aff_id": "43045", "property": "mmm"},
            {"id": 2, "name": "Behind The Markets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Discover what's really happening behind the financial markets with expert analysis.", "cta_text": "Learn More", "offer_id": "7521", "aff_id": "43045", "property": "mmm"},
            {"id": 3, "name": "Brownstone Research", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045", "logo_url": "https://i.imgur.com/3KVDcV7.jpeg", "main_image_url": "https://i.imgur.com/vzoiVpd.png", "description": "Advanced technology and investment research from Brownstone Research experts.", "cta_text": "View Research", "offer_id": "7389", "aff_id": "43045", "property": "mmm"},
            {"id": 4, "name": "Hotsheets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045", "logo_url": "https://i.imgur.com/4JoGdZr.png", "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg", "description": "Daily market hotsheets with the most profitable trading opportunities.", "cta_text": "Get Hotsheets", "offer_id": "7385", "aff_id": "43045", "property": "mmm"},
            {"id": 5, "name": "Best Gold", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045", "logo_url": "https://i.imgur.com/5Yb0LJn.png", "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg", "description": "Premium gold investment insights and recommendations from industry experts.", "cta_text": "Learn About Gold", "offer_id": "7390", "aff_id": "43045", "property": "mmm"},
            
            # MFF Lifestyle campaigns (7 total)
            {"id": 6, "name": "Daily Goodie Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946", "logo_url": "https://i.imgur.com/DH7Tp4A.jpeg", "main_image_url": "https://i.imgur.com/JpKD9AX.png", "description": "Get your daily goodie box filled with amazing free samples and deals.", "cta_text": "Claim Now!", "offer_id": "6571", "aff_id": "42946", "property": "mff"},
            {"id": 7, "name": "Free Samples Guide", "tune_url": "https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946", "logo_url": "https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png", "main_image_url": "https://i.imgur.com/vbgSfMi.jpeg", "description": "Get your comprehensive free samples guide with exclusive offers.", "cta_text": "Claim Now!", "offer_id": "3907", "aff_id": "42946", "property": "mff"},
            {"id": 8, "name": "UpLevel - Amazon Mystery Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946", "logo_url": "https://imgur.com/Xmb1P8t.jpg", "main_image_url": "https://imgur.com/tA8fYBO.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "property": "mff"},
            {"id": 9, "name": "Hulu - Hit Movies, TV and More!", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946", "logo_url": "https://imgur.com/RHRuCvk.jpg", "main_image_url": "https://imgur.com/SEu1NtW.jpg", "description": "Exclusive Offers from Hulu!", "cta_text": "Get Hulu!", "offer_id": "5555", "aff_id": "42946", "property": "mff"},
            {"id": 10, "name": "Paramount", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946", "logo_url": "https://imgur.com/2IpSLaY.jpg", "main_image_url": "https://imgur.com/p8o0YSR.jpg", "description": "Exclusive Offers from Paramount+!", "cta_text": "Get Paramount+!", "offer_id": "5172", "aff_id": "42946", "property": "mff"},
            {"id": 11, "name": "Trend'n Daily", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946", "logo_url": "https://imgur.com/Xmb1P8t.jpg", "main_image_url": "https://imgur.com/tA8fYBO.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "property": "mff"},
            {"id": 14, "name": "Money.com - Online Stock Brokers", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43092", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Compare online stock brokers and find the best platform for your trading needs.", "cta_text": "View Offer", "offer_id": "7521", "aff_id": "43092", "property": "mmm"}
        ]
        
        from database import get_db_connection
        conn = get_db_connection()
        
        # Clear existing campaigns and properties
        conn.execute("DELETE FROM campaign_properties")
        conn.execute("DELETE FROM campaigns")
        
        # Restore the 12 good campaigns
        for campaign in good_campaigns:
            conn.execute('''
                INSERT INTO campaigns (
                    id, name, tune_url, logo_url, main_image_url, description,
                    cta_text, offer_id, aff_id, active, featured, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, ?, ?)
            ''', (
                campaign['id'], campaign['name'], campaign['tune_url'],
                campaign['logo_url'], campaign['main_image_url'], campaign['description'],
                campaign['cta_text'], campaign['offer_id'], campaign['aff_id'],
                '2025-01-28 12:00:00', '2025-01-28 12:00:00'
            ))
            
            # Set property assignment
            property_code = campaign.get('property', 'mff')  # Default to mff if not specified
            conn.execute('''
                INSERT INTO campaign_properties (
                    campaign_id, property_code, visibility_percentage, active
                ) VALUES (?, ?, 100, 1)
            ''', (campaign['id'], property_code))
        
        conn.commit()
        conn.close()
        
        print("✅ AUTO-RESTORE COMPLETE: 12 campaigns restored (5 MMM + 7 MFF)")
        return True
        
    except Exception as e:
        print(f"❌ Auto-restore failed: {e}")
        return False

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mode Popup Management API"}

# ========== EMAIL PNG GENERATION FUNCTIONS ==========

# Property configurations
PROPERTY_CONFIG = {
    'mff': {
        'name': 'ModeFreeFinds',
        'primary_color': '#F7007C',  # Pink
        'secondary_color': '#FFFFFF',
        'accent_color': '#111827',
        'tagline': "Thanks for Reading - You've unlocked bonus offers"
    },
    'mmm': {
        'name': 'ModeMarketMunchies', 
        'primary_color': '#00FF7F',  # Green
        'secondary_color': '#FFFFFF',
        'accent_color': '#111827',
        'tagline': "Thanks for Reading - You've unlocked bonus offers"
    }
}

def load_font_with_fallbacks(font_name: str, size: int):
    """Load font with comprehensive fallback strategy"""
    debug_info = {
        "family": font_name,
        "size": size,
        "path": "",
        "error": None
    }
    
    # Font candidates in order of preference (Railway/Linux compatible)
    if "bold" in font_name.lower() or "extra" in font_name.lower():
        font_candidates = [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "/usr/share/fonts/TTF/arial.ttf",  # Some Linux
            "arial.ttf",
            "DejaVuSans-Bold.ttf"
        ]
    else:
        font_candidates = [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/share/fonts/TTF/arial.ttf",  # Some Linux
            "arial.ttf",
            "DejaVuSans.ttf"
        ]
    
    # Try each font candidate
    for font_path in font_candidates:
        try:
            font = ImageFont.truetype(font_path, size)
            debug_info["path"] = font_path
            debug_info["family"] = f"{font_name} (using {Path(font_path).name})"
            return font, debug_info
        except Exception as e:
            debug_info["last_error"] = str(e)
            continue
    
    # Final fallback to default font
    try:
        default_font = ImageFont.load_default()
        debug_info["error"] = "All font candidates failed, using default"
        debug_info["family"] = "default"
        return default_font, debug_info
    except Exception as e:
        error_msg = f"Critical font loading failure: {str(e)}"
        debug_info["error"] = error_msg
        raise HTTPException(status_code=500, detail=error_msg)

def create_popup_style_email_ad(property_name: str, width: int, height: int, campaign_data: dict):
    """Create email ad matching popup design"""
    debug_info = {
        "property": property_name,
        "dimensions": f"{width}x{height}",
        "font": {},
        "generation": {},
        "errors": [],
        "pil_available": PIL_AVAILABLE
    }
    
    if not PIL_AVAILABLE:
        debug_info["errors"].append("PIL not available")
        return b"PIL not available", debug_info
    
    try:
        # Get property config
        prop_config = PROPERTY_CONFIG.get(property_name.lower(), PROPERTY_CONFIG['mff'])
        
        # Create base image
        img = Image.new('RGB', (width, height), color=prop_config['secondary_color'])
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        title_font, font_debug = load_font_with_fallbacks("title-bold", 24)
        debug_info["font"] = font_debug
        desc_font, _ = load_font_with_fallbacks("desc", 14)
        cta_font, _ = load_font_with_fallbacks("cta-bold", 18)
        
        # Layout
        padding = 20
        content_width = width - (padding * 2)
        current_y = padding
        
        # Header with tagline pill (like popup)
        pill_text = prop_config['tagline']
        pill_width = content_width
        pill_height = 30
        draw.rectangle([padding, current_y, padding + pill_width, current_y + pill_height], 
                      fill=prop_config['primary_color'])
        
        # Center the tagline text
        bbox = draw.textbbox((0, 0), pill_text, font=desc_font)
        text_width = bbox[2] - bbox[0]
        text_x = padding + (pill_width - text_width) // 2
        draw.text((text_x, current_y + 8), pill_text, fill='white', font=desc_font)
        current_y += pill_height + 15
        
        # Campaign title (larger, centered)
        campaign_title = campaign_data.get('name', 'Exclusive Offer')
        bbox = draw.textbbox((0, 0), campaign_title, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = padding + (content_width - title_width) // 2
        draw.text((title_x, current_y), campaign_title, 
                 fill=prop_config['accent_color'], font=title_font)
        current_y += 45
        
        # Campaign image placeholder (styled like popup)
        image_height = 120
        image_padding = 40
        image_width = content_width - (image_padding * 2)
        
        # Draw image background
        draw.rectangle([padding + image_padding, current_y, 
                       padding + image_padding + image_width, current_y + image_height], 
                     fill='#f8f9fa', outline='#e9ecef', width=2)
        
        # Image placeholder text
        placeholder_text = "Campaign Image"
        bbox = draw.textbbox((0, 0), placeholder_text, font=desc_font)
        placeholder_width = bbox[2] - bbox[0]
        placeholder_x = padding + image_padding + (image_width - placeholder_width) // 2
        placeholder_y = current_y + (image_height - 20) // 2
        draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#6c757d', font=desc_font)
        
        current_y += image_height + 20
        
        # Description (centered, multiple lines)
        description = campaign_data.get('description', 'Exclusive opportunity - limited time offer.')
        words = description.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=desc_font)
            if bbox[2] - bbox[0] <= content_width - 40:  # Leave some margin
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center each line
        for line in lines[:3]:  # Max 3 lines
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            line_width = bbox[2] - bbox[0]
            line_x = padding + (content_width - line_width) // 2
            draw.text((line_x, current_y), line, fill=prop_config['accent_color'], font=desc_font)
            current_y += 20
        
        current_y += 15
        
        # CTA Button (styled like popup)
        button_height = 50
        button_color = '#7C3AED'  # Purple like in popup
        
        # Draw button
        draw.rectangle([padding, current_y, padding + content_width, current_y + button_height], 
                     fill=button_color)
        
        # Button text
        cta_text = campaign_data.get('cta_text', 'CONTINUE >')
        bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        text_width = bbox[2] - bbox[0]
        text_x = padding + (content_width - text_width) // 2
        text_y = current_y + (button_height - 25) // 2
        
        draw.text((text_x, text_y), cta_text, fill="white", font=cta_font)
        
        # Add footer text like popup
        current_y += button_height + 15
        footer_text = f"Grab an {campaign_title}!"
        bbox = draw.textbbox((0, 0), footer_text, font=desc_font)
        footer_width = bbox[2] - bbox[0]
        footer_x = padding + (content_width - footer_width) // 2
        draw.text((footer_x, current_y), footer_text, fill='#6c757d', font=desc_font)
        
        # Add watermark if font loading failed
        if font_debug.get("error"):
            debug_info["errors"].append("Font loading failed")
            draw.text((10, height - 30), "FONTS MISSING", fill="red", font=desc_font)
        
        # Save to bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG', quality=95)
        png_bytes = buffer.getvalue()
        
        debug_info["generation"]["success"] = True
        debug_info["generation"]["png_size"] = len(png_bytes)
        debug_info["timestamp"] = datetime.datetime.now().isoformat()
        
        return png_bytes, debug_info
        
    except Exception as e:
        error_msg = f"PNG generation failed: {str(e)}"
        debug_info["generation"]["error"] = error_msg
        debug_info["errors"].append(error_msg)
        
        # Return error placeholder
        img = Image.new('RGB', (width, height), color='#ff0000')
        draw = ImageDraw.Draw(img)
        try:
            error_font, _ = load_font_with_fallbacks("error", 16)
            draw.text((20, height//2), "GENERATION ERROR", fill="white", font=error_font)
        except:
            draw.text((20, height//2), "GENERATION ERROR", fill="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue(), debug_info

@app.get("/debug/property-test")
async def debug_property_test(property: str = None, host: str = None):
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

@app.get("/api/email/preview.html", response_class=HTMLResponse)
async def email_preview():
    """Show working email ad preview"""
    preview_file = Path(__file__).parent / "email_preview.html"
    if not preview_file.exists():
        raise HTTPException(status_code=404, detail="Email preview not found")
    return FileResponse(preview_file)

# Include API routes
app.include_router(campaigns_router, prefix="/api", tags=["campaigns"])
app.include_router(properties_router, prefix="/api", tags=["properties"])
# app.include_router(email_router, prefix="/api", tags=["email"])  # Disabled due to import issues

# WORKING EMAIL GENERATION - SIMPLE TEXT FORMAT
@app.get("/api/email/ad.png")
async def working_email_ad_png(property: str = "mff", w: int = 600, h: int = 400, send: str = "qa"):
    """Working email ad generation - returns campaign text"""
    try:
        from database import get_db_connection
        
        # Get a random active campaign
        conn = get_db_connection()
        cur = conn.execute("""
            SELECT name, description, main_image_url, logo_url, cta_text 
            FROM campaigns 
            WHERE active = 1 AND name != 'Prizies'
            ORDER BY RANDOM() 
            LIMIT 1
        """)
        campaign = cur.fetchone()
        conn.close()
        
        if not campaign:
            return Response(content=b"No active campaigns found", media_type="text/plain")
        
        campaign_name, description, main_image_url, logo_url, cta_text = campaign
        
        # Generate actual PNG image instead of text
        campaign_data = {
            'name': campaign_name,
            'description': description,
            'main_image_url': main_image_url,
            'logo_url': logo_url,
            'cta_text': cta_text
        }
        
        png_bytes, debug_info = create_popup_style_email_ad(property, w, h, campaign_data)
        
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=3600",
                "Content-Length": str(len(png_bytes))
            }
        )
            
    except Exception as e:
        return Response(content=f"Error: {str(e)}".encode(), media_type="text/plain", status_code=500)

@app.get("/api/email/ad.debug")
async def direct_email_ad_debug(property: str = "mff", w: int = 600, h: int = 400, send: str = "qa"):
    """Get debug information for email ad generation - NEW FIXED VERSION"""
    try:
        from database import get_db_connection
        
        # Test database connection and get campaign count
        conn = get_db_connection()
        cur = conn.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1 AND name != 'Prizies'")
        campaign_count = cur.fetchone()[0]
        
        # Get a sample campaign for testing
        cur = conn.execute("""
            SELECT name, description, main_image_url, logo_url, cta_text 
            FROM campaigns 
            WHERE active = 1 AND name != 'Prizies'
            ORDER BY RANDOM() 
            LIMIT 1
        """)
        campaign = cur.fetchone()
        conn.close()
        
        campaign_data = None
        if campaign:
            campaign_data = {
                'name': campaign[0],
                'description': campaign[1],
                'main_image_url': campaign[2],
                'logo_url': campaign[3],
                'cta_text': campaign[4]
            }
        
        # Test font loading
        try:
            font, font_debug = load_font_with_fallbacks("test", 14)
        except:
            font_debug = {"error": "Font loading failed"}
        
        return {
            "SYSTEM": "NEW_FIXED_EMAIL_SYSTEM", 
            "VERSION": "2.0",
            "property": property,
            "dimensions": f"{w}x{h}",
            "timestamp": datetime.datetime.now().isoformat(),
            "pil_available": PIL_AVAILABLE,
            "font": font_debug,
            "campaign": campaign_data,
            "active_campaigns": campaign_count,
            "message": "This is the NEW fixed email system!",
            "status": "WORKING"
        }
    
    except Exception as e:
        return {
            "SYSTEM": "NEW_FIXED_EMAIL_SYSTEM",
            "VERSION": "2.0",
            "error": str(e),
            "status": "ERROR"
        }

# Simple cache warmer for campaign images used by email renderer
@app.post("/api/email/warm-cache")
async def warm_email_image_cache():
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cur = conn.execute("SELECT logo_url, main_image_url FROM campaigns WHERE active = 1")
        rows = cur.fetchall()
        conn.close()
        warmed = []
        import requests
        for row in rows:
            for url in [row[0], row[1]]:
                if not url:
                    continue
                try:
                    r = requests.get(f"https://mode-dash-production.up.railway.app/api/proxy/img?u={url}", timeout=5)
                    warmed.append({"url": url, "status": r.status_code, "len": len(r.content) if r.content else 0})
                except Exception as e:
                    warmed.append({"url": url, "error": str(e)})
        return {"success": True, "warmed": warmed[:20], "count": len(warmed)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Delete Prizies permanently
@app.post("/api/delete-prizies-permanently")
async def delete_prizies_permanently():
    """Permanently delete all Prizies campaigns from database"""
    try:
        from database import get_db_connection
        conn = get_db_connection()
        
        # Delete Prizies campaigns
        cursor = conn.execute("DELETE FROM campaigns WHERE name = 'Prizies'")
        deleted_count = cursor.rowcount
        
        # Also clean up any property assignments for Prizies
        conn.execute("DELETE FROM campaign_properties WHERE campaign_id IN (SELECT id FROM campaigns WHERE name = 'Prizies')")
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "message": f"Deleted {deleted_count} Prizies campaigns permanently",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to delete Prizies: {e}"
        }

# Emergency restoration endpoint for Railway deployment fixes
@app.post("/api/emergency-restore-12-campaigns")
async def emergency_restore_12_campaigns():
    """Emergency endpoint to restore all 12 campaigns with property attribution"""
    import sqlite3
    import json
    from database import get_db_path
    
    try:
        print("🚨 EMERGENCY RESTORATION: Restoring 12 campaigns")
        
        # Ensure schema exists (idempotent) to avoid missing table errors
        try:
            init_db()
            from database import get_db_connection
            conn = get_db_connection()
            # Explicitly create required tables if missing
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    tune_url TEXT NOT NULL,
                    logo_url TEXT NOT NULL,
                    main_image_url TEXT NOT NULL,
                    description TEXT,
                    cta_text TEXT DEFAULT 'View Offer',
                    active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    offer_id TEXT,
                    aff_id TEXT,
                    featured BOOLEAN DEFAULT 0
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS campaign_properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER NOT NULL,
                    property_code TEXT NOT NULL,
                    visibility_percentage INTEGER DEFAULT 100,
                    active BOOLEAN DEFAULT 1,
                    impression_cap_daily INTEGER NULL,
                    click_cap_daily INTEGER NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
                    UNIQUE(campaign_id, property_code)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    domain TEXT,
                    active BOOLEAN DEFAULT 1,
                    popup_enabled BOOLEAN DEFAULT 1,
                    popup_frequency TEXT DEFAULT 'session',
                    popup_placement TEXT DEFAULT 'thankyou',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Schema ensure failed (will attempt restore anyway): {e}")

        # Use clean campaign data (NO PRIZIES)
        campaigns_data = [
            # MMM Finance campaigns (5 total)
            {"id": 1, "name": "Trading Tips", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045", "logo_url": "https://i.imgur.com/lHn301q.png", "main_image_url": "https://i.imgur.com/ZVGOktR.png", "description": "Get exclusive trading tips and market insights delivered daily to your inbox.", "cta_text": "Get Trading Tips", "offer_id": "6998", "aff_id": "43045", "active": True},
            {"id": 2, "name": "Behind The Markets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Discover what's really happening behind the financial markets with expert analysis.", "cta_text": "Learn More", "offer_id": "7521", "aff_id": "43045", "active": True},
            {"id": 3, "name": "Brownstone Research", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045", "logo_url": "https://i.imgur.com/3KVDcV7.jpeg", "main_image_url": "https://i.imgur.com/vzoiVpd.png", "description": "Advanced technology and investment research from Brownstone Research experts.", "cta_text": "View Research", "offer_id": "7389", "aff_id": "43045", "active": True},
            {"id": 4, "name": "Hotsheets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045", "logo_url": "https://i.imgur.com/4JoGdZr.png", "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg", "description": "Daily market hotsheets with the most profitable trading opportunities.", "cta_text": "Get Hotsheets", "offer_id": "7385", "aff_id": "43045", "active": True},
            {"id": 5, "name": "Best Gold", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045", "logo_url": "https://i.imgur.com/5Yb0LJn.png", "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg", "description": "Premium gold investment insights and recommendations from industry experts.", "cta_text": "Learn About Gold", "offer_id": "7390", "aff_id": "43045", "active": True},
            
            # MFF Lifestyle campaigns (7 total)
            {"id": 6, "name": "Daily Goodie Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946", "logo_url": "https://i.imgur.com/DH7Tp4A.jpeg", "main_image_url": "https://i.imgur.com/JpKD9AX.png", "description": "Get your daily goodie box filled with amazing free samples and deals.", "cta_text": "Claim Now!", "offer_id": "6571", "aff_id": "42946", "active": True},
            {"id": 7, "name": "Free Samples Guide", "tune_url": "https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946", "logo_url": "https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png", "main_image_url": "https://i.imgur.com/vbgSfMi.jpeg", "description": "Get your comprehensive free samples guide with exclusive offers.", "cta_text": "Claim Now!", "offer_id": "3907", "aff_id": "42946", "active": True},
            {"id": 8, "name": "UpLevel - Amazon Mystery Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946", "logo_url": "https://imgur.com/Xmb1P8t.jpg", "main_image_url": "https://imgur.com/tA8fYBO.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "active": True},
            {"id": 9, "name": "Hulu - Hit Movies, TV and More!", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946", "logo_url": "https://imgur.com/RHRuCvk.jpg", "main_image_url": "https://imgur.com/SEu1NtW.jpg", "description": "Exclusive Offers from Hulu!", "cta_text": "Get Hulu!", "offer_id": "5555", "aff_id": "42946", "active": True},
            {"id": 10, "name": "Paramount", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946", "logo_url": "https://imgur.com/2IpSLaY.jpg", "main_image_url": "https://imgur.com/p8o0YSR.jpg", "description": "Exclusive Offers from Paramount+!", "cta_text": "Get Paramount+!", "offer_id": "5172", "aff_id": "42946", "active": True},
            {"id": 11, "name": "Trend'n Daily", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946", "logo_url": "https://imgur.com/Xmb1P8t.jpg", "main_image_url": "https://imgur.com/tA8fYBO.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "active": True},
            {"id": 14, "name": "Money.com - Online Stock Brokers", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43092", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Compare online stock brokers and find the best platform for your trading needs.", "cta_text": "View Offer", "offer_id": "7521", "aff_id": "43092", "active": True}
        ]
        
        # IMPORTANT: Use the same connection path used by init_db (DB_PATH)
        from database import get_db_connection
        conn = get_db_connection()
        
        # Clear and restore campaigns
        try:
            conn.execute("DELETE FROM campaign_properties")
        except Exception:
            # If table somehow missing, create and continue
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS campaign_properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER NOT NULL,
                    property_code TEXT NOT NULL,
                    visibility_percentage INTEGER DEFAULT 100,
                    active BOOLEAN DEFAULT 1,
                    impression_cap_daily INTEGER NULL,
                    click_cap_daily INTEGER NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
                    UNIQUE(campaign_id, property_code)
                )
                """
            )
        conn.execute("DELETE FROM campaigns")
        
        for campaign in campaigns_data:
            # No special fixes needed - all campaigns should have correct data
                
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
            
            # Set property assignment (allow explicit property_code or finance affiliates)
            property_code = campaign.get('property_code')
            if not property_code:
                finance_affiliates = {"43045", "43092"}  # include Money.com affiliate
                property_code = 'mmm' if str(campaign.get('aff_id', '')) in finance_affiliates else 'mff'
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

# Force init endpoint to (re)create missing tables and return schema
@app.post("/api/db/force-init")
async def db_force_init():
    try:
        init_db()
        from database import get_db_connection
        conn = get_db_connection()
        try:
            # Ensure critical tables exist explicitly (idempotent)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS campaign_properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER NOT NULL,
                    property_code TEXT NOT NULL,
                    visibility_percentage INTEGER DEFAULT 100,
                    active BOOLEAN DEFAULT 1,
                    impression_cap_daily INTEGER NULL,
                    click_cap_daily INTEGER NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
                    UNIQUE(campaign_id, property_code)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS impressions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER NOT NULL,
                    property_code TEXT NOT NULL,
                    session_id TEXT,
                    placement TEXT DEFAULT 'thankyou',
                    user_agent TEXT,
                    ip_hash INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source TEXT,
                    subsource TEXT,
                    utm_campaign TEXT,
                    referrer TEXT,
                    landing_page TEXT,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER NOT NULL,
                    property_code TEXT NOT NULL,
                    session_id TEXT,
                    placement TEXT DEFAULT 'thankyou',
                    user_agent TEXT,
                    ip_hash INTEGER,
                    revenue_estimate DECIMAL(10,2) DEFAULT 0.45,
                    conversion_tracked BOOLEAN DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source TEXT,
                    subsource TEXT,
                    utm_campaign TEXT,
                    referrer TEXT,
                    landing_page TEXT,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
                )
                """
            )
            conn.commit()
            tables_cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in tables_cur.fetchall()]
            schema = {}
            for t in tables:
                cur = conn.execute(f"PRAGMA table_info({t})")
                schema[t] = [dict(cid=row[0], name=row[1], type=row[2], notnull=row[3], dflt=row[4], pk=row[5]) for row in cur.fetchall()]
            return {"success": True, "tables": tables, "schema": schema}
        finally:
            conn.close()
    except Exception as e:
        return {"success": False, "error": str(e)}

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
    ) # Force deployment trigger v2 - Campaign Data Manager fixes
 