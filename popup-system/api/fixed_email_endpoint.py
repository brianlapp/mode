"""
NEW EMAIL GENERATION ENDPOINT - PROPER POPUP DIMENSIONS
No more stretched garbage - generates 320px wide images like the popup
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import sqlite3
from database import get_db_connection

router = APIRouter()

@router.get("/api/email/fixed.png")
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
