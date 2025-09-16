#!/usr/bin/env python3
"""
FIXED EMAIL GENERATOR - Based on actual popup screenshot
Creates email ads that match the real popup design exactly
"""

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json

def create_popup_style_email(campaign_data, width=320, height=480):
    """Create email that matches the EXACT popup design from screenshot"""
    
    # Create image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load fonts - try to get larger sizes
    try:
        # Try to load better fonts
        font_title = ImageFont.truetype("Arial", 24)  # Large title
        font_desc = ImageFont.truetype("Arial", 14)   # Description
        font_small = ImageFont.truetype("Arial", 12)  # Header text
        font_button = ImageFont.truetype("Arial", 16) # Button text
    except:
        # Fallback to default but try to make them bigger
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_button = ImageFont.load_default()
    
    padding = 20
    current_y = padding
    
    # 1. CIRCLE LOGO (top left) - Blue circle with white mountain icon
    logo_size = 48
    logo_x = padding
    logo_y = current_y
    
    # Draw blue circle
    draw.ellipse([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], 
                fill='#1e40af')  # Blue color
    
    # Draw simple mountain icon (white triangle)
    mountain_points = [
        (logo_x + logo_size//2, logo_y + 12),           # Top point
        (logo_x + 12, logo_y + logo_size - 12),         # Bottom left
        (logo_x + logo_size - 12, logo_y + logo_size - 12)  # Bottom right
    ]
    draw.polygon(mountain_points, fill='white')
    
    # 2. PINK PILL HEADER (centered, not full width!)
    header_text = "Thanks for Reading - You've unlocked bonus offers"
    
    # Calculate text size for pill
    text_bbox = draw.textbbox((0, 0), header_text, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Pill dimensions
    pill_padding = 16
    pill_width = text_width + (pill_padding * 2)
    pill_height = text_height + 12
    pill_x = (width - pill_width) // 2  # Centered
    pill_y = current_y + 8
    
    # Draw rounded pill background
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_width, pill_y + pill_height],
        radius=pill_height//2,  # Fully rounded
        fill='#F7007C'  # Mode pink
    )
    
    # Draw white text on pink pill
    text_x = pill_x + pill_padding
    text_y = pill_y + 6
    draw.text((text_x, text_y), header_text, fill='white', font=font_small)
    
    current_y = pill_y + pill_height + 25
    
    # 3. CAMPAIGN TITLE (large, bold, centered)
    title = campaign_data.get('name', 'Campaign Title')
    
    # Draw title with proper size
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    draw.text((title_x, current_y), title, fill='#1f2937', font=font_title)
    current_y += 35
    
    # 4. CAMPAIGN IMAGE (large, centered, with proper aspect ratio)
    image_height = 180
    image_width = width - (padding * 2)
    image_x = padding
    
    try:
        image_url = campaign_data.get('main_image_url')
        if image_url:
            print(f"Loading image: {image_url}")
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                campaign_img = Image.open(BytesIO(response.content))
                
                # Resize maintaining aspect ratio
                campaign_img.thumbnail((image_width, image_height), Image.Resampling.LANCZOS)
                
                # Center the image
                img_w, img_h = campaign_img.size
                paste_x = image_x + (image_width - img_w) // 2
                paste_y = current_y + (image_height - img_h) // 2
                
                img.paste(campaign_img, (paste_x, paste_y))
                print(f"✅ Image loaded: {img_w}x{img_h}")
            else:
                raise Exception(f"HTTP {response.status_code}")
        else:
            raise Exception("No image URL")
            
    except Exception as e:
        print(f"❌ Image failed: {e}")
        # Draw a better placeholder that looks more like the real popup
        draw.rounded_rectangle(
            [image_x, current_y, image_x + image_width, current_y + image_height],
            radius=8,
            fill='#f3f4f6',
            outline='#e5e7eb',
            width=2
        )
        
        # Placeholder text
        placeholder_text = f"{title} Image"
        placeholder_bbox = draw.textbbox((0, 0), placeholder_text, font=font_desc)
        placeholder_width = placeholder_bbox[2] - placeholder_bbox[0]
        placeholder_x = image_x + (image_width - placeholder_width) // 2
        placeholder_y = current_y + (image_height - 20) // 2
        draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#6b7280', font=font_desc)
    
    current_y += image_height + 20
    
    # 5. DESCRIPTION TEXT (centered, readable)
    description = campaign_data.get('description', 'Exclusive offers available!')
    
    # Wrap description text properly
    words = description.split()
    lines = []
    current_line = ""
    max_line_width = width - (padding * 2)
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        test_bbox = draw.textbbox((0, 0), test_line, font=font_desc)
        if test_bbox[2] - test_bbox[0] <= max_line_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Draw description lines (centered)
    for line in lines[:2]:  # Max 2 lines
        line_bbox = draw.textbbox((0, 0), line, font=font_desc)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (width - line_width) // 2
        draw.text((line_x, current_y), line, fill='#4b5563', font=font_desc)
        current_y += 22
    
    current_y += 15
    
    # 6. PURPLE CTA BUTTON (rounded, centered)
    cta_text = campaign_data.get('cta_text', 'Learn More')
    
    # Button dimensions
    button_padding = 24
    button_bbox = draw.textbbox((0, 0), cta_text, font=font_button)
    button_text_width = button_bbox[2] - button_bbox[0]
    button_width = button_text_width + (button_padding * 2)
    button_height = 44
    button_x = (width - button_width) // 2
    
    # Draw rounded button
    draw.rounded_rectangle(
        [button_x, current_y, button_x + button_width, current_y + button_height],
        radius=22,  # Fully rounded
        fill='#8b5cf6'  # Purple
    )
    
    # Button text (centered)
    button_text_x = button_x + button_padding
    button_text_y = current_y + (button_height - 20) // 2
    draw.text((button_text_x, button_text_y), cta_text, fill='white', font=font_button)
    
    return img

def main():
    """Generate email ads that match the real popup design"""
    
    print("🎯 GENERATING POPUP-STYLE EMAIL ADS...")
    print("Based on actual popup screenshot")
    
    # Get campaign data
    try:
        response = requests.get('https://mode-dash-production.up.railway.app/api/campaigns')
        campaigns = response.json()
        print(f"✅ Got {len(campaigns)} campaigns")
        
        # Generate for first campaign
        campaign = campaigns[0]
        print(f"\n📧 Generating for: {campaign['name']}")
        
        img = create_popup_style_email(campaign, width=320, height=480)
        filename = "popup_style_email.png"
        img.save(filename, 'PNG', quality=95)
        
        print(f"✅ Saved: {filename}")
        print("\n🔍 This should now match the popup design:")
        print("- Circle logo (top left)")
        print("- Pink pill header (centered)")
        print("- Large title")
        print("- Campaign image")
        print("- Readable description")
        print("- Purple CTA button")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()