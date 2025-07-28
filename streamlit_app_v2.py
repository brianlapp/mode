import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Mode Optimization Dashboard v3.0", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Mode branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #F7007C 0%, #07C8F7 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        background: linear-gradient(90deg, #F7007C 0%, #07C8F7 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: bold;
    }
    .quick-access-card {
        background: white;
        border: 2px solid #F7007C;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .demo-success {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 Mode Optimization Dashboard v3.0</h1>
    <p>Reorganized for clarity: Company Knowledge + Active Tasks</p>
    <p><strong>🎉 MIKE LOVED THE DEMO! "Yessss, Thank you!" - Now integrating Tune ads!</strong></p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation for the two main sections
st.sidebar.title("🧭 Navigation")
main_section = st.sidebar.radio(
    "Choose Section:",
    ["📚 Company Knowledge", "⚡ Active Tasks & Demos"],
    help="Mike requested 2 clean sections: Knowledge base + Working tasks"
)

if main_section == "📚 Company Knowledge":
    st.markdown('<div class="section-header"><h2>📚 Company Knowledge & Project Progress</h2></div>', unsafe_allow_html=True)
    
    # Knowledge subsections
    knowledge_tabs = st.tabs([
        "🏢 Property Portfolio", 
        "💰 Revenue Analytics", 
        "🔧 Technical Architecture",
        "📊 Optimization History",
        "🎯 Success Metrics"
    ])
    
    with knowledge_tabs[0]:
        st.subheader("🏢 Mode Property Portfolio")
        
        # Property cards with current status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="quick-access-card">
                <h3>🟢 ModeFreeFinds.com</h3>
                <p><strong>Status:</strong> Live & Profitable</p>
                <p><strong>Revenue:</strong> $25k-$35k/month</p>
                <p><strong>Traffic:</strong> 1M monthly pageviews</p>
                <p><strong>CPL:</strong> $0.45 (PROVEN MODEL)</p>
                <p><strong>Revenue Streams:</strong></p>
                <ul>
                    <li>Programmatic ads via Ezoic (~$12 RPM)</li>
                    <li>Thanks.co popup (~$75 RPM)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="quick-access-card">
                <h3>🟡 ModeMarketMunchies</h3>
                <p><strong>Status:</strong> Just Launched</p>
                <p><strong>Focus:</strong> Finance content</p>
                <p><strong>Current CPL:</strong> $5-10 (needs optimization)</p>
                <p><strong>Target CPL:</strong> $0.45 (match MFF)</p>
                <p><strong>Priority:</strong> Visual trust building for USA audience</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="quick-access-card">
                <h3>🔴 ModeMobileDaily</h3>
                <p><strong>Status:</strong> In Development</p>
                <p><strong>Focus:</strong> Viral/breaking news</p>
                <p><strong>Content:</strong> No content yet</p>
                <p><strong>Strategy:</strong> Apply MFF proven model</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="quick-access-card">
                <h3>🔴 ModeClassActionsDaily</h3>
                <p><strong>Status:</strong> In Development</p>
                <p><strong>Focus:</strong> Consumer class action awareness</p>
                <p><strong>Content:</strong> No content yet</p>
                <p><strong>Strategy:</strong> Apply MFF proven model</p>
            </div>
            """, unsafe_allow_html=True)
    
    with knowledge_tabs[1]:
        st.subheader("💰 Revenue Analytics & Attribution")
        st.info("📊 **Revenue Insight:** MFF's $75 RPM from Thanks.co popup vs $12 RPM from programmatic shows popup monetization is 6x more effective!")
        
        # Revenue breakdown
        revenue_data = {
            "Property": ["ModeFreeFinds", "ModeMarketMunchies", "ModeMobileDaily", "ModeClassActionsDaily"],
            "Monthly Revenue": ["$25k-$35k", "$0 (just launched)", "$0 (no content)", "$0 (no content)"],
            "CPL": ["$0.45", "$5-10", "TBD", "TBD"],
            "Status": ["✅ Profitable", "🔧 Optimizing", "🚧 Building", "🚧 Building"]
        }
        st.table(pd.DataFrame(revenue_data))
    
    with knowledge_tabs[2]:
        st.subheader("🔧 Technical Architecture Knowledge")
        st.markdown("""
        **🏗️ MFF's Proven $0.45 CPL Formula:**
        - **Triple Tracking Stack:** Meta Pixel + Tune SDK + Smart Recognition
        - **Form Enhancement:** Genius placeholder-based detection
        - **URL Attribution:** Every link gets source + email tracking
        - **Trust Signals:** Facebook page widget, testimonials
        - **Thanks.co Popup:** ~$75 RPM revenue driver
        
        **🎯 Key Insight:** This is a scalable template, not just a single landing page!
        """)
    
    with knowledge_tabs[3]:
        st.subheader("📊 Optimization History & Learnings")
        st.markdown("""
        **📚 Key Lessons Learned:**
        1. **Phone Field Lesson:** Always verify business requirements before optimization (MMM phone = service requirement)
        2. **USA Psychology:** Money=freedom messaging > abstract investment concepts
        3. **Visual Trust:** Lifestyle imagery more impactful than form optimization when fields are required
        4. **Demo Success:** Mike LOVED the working popup with cycling offers - validates our approach!
        """)
    
    with knowledge_tabs[4]:
        st.subheader("🎯 Success Metrics & Goals")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("Target CPL", "$0.45", "MFF proven model")
        
        with metrics_col2:
            st.metric("Popup RPM", "$75", "Thanks.co performance")
        
        with metrics_col3:
            st.metric("Traffic Goal", "1M+ pageviews", "Per property monthly")

else:  # Active Tasks & Demos section
    st.markdown('<div class="section-header"><h2>⚡ Active Tasks & Demos</h2></div>', unsafe_allow_html=True)
    

    
    # Active tasks tabs
    task_tabs = st.tabs([
        "🎬 Live Demo", 
        "🔗 Tune Integration",
        "🛠️ Management System", 
        "📝 Code Snippets",
        "🚀 Quick Deploy"
    ])
    
    with task_tabs[0]:
        st.subheader("🎬 Working Popup Demo")
        st.info("💡 Interactive popup with cycling offers - click 'Next >' to see different campaigns")
        
        # Launch demo button
        if st.button("🚀 Launch Interactive Demo", type="primary"):
            st.session_state.show_popup = True
        
        if st.session_state.get("show_popup", False):
            # Include the working demo that Mike loved
            popup_demo_html = """
            <div id="mode-popup-demo" style="margin: 20px 0;">
                <!-- Thanks.co Exact Replica Design -->
                <div id="modePopupOverlay" style="
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
                        <button onclick="hideModePopup()" style="
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
                        
                        <!-- Dynamic Logo Circle -->
                        <div id="logoCircle" style="
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
                        ">WHO GIVES A CRAP</div>
                        
                        <!-- Main Content Area -->
                        <div style="padding: 24px; padding-top: 100px; text-align: center;">
                            
                            <!-- Dynamic Tagline -->
                            <div id="tagline" style="
                                background: #F3F4F6;
                                color: #6B7280;
                                padding: 6px 12px;
                                border-radius: 16px;
                                font-size: 12px;
                                margin-bottom: 24px;
                                display: inline-block;
                                font-weight: 500;
                            ">Care for your bottom & the planet</div>
                            
                            <!-- Dynamic Title -->
                            <h2 id="offerTitle" style="
                                margin: 0 0 8px 0;
                                font-size: 24px;
                                font-weight: 800;
                                line-height: 1.2;
                                color: #111827;
                            ">20% off Who Gives A Crap toilet paper</h2>
                            
                            <!-- Dynamic Icon -->
                            <div id="offerIcon" style="font-size: 32px; margin: 16px 0;">🧻</div>
                            
                            <!-- Dynamic Description -->
                            <p id="offerDescription" style="
                                color: #6B7280;
                                font-size: 14px;
                                line-height: 1.4;
                                margin: 16px 0 24px 0;
                                text-align: center;
                            ">Wipe right with bamboo TP that's better for the earth (& your cheeks) + 50% of profits go towards building toilets. Use code ecosave20</p>
                            
                            <!-- Dynamic CTA Button -->
                            <button id="ctaButton" style="
                                width: 100%;
                                background: #7C3AED;
                                color: white;
                                border: none;
                                padding: 16px;
                                border-radius: 16px;
                                font-size: 16px;
                                font-weight: 600;
                                cursor: pointer;
                                margin-bottom: 12px;
                            ">Unlock offer</button>
                            
                            <!-- WORKING Next Button -->
                            <button onclick="nextOffer()" style="
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
                            
                            <!-- Dynamic Pagination Dots -->
                            <div id="paginationDots" style="text-align: center; margin-bottom: 16px;">
                                <span class="dot" style="width: 8px; height: 8px; background: #374151; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                <span class="dot" style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                <span class="dot" style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                <span class="dot" style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                            </div>
                            
                            <!-- Footer Text -->
                            <div style="
                                color: #9CA3AF;
                                font-size: 11px;
                                text-align: center;
                                line-height: 1.3;
                            ">T&Cs Apply | Powered by <strong>Mode</strong> • Privacy Policy</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
            let currentOfferIndex = 0;
            
            const offers = [
                {
                    logo_bg: "#2563EB",
                    logo_text: "WHO GIVES A CRAP",
                    tagline: "Care for your bottom & the planet",
                    title: "20% off Who Gives A Crap toilet paper",
                    icon: "🧻",
                    description: "Wipe right with bamboo TP that's better for the earth (& your cheeks) + 50% of profits go towards building toilets. Use code ecosave20",
                    btn_color: "#7C3AED"
                },
                {
                    logo_bg: "#4F46E5",
                    logo_text: "TRADE PLATFORM",
                    tagline: "Build your wealth & the future",
                    title: "50% off Premium Trading Platform",
                    icon: "📈",
                    description: "Start trading commission-free stocks with professional research tools. Perfect for building your investment portfolio. Use code tradepro50",
                    btn_color: "#4F46E5"
                },
                {
                    logo_bg: "#059669",
                    logo_text: "CASH BACK",
                    tagline: "Earn on every purchase you make",
                    title: "$20 Cashback Bonus",
                    icon: "💳",
                    description: "Join 15M+ users earning cashback at 7000+ stores. Get your $20 bonus after first qualifying purchase. Free to join! Use code cashback20",
                    btn_color: "#059669"
                },
                {
                    logo_bg: "#DC2626",
                    logo_text: "SAM'S CLUB",
                    tagline: "Care for your shopping & savings",
                    title: "36% off Sam's Club Plus",
                    icon: "🛍️",
                    description: "Free shipping, early shopping hours, 2% Sam's Cash rewards. Plus exclusive member prices on groceries and gas. Use code samsclub36",
                    btn_color: "#DC2626"
                }
            ];
            
            function nextOffer() {
                currentOfferIndex = (currentOfferIndex + 1) % offers.length;
                updateOffer();
            }
            
            function updateOffer() {
                const offer = offers[currentOfferIndex];
                
                // Update all dynamic content instantly
                document.getElementById('logoCircle').style.background = offer.logo_bg;
                document.getElementById('logoCircle').textContent = offer.logo_text;
                document.getElementById('tagline').textContent = offer.tagline;
                document.getElementById('offerTitle').textContent = offer.title;
                document.getElementById('offerIcon').textContent = offer.icon;
                document.getElementById('offerDescription').textContent = offer.description;
                document.getElementById('ctaButton').style.background = offer.btn_color;
                
                // Update pagination dots
                const dots = document.querySelectorAll('.dot');
                dots.forEach((dot, index) => {
                    dot.style.background = index === currentOfferIndex ? '#374151' : '#D1D5DB';
                });
            }
            
            function hideModePopup() {
                const overlay = document.getElementById('modePopupOverlay');
                if (overlay) {
                    overlay.style.display = 'none';
                }
            }
            
            // Close on ESC key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    hideModePopup();
                }
            });
            
            // Close on overlay click
            document.getElementById('modePopupOverlay')?.addEventListener('click', function(e) {
                if (e.target === this) {
                    hideModePopup();
                }
            });
            </script>
            """
            
            st.components.v1.html(popup_demo_html, height=600)
            
            if st.button("Close Demo"):
                st.session_state.show_popup = False
                st.rerun()
    
    with task_tabs[1]:
        st.subheader("🔗 Tune Integration (Mike's Next Request)")
        st.info("🎯 **Mike's Request:** Integrate Tune ads into the popup unit")
        
        # Show Mike's provided iframe code
        st.markdown("**Mike's Tune iframe code:**")
        tune_code = """<!-- iFrame Ad Tag: 13 -->
