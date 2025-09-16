#!/usr/bin/env python3
"""
WORKING EMAIL GENERATOR - Actually generates PNGs that look good
No more broken popup attempts - direct image creation
"""

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json

def create_email_ad(campaign_data, width=320, height=480):
    """Create a working email ad that looks professional"""
    
    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Use default font (which actually works)
    try:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default() 
        font_small = ImageFont.load_default()
    except:
        font_large = font_medium = font_small = None
    
    current_y = 20
    padding = 20
    content_width = width - (padding * 2)
    
    # Header bar (pink like Mode)
    header_height = 40
    draw.rectangle([0, 0, width, header_height], fill='#F7007C')
    
    # Header text
    header_text = "Thanks for Reading - You've unlocked bonus offers"
    if font_small:
        # Calculate text size
        bbox = draw.textbbox((0, 0), header_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, 12), header_text, fill='white', font=font_small)
    
    current_y = header_height + 20
    
    # Campaign title
    title = campaign_data.get('name', 'Campaign')
    if font_large:
        # Wrap title if needed
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font_large:
                bbox = draw.textbbox((0, 0), test_line, font=font_large)
                if bbox[2] - bbox[0] <= content_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw title lines
        for line in lines[:2]:  # Max 2 lines
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_x = padding + (content_width - text_width) // 2
            draw.text((text_x, current_y), line, fill='#111827', font=font_large)
            current_y += 25
    
    current_y += 10
    
    # Campaign image
    image_height = 180
    image_width = content_width
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
                print(f"✅ Image loaded and pasted: {img_w}x{img_h}")
            else:
                raise Exception(f"HTTP {response.status_code}")
        else:
            raise Exception("No image URL")
            
    except Exception as e:
        print(f"❌ Image failed: {e}")
        # Draw placeholder
        draw.rectangle([image_x, current_y, image_x + image_width, current_y + image_height], 
                      fill='#f0f0f0', outline='#ddd', width=2)
        
        if font_medium:
            placeholder_text = "Campaign Image"
            bbox = draw.textbbox((0, 0), placeholder_text, font=font_medium)
            text_width = bbox[2] - bbox[0]
            text_x = image_x + (image_width - text_width) // 2
            text_y = current_y + (image_height - 15) // 2
            draw.text((text_x, text_y), placeholder_text, fill='#666', font=font_medium)
    
    current_y += image_height + 20
    
    # Description
    description = campaign_data.get('description', '')[:120] + "..."
    if font_medium and description:
        # Simple wrapping
        words = description.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=font_medium)
            if bbox[2] - bbox[0] <= content_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw description
        for line in lines[:3]:
            bbox = draw.textbbox((0, 0), line, font=font_medium)
            text_width = bbox[2] - bbox[0]
            text_x = padding + (content_width - text_width) // 2
            draw.text((text_x, current_y), line, fill='#4b5563', font=font_medium)
            current_y += 18
    
    current_y += 20
    
    # CTA Button
    cta_text = campaign_data.get('cta_text', 'Learn More')
    button_height = 44
    button_width = min(content_width - 20, 200)
    button_x = padding + (content_width - button_width) // 2
    
    # Draw button
    draw.rectangle([button_x, current_y, button_x + button_width, current_y + button_height], 
                  fill='#8b5cf6')
    
    if font_medium:
        bbox = draw.textbbox((0, 0), cta_text, font=font_medium)
        text_width = bbox[2] - bbox[0]
        text_x = button_x + (button_width - text_width) // 2
        text_y = current_y + (button_height - 15) // 2
        draw.text((text_x, text_y), cta_text, fill='white', font=font_medium)
    
    return img

def main():
    """Generate actual working email ads"""
    
    print("🎯 GENERATING WORKING EMAIL ADS...")
    
    # Get campaign data from API
    try:
        response = requests.get('https://mode-dash-production.up.railway.app/api/campaigns')
        campaigns = response.json()
        print(f"✅ Got {len(campaigns)} campaigns")
        
        # Generate ads for first few campaigns
        for i, campaign in enumerate(campaigns[:3]):
            print(f"\n📧 Generating ad for: {campaign['name']}")
            
            img = create_email_ad(campaign, width=320, height=480)
            filename = f"working_email_ad_{i+1}_{campaign['name'].replace(' ', '_').lower()}.png"
            img.save(filename, 'PNG', quality=95)
            
            print(f"✅ Saved: {filename}")
            
            # Also create 2x version
            img_2x = create_email_ad(campaign, width=640, height=960)
            filename_2x = f"working_email_ad_{i+1}_{campaign['name'].replace(' ', '_').lower()}_2x.png"
            img_2x.save(filename_2x, 'PNG', quality=95)
            
            print(f"✅ Saved 2x: {filename_2x}")
        
        print("\n🎉 DONE! Check the generated PNG files.")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
