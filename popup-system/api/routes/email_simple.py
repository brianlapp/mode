"""
Email Ad PNG Generation Routes - Simplified for Railway deployment
Handles generation of PNG email ads with proper font loading and basic image handling
"""

import os
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from fastapi import APIRouter, HTTPException, Response
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Property configurations
PROPERTY_CONFIG = {
    'mff': {
        'name': 'ModeFreeFinds',
        'primary_color': '#F7007C',
        'secondary_color': '#FFFFFF',
        'accent_color': '#111827',
        'tagline': "Thanks for Reading - You've unlocked bonus offers"
    },
    'mmm': {
        'name': 'ModeMarketMunchies', 
        'primary_color': '#00FF7F',
        'secondary_color': '#FFFFFF',
        'accent_color': '#111827',
        'tagline': "Thanks for Reading - You've unlocked bonus offers"
    }
}

def load_font_with_fallbacks(font_name: str, size: int) -> tuple[ImageFont.FreeTypeFont, dict]:
    """Load font with comprehensive fallback strategy"""
    debug_info = {
        "family": font_name,
        "size": size,
        "path": "",
        "error": None
    }
    
    # Font candidates in order of preference
    if "bold" in font_name.lower() or "extra" in font_name.lower():
        font_candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial Bold.ttf",
            "arial.ttf",
            "DejaVuSans-Bold.ttf"
        ]
    else:
        font_candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf", 
            "arial.ttf",
            "DejaVuSans.ttf"
        ]
    
    # Try each font candidate
    for font_path in font_candidates:
        try:
            font = ImageFont.truetype(font_path, size)
            debug_info["path"] = font_path
            debug_info["family"] = f"{font_name} (using {Path(font_path).name})"
            logger.info(f"Successfully loaded font: {font_path}")
            return font, debug_info
        except Exception as e:
            debug_info["last_error"] = str(e)
            continue
    
    # Final fallback to default font
    try:
        default_font = ImageFont.load_default()
        debug_info["error"] = "All font candidates failed, using default"
        debug_info["family"] = "default"
        logger.warning(f"Using default font for {font_name}")
        return default_font, debug_info
    except Exception as e:
        error_msg = f"Critical font loading failure: {str(e)}"
        debug_info["error"] = error_msg
        raise HTTPException(status_code=500, detail=error_msg)

def create_popup_style_email_ad(property_name: str, width: int, height: int, campaign_data: dict) -> tuple[bytes, dict]:
    """Create email ad matching popup design"""
    debug_info = {
        "property": property_name,
        "dimensions": f"{width}x{height}",
        "font": {},
        "generation": {},
        "errors": []
    }
    
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
        
        # Campaign image (actual image loading)
        image_height = 120
        image_padding = 40
        image_width = content_width - (image_padding * 2)
        image_x = padding + image_padding
        
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
                        # Load and resize image
                        campaign_image = Image.open(BytesIO(image_data))
                        if campaign_image.mode in ('RGBA', 'P'):
                            campaign_image = campaign_image.convert('RGB')
                        campaign_image = campaign_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
                        debug_info["image_loading"] = f"Successfully loaded: {fixed_url} ({len(image_data)} bytes)"
                    else:
                        debug_info["image_loading"] = f"HTTP {response.status} for {fixed_url}"
                        
            except Exception as e:
                debug_info["image_loading"] = f"Failed to load {image_url}: {str(e)}"
                campaign_image = None
        
        if campaign_image:
            # Paste the actual campaign image
            img.paste(campaign_image, (image_x, current_y))
        else:
            # Draw fallback with border
            draw.rectangle([image_x, current_y, 
                           image_x + image_width, current_y + image_height], 
                         fill='#f8f9fa', outline='#e9ecef', width=2)
            
            # Fallback text
            placeholder_text = "IMAGE MISSING" if image_url else "No Image URL"
            bbox = draw.textbbox((0, 0), placeholder_text, font=desc_font)
            placeholder_width = bbox[2] - bbox[0]
            placeholder_x = image_x + (image_width - placeholder_width) // 2
            placeholder_y = current_y + (image_height - 20) // 2
            draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#dc3545', font=desc_font)
        
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
        
        import datetime
        debug_info["timestamp"] = datetime.datetime.now().isoformat()
        
        logger.info(f"Successfully generated {width}x{height} PNG for {property_name}")
        return png_bytes, debug_info
        
    except Exception as e:
        error_msg = f"PNG generation failed: {str(e)}"
        logger.error(error_msg)
        debug_info["generation"]["error"] = error_msg
        debug_info["errors"].append(error_msg)
        
        # Return error placeholder
        img = Image.new('RGB', (width, height), color='#ff0000')
        draw = ImageDraw.Draw(img)
        draw.text((20, height//2), "GENERATION ERROR", fill="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue(), debug_info

@router.get("/ad.png")
async def get_email_ad_png(
    property: str = "mff",
    w: int = 600,
    h: int = 400,
    send: str = "qa"
):
    """Generate email ad PNG"""
    try:
        # Get campaign data from database
        try:
            from database import get_db_connection
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
            
            if campaign:
                campaign_data = {
                    'name': campaign[0],
                    'description': campaign[1],
                    'main_image_url': campaign[2],
                    'logo_url': campaign[3],
                    'cta_text': campaign[4]
                }
            else:
                campaign_data = {
                    'name': 'Trading Tips',
                    'description': 'Get exclusive trading tips and market insights delivered daily to your inbox.',
                    'cta_text': 'Get Trading Tips'
                }
        except Exception as e:
            logger.warning(f"Database error, using fallback: {e}")
            campaign_data = {
                'name': 'Trading Tips',
                'description': 'Get exclusive trading tips and market insights delivered daily to your inbox.',
                'cta_text': 'Get Trading Tips'
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
        logger.error(f"PNG endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ad.debug")
async def get_email_ad_debug(
    property: str = "mff", 
    w: int = 600,
    h: int = 400,
    send: str = "qa"
):
    """Get debug information for email ad generation"""
    try:
        # Use fallback campaign data for debug
        campaign_data = {
            'name': 'Trading Tips',
            'description': 'Get exclusive trading tips and market insights delivered daily to your inbox.',
            'cta_text': 'Get Trading Tips'
        }
        
        _, debug_info = create_popup_style_email_ad(property, w, h, campaign_data)
        return debug_info
    except Exception as e:
        logger.error(f"Debug endpoint error: {str(e)}")
        return {
            "error": str(e),
            "property": property,
            "dimensions": f"{w}x{h}",
            "timestamp": "",
            "font": {"error": "Debug generation failed"},
            "generation": {"error": str(e)}
        }
