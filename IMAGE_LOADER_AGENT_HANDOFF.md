# 🖼️ Image Loader Agent - URGENT HANDOFF

## 🚨 **CRITICAL ISSUE: CAMPAIGN IMAGES NOT LOADING**

Your mission is to **fix the campaign image loading issues** that are causing gray placeholder boxes to appear instead of actual campaign images in the email PNGs.

## 📸 **THE PROBLEM**

### **Current Behavior**
- Campaign images show as gray boxes with "IMAGE MISSING" text
- Image URLs exist in database but aren't loading
- Affects professional appearance of email ads
- Makes campaigns look broken/incomplete

### **From User's Screenshots**
- Gray placeholder box where campaign image should be
- "IMAGE MISSING" text in the center
- Proper layout but no visual content
- Everything else renders correctly

## 🔍 **ROOT CAUSE ANALYSIS**

The code attempts to load images but fails. Let's trace the issue:

1. **Database has image URLs**:
   ```
   main_image_url: "https://imgur.com/xyz.jpg"
   logo_url: "https://imgur.com/abc.jpg"
   ```

2. **Code tries to fetch images** (from error in screenshot):
   - Attempts to load from URL
   - Falls back to gray placeholder on failure
   - No proper error handling or retry

3. **Possible failure points**:
   - Imgur URLs returning 404 or 429 (rate limited)
   - Image format issues
   - Caching problems
   - Network timeouts

## 🔧 **IMMEDIATE ACTIONS NEEDED**

### **Step 1: Diagnose Current Image URLs**
Create a diagnostic script to test all campaign image URLs:

