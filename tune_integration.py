"""
Tune Integration Module
Handles Mike's Tune CPL iframe ads in the popup system
"""

import streamlit as st
import json
from datetime import datetime

class TunePopupManager:
    """Manages Tune-powered popup campaigns"""
    
    def __init__(self):
        self.campaigns = self._load_campaigns()
        self.tracking_url = "https://track.modemobile.com/aff_ad"
    
    def _load_campaigns(self):
        """Load campaigns from session state or defaults"""
        if 'tune_campaigns' not in st.session_state:
            # Using REAL extracted data from successful proxy test
            st.session_state.tune_campaigns = [{
                "id": 13,
                "aff_id": 43045,
                "name": "Tesla Stock Alert - Real Campaign",
                "display_title": "Tesla Down 50% - Insider Alert",
                "tagline": "Campaign ID: 13",
                "description": "Tesla stock has dropped significantly. Insiders may know something - get the latest trading intelligence and insider information now.",
                "cta_text": "Get Trading Intel",
                "btn_color": "#2563EB",
                "logo_bg": "#1F2937",
                "logo_text": "TUNE #13",
                "logo_url": None,
                "icon": "📊",
                # REAL IMAGE extracted from actual Tune campaign
                "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAlgAAAGQCAYAAAByNR6YAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEvmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRhLyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRyaWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgogICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxBdHRyaWI6Q3JlYXRlZD4yMDI1LTA3LTIxPC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkV4dElkPmQ3ZWVkNmNjLWZjNzUtNDIxNy1iYjZjLWIyYjIzMjBjOTA2YzwvQXR0cmliOkV4dElkPgogICAgIDxBdHRyaWI6RmJJZD41MjUyNjU5MTQxNzk1ODA8L0F0dHJpYjpGYklkPgogICAgIDxBdHRyaWI6VG91Y2hUeXBlPjI8L0F0dHJpYjpUb3VjaFR5cGU+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvQXR0cmliOkFkcz4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvJz4KICA8ZGM6dGl0bGU+CiAgIDxyZGY6QWx0PgogICAgPHJkZjpsaSB4bWw6bGFuZz0neC1kZWZhdWx0Jz5FbG9uIE11c2sgLSBUZXNsYSBTdG9ja8KgQWxlcnQ8L3JkZjpsaT4KICAgPC9yZGY6QWx0PgogIDwvZGM6dGl0bGU+CiA8L3JkZjpEZXNjcmlwdGlvbj4KCiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0nJwogIHhtbG5zOnBob3Rvc2hvcD0naHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyc+CiAgPHBob3Rvc2hvcDpDb2xvck1vZGU+MzwvcGhvdG9zaG9wOkNvbG9yTW9kZT4KICA8cGhvdG9zaG9wOklDQ1Byb2ZpbGU+c1JHQjwvcGhvdG9zaG9wOklDQ1Byb2ZpbGU+CiA8L3JkZjpEZXNjcmlwdGlvbj4KCiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0nJwogIHhtbG5zOnRpZmY9J2h0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvJz4KICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogIDx0aWZmOlhSZXNvbHV0aW9uPjcyMDAwMC8xMDAwMDwvdGlmZjpYUmVzb2x1dGlvbj4KICA8dGlmZjpZUmVzb2x1dGlvbj43MjAwMDAvMTAwMDA8L3RpZmY6WVJlc29sdXRpb24+CiAgPHRpZmY6UmVzb2x1dGlvblVuaXQ+MjwvdGlmZjpSZXNvbHV0aW9uVW5pdD4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6eG1wPSdodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvJz4KICA8eG1wOkNyZWF0ZURhdGU+MjAyNS0wNy0yMVQxNTo0MDowMy0wNDowMDwveG1wOkNyZWF0ZURhdGU+CiAgPHhtcDpNb2RpZnlEYXRlPjIwMjUtMDctMjFUMTU6NDA6MDMtMDQ6MDA8L3htcDpNb2RpZnlEYXRlPgogIDx4bXA6TWV0YWRhdGFEYXRlPjIwMjUtMDctMjFUMTU6NDA6MDMtMDQ6MDA8L3htcDpNZXRhZGF0YURhdGU+CiAgPHhtcDpDcmVhdG9yVG9vbD5BZG9iZSBQaG90b3Nob3AgMjAyNCAoTWFjaW50b3NoKTwveG1wOkNyZWF0b3JUb29sPgogPC9yZGY6RGVzY3JpcHRpb24+CjwvcmRmOlJERj4KPC94OnhtcG1ldGE+Cjw/eHBhY2tldCBlbmQ9J3InPz7kuL6IAAAQ5klEQVR4nO3de5Sc913n8fe3nu5",
                "iframe_url": f"https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045&format=iframe",
                "width": 600,
                "height": 400,
                "active": True,
                "priority": 5,
                "created": datetime.now().isoformat()
            }]
        return st.session_state.tune_campaigns
    
    def add_campaign(self, campaign_data):
        """Add new Tune campaign"""
        self.campaigns.append(campaign_data)
        st.session_state.tune_campaigns = self.campaigns
        return True
    
    def update_campaign_logo(self, campaign_id, logo_url):
        """Update campaign logo URL"""
        for i, campaign in enumerate(self.campaigns):
            if campaign['id'] == campaign_id:
                self.campaigns[i]['logo_url'] = logo_url
                st.session_state.tune_campaigns = self.campaigns
                return True
        return False
    
    def get_iframe_url(self, campaign_id, aff_id):
        """Generate Tune iframe URL"""
        return f"{self.tracking_url}?campaign_id={campaign_id}&aff_id={aff_id}&format=iframe"
    
    def render_tune_popup_demo(self):
        """Render popup with real Tune iframe integration"""
        st.subheader("🔗 Tune-Powered Popup Demo")
        st.success("🚀 **REAL TUNE INTEGRATION** - This serves Mike's actual campaigns!")
        
        if st.button("🎬 Launch Tune Demo", type="primary", key="tune_demo"):
            st.session_state.show_tune_popup = True
        
        if st.session_state.get("show_tune_popup", False):
            active_campaigns = [c for c in self.campaigns if c.get('active', True)]
            
            if not active_campaigns:
                st.warning("No active campaigns found!")
                return
            
            # Campaign selector
            campaign_names = [f"{c['name']} (ID: {c['id']})" for c in active_campaigns]
            selected_idx = st.selectbox("Select Campaign:", range(len(campaign_names)), 
                                      format_func=lambda x: campaign_names[x])
            
            campaign = active_campaigns[selected_idx]
            iframe_url = self.get_iframe_url(campaign['id'], campaign['aff_id'])
            
            # Display the actual Tune iframe
            st.markdown(f"**Loading Campaign:** {campaign['name']}")
            st.markdown(f"**Iframe URL:** `{iframe_url}`")
            
            # Render iframe in popup-style container
            popup_html = f"""
            <div style="
                background: white;
                border-radius: 24px;
                padding: 20px;
                max-width: {campaign['width'] + 40}px;
                margin: 20px auto;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                border: 3px solid #F7007C;
            ">
                <div style="text-align: center; margin-bottom: 15px;">
                    <h3 style="color: #F7007C; margin: 0;">🔗 Live Tune Campaign</h3>
                    <p style="color: #666; margin: 5px 0;">{campaign['name']} - Campaign ID: {campaign['id']}</p>
                </div>
                
                <iframe 
                    src="{iframe_url}"
                    width="{campaign['width']}"
                    height="{campaign['height']}"
                    frameborder="0"
                    scrolling="no"
                    marginheight="0"
                    marginwidth="0"
                    style="border-radius: 12px; display: block; margin: 0 auto;">
                </iframe>
                
                <div style="text-align: center; margin-top: 15px; font-size: 12px; color: #999;">
                    Powered by Tune • Campaign tracking active
                </div>
            </div>
            """
            
            st.components.v1.html(popup_html, height=campaign['height'] + 150)
            
            # Track impression
            self._track_impression(campaign['id'])
            
            if st.button("Close Demo", key="close_tune_demo"):
                st.session_state.show_tune_popup = False
                st.rerun()
    
    def render_campaign_manager(self):
        """Render campaign management interface"""
        st.subheader("🛠️ Tune Campaign Manager")
        st.info("💡 **Mike's Request:** Backend system to manually add Tune links/impression pixels")
        
        # Current campaigns
        st.markdown("**📋 Current Campaigns:**")
        for i, campaign in enumerate(self.campaigns):
            with st.expander(f"📈 {campaign['name']} (ID: {campaign['id']})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Campaign ID:** {campaign['id']}")
                    st.write(f"**Affiliate ID:** {campaign['aff_id']}")
                    st.write(f"**Dimensions:** {campaign['width']}x{campaign['height']}")
                
                with col2:
                    status = "✅ Active" if campaign.get('active', True) else "⏸️ Paused"
                    st.write(f"**Status:** {status}")
                
                with col3:
                    if st.button(f"{'Pause' if campaign.get('active', True) else 'Activate'}", 
                               key=f"toggle_{i}"):
                        self.campaigns[i]['active'] = not campaign.get('active', True)
                        st.session_state.tune_campaigns = self.campaigns
                        st.rerun()
                
                # Show iframe code
                iframe_url = self.get_iframe_url(campaign['id'], campaign['aff_id'])
                st.code(f"""<iframe src="{iframe_url}" scrolling="no" frameborder="0" marginheight="0" marginwidth="0" width="{campaign['width']}" height="{campaign['height']}"></iframe>""", 
                       language="html")
        
        # Add new campaign form
        st.markdown("---")
        st.markdown("**➕ Add New Campaign:**")
        
        with st.form("add_tune_campaign"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Campaign Name*", placeholder="Trading Platform Signup")
                campaign_id = st.number_input("Campaign ID*", min_value=1, value=14)
                aff_id = st.number_input("Affiliate ID*", min_value=1, value=43045)
            
            with col2:
                width = st.number_input("Width (px)", min_value=100, value=600)
                height = st.number_input("Height (px)", min_value=100, value=400)
                active = st.checkbox("Active", value=True)
            
            submitted = st.form_submit_button("🚀 Add Campaign", type="primary")
            
            if submitted:
                if name and campaign_id and aff_id:
                    new_campaign = {
                        "id": campaign_id,
                        "aff_id": aff_id,
                        "name": name,
                        "width": width,
                        "height": height,
                        "active": active,
                        "created": datetime.now().isoformat()
                    }
                    
                    self.add_campaign(new_campaign)
                    st.success(f"✅ Campaign '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")
    
    def render_cycling_popup_with_tune(self):
        """Render cycling popup that uses real Tune campaigns"""
        st.subheader("🔄 Cycling Tune Popup with Real Campaigns")
        st.info("🎯 Combines cycling popup UX with real Tune campaign revenue")
        
        if st.button("🚀 Launch Cycling Tune Demo", type="primary", key="cycling_tune"):
            st.session_state.show_cycling_tune = True
        
        if st.session_state.get("show_cycling_tune", False):
            active_campaigns = [c for c in self.campaigns if c.get('active', True)]
            
            # Convert Tune campaigns to use real campaign data
            tune_offers = []
            for i, campaign in enumerate(active_campaigns):
                colors = ["#2563EB", "#4F46E5", "#059669", "#DC2626", "#7C3AED", "#F59E0B"]
                
                # Use real campaign data or fallbacks
                campaign_title = campaign.get('display_title', campaign['name'])
                campaign_tagline = campaign.get('tagline', f"Campaign ID: {campaign['id']}")
                campaign_description = campaign.get('description', f"Live Tune campaign from track.modemobile.com - Affiliate ID: {campaign['aff_id']}. Real revenue tracking active.")
                campaign_cta = campaign.get('cta_text', 'View Campaign')
                campaign_logo_url = campaign.get('logo_url', None)
                campaign_image_url = campaign.get('image_url', None)
                
                # Generate iframe URL to potentially extract real content
                iframe_url = self.get_iframe_url(campaign['id'], campaign['aff_id'])
                
                tune_offers.append({
                    "logo_bg": colors[i % len(colors)],
                    "logo_text": f"TUNE #{campaign['id']}" if not campaign_logo_url else "",
                    "logo_url": campaign_logo_url,
                    "tagline": campaign_tagline,
                    "title": campaign_title,
                    "icon": "🔗",
                    "image_url": campaign_image_url,
                    "description": campaign_description,
                    "btn_color": colors[i % len(colors)],
                    "campaign_id": campaign['id'],
                    "aff_id": campaign['aff_id'],
                    "iframe_url": iframe_url,
                    "cta_text": campaign_cta
                })
            
            cycling_popup_html = f"""
            <div id="tune-cycling-popup" style="margin: 20px 0;">
                <!-- Thanks.co Exact Replica Design with Tune Data -->
                <div id="tunePopupOverlay" style="
                    display: block;
                    position: fixed;
                    top: 0; left: 0;
                    width: 100%; height: 100%;
                    background: rgba(0,0,0,0.5);
                    z-index: 10000;
                ">
                    <div style="
                        position: absolute;
                        top: 50%; left: 50%;
                        transform: translate(-50%, -50%);
                        background: white;
                        border-radius: 24px;
                        padding: 0;
                        max-width: 320px;
                        width: 90%;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        overflow: hidden;
                    ">
                        <!-- Close Button -->
                        <button onclick="hideTunePopup()" style="
                            position: absolute;
                            top: 12px; right: 12px;
                            background: #E5E7EB;
                            border: none;
                            color: #6B7280;
                            font-size: 18px;
                            cursor: pointer;
                            width: 28px;
                            height: 28px;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            z-index: 10001;
                        ">×</button>
                        
                        <!-- Dynamic Logo Circle with Image Support -->
                        <div id="tuneLogoCircle" style="
                            position: absolute;
                            top: 24px; left: 24px;
                            width: 56px; height: 56px;
                            background: #2563EB;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 700;
                            color: white;
                            font-size: 10px;
                            text-align: center;
                            line-height: 1.1;
                            z-index: 10001;
                            overflow: hidden;
                        ">
                            <span id="tuneLogoText">TUNE #13</span>
                            <img id="tuneLogoImage" style="width: 100%; height: 100%; object-fit: cover; display: none;" alt="Campaign Logo">
                        </div>
                        
                        <!-- Main Content Area (Exactly like yesterday) -->
                        <div style="padding: 24px; padding-top: 100px; text-align: center;">
                            
                            <!-- Dynamic Tagline -->
                            <div id="tuneTagline" style="
                                background: #F3F4F6;
                                color: #6B7280;
                                padding: 6px 12px;
                                border-radius: 16px;
                                font-size: 12px;
                                margin-bottom: 24px;
                                display: inline-block;
                                font-weight: 500;
                            ">Campaign ID: 13</div>
                            
                            <!-- Dynamic Title -->
                            <h2 id="tuneOfferTitle" style="
                                margin: 0 0 8px 0;
                                font-size: 24px;
                                font-weight: 800;
                                line-height: 1.2;
                                color: #111827;
                            ">Demo Campaign</h2>
                            
                            <!-- Dynamic Campaign Image -->
                            <div id="tuneOfferImageContainer" style="margin: 16px 0; min-height: 100px; display: flex; align-items: center; justify-content: center;">
                                <img id="tuneOfferImage" style="max-width: 200px; max-height: 100px; border-radius: 8px; display: none;" alt="Campaign Image">
                                <div id="tuneOfferIcon" style="font-size: 32px;">🔗</div>
                            </div>
                            
                            <!-- Dynamic Description -->
                            <p id="tuneOfferDescription" style="
                                color: #6B7280;
                                font-size: 14px;
                                line-height: 1.4;
                                margin: 16px 0 24px 0;
                                text-align: center;
                            ">Live Tune campaign from track.modemobile.com - Affiliate ID: 43045. Real revenue tracking active.</p>
                            
                            <!-- Dynamic CTA Button -->
                            <button id="tuneCtaButton" onclick="openTuneCampaign()" style="
                                width: 100%;
                                background: #2563EB;
                                color: white;
                                border: none;
                                padding: 16px;
                                border-radius: 16px;
                                font-size: 16px;
                                font-weight: 600;
                                cursor: pointer;
                                margin-bottom: 12px;
                            ">View Campaign</button>
                            
                            <!-- WORKING Next Button (Exactly like yesterday) -->
                            <button onclick="nextTuneOffer()" style="
                                width: 100%;
                                background: white;
                                color: #6B7280;
                                border: 2px solid #E5E7EB;
                                padding: 14px;
                                border-radius: 16px;
                                font-size: 14px;
                                font-weight: 500;
                                cursor: pointer;
                                margin-bottom: 16px;
                            ">Next ></button>
                            
                            <!-- Dynamic Pagination Dots (Exactly like yesterday) -->
                            <div id="tunePaginationDots" style="text-align: center; margin-bottom: 16px;">
                                <!-- Dynamic dots will be inserted here -->
                            </div>
                            
                            <!-- Footer Text -->
                            <div style="
                                color: #9CA3AF;
                                font-size: 11px;
                                text-align: center;
                                line-height: 1.3;
                            ">T&Cs Apply | Powered by <strong>Tune</strong> • Privacy Policy</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
            let currentTuneOfferIndex = 0;
            
            const tuneOffers = {json.dumps(tune_offers)};
            
            function nextTuneOffer() {{
                currentTuneOfferIndex = (currentTuneOfferIndex + 1) % tuneOffers.length;
                updateTuneOffer();
            }}
            
            function updateTuneOffer() {{
                const offer = tuneOffers[currentTuneOfferIndex];
                
                // Update logo (image or text)
                const logoCircle = document.getElementById('tuneLogoCircle');
                const logoText = document.getElementById('tuneLogoText');
                const logoImage = document.getElementById('tuneLogoImage');
                
                logoCircle.style.background = offer.logo_bg;
                
                if (offer.logo_url) {{
                    // Show image logo
                    logoImage.src = offer.logo_url;
                    logoImage.style.display = 'block';
                    logoText.style.display = 'none';
                }} else {{
                    // Show text logo
                    logoText.textContent = offer.logo_text;
                    logoImage.style.display = 'none';
                    logoText.style.display = 'block';
                }}
                
                // Update all other content with real campaign data
                document.getElementById('tuneTagline').textContent = offer.tagline;
                document.getElementById('tuneOfferTitle').textContent = offer.title;
                
                // Handle campaign image
                const campaignImage = document.getElementById('tuneOfferImage');
                const campaignIcon = document.getElementById('tuneOfferIcon');
                
                if (offer.image_url) {{
                    // Show real campaign image
                    campaignImage.src = offer.image_url;
                    campaignImage.style.display = 'block';
                    campaignIcon.style.display = 'none';
                }} else {{
                    // Show fallback icon
                    campaignIcon.textContent = offer.icon;
                    campaignImage.style.display = 'none';
                    campaignIcon.style.display = 'block';
                }}
                
                document.getElementById('tuneOfferDescription').textContent = offer.description;
                document.getElementById('tuneCtaButton').textContent = offer.cta_text;
                document.getElementById('tuneCtaButton').style.background = offer.btn_color;
                
                // Store current offer for CTA click
                window.currentTuneOffer = offer;
                
                // Update pagination dots (exactly like yesterday)
                const dots = document.querySelectorAll('#tunePaginationDots .dot');
                dots.forEach((dot, index) => {{
                    dot.style.background = index === currentTuneOfferIndex ? '#374151' : '#D1D5DB';
                }});
                
                // Track impression for real Tune campaign
                trackTuneImpression(offer.campaign_id);
            }}
            
            function openTuneCampaign() {{
                if (window.currentTuneOffer) {{
                    // Open the actual Tune campaign URL
                    window.open(window.currentTuneOffer.iframe_url, '_blank');
                    
                    // Track click
                    console.log(`Click tracked for campaign ${{window.currentTuneOffer.campaign_id}}`);
                }}
            }}
            
            function trackTuneImpression(campaignId) {{
                // Track real Tune campaign impressions
                console.log(`Tracking Tune impression for campaign ${{campaignId}}`);
                
                // Send to your analytics (real implementation would POST to server)
                fetch('/track-tune-impression', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        campaign_id: campaignId,
                        timestamp: Date.now(),
                        source: 'cycling_popup'
                    }})
                }}).catch(e => console.log('Tracking endpoint not available:', e));
            }}
            
            function hideTunePopup() {{
                const overlay = document.getElementById('tunePopupOverlay');
                if (overlay) {{
                    overlay.style.display = 'none';
                }}
            }}
            
            // Create pagination dots (exactly like yesterday)
            function createTunePaginationDots() {{
                const dotsContainer = document.getElementById('tunePaginationDots');
                dotsContainer.innerHTML = '';
                
                tuneOffers.forEach((_, index) => {{
                    const dot = document.createElement('span');
                    dot.className = 'dot';
                    dot.style.width = '8px';
                    dot.style.height = '8px';
                    dot.style.borderRadius = '50%';
                    dot.style.margin = '0 3px';
                    dot.style.display = 'inline-block';
                    dot.style.background = index === currentTuneOfferIndex ? '#374151' : '#D1D5DB';
                    dotsContainer.appendChild(dot);
                }});
            }}
            
            // Initialize first offer (exactly like yesterday)
            if (tuneOffers.length > 0) {{
                createTunePaginationDots();
                updateTuneOffer();
            }}
            
            // Close on ESC key (exactly like yesterday)
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    hideTunePopup();
                }}
            }});
            
            // Close on overlay click (exactly like yesterday)
            document.getElementById('tunePopupOverlay')?.addEventListener('click', function(e) {{
                if (e.target === this) {{
                    hideTunePopup();
                }}
            }});
            </script>
            """
            
            st.components.v1.html(cycling_popup_html, height=600)
            
            if st.button("Close Cycling Demo", key="close_cycling_tune"):
                st.session_state.show_cycling_tune = False
                st.rerun()
    
    def _track_impression(self, campaign_id):
        """Track campaign impression (placeholder for analytics)"""
        if 'tune_impressions' not in st.session_state:
            st.session_state.tune_impressions = []
        
        impression = {
            "campaign_id": campaign_id,
            "timestamp": datetime.now().isoformat(),
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        st.session_state.tune_impressions.append(impression)
    
    def render_analytics(self):
        """Render campaign analytics"""
        st.subheader("📊 Tune Campaign Analytics")
        
        impressions = st.session_state.get('tune_impressions', [])
        
        if impressions:
            import pandas as pd
            
            df = pd.DataFrame(impressions)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Impressions", len(impressions))
            
            with col2:
                if len(df) > 0:
                    campaign_counts = df['campaign_id'].value_counts()
                    st.metric("Top Campaign", f"ID: {campaign_counts.index[0]}", f"{campaign_counts.iloc[0]} impressions")
            
            st.markdown("**Recent Impressions:**")
            st.dataframe(df.tail(10))
        else:
            st.info("No impressions tracked yet. Launch some demos to see analytics!")

# Initialize the manager
tune_manager = TunePopupManager() 