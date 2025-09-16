#!/usr/bin/env python3
"""
CLEAN WORKING GENERATOR - Based on successful debug version
Creates email ads that actually work and match the popup
"""

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def create_working_email_ad(campaign_data, width=320, height=480):
    """Create email ad that actually works - based on debug success"""
    
    # Create white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load font
    try:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    except:
        font_title = None
        font_text = None
    
    current_y = 20
    
    # 1. BLUE CIRCLE LOGO (top left)
    logo_size = 48
    logo_x = 20
    logo_y = current_y
    
    # Draw blue circle
    draw.ellipse([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], 
                fill='#1e40af')
    
    # Simple white mountain shape
    mountain_center_x = logo_x + logo_size // 2
    mountain_center_y = logo_y + logo_size // 2
    mountain_points = [
        (mountain_center_x, mountain_center_y - 10),      # Top
        (mountain_center_x - 12, mountain_center_y + 8),  # Bottom left
        (mountain_center_x + 12, mountain_center_y + 8)   # Bottom right
    ]
    draw.polygon(mountain_points, fill='white')
    
    # 2. PINK PILL HEADER (centered)
    header_text = "Thanks for Reading - You've unlocked bonus offers"
    
    # Calculate pill size
    if font_text:
        text_bbox = draw.textbbox((0, 0), header_text, font=font_text)
        text_width = text_bbox[2] - text_bbox[0]
    else:
        text_width = len(header_text) * 6  # Rough estimate
    
    pill_padding = 16
    pill_width = text_width + (pill_padding * 2)
    pill_height = 32
    pill_x = (width - pill_width) // 2
    pill_y = current_y + 5
    
    # Draw pink pill
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_width, pill_y + pill_height],
        radius=16,
        fill='#F7007C'
    )
    
    # White text on pink pill
    if font_text:
        text_x = pill_x + pill_padding
        text_y = pill_y + 8
        draw.text((text_x, text_y), header_text, fill='white', font=font_text)
    
    current_y = pill_y + pill_height + 25
    
    # 3. CAMPAIGN TITLE (large, centered)
    title = campaign_data.get('name', 'Campaign Title')
    
    if font_title:
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        draw.text((title_x, current_y), title, fill='#1f2937', font=font_title)
    
    current_y += 40
    
    # 4. CAMPAIGN IMAGE AREA
    image_width = width - 40
    image_height = 160
    image_x = 20
    
    # Try to load real image
    image_loaded = False
    try:
        image_url = campaign_data.get('main_image_url')
        if image_url and not image_url.startswith('https://imgur.com'):  # Skip imgur due to rate limits
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                campaign_img = Image.open(BytesIO(response.content))
                campaign_img.thumbnail((image_width, image_height), Image.Resampling.LANCZOS)
                
                # Center and paste
                img_w, img_h = campaign_img.size
                paste_x = image_x + (image_width - img_w) // 2
                paste_y = current_y + (image_height - img_h) // 2
                img.paste(campaign_img, (paste_x, paste_y))
                image_loaded = True
                print(f"✅ Loaded real image: {img_w}x{img_h}")
    except Exception as e:
        print(f"⚠️  Image load failed: {e}")
    
    if not image_loaded:
        # Draw placeholder with rounded corners
        draw.rounded_rectangle(
            [image_x, current_y, image_x + image_width, current_y + image_height],
            radius=8,
            fill='#f3f4f6',
            outline='#d1d5db',
            width=2
        )
        
        # Placeholder text
        placeholder_text = f"{title} Campaign"
        if font_text:
            placeholder_bbox = draw.textbbox((0, 0), placeholder_text, font=font_text)
            placeholder_width = placeholder_bbox[2] - placeholder_bbox[0]
            placeholder_x = image_x + (image_width - placeholder_width) // 2
            placeholder_y = current_y + (image_height - 15) // 2
            draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#6b7280', font=font_text)
    
    current_y += image_height + 25
    
    # 5. DESCRIPTION TEXT
    description = campaign_data.get('description', 'Exclusive offers available now!')
    
    # Simple text wrapping
    max_chars_per_line = 35
    if len(description) > max_chars_per_line:
        words = description.split()
        line1 = ""
        line2 = ""
        
        for word in words:
            if len(line1 + " " + word) <= max_chars_per_line:
                line1 += (" " if line1 else "") + word
            elif len(line2 + " " + word) <= max_chars_per_line:
                line2 += (" " if line2 else "") + word
            else:
                break
        
        # Draw both lines centered
        if font_text:
            for line in [line1, line2]:
                if line:
                    line_bbox = draw.textbbox((0, 0), line, font=font_text)
                    line_width = line_bbox[2] - line_bbox[0]
                    line_x = (width - line_width) // 2
                    draw.text((line_x, current_y), line, fill='#4b5563', font=font_text)
                    current_y += 20
    else:
        # Single line
        if font_text:
            desc_bbox = draw.textbbox((0, 0), description, font=font_text)
            desc_width = desc_bbox[2] - desc_bbox[0]
            desc_x = (width - desc_width) // 2
            draw.text((desc_x, current_y), description, fill='#4b5563', font=font_text)
        current_y += 25
    
    current_y += 15
    
    # 6. PURPLE CTA BUTTON
    cta_text = campaign_data.get('cta_text', 'Get Offer')
    
    button_width = 200
    button_height = 44
    button_x = (width - button_width) // 2
    
    # Draw purple button
    draw.rounded_rectangle(
        [button_x, current_y, button_x + button_width, current_y + button_height],
        radius=22,
        fill='#8b5cf6'
    )
    
    # Button text
    if font_text:
        button_bbox = draw.textbbox((0, 0), cta_text, font=font_text)
        button_text_width = button_bbox[2] - button_bbox[0]
        button_text_x = button_x + (button_width - button_text_width) // 2
        button_text_y = current_y + (button_height - 15) // 2
        draw.text((button_text_x, button_text_y), cta_text, fill='white', font=font_text)
    
    return img