```python
import requests
import sqlite3
from urllib.parse import urlparse

def test_campaign_images():
    conn = sqlite3.connect('popup-system/api/popup_campaigns.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, main_image_url, logo_url FROM campaigns WHERE active = 1")
    campaigns = cursor.fetchall()
    
    results = []
    for campaign in campaigns:
        id, name, main_url, logo_url = campaign
        
        # Test main image
        main_status = test_image_url(main_url)
        logo_status = test_image_url(logo_url) if logo_url else "No logo"
        
        results.append({
            "campaign": name,
            "main_image": {"url": main_url, "status": main_status},
            "logo": {"url": logo_url, "status": logo_status}
        })
    
    return results

def test_image_url(url):
    if not url:
        return "Empty URL"
    
    try:
        # Fix common imgur issues
        if "imgur.com/" in url and not url.startswith("https://i.imgur.com/"):
            url = url.replace("imgur.com/", "i.imgur.com/")
            if not url.endswith(('.jpg', '.png', '.gif')):
                url += '.jpg'
        
        response = requests.get(url, timeout=5, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ModeEmailBot/1.0)'
        })
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                return f"OK ({len(response.content)} bytes)"
            else:
                return f"Not an image: {content_type}"
        else:
            return f"HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### **Step 2: Fix Image Loading in Code**

Update the image loading logic in `popup-system/api/main.py`:

```python
def fetch_image_with_retry(url: str, max_retries: int = 3) -> Optional[bytes]:
    """Fetch image with retry logic and proper error handling"""
    if not url:
        return None
    
    # Fix common imgur URL issues
    if "imgur.com/" in url:
        # Convert gallery URLs to direct image URLs
        if not url.startswith("https://i.imgur.com/"):
            url = url.replace("imgur.com/", "i.imgur.com/")
        
        # Ensure file extension
        if not url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            url += '.jpg'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type:
                    return response.content
                else:
                    logger.error(f"URL returned non-image content: {content_type}")
                    return None
            elif response.status_code == 429:  # Rate limited
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                logger.error(f"Failed to fetch image: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching image from {url}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None
    
    return None
```

### **Step 3: Implement Image Caching**

Add proper caching to avoid repeated fetches:

```python
import hashlib
from pathlib import Path

class ImageCache:
    def __init__(self, cache_dir: str = ".cache/images"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_key(self, url: str) -> str:
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()[:16]
    
    def get(self, url: str) -> Optional[bytes]:
        """Get image from cache"""
        cache_file = self.cache_dir / f"{self.get_cache_key(url)}.img"
        if cache_file.exists():
            try:
                return cache_file.read_bytes()
            except:
                return None
        return None
    
    def set(self, url: str, data: bytes) -> None:
        """Store image in cache"""
        cache_file = self.cache_dir / f"{self.get_cache_key(url)}.img"
        try:
            cache_file.write_bytes(data)
        except Exception as e:
            logger.error(f"Failed to cache image: {e}")

# Use in image loading
image_cache = ImageCache()

def load_campaign_image(url: str) -> Optional[Image.Image]:
    """Load campaign image with caching"""
    # Check cache first
    cached = image_cache.get(url)
    if cached:
        try:
            return Image.open(BytesIO(cached))
        except:
            pass
    
    # Fetch fresh
    image_data = fetch_image_with_retry(url)
    if image_data:
        # Cache for next time
        image_cache.set(url, image_data)
        try:
            return Image.open(BytesIO(image_data))
        except Exception as e:
            logger.error(f"Failed to open image: {e}")
    
    return None
```

### **Step 4: Update Image URLs in Database**

If many URLs are broken, update them with working alternatives:

```python
# Working placeholder images (as fallbacks)
FALLBACK_IMAGES = {
    'finance': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=400&fit=crop',  # Trading chart
    'lifestyle': 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=600&h=400&fit=crop',  # Gift box
    'generic': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop'   # Money/success
}

def update_broken_image_urls():
    """Update campaigns with broken images to use working URLs"""
    # Test all URLs first
    test_results = test_campaign_images()
    
    conn = sqlite3.connect('popup-system/api/popup_campaigns.db')
    cursor = conn.cursor()
    
    for result in test_results:
        if 'OK' not in result['main_image']['status']:
            # Determine fallback based on campaign type
            campaign_name = result['campaign'].lower()
            if any(word in campaign_name for word in ['trading', 'market', 'gold', 'research']):
                fallback = FALLBACK_IMAGES['finance']
            elif any(word in campaign_name for word in ['box', 'sample', 'hulu', 'paramount']):
                fallback = FALLBACK_IMAGES['lifestyle']
            else:
                fallback = FALLBACK_IMAGES['generic']
            
            # Update database
            cursor.execute(
                "UPDATE campaigns SET main_image_url = ? WHERE name = ?",
                (fallback, result['campaign'])
            )
            print(f"Updated {result['campaign']} with new image URL")
    
    conn.commit()
    conn.close()
```

## 🧪 **TESTING REQUIREMENTS**

### **Image URL Testing**
```bash
# Create and run diagnostic script
python popup-system/api/test_image_urls.py

# Should output:
# Trading Tips: main_image OK (123456 bytes), logo OK (45678 bytes)
# Behind The Markets: main_image HTTP 404, logo Empty URL
# etc...
```

### **Cache Testing**
```bash
# Check cache directory
ls -la popup-system/api/.cache/images/

# Should see cached image files
```

### **Visual Testing**
```bash
# Generate test image locally
curl "http://localhost:8000/api/email/ad.png?property=mff" > test_local.png

# Generate from Railway
curl "https://mode-dash-production.up.railway.app/api/email/ad.png?property=mff" > test_railway.png

# Both should show actual campaign images, not gray boxes
```

## 📁 **FILES TO MODIFY**

### **Primary Targets**
- `popup-system/api/main.py` - Add image fetching/caching logic
- `popup-system/api/routes/email.py` - Update image loading in email generation

### **New Files to Create**
- `popup-system/api/test_image_urls.py` - Diagnostic script
- `popup-system/api/utils/image_cache.py` - Caching utility
- `popup-system/api/fix_broken_images.py` - URL update script

### **Database Updates**
- Update campaigns table with working image URLs
- Add image_cache table if persistent caching needed

## 🎯 **SUCCESS CRITERIA**

### **MUST ACHIEVE**
- [ ] **No more gray placeholder boxes**
- [ ] **Actual campaign images display**
- [ ] **Fast image loading** (via caching)
- [ ] **Resilient to failures** (fallbacks work)

### **Visual Check**
- Before: Gray box with "IMAGE MISSING"
- After: Actual campaign imagery (products, offers, etc.)

## 🚀 **QUICK WIN STRATEGY**

If time is critical, implement this minimal fix:

1. **Update all image URLs to working ones**:
```sql
-- Quick fix with Unsplash placeholders
UPDATE campaigns SET main_image_url = 
  CASE 
    WHEN property = 'mmm' THEN 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=280&h=120&fit=crop'
    ELSE 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=280&h=120&fit=crop'
  END
WHERE main_image_url IS NULL OR main_image_url LIKE '%imgur%';
```

2. **Add simple retry logic** to existing fetch code

3. **Deploy and test**

## ⚠️ **COMMON PITFALLS**

1. **Imgur rate limiting** - Use proper headers and delays
2. **Wrong URL format** - imgur.com vs i.imgur.com
3. **Missing file extensions** - Add .jpg if needed
4. **CORS issues** - Not applicable for server-side
5. **Memory issues** - Stream large images

## 🔄 **COORDINATION WITH OTHER AGENTS**

- **Font Fixer Agent**: Don't interfere with font loading changes
- **Quality Assurance Agent**: Will verify final image quality

## 🔄 **HANDOFF BACK**

When images are loading:
1. **Confirm all campaigns show images**
2. **Document which URLs were updated**
3. **Verify caching is working**
4. **Pass to Quality Assurance Agent**

**Remember: User wants to see actual campaign images, not placeholders!**
