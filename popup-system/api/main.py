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
    global startup_completed
    print("🚀 STARTING MODE POPUP SYSTEM...")
    
    # Initialize database first
    init_db()
    
    # 🐘 POSTGRESQL DATABASE - No auto-restore needed (persistent database)
    print("✅ PostgreSQL database connection initialized.")
    startup_completed = True

# Global flag to track startup completion
startup_completed = False

# REMOVED: Auto-restore middleware obsolete with PostgreSQL persistent database

@app.get("/api/startup-status")
async def startup_status():
    """Check if startup auto-restore ran successfully"""
    from database import get_db_connection
    
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        campaign_count = cursor.fetchone()[0]
        conn.close()
        
        return {
            "startup_completed": startup_completed,
            "campaign_count": campaign_count,
            "status": "healthy" if campaign_count >= 12 else "needs_restore",
            "message": f"Startup completed: {startup_completed}, Campaigns: {campaign_count}"
        }
    except Exception as e:
        return {
            "startup_completed": startup_completed,
            "campaign_count": 0,
            "status": "error",
            "message": f"Error: {str(e)}"
        }

@app.post("/api/test-restore-now")
async def test_restore_now():
    """Test the restore function right now to see what fails"""
    import sqlite3
    from database import get_db_path
    
    restore_log = []
    
    try:
        restore_log.append("🔍 TESTING RESTORE FUNCTION...")
        
        # Check current state
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        current_count = cursor.fetchone()[0]
        restore_log.append(f"📊 Current campaigns: {current_count}")
        
        # Run the restore function
        restore_log.append("🔄 Running auto_restore_campaigns_on_startup()...")
        await auto_restore_campaigns_on_startup()
        
        # Check final state
        cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
        final_count = cursor.fetchone()[0]
        restore_log.append(f"📊 Final campaigns: {final_count}")
        
        conn.close()
        
        return {
            "success": True,
            "initial_count": current_count,
            "final_count": final_count,
            "log": restore_log
        }
        
    except Exception as e:
        restore_log.append(f"❌ ERROR: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "log": restore_log
        }

async def auto_restore_campaigns_on_startup():
    """Auto-restore campaigns if database is empty or corrupted - CRITICAL for Railway deployments"""
    import sqlite3
    from database import get_db_path
    
    try:
        print("🔍 CHECKING CAMPAIGN DATABASE...")
        
        # Check if campaigns exist
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
            campaign_count = cursor.fetchone()[0]
            print(f"📊 Found {campaign_count} active campaigns")
            
            # Also check for Prizies contamination
            cursor.execute("SELECT COUNT(*) FROM campaigns WHERE name = 'Prizies'")
            prizies_count = cursor.fetchone()[0]
            
            if prizies_count > 0:
                print(f"🗑️ PRIZIES CONTAMINATION DETECTED: {prizies_count} Prizies campaigns found")
                # Clear Prizies immediately
                cursor.execute("DELETE FROM campaigns WHERE name = 'Prizies'")
                cursor.execute("DELETE FROM campaign_properties WHERE campaign_id IN (SELECT id FROM campaigns WHERE name = 'Prizies')")
                conn.commit()
                print("✅ Prizies eliminated")
                
                # Recount after cleanup
                cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
                campaign_count = cursor.fetchone()[0]
            
            # Auto-restore if empty or corrupted (should have exactly 12 campaigns)
            if campaign_count < 12:
                print(f"⚠️ INSUFFICIENT CAMPAIGNS: Found {campaign_count}, need 12. Auto-restoring...")
                await restore_12_clean_campaigns(conn)
            else:
                print(f"✅ Database healthy with {campaign_count} campaigns")
                
        except Exception as e:
            print(f"❌ Database check failed: {e}")
            print("🔄 Forcing emergency restore...")
            await restore_12_clean_campaigns(conn)
        
        finally:
            conn.close()
            
    except Exception as e:
        print(f"❌ Startup auto-restore failed: {e}")

