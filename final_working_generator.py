#!/usr/bin/env python3
"""
FINAL WORKING GENERATOR - Fix positioning so elements don't overlap
"""

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def create_final_email_ad(campaign_data, width=320, height=480):
    """Create email ad with proper positioning - no overlaps"""
    
    # Create white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = ImageFont.load_default()
    
    # LAYOUT PLANNING - avoid overlaps
    current_y = 15
    
    # 1. BLUE CIRCLE LOGO (top left) - FIRST, before anything else
    logo_size = 40
    logo_x = 20
    logo_y = current_y
    
    print(f"Drawing blue logo at ({logo_x}, {logo_y})")
    draw.ellipse([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], 
                fill='#1e40af')
    
    # White mountain in logo
    mountain_center_x = logo_x + logo_size // 2
    mountain_center_y = logo_y + logo_size // 2
    mountain_points = [
        (mountain_center_x, mountain_center_y - 8),
        (mountain_center_x - 10, mountain_center_y + 6),
        (mountain_center_x + 10, mountain_center_y + 6)
    ]
    draw.polygon(mountain_points, fill='white')
    
    # 2. PINK PILL HEADER (centered, BELOW logo, not overlapping)
    current_y = logo_y + logo_size + 15  # Clear space after logo
    
    header_text = "Thanks for Reading - You've unlocked bonus offers"
    text_bbox = draw.textbbox((0, 0), header_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    pill_padding = 12
    pill_width = text_width + (pill_padding * 2)
    pill_height = 28
    pill_x = (width - pill_width) // 2
    pill_y = current_y
    
    print(f"Drawing pink pill at ({pill_x}, {pill_y})")
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_width, pill_y + pill_height],
        radius=14,
        fill='#F7007C'
    )
    
    # White text on pink pill
    text_x = pill_x + pill_padding
    text_y = pill_y + 6
    draw.text((text_x, text_y), header_text, fill='white', font=font)
    
    current_y = pill_y + pill_height + 20
    
    # 3. CAMPAIGN TITLE (large, centered)
    title = campaign_data.get('name', 'Campaign Title')
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    print(f"Drawing title '{title}' at ({title_x}, {current_y})")
    draw.text((title_x, current_y), title, fill='#1f2937', font=font)
    
    current_y += 35
    
    # 4. CAMPAIGN IMAGE AREA
    image_width = width - 40
    image_height = 140
    image_x = 20
    
    # Placeholder for now (skip image loading to focus on layout)
    print(f"Drawing image placeholder at ({image_x}, {current_y})")
    draw.rounded_rectangle(
        [image_x, current_y, image_x + image_width, current_y + image_height],
        radius=8,
        fill='#f3f4f6',
        outline='#d1d5db',
        width=2
    )
    
    # Placeholder text
    placeholder_text = f"{title} Image"
    placeholder_bbox = draw.textbbox((0, 0), placeholder_text, font=font)
    placeholder_width = placeholder_bbox[2] - placeholder_bbox[0]
    placeholder_x = image_x + (image_width - placeholder_width) // 2
    placeholder_y = current_y + (image_height - 15) // 2
    draw.text((placeholder_x, placeholder_y), placeholder_text, fill='#6b7280', font=font)
    
    current_y += image_height + 20
    
    # 5. DESCRIPTION TEXT
    description = campaign_data.get('description', 'Exclusive offers!')[:60] + "..."
    desc_bbox = draw.textbbox((0, 0), description, font=font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (width - desc_width) // 2
    
    print(f"Drawing description at ({desc_x}, {current_y})")
    draw.text((desc_x, current_y), description, fill='#4b5563', font=font)
    
    current_y += 30
    
    # 6. PURPLE CTA BUTTON (make sure it's visible)
    cta_text = campaign_data.get('cta_text', 'Get Offer')
    
    button_width = 180
    button_height = 40
    button_x = (width - button_width) // 2
    
    print(f"Drawing purple button at ({button_x}, {current_y})")
    draw.rounded_rectangle(
        [button_x, current_y, button_x + button_width, current_y + button_height],
        radius=20,
        fill='#8b5cf6'
    )
    
    # Button text
    button_bbox = draw.textbbox((0, 0), cta_text, font=font)
    button_text_width = button_bbox[2] - button_bbox[0]
    button_text_x = button_x + (button_width - button_text_width) // 2
    button_text_y = current_y + (button_height - 15) // 2
    draw.text((button_text_x, button_text_y), cta_text, fill='white', font=font)
    
    print(f"Final layout height: {current_y + button_height}")
    
    return img

def main():
    """Generate and verify the final email ad"""
    
    print("🎯 GENERATING FINAL EMAIL AD WITH PROPER POSITIONING...")
    
    # Get campaign data
    try:
        response = requests.get('https://mode-dash-production.up.railway.app/api/campaigns')
        campaigns = response.json()
        campaign = campaigns[0]
        
        print(f"📧 Creating ad for: {campaign['name']}")
        
        # Generate the ad
        img = create_final_email_ad(campaign)
        filename = "final_working_email.png"
        img.save(filename, 'PNG', quality=95)
        
        print(f"✅ Saved: {filename}")
        
        # VERIFY each element is present
        pixels = img.load()
        
        # Check specific locations
        logo_pixel = pixels[40, 35]  # Logo center
        pill_pixel = pixels[160, 90]  # Pill center
        button_pixel = pixels[160, 420]  # Button center
        
        print(f"\n🔍 VERIFICATION:")
        print(f"Logo pixel (should be blue): {logo_pixel}")
        print(f"Pill pixel (should be pink): {pill_pixel}")
        print(f"Button pixel (should be purple): {button_pixel}")
        
        # Check colors
        blue_ok = logo_pixel[0] < 100 and logo_pixel[2] > 100  # More blue than red
        pink_ok = pill_pixel[0] > 200 and pill_pixel[1] < 50   # High red, low green
        purple_ok = button_pixel[0] > 100 and button_pixel[2] > 200  # Purple-ish
        
        print(f"🔵 Blue logo: {'✅' if blue_ok else '❌'}")
        print(f"💗 Pink pill: {'✅' if pink_ok else '❌'}")
        print(f"💜 Purple button: {'✅' if purple_ok else '❌'}")
        
        if blue_ok and pink_ok and purple_ok:
            print("\n🎉 SUCCESS! All elements are properly positioned and colored!")
            print("📊 This should now match the popup design at https://mode-thankyou.netlify.app/")
        else:
            print("\n⚠️  Still needs work on positioning or colors")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
