#!/usr/bin/env python3
"""
DEBUG GENERATOR - Step by step to see what's broken
"""

from PIL import Image, ImageDraw, ImageFont

def debug_step_by_step():
    """Debug each step to see where it breaks"""
    
    print("🔍 DEBUGGING STEP BY STEP...")
    
    # Create basic image
    img = Image.new('RGB', (320, 480), color='white')
    draw = ImageDraw.Draw(img)
    print("✅ Step 1: Created white image")
    
    # Test 1: Draw blue circle for logo
    try:
        draw.ellipse([20, 20, 68, 68], fill='#1e40af')
        print("✅ Step 2: Drew blue circle")
    except Exception as e:
        print(f"❌ Step 2 failed: {e}")
    
    # Test 2: Draw pink pill
    try:
        pill_x = 50
        pill_y = 80
        pill_width = 220
        pill_height = 30
        draw.rounded_rectangle(
            [pill_x, pill_y, pill_x + pill_width, pill_y + pill_height],
            radius=15,
            fill='#F7007C'
        )
        print("✅ Step 3: Drew pink pill")
    except Exception as e:
        print(f"❌ Step 3 failed: {e}")
    
    # Test 3: Add text
    try:
        font = ImageFont.load_default()
        draw.text((50, 130), "Trading Tips", fill='#000000', font=font)
        print("✅ Step 4: Drew title text")
    except Exception as e:
        print(f"❌ Step 4 failed: {e}")
    
    # Test 4: Draw purple button
    try:
        button_x = 60
        button_y = 400
        button_width = 200
        button_height = 44
        draw.rounded_rectangle(
            [button_x, button_y, button_x + button_width, button_y + button_height],
            radius=22,
            fill='#8b5cf6'
        )
        print("✅ Step 5: Drew purple button")
    except Exception as e:
        print(f"❌ Step 5 failed: {e}")
    
    # Save and analyze
    img.save('debug_step_by_step.png')
    print("✅ Saved debug image")
    
    # Check what we actually got
    pixels = img.load()
    colors = set()
    for y in range(0, 480, 50):
        for x in range(0, 320, 50):
            colors.add(pixels[x, y])
    
    print(f"🎨 Colors found: {len(colors)}")
    print(f"Colors: {list(colors)[:10]}")  # Show first 10 colors
    
    # Check specific pixels
    blue_pixel = pixels[44, 44]  # Should be blue circle
    pink_pixel = pixels[160, 95]  # Should be pink pill
    purple_pixel = pixels[160, 422]  # Should be purple button
    
    print(f"Blue circle pixel: {blue_pixel}")
    print(f"Pink pill pixel: {pink_pixel}")
    print(f"Purple button pixel: {purple_pixel}")

if __name__ == "__main__":
    debug_step_by_step()