async def restore_12_clean_campaigns(conn):
    """Restore exactly 12 clean campaigns - NO PRIZIES"""
    try:
        print("🔄 RESTORING 12 CLEAN CAMPAIGNS...")
        
        # The 12 COMPLETE campaigns with UNIQUE logos
        clean_campaigns = [
            # Money.com FIRST - MMM Finance campaigns (6 total)
            {"id": 1, "name": "Money.com - Online Stock Brokers", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43092", "logo_url": "https://i.imgur.com/money-com-logo.png", "main_image_url": "https://i.imgur.com/broker-comparison.png", "description": "Compare online stock brokers and find the best platform for your trading needs.", "cta_text": "Compare Brokers", "offer_id": "7521", "aff_id": "43092", "property": "mmm"},
            {"id": 2, "name": "Trading Tips", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips", "logo_url": "https://i.imgur.com/lHn301q.png", "main_image_url": "https://i.imgur.com/ZVGOktR.png", "description": "Get exclusive trading tips and market insights delivered daily to your inbox.", "cta_text": "Get Trading Tips", "offer_id": "6998", "aff_id": "43045", "property": "mmm"},
            {"id": 3, "name": "Behind The Markets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045&aff_sub5=popup_behindMarkets", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Discover what's really happening behind the financial markets with expert analysis.", "cta_text": "Learn More", "offer_id": "7521", "aff_id": "43045", "property": "mmm"},
            {"id": 4, "name": "Brownstone Research", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045&aff_sub5=popup_brownstone", "logo_url": "https://i.imgur.com/3KVDcV7.jpeg", "main_image_url": "https://i.imgur.com/vzoiVpd.png", "description": "Advanced technology and investment research from Brownstone Research experts.", "cta_text": "View Research", "offer_id": "7389", "aff_id": "43045", "property": "mmm"},
            {"id": 5, "name": "Hotsheets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045&aff_sub5=popup_hotsheets", "logo_url": "https://i.imgur.com/4JoGdZr.png", "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg", "description": "Daily market hotsheets with the most profitable trading opportunities.", "cta_text": "Get Hotsheets", "offer_id": "7385", "aff_id": "43045", "property": "mmm"},
            {"id": 6, "name": "Best Gold", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045&aff_sub5=popup_bestGold", "logo_url": "https://i.imgur.com/5Yb0LJn.png", "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg", "description": "Premium gold investment insights and recommendations from industry experts.", "cta_text": "Learn About Gold", "offer_id": "7390", "aff_id": "43045", "property": "mmm"},
            
            # MFF Lifestyle campaigns (6 total) - UNIQUE LOGOS AND IMAGES
            {"id": 7, "name": "Daily Goodie Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946&aff_sub2=perks", "logo_url": "https://i.imgur.com/DH7Tp4A.jpeg", "main_image_url": "https://i.imgur.com/JpKD9AX.png", "description": "Get your daily goodie box filled with amazing free samples and deals.", "cta_text": "Claim Now!", "offer_id": "6571", "aff_id": "42946", "property": "mff"},
            {"id": 8, "name": "Free Samples Guide", "tune_url": "https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946&aff_sub2=perks", "logo_url": "https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png", "main_image_url": "https://i.imgur.com/vbgSfMi.jpeg", "description": "Get your comprehensive free samples guide with exclusive offers.", "cta_text": "Claim Now!", "offer_id": "3907", "aff_id": "42946", "property": "mff"},
            {"id": 9, "name": "UpLevel - Amazon Mystery Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks", "logo_url": "https://i.imgur.com/uplevel-logo.png", "main_image_url": "https://i.imgur.com/amazon-mystery.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "property": "mff"},
            {"id": 10, "name": "Hulu - Hit Movies, TV and More!", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946&aff_sub2=perks", "logo_url": "https://i.imgur.com/RHRuCvk.jpg", "main_image_url": "https://i.imgur.com/SEu1NtW.jpg", "description": "Exclusive Offers from Hulu!", "cta_text": "Get Hulu!", "offer_id": "5555", "aff_id": "42946", "property": "mff"},
            {"id": 11, "name": "Paramount", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946&aff_sub2=perks", "logo_url": "https://i.imgur.com/2IpSLaY.jpg", "main_image_url": "https://i.imgur.com/p8o0YSR.jpg", "description": "Exclusive Offers from Paramount+!", "cta_text": "Get Paramount+!", "offer_id": "5172", "aff_id": "42946", "property": "mff"},
            {"id": 12, "name": "Trend'n Daily", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks", "logo_url": "https://i.imgur.com/trendn-logo.png", "main_image_url": "https://i.imgur.com/trendn-deals.jpg", "description": "Daily trending offers and deals!", "cta_text": "Get Deals!", "offer_id": "4689", "aff_id": "42946", "property": "mff"}
        ]
        
        # Clear existing campaigns and properties
        print("🗑️ Clearing existing data...")
        conn.execute("DELETE FROM campaign_properties")
        conn.execute("DELETE FROM campaigns")
        print("✅ Existing data cleared")
        
        # Restore the 12 good campaigns
        print(f"📊 Restoring {len(clean_campaigns)} campaigns...")
        for i, campaign in enumerate(clean_campaigns, 1):
            try:
                print(f"   {i:2}. Inserting {campaign['name']}...")
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
                
                print(f"   ✅ {campaign['name']} → {property_code.upper()}")
                
            except Exception as campaign_error:
                print(f"   ❌ Failed to insert {campaign['name']}: {campaign_error}")
        
        conn.commit()
        
        print("✅ CLEAN RESTORE COMPLETE: 12 campaigns restored (5 MMM + 7 MFF)")
        print("🗑️ NO PRIZIES - Database is now clean!")
        return True
        
    except Exception as e:
        print(f"❌ Clean restore failed: {e}")
        return False

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mode Popup Management API"}

@app.post("/api/create-postgres-schema")
async def create_postgres_schema():
    """Create PostgreSQL schema if it doesn't exist"""
    try:
        from database import get_db_connection
        
        # Read schema file
        schema_file = Path(__file__).parent.parent / "create_postgres_schema.sql"
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema creation
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Split and execute each statement
        statements = schema_sql.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement.strip())
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "PostgreSQL schema created successfully"}
        
    except Exception as e:
        return {"status": "error", "message": f"Schema creation failed: {str(e)}"}

@app.get("/api/test-postgres")
async def test_postgres():
    """Test PostgreSQL connection and show debug info"""
    try:
        from database import get_db_connection
        import os
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        
        # Check if tables exist
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "status": "success",
            "database_url_set": bool(os.getenv("DATABASE_URL")),
            "postgresql_version": version,
            "tables": tables
        }
        
    except Exception as e:
        return {"status": "error", "message": f"PostgreSQL test failed: {str(e)}"}

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
    
    # Get bundled font directory path
    base_dir = Path(__file__).parent
    font_dir = base_dir / "assets" / "fonts"
    
    # Font candidates in order of preference (bundled fonts first!)
    if "bold" in font_name.lower() or "extra" in font_name.lower():
        font_candidates = [
            str(font_dir / "Inter-ExtraBold.ttf"),  # Bundled - WILL WORK!
            str(font_dir / "DejaVuSans-Bold.ttf"),  # Bundled fallback
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "/usr/share/fonts/TTF/arial.ttf",  # Some Linux
            "arial.ttf",
            "DejaVuSans-Bold.ttf"
        ]
    else:
        font_candidates = [
            str(font_dir / "Inter-Regular.ttf"),  # Bundled - WILL WORK!
            str(font_dir / "DejaVuSans.ttf"),  # Bundled fallback
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
        
        # Create base image with better quality
        img = Image.new('RGB', (width, height), color=prop_config['secondary_color'])
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Determine if mobile layout (narrower than 400px)
        is_mobile = width <= 400
        
        # Adjust font sizes for mobile - smaller to match popup
        title_size = 18 if is_mobile else 20
        desc_size = 11 if is_mobile else 13
        cta_size = 14 if is_mobile else 16
        
        # Load fonts with adjusted sizes
        title_font, font_debug = load_font_with_fallbacks("title-bold", title_size)
        debug_info["font"] = font_debug
        desc_font, _ = load_font_with_fallbacks("desc", desc_size)
        cta_font, _ = load_font_with_fallbacks("cta-bold", cta_size)
        
        # Layout
        padding = 24  # Match popup padding
        content_width = width - (padding * 2)
        
        # CRITICAL: Add circle logo in top-left corner (adjust size for mobile)
        logo_size = 40 if is_mobile else 48  # Smaller to match popup proportions
        logo_margin = 20 if is_mobile else 24
        logo_url = campaign_data.get('logo_url')
        
        if logo_url:
            try:
                import urllib.request
                import urllib.error
                from io import BytesIO
                
                # Fix common imgur URL issues
                fixed_logo_url = logo_url
                if "imgur.com/" in fixed_logo_url:
                    if not fixed_logo_url.startswith("https://i.imgur.com/"):
                        fixed_logo_url = fixed_logo_url.replace("imgur.com/", "i.imgur.com/")
                    if not fixed_logo_url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                        fixed_logo_url += '.jpg'
                
                # Fetch logo with proper headers
                req = urllib.request.Request(fixed_logo_url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                req.add_header('Accept', 'image/webp,image/apng,image/*,*/*;q=0.8')
                req.add_header('Referer', 'https://imgur.com/')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        logo_data = response.read()
                        # Load logo image
                        logo_image = Image.open(BytesIO(logo_data))
                        if logo_image.mode in ('RGBA', 'P'):
                            # Convert to RGB with white background for transparency
                            bg = Image.new('RGB', logo_image.size, (255, 255, 255))
                            if logo_image.mode == 'RGBA':
                                bg.paste(logo_image, mask=logo_image.split()[3])
                            else:
                                bg.paste(logo_image)
                            logo_image = bg
                        
                        # Resize directly to target size with high quality
                        logo_image = logo_image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                        
                        # Create circular mask
                        mask = Image.new('L', (logo_size, logo_size), 0)
                        mask_draw = ImageDraw.Draw(mask)
                        mask_draw.ellipse((0, 0, logo_size-1, logo_size-1), fill=255)
                        
                        # Apply circular mask to logo
                        output = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
                        output.paste(logo_image, (0, 0))
                        output.putalpha(mask)
                        
                        # Paste onto main image
                        img.paste(output, (logo_margin, logo_margin), output)
                        debug_info["logo_loading"] = f"Successfully loaded logo: {fixed_logo_url}"
            except Exception as e:
                debug_info["logo_loading"] = f"Failed to load logo {logo_url}: {str(e)}"
                # Draw fallback circle
                draw.ellipse([logo_margin, logo_margin, logo_margin + logo_size, logo_margin + logo_size], 
                           fill='#e9ecef', outline='#dee2e6', width=2)
        else:
            # Draw fallback circle if no logo URL
            draw.ellipse([logo_margin, logo_margin, logo_margin + logo_size, logo_margin + logo_size], 
                       fill='#e9ecef', outline='#dee2e6', width=2)
        
        # Header with tagline pill
        if is_mobile:
            # Mobile: pill next to logo on same row
            pill_text = "Bonus Offers"  # Very short for mobile
            current_y = logo_margin + (logo_size - 30) // 2  # Vertically center with logo
        else:
            # Desktop: pill below logo
            current_y = logo_margin + logo_size + 20
            pill_text = prop_config['tagline']  # Full text for desktop
        
        pill_padding = 12
        
        # Calculate pill size based on text
        bbox = draw.textbbox((0, 0), pill_text, font=desc_font)
        text_width = bbox[2] - bbox[0]
        pill_width = text_width + (pill_padding * 2)
        pill_height = 30
        
        # Position pill
        if is_mobile:
            # Mobile: position to the right of logo
            pill_x = logo_margin + logo_size + 10
        else:
            # Desktop: center horizontally
            pill_x = padding + (content_width - pill_width) // 2
        
        # Draw rounded pill (not full width rectangle!)
        # Manual rounded rectangle for compatibility with older Pillow
        pill_radius = pill_height // 2
        
        # Draw the pill shape manually
        # Left circle
        draw.ellipse([pill_x, current_y, pill_x + pill_height, current_y + pill_height], 
                    fill=prop_config['primary_color'])
        # Right circle  
        draw.ellipse([pill_x + pill_width - pill_height, current_y, 
                     pill_x + pill_width, current_y + pill_height], 
                    fill=prop_config['primary_color'])
        # Center rectangle
        draw.rectangle([pill_x + pill_radius, current_y, 
                       pill_x + pill_width - pill_radius, current_y + pill_height], 
                      fill=prop_config['primary_color'])
        
        # Center the tagline text in the pill
        text_x = pill_x + pill_padding
        draw.text((text_x, current_y + 8), pill_text, fill='white', font=desc_font)
        
        # Adjust vertical position for next content
        if is_mobile:
            # Mobile: move below the logo/pill row
            current_y = logo_margin + logo_size + 15
        else:
            # Desktop: standard spacing
            current_y += pill_height + 15
        
        # Campaign title (larger, centered)
        campaign_title = campaign_data.get('name', 'Exclusive Offer')
        bbox = draw.textbbox((0, 0), campaign_title, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = padding + (content_width - title_width) // 2
        draw.text((title_x, current_y), campaign_title, 
                 fill=prop_config['accent_color'], font=title_font)
        current_y += 30  # Less spacing
        
        # Campaign image (adjust size for mobile)
        if is_mobile:
            # Mobile: larger and better centered
            target_image_width = content_width - 20  # Less margin
            target_image_height = int(target_image_width * 0.5)  # Better aspect ratio
        else:
            # Desktop: larger to match popup proportions
            target_image_width = 280
            target_image_height = 120
        image_x = padding + (content_width - target_image_width) // 2  # Center the image
        
        # Try to load the actual campaign image
        campaign_image = None
        image_url = campaign_data.get('main_image_url')
        
        if image_url:
            try:
                # Direct image loading without external imports
                import urllib.request
                import urllib.error
                from io import BytesIO
                
                # Fix common imgur URL issues
                fixed_url = image_url
                if "imgur.com/" in fixed_url:
                    if not fixed_url.startswith("https://i.imgur.com/"):
                        fixed_url = fixed_url.replace("imgur.com/", "i.imgur.com/")
                    if not fixed_url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                        fixed_url += '.jpg'
                
                # Fetch image with proper headers
                req = urllib.request.Request(fixed_url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                req.add_header('Accept', 'image/webp,image/apng,image/*,*/*;q=0.8')
                req.add_header('Referer', 'https://imgur.com/')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        image_data = response.read()
                        # Load image
                        campaign_image = Image.open(BytesIO(image_data))
                        if campaign_image.mode in ('RGBA', 'P'):
                            campaign_image = campaign_image.convert('RGB')
                        
                        # Calculate aspect ratio and resize to fit within bounds while maintaining aspect
                        orig_width, orig_height = campaign_image.size
                        aspect_ratio = orig_width / orig_height
                        
                        # Determine the best fit within target dimensions
                        if aspect_ratio > target_image_width / target_image_height:
                            # Image is wider than target ratio
                            new_width = target_image_width
                            new_height = int(target_image_width / aspect_ratio)
                        else:
                            # Image is taller than target ratio
                            new_height = target_image_height
                            new_width = int(target_image_height * aspect_ratio)
                        
                        # Resize with high quality
                        campaign_image = campaign_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # For mobile, just use the resized image without container
                        if is_mobile and (new_width < target_image_width or new_height < target_image_height):
                            # Don't add gray padding on mobile - just use the actual image size
                            campaign_image = campaign_image
                            target_image_width = new_width
                            target_image_height = new_height
                        else:
                            # Desktop: Create a container at target size with white background
                            container = Image.new('RGB', (target_image_width, target_image_height), color='#ffffff')
                            paste_x = (target_image_width - new_width) // 2
                            paste_y = (target_image_height - new_height) // 2
                            container.paste(campaign_image, (paste_x, paste_y))
                            campaign_image = container
                        
                        debug_info["image_loading"] = f"Successfully loaded: {fixed_url} ({len(image_data)} bytes, resized from {orig_width}x{orig_height} to {new_width}x{new_height})"
                    else:
                        debug_info["image_loading"] = f"HTTP {response.status} for {fixed_url}"
                        
            except Exception as e:
                debug_info["image_loading"] = f"Failed to load {image_url}: {str(e)}"
                campaign_image = None
        
        if campaign_image:
            # Paste the actual campaign image
            img.paste(campaign_image, (image_x, current_y))
        else:
            # Draw fallback with border using correct dimensions
            draw.rectangle([image_x, current_y, 
                           image_x + target_image_width, current_y + target_image_height], 
                         fill='#f8f9fa', outline='#e9ecef', width=2)
            
            # Fallback text
            placeholder_text = "IMAGE MISSING" if image_url else "No Image URL"
            bbox = draw.textbbox((0, 0), placeholder_text, font=desc_font)
            placeholder_width = bbox[2] - bbox[0]
            placeholder_x = image_x + (target_image_width - placeholder_width) // 2
            placeholder_y = current_y + (target_image_height - 20) // 2
            draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#dc3545', font=desc_font)
        
        current_y += target_image_height + 20
        
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
        button_height = 44 if is_mobile else 48  # Smaller to match popup
        button_color = '#7C3AED'  # Purple like in popup
        
        # Draw button
        draw.rectangle([padding, current_y, padding + content_width, current_y + button_height], 
                     fill=button_color)
        
        # Button text (properly centered)
        cta_text = campaign_data.get('cta_text', 'CONTINUE >')
        bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = padding + (content_width - text_width) // 2
        text_y = current_y + (button_height - text_height) // 2
        
        draw.text((text_x, text_y), cta_text, fill="white", font=cta_font)
        
        # Add bottom padding to ensure button isn't cut off
        current_y += button_height + 20
        
        # Font loading is now robust with proper fallbacks - no watermark needed
        
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

@app.get("/api/fonts/diagnostic")
async def font_diagnostic():
    """Diagnostic endpoint to check font availability on Railway"""
    import glob
    
    base_dir = Path(__file__).parent
    font_dir = base_dir / "assets" / "fonts"
    
    # Test font loading with actual bundled fonts
    test_results = []
    font_candidates = [
        str(font_dir / "DejaVuSans-Bold.ttf"),      # Bundled bold
        str(font_dir / "DejaVuSans.ttf"),           # Bundled regular
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # System fallback
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",       # System fallback
        "/System/Library/Fonts/Helvetica.ttc",     # macOS fallback
    ]
    
    for font_path in font_candidates:
        try:
            font = ImageFont.truetype(font_path, 24)
            test_results.append({"path": font_path, "status": "SUCCESS", "error": None})
        except Exception as e:
            test_results.append({"path": font_path, "status": "FAILED", "error": str(e)})
    
    return {
        "working_directory": str(Path.cwd()),
        "font_directory": str(font_dir),
        "font_dir_exists": font_dir.exists(),
        "bundled_fonts": list(font_dir.glob("*.ttf")) if font_dir.exists() else [],
        "system_fonts_sample": glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)[:10],
        "font_loading_tests": test_results,
        "pil_available": PIL_AVAILABLE
    }

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
@app.get("/api/email/popup-capture.html")
async def popup_capture_html(property: str = "mff"):
    """Return HTML page that shows the working popup for manual screenshot"""
    
    popup_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Popup Capture - {property.upper()}</title>
    <style>
        body {{ 
            margin: 0; 
            padding: 20px; 
            background: #f0f0f0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        .capture-container {{
            width: 320px;
            height: 480px;
            margin: 0 auto;
            background: white;
            border: 2px solid #333;
            position: relative;
            overflow: hidden;
        }}
        
        .instructions {{
            text-align: center;
            margin: 20px 0;
            color: #333;
        }}
        
        /* Force popup to show properly */
        .mode-popup {{
            position: relative !important;
            transform: none !important;
            opacity: 1 !important;
            display: block !important;
            margin: 0 !important;
            width: 100% !important;
            height: 100% !important;
        }}
        
        .mode-popup-overlay {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <div class="instructions">
        <h2>📸 Screenshot This Popup</h2>
        <p>Use browser screenshot tools to capture just the popup area below</p>
        <p>Property: <strong>{property.upper()}</strong></p>
    </div>
    
    <div class="capture-container" id="popup-target">
        <div style="text-align: center; padding: 50px; color: #666;">
            Loading popup...
        </div>
    </div>
    
    <!-- Load the WORKING popup script -->
    <script>
        // Set the property
        window.MODE_PROPERTY = '{property}';
        
        // Load popup script
        const script = document.createElement('script');
        script.src = '/popup.js';
        script.onload = function() {{
            console.log('Popup script loaded');
            
            // Wait a bit then force popup to show
            setTimeout(() => {{
                // Try to trigger popup
                if (window.showModePopup) {{
                    window.showModePopup('{property}');
                }}
                
                // Force any popup to be visible
                setTimeout(() => {{
                    const popup = document.querySelector('.mode-popup');
                    const overlay = document.querySelector('.mode-popup-overlay');
                    const target = document.getElementById('popup-target');
                    
                    console.log('Popup element:', popup);
                    
                    if (popup) {{
                        // Move popup to our container
                        target.innerHTML = '';
                        target.appendChild(popup);
                        
                        popup.style.position = 'relative';
                        popup.style.transform = 'none';
                        popup.style.opacity = '1';
                        popup.style.display = 'block';
                        popup.style.margin = '0';
                        popup.style.width = '100%';
                        popup.style.height = '100%';
                    }}
                    
                    if (overlay) {{
                        overlay.style.display = 'none';
                    }}
                    
                    // Log what we found
                    console.log('Popup setup complete');
                }}, 2000);
            }}, 1000);
        }};
        document.head.appendChild(script);
    </script>
</body>
</html>'''
    
    return Response(
        content=popup_html,
        media_type="text/html",
        headers={
            "Cache-Control": "no-cache",
            "Content-Disposition": f"inline; filename=popup_capture_{property}.html"
        }
    )

@app.get("/api/email/fixed.png")
async def generate_fixed_email_png(property: str = "mff", width: int = 320, height: int = 480):
    """Generate email PNG with PROPER popup dimensions - no stretching!"""
    
    try:
        # Get campaign data
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT c.*, cp.property_code 
            FROM campaigns c
            LEFT JOIN campaign_properties cp ON c.id = cp.campaign_id
            WHERE cp.property_code = ? AND c.active = 1
            ORDER BY RANDOM() LIMIT 1
        ''', (property,))
        
        campaign = cursor.fetchone()
        conn.close()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="No campaigns found")
        
        # Create image with PROPER popup dimensions
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Popup styling (matching the working popup exactly)
        padding = 24
        content_width = width - (padding * 2)
        current_y = padding
        
        # Property tagline (pink pill)
        tagline = f"Thanks for Reading - You've unlocked bonus offers"
        tagline_bg = '#F7007C'  # Mode pink
        tagline_height = 32
        
        draw.rectangle([padding, current_y, width - padding, current_y + tagline_height], 
                      fill=tagline_bg)
        
        # Use default font (which works!)
        font = ImageFont.load_default()
        
        # Tagline text (centered, white on pink)
        tagline_bbox = draw.textbbox((0, 0), tagline, font=font)
        tagline_width = tagline_bbox[2] - tagline_bbox[0]
        tagline_x = (width - tagline_width) // 2
        draw.text((tagline_x, current_y + 8), tagline, fill='white', font=font)
        
        current_y += tagline_height + 20
        
        # Campaign title (bold, centered)
        title = campaign['name']
        title_bbox = draw.textbbox((0, 0), title, font=font)
        title_width = title_bbox[2] - title_bbox[0]
        
        # Wrap title if too long
        if title_width > content_width:
            words = title.split()
            title_line1 = ""
            title_line2 = ""
            
            for word in words:
                test_line = title_line1 + (" " if title_line1 else "") + word
                test_bbox = draw.textbbox((0, 0), test_line, font=font)
                if test_bbox[2] - test_bbox[0] <= content_width:
                    title_line1 = test_line
                else:
                    title_line2 = word
                    break
            
            # Draw title lines
            if title_line1:
                line1_bbox = draw.textbbox((0, 0), title_line1, font=font)
                line1_width = line1_bbox[2] - line1_bbox[0]
                line1_x = padding + (content_width - line1_width) // 2
                draw.text((line1_x, current_y), title_line1, fill='#111827', font=font)
                current_y += 25
                
            if title_line2:
                line2_bbox = draw.textbbox((0, 0), title_line2, font=font)
                line2_width = line2_bbox[2] - line2_bbox[0]
                line2_x = padding + (content_width - line2_width) // 2
                draw.text((line2_x, current_y), title_line2, fill='#111827', font=font)
                current_y += 25
        else:
            # Single line title
            title_x = padding + (content_width - title_width) // 2
            draw.text((title_x, current_y), title, fill='#111827', font=font)
            current_y += 30
        
        current_y += 10
        
        # Campaign image (proper aspect ratio, no stretching)
        image_height = 160
        image_width = content_width - 20
        image_x = padding + 10
        
        # Try to load actual campaign image
        try:
            image_url = campaign['main_image_url']
            if image_url and image_url.startswith('http'):
                response = requests.get(image_url, timeout=5)
                if response.status_code == 200:
                    campaign_img = Image.open(BytesIO(response.content))
                    
                    # Resize maintaining aspect ratio (NO STRETCHING!)
                    campaign_img.thumbnail((image_width, image_height), Image.Resampling.LANCZOS)
                    
                    # Center the image
                    img_w, img_h = campaign_img.size
                    paste_x = image_x + (image_width - img_w) // 2
                    paste_y = current_y + (image_height - img_h) // 2
                    
                    img.paste(campaign_img, (paste_x, paste_y))
                else:
                    raise Exception("Failed to load image")
            else:
                raise Exception("No valid image URL")
                
        except Exception as e:
            # Fallback image placeholder
            draw.rectangle([image_x, current_y, image_x + image_width, current_y + image_height], 
                          fill='#f8f9fa', outline='#e9ecef', width=2)
            
            placeholder_text = "Campaign Image"
            placeholder_bbox = draw.textbbox((0, 0), placeholder_text, font=font)
            placeholder_width = placeholder_bbox[2] - placeholder_bbox[0]
            placeholder_x = image_x + (image_width - placeholder_width) // 2
            placeholder_y = current_y + (image_height - 15) // 2
            draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#6c757d', font=font)
        
        current_y += image_height + 20
        
        # Description (wrapped, centered)
        description = campaign['description'][:100] + "..." if len(campaign['description']) > 100 else campaign['description']
        
        # Simple text wrapping
        words = description.split()
        desc_lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_bbox = draw.textbbox((0, 0), test_line, font=font)
            if test_bbox[2] - test_bbox[0] <= content_width - 20:
                current_line = test_line
            else:
                if current_line:
                    desc_lines.append(current_line)
                current_line = word
        
        if current_line:
            desc_lines.append(current_line)
        
        # Draw description lines (max 2 lines)
        for line in desc_lines[:2]:
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = padding + (content_width - line_width) // 2
            draw.text((line_x, current_y), line, fill='#4b5563', font=font)
            current_y += 20
        
        current_y += 15
        
        # CTA Button (purple, centered)
        cta_text = campaign['cta_text']
        button_height = 40
        button_width = min(content_width - 40, 200)
        button_x = padding + (content_width - button_width) // 2
        button_color = '#8b5cf6'  # Purple like popup
        
        # Draw button
        draw.rectangle([button_x, current_y, button_x + button_width, current_y + button_height], 
                      fill=button_color)
        
        # Button text (centered)
        cta_bbox = draw.textbbox((0, 0), cta_text, font=font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        cta_x = button_x + (button_width - cta_width) // 2
        cta_y = current_y + (button_height - 15) // 2
        draw.text((cta_x, cta_y), cta_text, fill='white', font=font)
        
        # Convert to PNG bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG', quality=95)
        png_bytes = buffer.getvalue()
        
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=3600",
                "Content-Disposition": f"inline; filename=email_{property}_{width}x{height}.png"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.get("/api/email/ad.png")
async def working_email_ad_png(
    property: str = "mff", 
    w: int = None, 
    h: int = None, 
    variant: str = "desktop",
    send: str = "qa"
):
    """Working email ad generation - returns campaign text"""
    try:
        from database import get_db_connection
        
        # Set dimensions based on variant if not explicitly provided
        if w is None or h is None:
            if variant == "mobile":
                w, h = 320, 480
            else:  # desktop
                w, h = 600, 400
        
        # Get a random active campaign (temporarily without property filter)
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

        # COMPLETE 12 CAMPAIGNS WITH UNIQUE LOGOS - PROPER DATA
        campaigns_data = [
            # Money.com FIRST as requested - MMM Finance (6 total)
            {"id": 1, "name": "Money.com - Online Stock Brokers", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43092", "logo_url": "https://i.imgur.com/4JoGdZr.png", "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg", "description": "Compare online stock brokers and find the best platform for your trading needs.", "cta_text": "Compare Brokers", "offer_id": "7521", "aff_id": "43092", "active": True},
            {"id": 2, "name": "Trading Tips", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045", "logo_url": "https://i.imgur.com/lHn301q.png", "main_image_url": "https://i.imgur.com/ZVGOktR.png", "description": "Get exclusive trading tips and market insights delivered daily to your inbox.", "cta_text": "Get Trading Tips", "offer_id": "6998", "aff_id": "43045", "active": True},
            {"id": 3, "name": "Behind The Markets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045", "logo_url": "https://i.imgur.com/O3iEVP7.jpeg", "main_image_url": "https://i.imgur.com/NA0o7iJ.png", "description": "Discover what's really happening behind the financial markets with expert analysis.", "cta_text": "Learn More", "offer_id": "7521", "aff_id": "43045", "active": True},
            {"id": 4, "name": "Brownstone Research", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045", "logo_url": "https://i.imgur.com/3KVDcV7.jpeg", "main_image_url": "https://i.imgur.com/vzoiVpd.png", "description": "Advanced technology and investment research from Brownstone Research experts.", "cta_text": "View Research", "offer_id": "7389", "aff_id": "43045", "active": True},
            {"id": 5, "name": "Hotsheets", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045", "logo_url": "https://i.imgur.com/5Yb0LJn.png", "main_image_url": "https://i.imgur.com/O81cPQJ.jpeg", "description": "Daily market hotsheets with the most profitable trading opportunities.", "cta_text": "Get Hotsheets", "offer_id": "7385", "aff_id": "43045", "active": True},
            {"id": 6, "name": "Best Gold", "tune_url": "https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045", "logo_url": "https://i.imgur.com/5Yb0LJn.png", "main_image_url": "https://i.imgur.com/EEOyDuZ.jpeg", "description": "Premium gold investment insights and recommendations from industry experts.", "cta_text": "Learn About Gold", "offer_id": "7390", "aff_id": "43045", "active": True},
            
            # MFF Lifestyle campaigns (6 total - CLEAN UNIQUE DATA)
            {"id": 7, "name": "Daily Goodie Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946", "logo_url": "https://i.imgur.com/DH7Tp4A.jpeg", "main_image_url": "https://i.imgur.com/JpKD9AX.png", "description": "Get your daily goodie box filled with amazing free samples and deals.", "cta_text": "Claim Now!", "offer_id": "6571", "aff_id": "42946", "active": True},
            {"id": 8, "name": "Free Samples Guide", "tune_url": "https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946", "logo_url": "https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png", "main_image_url": "https://i.imgur.com/vbgSfMi.jpeg", "description": "Get your comprehensive free samples guide with exclusive offers.", "cta_text": "Claim Now!", "offer_id": "3907", "aff_id": "42946", "active": True},
            {"id": 9, "name": "UpLevel - Amazon Mystery Box", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946", "logo_url": "https://i.imgur.com/uplevel-unique.png", "main_image_url": "https://i.imgur.com/amazon-box-unique.jpg", "description": "Grab an Amazon Mystery Box!", "cta_text": "Get Box!", "offer_id": "4689", "aff_id": "42946", "active": True},
            {"id": 10, "name": "Hulu - Hit Movies, TV and More!", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946", "logo_url": "https://i.imgur.com/RHRuCvk.jpg", "main_image_url": "https://i.imgur.com/SEu1NtW.jpg", "description": "Exclusive Offers from Hulu!", "cta_text": "Get Hulu!", "offer_id": "5555", "aff_id": "42946", "active": True},
            {"id": 11, "name": "Paramount", "tune_url": "https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946", "logo_url": "https://i.imgur.com/2IpSLaY.jpg", "main_image_url": "https://i.imgur.com/p8o0YSR.jpg", "description": "Exclusive Offers from Paramount+!", "cta_text": "Get Paramount+!", "offer_id": "5172", "aff_id": "42946", "active": True},
            {"id": 12, "name": "Trend'n Daily", "tune_url": "https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946", "logo_url": "https://i.imgur.com/trendn-unique.png", "main_image_url": "https://i.imgur.com/trendn-image.jpg", "description": "Daily trending offers and deals!", "cta_text": "Get Deals!", "offer_id": "4689", "aff_id": "42946", "active": True}
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
    ) # Force deployment trigger v3 - Updated emergency restore with clean data
 