"""
Tune Image Proxy Server
Fetches real images from Tune iframes and serves them publicly
For remote demos where both users need to see the same real campaign images
"""

import requests
import streamlit as st
from bs4 import BeautifulSoup
import re
import base64
from urllib.parse import urljoin, urlparse
import time
from io import BytesIO
from PIL import Image

class TuneImageProxy:
    """Proxy to extract real images from Tune campaigns"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.cached_images = {}
    
    def extract_campaign_image(self, campaign_id, aff_id):
        """Extract real image from Tune campaign iframe"""
        try:
            # Build the iframe URL
            iframe_url = f"https://track.modemobile.com/aff_ad?campaign_id={campaign_id}&aff_id={aff_id}&format=iframe"
            
            st.info(f"🔍 Fetching real campaign content from: {iframe_url}")
            
            # Fetch the iframe content
            response = self.session.get(iframe_url, timeout=10)
            response.raise_for_status()
            
            st.success(f"✅ Successfully fetched content ({len(response.content)} bytes)")
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all images in the content
            images = soup.find_all('img')
            st.info(f"📸 Found {len(images)} images in campaign")
            
            # Look for the main campaign image (usually the largest or most prominent)
            best_image = None
            best_score = 0
            
            for img in images:
                src = img.get('src')
                if not src:
                    continue
                
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin(iframe_url, src)
                elif not src.startswith('http'):
                    src = urljoin(iframe_url, src)
                
                # Score images based on likely importance
                score = 0
                
                # Check image attributes for campaign indicators
                alt_text = (img.get('alt', '') or '').lower()
                class_names = ' '.join(img.get('class', [])).lower()
                
                # Higher score for images with campaign-related attributes
                if any(keyword in alt_text for keyword in ['tesla', 'stock', 'campaign', 'ad', 'offer']):
                    score += 10
                
                if any(keyword in class_names for keyword in ['campaign', 'ad', 'main', 'hero', 'banner']):
                    score += 5
                
                # Prefer larger images
                width = img.get('width')
                height = img.get('height')
                if width and height:
                    try:
                        area = int(width) * int(height)
                        score += min(area / 1000, 10)  # Cap at 10 points
                    except:
                        pass
                
                # Avoid small icons and logos
                if width and height:
                    try:
                        if int(width) < 50 or int(height) < 50:
                            score -= 5
                    except:
                        pass
                
                if score > best_score:
                    best_score = score
                    best_image = src
            
            if best_image:
                st.success(f"🎯 Selected best image: {best_image} (score: {best_score})")
                
                # Fetch and convert the image to base64 for embedding
                return self._fetch_and_encode_image(best_image)
            else:
                # Fallback: look for any image with reasonable size
                for img in images:
                    src = img.get('src')
                    if src:
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = urljoin(iframe_url, src)
                        elif not src.startswith('http'):
                            src = urljoin(iframe_url, src)
                        
                        st.info(f"🔄 Trying fallback image: {src}")
                        return self._fetch_and_encode_image(src)
                
                st.warning("❌ No suitable images found in campaign")
                return None
                
        except requests.RequestException as e:
            st.error(f"❌ Failed to fetch campaign: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Error processing campaign: {e}")
            return None
    
    def _fetch_and_encode_image(self, image_url):
        """Fetch image and convert to base64 data URL"""
        try:
            st.info(f"📥 Downloading image: {image_url}")
            
            response = self.session.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Determine content type
            content_type = response.headers.get('content-type', 'image/jpeg')
            
            # Convert to base64
            image_b64 = base64.b64encode(response.content).decode('utf-8')
            data_url = f"data:{content_type};base64,{image_b64}"
            
            st.success(f"✅ Image converted to base64 ({len(image_b64)} chars)")
            
            return data_url
            
        except Exception as e:
            st.error(f"❌ Failed to fetch image {image_url}: {e}")
            return None
    
    def get_campaign_data(self, campaign_id, aff_id):
        """Get comprehensive campaign data including images and text"""
        try:
            iframe_url = f"https://track.modemobile.com/aff_ad?campaign_id={campaign_id}&aff_id={aff_id}&format=iframe"
            
            st.info(f"🔍 Extracting campaign data from: {iframe_url}")
            
            response = self.session.get(iframe_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            title = None
            description = None
            
            # Look for title in various places
            title_candidates = [
                soup.find('h1'),
                soup.find('h2'),
                soup.find('h3'),
                soup.find('title'),
                soup.find(text=re.compile(r'tesla|stock|down|drop', re.I))
            ]
            
            for candidate in title_candidates:
                if candidate and hasattr(candidate, 'get_text'):
                    text = candidate.get_text().strip()
                    if len(text) > 5 and len(text) < 100:
                        title = text
                        break
                elif candidate and isinstance(candidate, str):
                    text = candidate.strip()
                    if len(text) > 5 and len(text) < 100:
                        title = text
                        break
            
            # Extract main image
            image_url = self.extract_campaign_image(campaign_id, aff_id)
            
            # Look for CTA button text
            cta_text = "View Campaign"
            buttons = soup.find_all(['button', 'a'], text=re.compile(r'click|here|get|view|learn', re.I))
            if buttons:
                cta_text = buttons[0].get_text().strip()
            
            return {
                'title': title or f"Campaign {campaign_id}",
                'description': description or f"Live campaign from Tune (ID: {campaign_id})",
                'image_url': image_url,
                'cta_text': cta_text,
                'iframe_url': iframe_url
            }
            
        except Exception as e:
            st.error(f"❌ Failed to extract campaign data: {e}")
            return None


def render_tune_proxy_demo():
    """Render the Tune image proxy demo interface"""
    st.title("🔗 Tune Image Proxy - Real Campaign Extractor")
    st.markdown("**Extract real images and content from Tune campaigns for remote demos**")
    
    st.info("💡 This tool fetches real campaign content from Tune iframes so both you and Mike can see the same images during remote demos.")
    
    # Input form
    with st.form("proxy_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_id = st.number_input("Campaign ID", value=13, min_value=1)
            
        with col2:
            aff_id = st.number_input("Affiliate ID", value=43045, min_value=1)
        
        submitted = st.form_submit_button("🚀 Extract Real Campaign Data", type="primary")
    
    if submitted:
        st.markdown("---")
        st.subheader("🔄 Extracting Real Campaign Content...")
        
        proxy = TuneImageProxy()
        
        # Extract comprehensive campaign data
        campaign_data = proxy.get_campaign_data(campaign_id, aff_id)
        
        if campaign_data:
            st.success("✅ Successfully extracted real campaign content!")
            
            # Display extracted data
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**📊 Extracted Campaign Data:**")
                st.markdown(f"**Title:** {campaign_data['title']}")
                st.markdown(f"**Description:** {campaign_data['description']}")
                st.markdown(f"**CTA Text:** {campaign_data['cta_text']}")
                st.markdown(f"**Source:** {campaign_data['iframe_url']}")
            
            with col2:
                st.markdown("**📸 Extracted Image:**")
                if campaign_data['image_url']:
                    try:
                        st.image(campaign_data['image_url'], caption="Real Campaign Image", width=300)
                    except:
                        st.error("Could not display extracted image")
                else:
                    st.warning("No image extracted")
            
            # Provide data for campaign system
            if campaign_data['image_url']:
                st.markdown("---")
                st.subheader("🔗 Use in Campaign System")
                st.markdown("**Copy this data to your campaign manager:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text_input("Display Title", value=campaign_data['title'], key="extracted_title")
                    st.text_area("Description", value=campaign_data['description'], key="extracted_desc")
                
                with col2:
                    st.text_input("CTA Text", value=campaign_data['cta_text'], key="extracted_cta")
                    st.text_area("Image URL", value=campaign_data['image_url'], key="extracted_image", height=100)
                
                st.success("✅ **Ready for Mike!** This image URL will work for both of you in remote demos.")
                
                # Quick copy buttons
                if st.button("📋 Copy Image URL"):
                    st.code(campaign_data['image_url'])
                    st.info("📋 Copy the URL above and paste it into the 'Campaign Image URL' field")
        else:
            st.error("❌ Failed to extract campaign content. The campaign might be protected or unavailable.")


if __name__ == "__main__":
    render_tune_proxy_demo() 