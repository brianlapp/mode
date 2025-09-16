#!/usr/bin/env python3
"""
Image loading utilities with caching and retry logic
"""

import urllib.request
import urllib.error
import hashlib
import time
import logging
from pathlib import Path
from typing import Optional
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

class ImageCache:
    """Simple file-based image cache"""
    
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
            except Exception as e:
                logger.warning(f"Failed to read cache for {url}: {e}")
                return None
        return None
    
    def set(self, url: str, data: bytes) -> None:
        """Store image in cache"""
        cache_file = self.cache_dir / f"{self.get_cache_key(url)}.img"
        try:
            cache_file.write_bytes(data)
        except Exception as e:
            logger.error(f"Failed to cache image: {e}")

# Global cache instance
image_cache = ImageCache()

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
    
    for attempt in range(max_retries):
        try:
            # Create request with headers
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            req.add_header('Accept', 'image/webp,image/apng,image/*,*/*;q=0.8')
            req.add_header('Referer', 'https://imgur.com/')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        return response.read()
                    else:
                        logger.error(f"URL returned non-image content: {content_type}")
                        return None
                else:
                    logger.error(f"Failed to fetch image: HTTP {response.status}")
                    return None
                
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                wait_time = 2 ** attempt
                logger.warning(f"Rate limited, waiting {wait_time}s before retry {attempt+1}")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            logger.warning(f"URL Error fetching {url}, attempt {attempt+1}: {e.reason}")
        except Exception as e:
            logger.error(f"Error fetching image from {url}: {str(e)}")
        
        if attempt < max_retries - 1:
            time.sleep(1)
    
    return None

def load_campaign_image(url: str, target_size: tuple = (280, 120)) -> Optional[Image.Image]:
    """Load campaign image with caching and resizing"""
    if not url:
        return None
    
    # Check cache first
    cached = image_cache.get(url)
    if cached:
        try:
            img = Image.open(BytesIO(cached))
            # Resize to target size
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            logger.warning(f"Failed to load cached image: {e}")
    
    # Fetch fresh
    image_data = fetch_image_with_retry(url)
    if image_data:
        # Cache for next time
        image_cache.set(url, image_data)
        try:
            img = Image.open(BytesIO(image_data))
            # Convert to RGB if needed (for JPEG compatibility)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            # Resize to target size
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            logger.error(f"Failed to open image: {e}")
    
    return None

def create_fallback_image(target_size: tuple = (280, 120), text: str = "IMAGE MISSING") -> Image.Image:
    """Create a fallback image when the real image can't be loaded"""
    from PIL import ImageDraw, ImageFont
    
    img = Image.new('RGB', target_size, color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, target_size[0]-1, target_size[1]-1], outline='#e9ecef', width=2)
    
    # Add text
    try:
        font = ImageFont.truetype("assets/fonts/Inter-Regular.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (target_size[0] - text_width) // 2
    text_y = (target_size[1] - text_height) // 2
    
    draw.text((text_x, text_y), text, fill='#6c757d', font=font)
    
    return img
