#!/usr/bin/env python3
"""
Standalone test for email ad PNG generation
Tests the core functionality without external dependencies
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from io import BytesIO
import hashlib

def load_font_simple(font_name: str, size: int):
    """Simple font loading with fallbacks"""
    font_candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
    ]
    
    for font_path in font_candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    
    return ImageFont.load_default()

def create_popup_style_email_ad(width=600, height=400):
    """Create email ad that matches the popup design"""
    
    # Property config
    prop_config = {
        'name': 'ModeFreeFinds',
        'primary_color': '#F7007C',
        'secondary_color': '#FFFFFF',
        'accent_color': '#111827'
    }
    
    # Mock campaign data
    campaign = {
        'name': 'Trading Tips',
        'description': 'Get exclusive trading tips and market insights delivered daily to your inbox.',
        'cta_text': 'Get Trading Tips'
    }
    
    # Create base image
    img = Image.new('RGB', (width, height), color=prop_config['secondary_color'])
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    title_font = load_font_simple("title", 24)
    desc_font = load_font_simple("desc", 14)
    cta_font = load_font_simple("cta", 18)
    
    # Layout
    padding = 20
    content_width = width - (padding * 2)
    current_y = padding
    
    # Header with tagline pill (like popup)
    pill_text = "Thanks for Reading - You've unlocked bonus offers"
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
    campaign_title = campaign['name']
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
    description = campaign['description']
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
    cta_text = campaign['cta_text']
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    text_width = bbox[2] - bbox[0]
    text_x = padding + (content_width - text_width) // 2
    text_y = current_y + (button_height - 25) // 2
    
    draw.text((text_x, text_y), cta_text, fill="white", font=cta_font)
    
    # Add footer text like popup
    current_y += button_height + 15
    footer_text = f"Grab an {campaign['name']}!"
    bbox = draw.textbbox((0, 0), footer_text, font=desc_font)
    footer_width = bbox[2] - bbox[0]
    footer_x = padding + (content_width - footer_width) // 2
    draw.text((footer_x, current_y), footer_text, fill='#6c757d', font=desc_font)
    
    return img

if __name__ == "__main__":
    print("🎨 Generating popup-style email ad...")
    
    try:
        # Generate the email ad
        img = create_popup_style_email_ad()
        
        # Save as PNG
        img.save('popup_style_email_ad.png')
        print("✅ Popup-style email ad saved as 'popup_style_email_ad.png'")
        
        # Also save as bytes to test the format
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        png_bytes = buffer.getvalue()
        
        print(f"✅ PNG generation successful! Size: {len(png_bytes)} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