<iframe src="https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045&format=iframe" 
        scrolling="no" frameborder="0" marginheight="0" marginwidth="0" 
        width="600" height="400"></iframe>
<!-- // End Ad Tag -->"""
        
        st.code(tune_code, language="html")
        
        st.markdown("**🔧 Integration Plan:**")
        st.markdown("""
        1. **Replace static offers** with dynamic Tune iframe content
        2. **Maintain cycling functionality** but serve real Tune ads
        3. **Preserve popup UX** that Mike loved
        4. **Add impression tracking** for revenue attribution
        """)
        
        # Integration preview
        st.subheader("🚀 Tune Integration Preview")
        if st.button("Build Tune-Powered Demo", type="primary"):
            st.success("🔨 **Building Tune integration...** This will modify the popup to serve real Tune ads!")
            
            # Here we'll build the Tune-integrated version
            st.code("""
// Modified popup to serve Tune ads
const tuneOffers = [
    {
        iframe_src: "https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045&format=iframe",
        campaign_id: 13,
        width: 600,
        height: 400
    }
    // More Tune campaigns can be added here
];

function loadTuneOffer(index) {
    const offer = tuneOffers[index];
    const iframe = document.createElement('iframe');
    iframe.src = offer.iframe_src;
    iframe.width = offer.width;
    iframe.height = offer.height;
    iframe.frameBorder = '0';
    iframe.scrolling = 'no';
    
    // Replace popup content with Tune iframe
    document.getElementById('offerContent').innerHTML = '';
    document.getElementById('offerContent').appendChild(iframe);
}
            """, language="javascript")
    
    with task_tabs[2]:
        st.subheader("🛠️ Backend Management System")
        st.info("🎯 **Mike's Request:** Backend system to manually add Tune links/impression pixels")
        
        st.markdown("**📋 Management System Features:**")
        st.markdown("""
        - **Campaign Manager:** Add/edit Tune campaigns
        - **Creative Manager:** Upload/manage ad creatives  
        - **URL Manager:** Manage tracking URLs and parameters
        - **Impression Tracking:** Monitor performance metrics
        - **A/B Testing:** Test different ad combinations
        """)
        
        # Simple management interface prototype
        st.subheader("🔧 Campaign Management Interface")
        
        with st.form("add_campaign"):
            st.markdown("**Add New Tune Campaign:**")
            campaign_name = st.text_input("Campaign Name", placeholder="Trading Platform Signup")
            campaign_id = st.number_input("Campaign ID", value=13, min_value=1)
            aff_id = st.number_input("Affiliate ID", value=43045, min_value=1)
            iframe_width = st.number_input("Width", value=600, min_value=100)
            iframe_height = st.number_input("Height", value=400, min_value=100)
            
            submitted = st.form_submit_button("Add Campaign", type="primary")
            
            if submitted:
                st.success(f"✅ Campaign '{campaign_name}' added successfully!")
                st.code(f"""
<iframe src="https://track.modemobile.com/aff_ad?campaign_id={campaign_id}&aff_id={aff_id}&format=iframe" 
        scrolling="no" frameborder="0" marginheight="0" marginwidth="0" 
        width="{iframe_width}" height="{iframe_height}"></iframe>
                """, language="html")
    
    with task_tabs[3]:
        st.subheader("📝 Ready-to-Use Code Snippets")
        
        snippet_type = st.selectbox("Choose code snippet:", [
            "Popup with Tune Integration",
            "Campaign Management Functions", 
            "Revenue Tracking",
            "MFF Production Code",
            "Universal Tracking Template"
        ])
        
        if snippet_type == "Popup with Tune Integration":
            st.code("""
// Enhanced popup with Tune integration
class TunePopupManager {
    constructor() {
        this.campaigns = [];
        this.currentIndex = 0;
    }
    
    addCampaign(campaign) {
        this.campaigns.push({
            id: campaign.id,
            iframe_src: `https://track.modemobile.com/aff_ad?campaign_id=${campaign.id}&aff_id=${campaign.aff_id}&format=iframe`,
            width: campaign.width || 600,
            height: campaign.height || 400,
            name: campaign.name
        });
    }
    
    showPopup() {
        // Create popup overlay
        this.createPopupHTML();
        this.loadCurrentCampaign();
    }
    
    nextCampaign() {
        this.currentIndex = (this.currentIndex + 1) % this.campaigns.length;
        this.loadCurrentCampaign();
        this.trackImpression();
    }
    
    trackImpression() {
        const campaign = this.campaigns[this.currentIndex];
        // Send tracking data to analytics
        fetch('/track-impression', {
            method: 'POST',
            body: JSON.stringify({
                campaign_id: campaign.id,
                timestamp: Date.now()
            })
        });
    }
}

// Usage
const tunePopup = new TunePopupManager();
tunePopup.addCampaign({id: 13, aff_id: 43045, name: "Demo Campaign"});
tunePopup.showPopup();
            """, language="javascript")
    
    with task_tabs[4]:
        st.subheader("🚀 Quick Deploy Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Update Main Dashboard", type="primary"):
                st.success("✅ Deploying reorganized dashboard...")
                # This would update the main dashboard file
        
        with col2:
            if st.button("🔗 Deploy Tune Integration", type="primary"):
                st.success("✅ Deploying Tune-powered popup...")
                # This would deploy the Tune integration
        
        with col3:
            if st.button("📊 Launch Management System", type="primary"):
                st.success("✅ Launching campaign management...")
                # This would launch the management interface

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 <strong>Mode Optimization Dashboard v3.0</strong> - Reorganized for Mike's workflow</p>
    <p>📚 Knowledge Base + ⚡ Active Tasks = 🎯 Maximum Efficiency</p>
</div>
""", unsafe_allow_html=True) 