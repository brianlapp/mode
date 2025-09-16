# 🎨 Email PNG Generation Expert - AGENT 2 HANDOFF

## 🎯 **MISSION: Build Working PNG Generation System**

Your job is to implement **actual PNG image generation** that creates professional, branded email ads matching the popup design quality.

## 📋 **HANDOFF FROM AGENT 1 (Railway Specialist)**

Assuming Agent 1 has resolved:
- ✅ Email endpoints no longer return 404
- ✅ Database campaigns persist (no more resets)
- ✅ FastAPI routes loading properly on Railway

**If Agent 1 hasn't completed their tasks, coordinate with them first.**

## 🎨 **YOUR SPECIFIC OBJECTIVES**

### **Primary Goal**: Generate PNG images like this popup design
![Reference Design](https://user-provided-screenshot-2)
- Property-specific branding headers (pink/green)
- "Thanks for Reading - You've unlocked bonus offers" tagline
- Centered campaign titles
- Professional image placeholders
- Multi-line descriptions
- Styled CTA buttons ("CONTINUE >")
- Footer text ("Grab an [Offer]!")

### **NOT Like This** (current broken state)
![Broken Design](https://user-provided-screenshot-1)
- Basic "Prizes" text
- Simple purple "Win!" button
- No branding or professional layout

## 🛠️ **TECHNICAL REQUIREMENTS**

### **Dependencies Available**
```
Pillow==10.2.0  # For image generation
fastapi==0.104.1  # Web framework
requests==2.31.0  # For image fetching
```

### **Endpoints to Implement**
```python
@app.get("/api/email/ad.png")
# Parameters: property (mff|mmm), w (width), h (height), send (qa)
# Returns: PNG image with branded email ad

@app.get("/api/email/ad.debug") 
# Parameters: same as above
# Returns: JSON debug info with font/image status
```

### **Property Configurations**
```python
PROPERTY_CONFIG = {
    'mff': {
        'name': 'ModeFreeFinds',
        'primary_color': '#F7007C',  # Pink
        'tagline': "Thanks for Reading - You've unlocked bonus offers"
    },
    'mmm': {
        'name': 'ModeMarketMunchies', 
        'primary_color': '#00FF7F',  # Green
        'tagline': "Thanks for Reading - You've unlocked bonus offers"
    }
}
```

## 🎨 **DESIGN SPECIFICATIONS**

### **Layout Requirements** (600x400 default)
1. **Header Pill** (full width, 30px height)
   - Background: Property color (#F7007C for MFF, #00FF7F for MMM)
   - Text: "Thanks for Reading - You've unlocked bonus offers" (white, centered)

2. **Campaign Title** (centered, 24px font)
   - Text: Campaign name from database
   - Color: #111827 (dark gray)
   - Font: Bold/ExtraBold if available

3. **Campaign Image Area** (280x120px, centered)
   - Background: #f8f9fa with #e9ecef border
   - If image available: Load from main_image_url
   - If image fails: Show "IMAGE MISSING" placeholder

4. **Description** (multi-line, centered, 14px font)
   - Text: Campaign description from database
   - Color: #111827
   - Max 3 lines with proper text wrapping

5. **CTA Button** (full width, 50px height)
   - Background: #7C3AED (purple)
   - Text: Campaign cta_text (white, centered, bold)
   - Font: 18px

6. **Footer Text** (centered, 14px)
   - Text: "Grab an [Campaign Name]!"
   - Color: #6c757d (gray)

## 🔤 **FONT LOADING STRATEGY**

### **Priority Order**
1. **Inter fonts** (if bundled): `assets/fonts/Inter-ExtraBold.ttf`, `Inter-Regular.ttf`
2. **System fonts**: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` (Linux)
3. **Fallback fonts**: `arial.ttf`, `DejaVuSans.ttf`
4. **Final fallback**: `ImageFont.load_default()`

### **Error Handling**
- **Font loading fails**: Add "FONTS MISSING" watermark (red text, top-left)
- **Debug info required**: Return font path, SHA1, error status in debug endpoint

```python
def load_font_with_fallbacks(font_name: str, size: int) -> tuple[font, dict]:
    debug_info = {"family": font_name, "size": size, "path": "", "error": None}
    # Implementation needed...
    return font, debug_info
```

## 🖼️ **IMAGE CACHING SYSTEM**

### **Cache Strategy** (CRITICAL - avoid deadlocks)
- **Cache directory**: `/app/popup-system/api/.cache/images/`
- **Cache key**: SHA256 hash of image URL (first 16 chars)
- **Cache first**: Check disk cache before any fetching
- **Direct fetch only**: NO proxy calls (causes deadlocks)
- **Size limit**: 3.5MB max per image

### **Image Fetching**
```python
def get_cached_image(url: str) -> tuple[Optional[bytes], dict]:
    debug_info = {"url": url, "cache_hit": False, "bytes_len": 0, "error": None}
    # 1. Check cache first
    # 2. If miss, direct fetch with User-Agent
    # 3. Validate image format
    # 4. Cache successful fetches
    # 5. Return bytes + debug info
```

### **Image Processing**
- **Normalize imgur URLs**: `imgur.com/xyz.jpg` → `i.imgur.com/xyz.jpg`
- **Accept formats**: PNG, JPEG, WebP
- **Reject HTML/text**: Validate actual image content
- **Error placeholder**: Draw "IMAGE MISSING" box if fetch fails

## 📊 **DATABASE INTEGRATION**

### **Campaign Selection**
```sql
SELECT name, description, main_image_url, logo_url, cta_text 
FROM campaigns 
WHERE active = 1 AND name != 'Prizies'
ORDER BY RANDOM() 
LIMIT 1
```

### **Available Campaign Data**
- **Trading Tips**: "Get exclusive trading tips and market insights delivered daily to your inbox."
- **Behind The Markets**: "Discover what's really happening behind the financial markets with expert analysis."
- **Brownstone Research**: "Advanced technology and investment research from Brownstone Research experts."
- **Daily Goodie Box**: "Get your daily goodie box filled with amazing free samples and deals."
- **Hotsheets**: "Daily market hotsheets with the most profitable trading opportunities."
- **Best Gold**: "Premium gold investment insights and recommendations from industry experts."

## 🧪 **TESTING REQUIREMENTS**

### **Local Testing** (before deployment)
Create test script that:
1. **Tests font loading** with various fallbacks
2. **Tests image fetching** with cache simulation
3. **Generates sample PNGs** for MFF and MMM properties
4. **Validates output quality** against popup design

### **Production Testing** (after deployment)
1. **PNG endpoints return actual images** (not text/errors)
2. **Debug endpoints show proper font/image status**
3. **Multiple refreshes show different campaigns** (not stuck on one)
4. **Property branding works** (MFF pink, MMM green)

## 🚨 **CRITICAL SUCCESS CRITERIA**

### **MUST ACHIEVE**
- [ ] **No more "Prizies"** - only proper campaigns shown
- [ ] **Actual PNG images** generated (not text responses)
- [ ] **Professional design** matching popup quality
- [ ] **Property-specific branding** (colors, taglines)
- [ ] **Working fonts** (not default/broken fonts)
- [ ] **Campaign images** loaded (not "IMAGE MISSING")

### **DEBUG INFO REQUIRED**
```json
{
  "property": "mff",
  "dimensions": "600x400",
  "font": {
    "family": "DejaVuSans-Bold (using DejaVuSans-Bold.ttf)",
    "path": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "error": null
  },
  "image": {
    "url": "https://i.imgur.com/ZVGOktR.png",
    "cache_hit": true,
    "bytes_len": 64388,
    "error": null
  },
  "generation": {
    "success": true,
    "png_size": 15540
  },
  "timestamp": "2025-09-16T00:45:00.000Z"
}
```

## 📁 **CODE LOCATIONS**

### **Current Implementation** (needs replacement)
- `popup-system/api/routes/email.py` - Complex version with issues
- `popup-system/api/main.py` lines 262-302 - Direct routes (text only)

### **Test Files Available**
- `popup-system/api/test_email_generation.py` - Working local test
- `popup-system/api/FIXED_mff_email_ad.png` - Example output
- `popup-system/api/assets/fonts/` - Font directory (may be corrupted)

### **Working Examples**
- Local PNG generation works with system fonts
- Campaign data properly restored (13 campaigns)
- Database queries working correctly

## 🤝 **COORDINATION WITH OTHER AGENTS**

### **If Railway Agent (Agent 1) isn't done:**
- **Coordinate with them** on endpoint loading issues
- **Don't proceed** until basic routing works

### **If Email System Detective (Agent 4) finds old system:**
- **Coordinate** to ensure old system is disabled
- **Avoid conflicts** between old and new generation

### **When complete:**
- **Hand back to Orchestrator** with working PNG endpoints
- **Provide test URLs** for client preview
- **Document any remaining issues**

## ⏰ **TIMELINE EXPECTATION**
**User is extremely frustrated** - need working solution ASAP. Focus on:
1. **Get SOMETHING working** (even basic PNGs)
2. **Show proper campaign data** (not Prizies)
3. **Improve design quality** after basic functionality works

**Success = User can preview working email ads with proper campaigns!**