def main():
    """Generate working email ad"""
    
    print("🎯 GENERATING CLEAN WORKING EMAIL AD...")
    
    # Get campaign data
    try:
        response = requests.get('https://mode-dash-production.up.railway.app/api/campaigns')
        campaigns = response.json()
        campaign = campaigns[0]  # First campaign
        
        print(f"📧 Creating ad for: {campaign['name']}")
        
        # Generate the ad
        img = create_working_email_ad(campaign)
        filename = "clean_working_email.png"
        img.save(filename, 'PNG', quality=95)
        
        print(f"✅ Saved: {filename}")
        
        # Analyze what we created
        pixels = img.load()
        colors = set()
        for y in range(0, 480, 50):
            for x in range(0, 320, 50):
                colors.add(pixels[x, y])
        
        print(f"🎨 Colors in final image: {len(colors)}")
        
        # Check for key elements
        blue_found = any(abs(c[0] - 30) < 10 and abs(c[1] - 64) < 10 and abs(c[2] - 175) < 10 for c in colors if len(c) >= 3)
        pink_found = any(abs(c[0] - 247) < 10 and abs(c[1] - 0) < 10 and abs(c[2] - 124) < 10 for c in colors if len(c) >= 3)
        purple_found = any(abs(c[0] - 139) < 10 and abs(c[1] - 92) < 10 and abs(c[2] - 246) < 10 for c in colors if len(c) >= 3)
        
        print(f"🔵 Blue logo: {'✅' if blue_found else '❌'}")
        print(f"💗 Pink pill: {'✅' if pink_found else '❌'}")
        print(f"💜 Purple button: {'✅' if purple_found else '❌'}")
        
        if blue_found and pink_found and purple_found:
            print("🎉 SUCCESS! All key elements present")
        else:
            print("⚠️  Some elements missing - needs more work")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
