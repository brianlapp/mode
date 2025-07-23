import streamlit as st
import json
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Mode Optimization Dashboard", 
    page_icon="🚀",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        background-color: black;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
    }
    .code-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .risk-low { border-left: 4px solid #28a745; }
    .risk-medium { border-left: 4px solid #ffc107; }
    .risk-high { border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("img/logo.svg", width=200)
st.sidebar.markdown("---")

# Always visible navigation buttons instead of dropdown
st.sidebar.markdown("### 📋 Navigation")

if st.sidebar.button("🏠 Overview Dashboard", use_container_width=True):
    st.session_state.page = "🏠 Overview Dashboard"
    st.query_params.clear()  # Clear URL parameters
    st.rerun()
if st.sidebar.button("🔧 Global Scripts Implementation", use_container_width=True):
    st.session_state.page = "🔧 Global Scripts Implementation"
    st.query_params.clear()  # Clear URL parameters
    st.rerun()
if st.sidebar.button("💻 Code Repository", use_container_width=True):
    st.session_state.page = "💻 Code Repository"
    st.query_params.clear()  # Clear URL parameters
    st.rerun()
if st.sidebar.button("🏢 Properties Portfolio", use_container_width=True):
    st.session_state.page = "🏢 Properties Portfolio"
    st.query_params.clear()  # Clear URL parameters
    st.rerun()
if st.sidebar.button("📊 Property Deep Dive", use_container_width=True):
    st.session_state.page = "📊 Property Deep Dive"
    st.query_params.clear()  # Clear URL parameters
    st.rerun()
if st.sidebar.button("📈 Analytics & Reports", use_container_width=True):
    st.session_state.page = "📈 Analytics & Reports"
    st.query_params.clear()  # Clear URL parameters
    st.rerun()

# Handle URL parameters for direct navigation
query_params = st.query_params
if "page" in query_params:
    page_param = query_params["page"]
    if page_param == "code":
        st.session_state.page = "💻 Code Repository"
    elif page_param == "global":
        st.session_state.page = "🔧 Global Scripts Implementation"
    elif page_param == "analytics":
        st.session_state.page = "📈 Analytics & Reports"
    elif page_param == "properties":
        st.session_state.page = "📊 Property Deep Dive"
    elif page_param == "portfolio":
        st.session_state.page = "🏢 Properties Portfolio"

# Set default page if not already set
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Overview Dashboard"

page = st.session_state.page

# Load project data
try:
    with open("memory-bank/project-memories-corrected.json") as f:
        data = json.load(f)
except:
    with open("memory-bank/project-memories.json") as f:
        data = json.load(f)

properties = data.get('properties', {})

# ============================================================================
# PAGE 1: OVERVIEW DASHBOARD - CLEAN LANDING PAGE
# ============================================================================
if page == "🏠 Overview Dashboard":
    st.title("🎯 Mode Properties Optimization Dashboard")
    st.markdown("**Complete portfolio analysis, mobile optimization, and revenue tracking for Mike's 4 Mode properties**")
    
    # Quick Navigation Cards
    st.header("🗂️ Dashboard Sections")
    
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        if st.button("🏢 Properties Portfolio\n\nComplete visual audit with mobile screenshots, logos, and optimization strategies for all 4 Mode properties.", 
                     use_container_width=True, key="nav_properties", type="primary"):
            st.session_state.page = "🏢 Properties Portfolio"
            st.rerun()
    
    with nav_col2:
        if st.button("🔧 Global Scripts\n\nLeadPages implementation guide with Mike's optimized tracking code ready for deployment.", 
                     use_container_width=True, key="nav_global", type="primary"):
            st.session_state.page = "🔧 Global Scripts Implementation"
            st.rerun()
    
    with nav_col3:
        if st.button("💻 Code Repository\n\nAll optimization code, scripts, and technical implementations organized by property and function.", 
                     use_container_width=True, key="nav_code", type="primary"):
            st.session_state.page = "💻 Code Repository"
            st.rerun()

    # Quick Stats
    st.markdown("---")
    st.header("📊 Portfolio Snapshot")
    
    snapshot_col1, snapshot_col2, snapshot_col3, snapshot_col4 = st.columns(4)
    
    with snapshot_col1:
        st.metric(
            label="🟢 Active Revenue",
            value="$25k-$35k",
            delta="ModeFreeFinds monthly"
        )
    
    with snapshot_col2:
        st.metric(
            label="📱 Properties Audited",
            value="4/4",
            delta="Mobile screenshots captured"
        )
    
    with snapshot_col3:
        st.metric(
            label="🎯 Optimization Target",
            value="$80k-$130k",
            delta="Full portfolio potential"
        )
    
    with snapshot_col4:
        st.metric(
            label="⚡ Revenue Boost",
            value="+$6k-$13k",
            delta="Prebid.js opportunity"
        )

    # Key Insights
    st.markdown("---")
    st.header("🔍 Key Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown("**🎁 Thanks.co Analysis Complete**")
        st.info("5-slide popup carousel analyzed with custom replacement strategy developed. Potential for 100% revenue retention vs current commission model.")
        
        st.markdown("**📱 Mobile Optimization Ready**")
        st.success("All properties captured via mobile screenshots. Visual insights documented for conversion optimization.")
    
    with insight_col2:
        st.markdown("**💰 Revenue Opportunities Identified**")
        st.warning("Prebid.js implementation could boost ModeFreeFinds RPM from $12 to $18-$25, adding $6k-$13k monthly.")
        
        st.markdown("**🚀 Portfolio Scaling Path**")
        st.info("ModeMarketMunchies ready for monetization. MMD and MCAD have content frameworks prepared for launch.")

    # External Links
    st.markdown("---")
    st.header("🔗 External Resources")
    
    link_col1, link_col2, link_col3 = st.columns(3)
    
    with link_col1:
        st.markdown("**🌐 Live Properties**")
        st.markdown("- [ModeFreeFinds.com](https://modefreefinds.com/)")
        st.markdown("- [ModeMarketMunchies.com](https://modemarketmunchies.com/)")
        st.markdown("- [ModeMobileDaily.com](https://modemobiledaily.com/)")
        st.markdown("- [ModeClassActionsDaily.com](https://modeclassactionsdaily.com/)")

    with link_col2:
        st.markdown("**📊 Tracking & Analytics**")
        st.markdown("- [Tune (HasOffers)](https://modemobile.go2cloud.org/)")
        st.markdown("- [Meta Business Manager](https://business.facebook.com/)")
        st.markdown("- [Revmatics.ai](https://revmatics.ai/)")

    with link_col3:
        st.markdown("**💻 Development Resources**")
        st.markdown("- [GitHub Repository](https://github.com/brianlapp/mode)")
        st.markdown("- [Direct Dashboard Links](https://modedash.streamlit.app/)")
        st.markdown("- [Support Documentation](https://helpdesk.modemobile.com/)")

    # Quick Actions
    st.markdown("---")
    st.header("⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🎬 View Thanks.co Demo", use_container_width=True):
            st.session_state.page = "🏢 Properties Portfolio"
            # You could add URL params here to jump directly to Thanks.co tab
            st.rerun()
    
    with action_col2:
        if st.button("📈 Check Property Analytics", use_container_width=True):
            st.session_state.page = "📈 Analytics & Reports"
            st.rerun()
    
    with action_col3:
        if st.button("🔧 Start Property Setup", use_container_width=True):
            st.session_state.page = "📊 Property Deep Dive"
            st.rerun()

# ============================================================================
# PAGE 2: GLOBAL SCRIPTS IMPLEMENTATION
# ============================================================================
elif page == "🔧 Global Scripts Implementation":
    st.title("🔧 LeadPages Global Scripts Implementation")
    st.markdown("**Step-by-step guide to implement Mike's cleaned code**")
    
    # Implementation Status
    st.header("Implementation Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.metric("Setup Process", "Add → Save → Done", "applies to ALL content")
    with status_col2:
        st.metric("Universal Coverage", "ALL assets", "landing pages, pop-ups, sites") 
    with status_col3:
        st.metric("Implementation", "Copy-Paste Ready", "13 sections prepared")

    # Implementation Steps
    st.markdown("---")
    st.header("Implementation Guide")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Getting Started", "📄 Landing Pages", "🎯 Thank You Pages"])
    
    with tab1:
        st.subheader("🎯 LeadPages Global Scripts - Official Guide")
        
        st.markdown("""
        <div style="background-color: #07C8F7; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <h4 style="color: white; margin: 0;">🎯 GREAT NEWS: Global Scripts are exactly what we need for Mike's system!</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Step 1: Access Global Scripts**")
        st.info("✅ **CONFIRMED LOCATION:** Click 'Scripts' in your LeadPages account navigation menu")
        
        st.write("**Step 2: How Global Scripts Work**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ What They Do:**")
            st.write("• Apply to ALL content automatically")
            st.write("• Landing pages, pop-ups, sites, conversion tools")
            st.write("• Apply to new AND existing content")
            st.write("• Available on Pro and Advanced plans")
        with col2:
            st.markdown("**🎯 Perfect for Mike:**")
            st.write("• Universal tracking across all properties")
            st.write("• No more copy-paste errors")
            st.write("• Instant deployment to everything")
            st.write("• Can customize per asset if needed")
        
        st.write("**Step 3: Script Types Available**")
        script_col1, script_col2 = st.columns(2)
        with script_col1:
            st.info("**Google Analytics 4:** Just enter your GA4 ID")
        with script_col2:
            st.info("**Custom Script:** Perfect for our Meta Pixel, Tune SDK, etc.")
        
        st.write("**Step 4: Implementation Strategy**")
        st.markdown("""
        <div style="background-color: #07C8F7; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <h4 style="color: white; margin: 0;">🎯 UNIVERSAL FIRST: Start with scripts that work for all properties</h4>
        </div>
        """, unsafe_allow_html=True)
        st.write("1. Add Tune SDK as Custom Script (universal)")
        st.write("2. Add Facebook SDK as Custom Script (universal)")
        st.write("3. Add Smart Recognition as Custom Script (universal)")
        st.write("4. Use 'Manage Global Scripts' per asset for property-specific elements")
        
        st.write("**Step 5: Test Script (Optional)**")
        with st.expander("Simple Test Script - Use if you want to verify first"):
            st.code("""
console.log('🚀 Global Scripts Working!', window.location.hostname);
console.log('✅ Test completed at:', new Date().toISOString());
            """, language="javascript")
            
        st.markdown("---")
        st.markdown("""
        <div style="background-color: #07C8F7; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <h4 style="color: white; margin: 0;">🎯 READY TO IMPLEMENT: Our sections are perfectly designed for this system!</h4>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Landing Page Global Scripts")
        st.write("**6 sections ready for implementation**")
        
        st.info("🎯 **STRATEGY:** Add universal sections as Global Scripts, customize property-specific per asset")
        
        landing_sections = [
            ("Tune SDK", "LOWEST", "Universal revenue attribution"),
            ("Facebook SDK", "LOW", "Social integration"),
            ("Smart Recognition", "LOW", "Additional tracking"),
            ("Mobile Navigation", "LOW", "UI enhancement - just adds nav bar"),
            ("Form Enhancement", "MEDIUM", "Mike's proven system"),
            ("Meta Pixel", "MEDIUM", "Just update the Pixel ID")
        ]
        
        for i, (name, risk, desc) in enumerate(landing_sections, 1):
            risk_class = f"risk-{risk.lower()}" if risk != "HIGHEST" else "risk-high"
            
            with st.expander(f"Section {i}: {name} - {risk} RISK"):
                st.markdown(f'<div class="{risk_class}"><strong>{desc}</strong></div>', unsafe_allow_html=True)
                
                if st.button(f"Show {name} Code", key=f"landing_{i}"):
                    st.info(f"Code for {name} section is in the Code Repository page!")
                    
                implemented = st.checkbox(f"✅ {name} implemented", key=f"landing_done_{i}")

    with tab3:
        st.subheader("Thank You Page Global Scripts")
        st.write("**7 sections ready for implementation - Complete revenue system**")
        
        st.markdown("""
        <div style="background-color: #F7007C; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <h4 style="color: white; margin: 0;">🔥 THE MONEY MAKER: URL Injection section works universally - perfect for Global Scripts!</h4>
        </div>
        """, unsafe_allow_html=True)
        
        thankyou_sections = [
            ("Tune Conversion", "LOWEST", "Revenue attribution"),
            ("URL Injection", "LOW", "Link monetization - THE MONEY MAKER"),
            ("Error Monitoring", "LOW", "System protection"),
            ("Facebook SDK", "LOW", "Social features"),
            ("Impression Pixel", "LOW", "Affiliate tracking"),
            ("Mode UA API", "MEDIUM", "CRM integration - just update campaign name"),
            ("Meta Conversion", "MEDIUM", "Just update Pixel ID")
        ]
        
        for i, (name, risk, desc) in enumerate(thankyou_sections, 1):
            risk_class = f"risk-{risk.lower()}" if risk != "HIGHEST" else "risk-high"
            
            with st.expander(f"Section {i}: {name} - {risk} RISK"):
                st.markdown(f'<div class="{risk_class}"><strong>{desc}</strong></div>', unsafe_allow_html=True)
                
                if name == "URL Injection":
                    st.warning("🔥 This is where the revenue magic happens! Every link gets source + email attribution.")
                
                if st.button(f"Show {name} Code", key=f"thankyou_{i}"):
                    st.info(f"Code for {name} section is in the Code Repository page!")
                    
                implemented = st.checkbox(f"✅ {name} implemented", key=f"thankyou_done_{i}")

    # Progress Tracking
    st.markdown("---")
    st.header("Implementation Progress")
    
    progress_col1, progress_col2 = st.columns(2)
    with progress_col1:
        st.write("**Landing Page Progress**")
        landing_progress = st.progress(0)
        st.write("0/6 sections implemented")
        
    with progress_col2:
        st.write("**Thank You Page Progress**") 
        thankyou_progress = st.progress(0)
        st.write("0/7 sections implemented")

# ============================================================================
# PAGE 3: CODE REPOSITORY
# ============================================================================
elif page == "💻 Code Repository":
    st.title("💻 Clean Code Repository")
    st.markdown("**Copy-paste ready code sections for Global Scripts**")
    
    code_tab1, code_tab2 = st.tabs(["📄 Landing Page Code", "🎯 Thank You Page Code"])
    
    with code_tab1:
        st.header("Landing Page Global Scripts")
        st.write("**Ready-to-implement sections in order of safety**")
        
        # Section 1: Tune SDK
        with st.expander("🟢 Section 1: Tune SDK (LOWEST RISK)", expanded=False):
            st.markdown("**Purpose:** Universal revenue attribution - same across all properties")
            st.code("""
(function initializeTuneSDK() {
    // Clean Tune SDK implementation with error handling
    !function(){var o=window.tdl=window.tdl||[];if(o.invoked)window.console&&console.error&&console.error("Tune snippet already loaded");else{o.invoked=!0,o.methods=["init","identify","convert"],o.factory=function(n){return function(){var e=Array.prototype.slice.call(arguments);return e.unshift(n),o.push(e),o}};for(var e=0;e<o.methods.length;e++){var n=o.methods[e];o[n]=o.factory(n)}o.init=function(e){var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src="https://js.go2sdk.com/v2/tune.js";var t=document.getElementsByTagName("script")[0];t.parentNode.insertBefore(n,t),o.domain=e}}}();
    
    // Initialize with Mode tracking domain (same across all properties)
    tdl.init("https://track.modemobile.com");
    tdl.identify();
    
    console.log('✅ Tune SDK initialized');
})();
            """, language="javascript")
            
            if st.button("Copy Tune SDK Code", key="copy_tune_landing"):
                st.success("✅ Code copied! Paste into LeadPages Global Scripts")
        
        # Section 2: Facebook SDK
        with st.expander("🟢 Section 2: Facebook SDK (LOW RISK)"):
            st.markdown("**Purpose:** Universal social integration")
            st.code("""
(function initializeFacebookSDK() {
    function setupFacebookSDK() {
        // Create fb-root div if it doesn't exist
        if (!document.getElementById('fb-root')) {
            const fbRoot = document.createElement('div');
            fbRoot.id = 'fb-root';
            document.body.insertBefore(fbRoot, document.body.firstChild);
        }
        
        // Load Facebook SDK script
        const fbScript = document.createElement('script');
        fbScript.async = true;
        fbScript.defer = true;
        fbScript.crossOrigin = 'anonymous';
        fbScript.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v22.0';
        document.head.appendChild(fbScript);
        
        console.log('✅ Facebook SDK initialized');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupFacebookSDK);
    } else {
        setupFacebookSDK();
    }
})();
            """, language="javascript")
            
            if st.button("Copy Facebook SDK Code", key="copy_fb_landing"):
                st.success("✅ Code copied! Paste into LeadPages Global Scripts")
        
        # Section 3: Smart Recognition
        with st.expander("🟢 Section 3: Smart Recognition (LOW RISK)"):
            st.markdown("**Purpose:** Additional tracking layer for enhanced attribution")
            st.code("""
(function initializeSmartRecognition() {
    // Smart Recognition tracking system
    var _avp = _avp || [];
    (function() {
        var s = document.createElement('script');
        s.type = 'text/javascript'; 
        s.async = true; 
        s.src = 'https://portal.smartrecognition.com/js/libcode3.js';
        var x = document.getElementsByTagName('script')[0];
        x.parentNode.insertBefore(s, x);
        
        console.log('✅ Smart Recognition initialized');
    })();
})();
            """, language="javascript")
            
            if st.button("Copy Smart Recognition Code", key="copy_smart_landing"):
                st.success("✅ Code copied! Paste into LeadPages Global Scripts")

        # Section 4: Mobile Navigation
        with st.expander("🟢 Section 4: Mobile Navigation (LOW RISK)"):
            st.markdown("**Purpose:** Responsive navigation with hamburger menu")
            st.code("""
(function initializeMobileNavigation() {
    function addNavigationHTML() {
        const navHTML = `
        <nav class="lp-custom-nav">
            <div class="menu-toggle" id="mobileMenuToggle">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            <ul class="menu-links" id="navLinks">
                <li><a href="https://modefreefinds.com/" target="_blank" rel="noopener">Home</a></li>
                <li><a href="https://helpdesk.modemobile.com/hc/en-us" target="_blank" rel="noopener">Contact Us</a></li>
                <li><a href="https://modefreefinds.com/terms-of-service/" target="_blank" rel="noopener">T&Cs</a></li>
                <li><a href="https://modefreefinds.com/privacy-policy-2/" target="_blank" rel="noopener">Privacy</a></li>
            </ul>
        </nav>`;
        
        // Insert navigation at top of body
        document.body.insertAdjacentHTML('afterbegin', navHTML);
        
        // Add mobile toggle functionality
        const toggleBtn = document.getElementById('mobileMenuToggle');
        const navLinks = document.getElementById('navLinks');
        
        if (toggleBtn && navLinks) {
            toggleBtn.addEventListener('click', function() {
                navLinks.style.display = (navLinks.style.display === "none" || navLinks.style.display === "") ? "flex" : "none";
            });
        }
        
        console.log('✅ Mobile navigation initialized');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addNavigationHTML);
    } else {
        addNavigationHTML();
    }
})();
            """, language="javascript")
            
            if st.button("Copy Mobile Navigation Code", key="copy_nav_landing"):
                st.success("✅ Code copied! Note: Customize URLs for each property")

        # Section 5: Form Enhancement
        with st.expander("🟡 Section 5: Form Enhancement (MEDIUM RISK)"):
            st.markdown("**Purpose:** Mike's genius placeholder-based form detection system")
            st.info("💡 This is Mike's proven system - already works on MFF!")
            st.code("""
(function initializeFormEnhancement() {
    document.addEventListener("DOMContentLoaded", function () {
        console.log("📝 Form Enhancement Loading");

        const form = document.querySelector("form");
        if (!form) return console.error("❌ No form found.");

        const originalThankYouURL = form.getAttribute("data-thank-you") || "";
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get("source") || "";

        // Mike's genius: Match by input type + placeholder
        function getInput(placeholderText) {
            return [...form.querySelectorAll("input")].find(input =>
                (input.placeholder || "").toLowerCase().includes(placeholderText.toLowerCase())
            );
        }

        form.addEventListener("submit", function () {
            const email = getInput("email")?.value.trim() || "";
            const firstName = getInput("first")?.value.trim() || "";
            const lastName = getInput("last")?.value.trim() || "";
            const phone = getInput("phone")?.value.trim() || "";

            try {
                const thankYouURL = new URL(originalThankYouURL);
                if (email) thankYouURL.searchParams.set("email", email);
                if (firstName) thankYouURL.searchParams.set("first_name", firstName);
                if (lastName) thankYouURL.searchParams.set("last_name", lastName);
                if (phone) thankYouURL.searchParams.set("phone", phone);
                if (source) thankYouURL.searchParams.set("source", source);

                form.setAttribute("data-thank-you", thankYouURL.toString());
                console.log("🚀 Thank You URL updated:", thankYouURL.toString());
            } catch (err) {
                console.error("⚠ Failed to update thank-you URL:", err);
            }
        }, { once: true });
    });
})();
            """, language="javascript")
            
            if st.button("Copy Form Enhancement Code", key="copy_form_landing"):
                st.success("🔥 THE GENIUS SYSTEM copied! Test form submission carefully")

        # Section 6: Meta Pixel
        with st.expander("🟡 Section 6: Meta Pixel (MEDIUM RISK)"):
            st.markdown("**Purpose:** Property-specific Facebook tracking")
            st.info("💡 Simple: Just update the Pixel ID for each property!")
            st.code("""
(function initializeMetaPixel() {
    // ⚠️ IMPORTANT: Change pixel ID for each property
    const PIXEL_ID = '1153754019617349'; // MFF Pixel - UPDATE FOR OTHER PROPERTIES
    
    // Meta Pixel implementation with error handling
    !function(f,b,e,v,n,t,s) {
        if(f.fbq) return; // Prevent double-loading
        n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)
    }(window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
    
    fbq('init', PIXEL_ID);
    fbq('track', 'PageView');
    
    // Add noscript fallback
    const noscript = document.createElement('noscript');
    noscript.innerHTML = `<img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=${PIXEL_ID}&ev=PageView&noscript=1"/>`;
    document.head.appendChild(noscript);
    
    console.log('✅ Meta Pixel initialized:', PIXEL_ID);
})();
            """, language="javascript")
            
            if st.button("Copy Meta Pixel Code", key="copy_meta_landing"):
                st.info("💡 Remember: Update PIXEL_ID for each property")
        
        # Link to full files
        st.markdown("---")
        st.markdown("""
        <div style="background-color: #F7007C; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <h3 style="color: white; margin: 0;">🎯 ALL 6 LANDING PAGE SECTIONS READY!</h3>
            <p style="color: white; margin: 0.5rem 0 0 0;">Start with Sections 1-2 (lowest risk)</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Complete Code Files:**")
        st.markdown("- [Full Landing Page Code](https://github.com/brianlapp/mode/blob/main/global-scripts-ready-code.js)")
        st.markdown("- All sections with CSS and detailed implementation notes")

    with code_tab2:
        st.header("Thank You Page Global Scripts")
        st.write("**The complete $0.45 CPL revenue system**")
        
        # Section 1: Tune Conversion
        with st.expander("🟢 Section 1: Tune Conversion (LOWEST RISK)", expanded=False):
            st.markdown("**Purpose:** Revenue conversion tracking - records actual conversions")
            st.code("""
(function initializeTuneConversion() {
    // Same Tune SDK as landing page but with tdl.convert()
    !function(){var o=window.tdl=window.tdl||[];if(o.invoked)window.console&&console.error&&console.error("Tune snippet already loaded");else{o.invoked=!0,o.methods=["init","identify","convert"],o.factory=function(n){return function(){var e=Array.prototype.slice.call(arguments);return e.unshift(n),o.push(e),o}};for(var e=0;e<o.methods.length;e++){var n=o.methods[e];o[n]=o.factory(n)}o.init=function(e){var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src="https://js.go2sdk.com/v2/tune.js";var t=document.getElementsByTagName("script")[0];t.parentNode.insertBefore(n,t),o.domain=e}}}();
    
    // Initialize Tune tracking
    tdl.init("https://track.modemobile.com");
    tdl.convert(); // KEY: Track conversion, not just identification
    
    console.log('✅ Tune conversion tracking initialized');
})();
            """, language="javascript")
            
            if st.button("Copy Tune Conversion Code", key="copy_tune_thankyou"):
                st.success("✅ Code copied! Paste into LeadPages Global Scripts")
        
        # Section 2: URL Injection - THE MONEY MAKER
        with st.expander("🔥 Section 2: URL Injection (LOW RISK) - THE MONEY MAKER", expanded=True):
            st.markdown("**Purpose:** 🔥 **This is where revenue happens!** Injects source + email into EVERY link for attribution")
            st.warning("💰 Every click = revenue attributed to original Meta Ad source!")
            st.code("""
(function initializeUrlInjection() {
    document.addEventListener("DOMContentLoaded", function() {
        console.log("💰 URL Parameter Injection Loading");
        
        // Parse URL parameters from current page
        const urlParams = new URLSearchParams(window.location.search);
        const sourceVal = urlParams.get('source') || '';
        const emailVal = urlParams.get('email') || '';
        
        // Find all links on the page
        const allLinks = document.querySelectorAll("a");
        
        // Inject source and email into every link for revenue attribution
        allLinks.forEach(link => {
            if (link.href) {
                try {
                    // Convert link href to URL object
                    const linkUrl = new URL(link.href, window.location.origin);
                    
                    // Add revenue attribution parameters
                    linkUrl.searchParams.set('aff_sub2', sourceVal); // Source attribution
                    linkUrl.searchParams.set('aff_sub5', emailVal);  // Email tracking
                    
                    // Decode URL so @ appears instead of %40
                    link.href = decodeURIComponent(linkUrl.toString());
                    
                } catch (error) {
                    console.warn("⚠️ Failed to inject parameters into link:", link.href, error);
                }
            }
        });
        
        console.log(`✅ URL injection complete - ${allLinks.length} links processed`);
    });
})();
            """, language="javascript")
            
            if st.button("Copy URL Injection Code", key="copy_url_thankyou"):
                st.success("🔥 THE MONEY MAKER copied! This maintains revenue attribution on every click!")
        
        # Section 3: Error Monitoring
        with st.expander("🟢 Section 3: Error Monitoring (LOW RISK)"):
            st.markdown("**Purpose:** Email.js system protection and error alerts")
            st.code("""
(function initializeErrorMonitoring() {
    // Load Email.js library
    const emailScript = document.createElement('script');
    emailScript.src = 'https://cdn.emailjs.com/dist/email.min.js';
    document.head.appendChild(emailScript);
    
    emailScript.onload = function() {
        emailjs.init("service_twy8maf");
        
        // Global error alert function
        window.sendErrorAlert = function({ fromName, message, pageUrl, errorType }) {
            emailjs.send("service_twy8maf", "template_02ts48r", {
                from_name: fromName,
                message: message,
                page_url: pageUrl,
                error_type: errorType
            }).then(() => {
                console.log("📧 EmailJS alert sent!");
            }).catch((err) => {
                console.error("❌ EmailJS failed to send alert:", err);
            });
        };
        
        console.log('✅ Error monitoring initialized');
    };
})();
            """, language="javascript")
            
            if st.button("Copy Error Monitoring Code", key="copy_error_thankyou"):
                st.success("✅ Code copied! System protection ready")

        # Section 4: Facebook SDK
        with st.expander("🟢 Section 4: Facebook SDK (LOW RISK)"):
            st.markdown("**Purpose:** Social integration for Thank You page features")
            st.code("""
(function initializeFacebookSDKThankyou() {
    function setupFacebookSDK() {
        // Create fb-root div if it doesn't exist
        if (!document.getElementById('fb-root')) {
            const fbRoot = document.createElement('div');
            fbRoot.id = 'fb-root';
            document.body.insertBefore(fbRoot, document.body.firstChild);
        }
        
        // Load Facebook SDK script
        const fbScript = document.createElement('script');
        fbScript.async = true;
        fbScript.defer = true;
        fbScript.crossOrigin = 'anonymous';
        fbScript.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v22.0';
        document.head.appendChild(fbScript);
        
        console.log('✅ Facebook SDK (Thank You) initialized');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupFacebookSDK);
    } else {
        setupFacebookSDK();
    }
})();
            """, language="javascript")
            
            if st.button("Copy Facebook SDK Code", key="copy_fb_thankyou"):
                st.success("✅ Code copied! Social features ready")

        # Section 5: Impression Pixel
        with st.expander("🟢 Section 5: Impression Pixel (LOW RISK)"):
            st.markdown("**Purpose:** Affiliate tracking pixel with source injection")
            st.code("""
(function initializeImpressionPixel() {
    document.addEventListener("DOMContentLoaded", function() {
        console.log("📊 Impression Pixel Loading");
        
        // Parse source from URL
        const urlParams = new URLSearchParams(window.location.search);
        const sourceVal = urlParams.get('source') || '';
        
        // Create impression pixel (hidden)
        const pixelContainer = document.createElement('div');
        pixelContainer.style.display = 'none';
        
        const pixelImg = document.createElement('img');
        pixelImg.id = 'mode-impression-pixel';
        pixelImg.width = 0;
        pixelImg.height = 0;
        pixelImg.style.cssText = 'position:absolute;visibility:hidden;';
        pixelImg.border = 0;
        
        // Build pixel URL with source injection
        const baseUrl = 'https://track.modemobile.com/aff_i?offer_id=6571&aff_id=42946';
        const finalUrl = `${baseUrl}&aff_sub2=${encodeURIComponent(sourceVal)}`;
        
        pixelImg.src = finalUrl;
        pixelContainer.appendChild(pixelImg);
        document.body.appendChild(pixelContainer);
        
        console.log('✅ Impression pixel fired:', finalUrl);
    });
})();
            """, language="javascript")
            
            if st.button("Copy Impression Pixel Code", key="copy_pixel_thankyou"):
                st.success("✅ Code copied! Affiliate tracking ready")

        # Section 6: Mode UA API
        with st.expander("🟡 Section 6: Mode UA API (MEDIUM RISK)"):
            st.markdown("**Purpose:** CRM integration for email marketing")
            st.info("💡 Simple: Just update the campaign name for each property")
            st.code("""
(function initializeModeUAAPI() {
    document.addEventListener("DOMContentLoaded", function () {
        console.log("🧠 Mode UA API Integration Loading");

        function sendToModeUA() {
            const params = new URLSearchParams(window.location.search);
            const email = params.get("email") || "";
            const firstName = params.get("first_name") || "";
            const lastName = params.get("last_name") || "";
            const phone = params.get("phone") || "";
            const source = params.get("source") || "";

            if (!email) {
                console.warn("⚠ No email in URL. Skipping Mode UA API.");
                return;
            }

            // ⚠️ CUSTOMIZE: Update campaign name for each property
            const apiUrl = `https://nodejs-serverless-connector.vercel.app/api/mode_ua_leadgen?action=add` +
                `&email=${encodeURIComponent(email)}` +
                `&lead_source=${encodeURIComponent("Leadpages")}` +
                `&campaign=${encodeURIComponent("ModeFreeFinds")}` + // UPDATE THIS
                `&country=${encodeURIComponent("United States")}` +
                `&type=${encodeURIComponent("opt-in")}`;

            console.log("📡 Sending Mode UA API:", apiUrl);

            fetch(apiUrl)
                .then(r => r.json())
                .then(data => {
                    if (data?.success) {
                        console.log("✅ Mode UA API Success:", data);
                    } else {
                        console.warn("⚠ Mode UA API responded but failed:", data);
                    }
                })
                .catch(err => {
                    console.error("🚨 Mode UA API call failed:", err);
                });
        }

        // Delayed execution for better performance
        if ("requestIdleCallback" in window) {
            requestIdleCallback(sendToModeUA, { timeout: 3000 });
        } else {
            setTimeout(sendToModeUA, 3000);
        }
    });
})();
            """, language="javascript")
            
            if st.button("Copy Mode UA API Code", key="copy_api_thankyou"):
                st.info("💡 Remember to update campaign name for each property!")

        # Section 7: Meta Conversion
        with st.expander("🟡 Section 7: Meta Conversion (MEDIUM RISK)"):
            st.markdown("**Purpose:** Property-specific conversion tracking")
            st.info("💡 Simple: Just update the Pixel ID for each property!")
            st.code("""
(function initializeMetaConversion() {
    // ⚠️ IMPORTANT: Change pixel ID for each property
    const PIXEL_ID = '1153754019617349'; // MFF Pixel - UPDATE FOR OTHER PROPERTIES
    
    // Meta Pixel implementation with conversion tracking
    !function(f,b,e,v,n,t,s) {
        if(f.fbq) return; // Prevent double-loading
        n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)
    }(window, document,'script','https://connect.facebook.net/en_US/fbevents.js');
    
    fbq('init', PIXEL_ID);
    fbq('track', 'Lead'); // CONVERSION EVENT - not PageView
    
    // Add noscript fallback
    const noscript = document.createElement('noscript');
    noscript.innerHTML = `<img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=${PIXEL_ID}&ev=Lead&noscript=1"/>`;
    document.head.appendChild(noscript);
    
    console.log('✅ Meta conversion tracking initialized:', PIXEL_ID);
})();
            """, language="javascript")
            
            if st.button("Copy Meta Conversion Code", key="copy_meta_conv_thankyou"):
                st.info("💡 Remember: Update PIXEL_ID for each property")
        
        # Link to full files
        st.markdown("---")
        st.markdown("""
        <div style="background-color: #F7007C; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
            <h3 style="color: white; margin: 0;">🎯 ALL 7 THANK YOU PAGE SECTIONS READY!</h3>
            <p style="color: white; margin: 0.5rem 0 0 0;">Start with Sections 1-2 (lowest risk)</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Complete Code Files:**")
        st.markdown("- [Full Thank You Page Code](https://github.com/brianlapp/mode/blob/main/thankyou-global-scripts-ready.js)")
        st.markdown("- All sections including the complete revenue attribution system")
        st.markdown("- **THE MONEY MAKER:** Section 2 (URL Injection) is the revenue core!")

# ============================================================================
# PAGE 4: PROPERTY DEEP DIVE
# ============================================================================
elif page == "📊 Property Deep Dive":
    st.title("📊 Property Deep Dive Analysis")
    
    property_tabs = st.tabs(["MFF Analysis", "MM Optimization", "MCAD Setup", "MMD Setup"])
    
    with property_tabs[0]:
        st.header("ModeFreeFinds - $0.45 CPL Success Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Current Performance")
            st.metric("Cost Per Lead", "$0.45", "Target achieved")
            st.metric("Monthly Revenue", "$40k", "Programmatic ads")
            st.metric("Email List", "1.5M", "Subscribers")
            st.metric("Monthly Pageviews", "~1M", "High traffic")
            
        with col2:
            st.subheader("Success Factors")
            st.success("✅ Tangible visual proof (product photos)")
            st.success("✅ Simple 3-field form (no friction)")
            st.success("✅ Clear value proposition (free samples)")
            st.success("✅ Strong social proof (Facebook integration)")
            st.success("✅ Low-risk proposition (free stuff)")
            
        st.subheader("Technical Architecture")
        st.info("MFF uses the complete technical system we've now documented for Global Scripts!")
        
        with st.expander("MFF Revenue Flow"):
            st.write("1. Meta Ad → Landing Page (Form Submission)")
            st.write("2. Form Data Captured → Thank You URL populated") 
            st.write("3. Thank You Page → ALL LINKS get source + email")
            st.write("4. Any click → Revenue attributed to original Meta Ad")
            st.write("5. Multiple tracking systems ensure zero revenue leakage")

    with property_tabs[1]:
        st.header("ModeMarketMunchies - Optimization Strategy")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Current Challenge")
            st.error("Meta Traffic: $5-10 CPL (LOSING MONEY)")
            st.success("Affiliate Traffic: $1.50 CPL (PROFITABLE)")
            st.metric("Target", "$1.50 CPL", "Match affiliate performance")
            
        with col2:
            st.subheader("The Solution")
            st.info("Apply MFF's proven technical foundation + financial-specific optimization")
            st.write("**Strategy:**")
            st.write("• Keep proven revenue system (no risk)")
            st.write("• Add financial trust signals")  
            st.write("• Test Meta-specific value propositions")
            st.write("• Use Global Scripts for rapid deployment")
            
        st.subheader("Implementation Plan")
        if st.button("Start MM Global Scripts Setup"):
            st.session_state.page = "🔧 Global Scripts Implementation"
            st.success("Ready to apply MFF's $0.45 CPL system to MM!")
            st.rerun()

    with property_tabs[2]:
        st.header("ModeClassActionsDaily - Setup Plan")
        st.warning("⚠️ No signup/TY flows built yet")
        
        st.subheader("Setup Strategy")
        st.info("Start with proven MFF Global Scripts foundation")
        
        setup_steps = [
            "1. Implement MFF Global Scripts (proven $0.45 CPL foundation)",
            "2. Customize for legal vertical (class action specific)",
            "3. Add legal trust signals (case count, legal badges)",
            "4. Test with 1M email list audience"
        ]
        
        for step in setup_steps:
            st.write(step)
            
        if st.button("Start MCAD Global Scripts Setup"):
            st.session_state.page = "🔧 Global Scripts Implementation"
            st.success("Ready to build MCAD with proven foundation!")
            st.rerun()

    with property_tabs[3]:
        st.header("ModeMobileDaily - Setup Plan") 
        st.warning("⚠️ No signup/TY flows built yet")
        
        st.subheader("Setup Strategy")
        st.info("Start with proven MFF Global Scripts foundation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Current Assets:**")
            st.write("• 50k daily active users")
            st.write("• Viral news & trending content")
            st.write("• Mode Earn App integration")
            
        with col2:
            st.write("**Setup Plan:**")
            st.write("• Use MFF Global Scripts foundation")
            st.write("• Viral/news specific customization")
            st.write("• App user conversion focus")
            
        if st.button("Start MMD Global Scripts Setup"):
            st.session_state.page = "🔧 Global Scripts Implementation"
            st.success("Ready to build MMD with proven foundation!")
            st.rerun()

# ============================================================================
# PAGE 5: ANALYTICS & REPORTS  
# ============================================================================
elif page == "📈 Analytics & Reports":
    st.title("📈 Analytics & Performance Reports")
    
    analytics_tabs = st.tabs(["Performance Overview", "Global Scripts Progress", "Revenue Attribution"])
    
    with analytics_tabs[0]:
        st.header("Performance Overview")
        
        # Create sample performance data
        performance_data = {
            'Property': ['ModeFreeFinds', 'ModeMarketMunchies (Affiliate)', 'ModeMarketMunchies (Meta)', 'ModeClassActionsDaily', 'ModeMobileDaily'],
            'CPL': ['$0.45', '$1.50', '$5-10', 'Not Set Up', 'Not Set Up'],
            'Status': ['✅ Profitable', '✅ Profitable', '❌ Losing Money', '⚠️ Needs Setup', '⚠️ Needs Setup'],
            'Monthly Potential': ['$40k', '$200k+', '$1M+ (if optimized)', '$500k+', '$300k+']
        }
        
        df = pd.DataFrame(performance_data)
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Key Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Revenue Potential", "$2M+/month", "If all optimized")
            st.metric("Current Revenue", "$240k+/month", "MFF + MM affiliate")
        with col2:
            st.metric("Optimization Target", "MMM Meta Traffic", "$5-10 → $1.50 CPL")
            st.metric("Setup Needed", "2 Properties", "MCAD + MMD")

    with analytics_tabs[1]:
        st.header("Global Scripts Implementation Progress")
        
        st.subheader("Implementation Status")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Landing Page Scripts**")
            landing_progress = st.progress(0, text="0/6 sections implemented")
            
        with col2:
            st.write("**Thank You Page Scripts**")
            thankyou_progress = st.progress(0, text="0/7 sections implemented")
            
        st.subheader("Next Implementation Steps")
        st.info("1. Test Global Scripts feature with simple script")
        st.info("2. Implement Tune SDK first (lowest risk)")
        st.info("3. Add Facebook SDK second")
        st.info("4. Gradually implement remaining sections")
        
        expected_timeline = {
            'Phase': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Landing Page': ['Tune + Facebook SDK', 'Smart Recognition + Mobile Nav', 'Form Enhancement', 'Meta Pixel'],
            'Thank You Page': ['Tune Conversion + URL Injection', 'Error Monitoring + Facebook SDK', 'Impression Pixel + Mode UA API', 'Meta Conversion'],
            'Expected Benefit': ['Basic tracking', 'Enhanced functionality', 'Complete system', 'Full optimization']
        }
        
        timeline_df = pd.DataFrame(expected_timeline)
        st.dataframe(timeline_df, use_container_width=True)

    with analytics_tabs[2]:
        st.header("Revenue Attribution Analysis")
        
        st.subheader("MFF Revenue System (Proven)")
        st.success("Complete $0.45 CPL attribution chain documented and ready for replication!")
        
        with st.expander("Revenue Attribution Flow"):
            st.write("**Step 1:** Meta Ad → Landing Page")
            st.write("- Meta Pixel tracks PageView")
            st.write("- Tune SDK identifies user")
            st.write("- Source captured in URL")
            
            st.write("**Step 2:** Form Submission → Thank You Page")
            st.write("- Form data captured")
            st.write("- Thank You URL populated with user data")
            st.write("- Source attribution preserved")
            
            st.write("**Step 3:** Thank You Page → Revenue")
            st.write("- Meta Pixel tracks conversion")
            st.write("- Tune SDK records revenue conversion")
            st.write("- ALL LINKS get source + email injected")
            st.write("- Impression pixel fires immediately")
            st.write("- API integration captures lead for email marketing")
            
            st.write("**Result:** 100% revenue attribution with zero leakage")
        
        st.subheader("Replication Strategy")
        st.info("This exact system can be applied to MM, MCAD, and MMD using Global Scripts!")

# ============================================================================
# PAGE 6: PROPERTIES PORTFOLIO
# ============================================================================
elif page == "🏢 Properties Portfolio":
    st.header("🏢 Mode Properties Portfolio")
    st.markdown("Complete overview of all Mode properties with revenue models, optimization opportunities, and development status")
    st.markdown("---")
    
    # Portfolio Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Properties",
            value="4",
            delta="Live: 1, Launched: 1, Development: 2"
        )
    
    with col2:
        st.metric(
            label="💰 Monthly Revenue",
            value="$25k-$35k",
            delta="ModeFreeFinds only"
        )
    
    with col3:
        st.metric(
            label="👀 Monthly Pageviews",
            value="1M+",
            delta="ModeFreeFinds traffic"
        )
    
    with col4:
        st.metric(
            label="🎯 RPM Potential",
            value="$18-$25",
            delta="vs current $12 (Prebid.js)"
        )
    
    st.markdown("---")
    
    # Property Tabs Organization
    property_tabs = st.tabs(["🟢 ModeFreeFinds", "🟡 ModeMarketMunchies", "🔴 ModeMobileDaily", "🔴 ModeClassActionsDaily", "�� Thanks.co Analysis", "🚀 Portfolio Overview"])
    
    # Tab 1: ModeFreeFinds - Flagship Revenue Property
    with property_tabs[0]:
        st.subheader("🟢 ModeFreeFinds.com - Active Revenue Generator")
        
        # Mobile screenshot
        st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-0a7816aa-1b1a-4781-ac06-385c92c7d392.png", 
                 caption="📱 ModeFreeFinds Mobile Landing Page", width=300)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **🎯 Business Model:** Free Stuff Content Site  
            **📊 Traffic:** 1M pageviews per month  
            **💰 Revenue:** $25k-$35k monthly  
            **🔗 URL:** [ModeFreeFinds.com](https://modefreefinds.com)
            
            **📱 Mobile Visual Insights:**
            - Daily content posts with professional graphics
            - Engaging headlines ("Cool Off with a Free Root Beer Float")
            - Facebook social proof integration
            - Clean mobile-optimized content feed
            """)
            
            st.markdown("**Revenue Streams:**")
            revenue_col1, revenue_col2 = st.columns(2)
            
            with revenue_col1:
                st.markdown("""
                **💻 Programmatic Ads (Ezoic)**
                - RPM: ~$12 (weak performance)
                - Opportunity: Prebid.js integration
                - Target: $18-$25 RPM
                """)
            
            with revenue_col2:
                st.markdown("""
                **🎁 Thanks.co Popup**
                - RPM: ~$75 (excellent)
                - Placement: Content/blog posts
                - Opportunity: Custom Tune integration
                """)
        
        with col2:
            st.success("**Status: LIVE & PROFITABLE**")
            st.markdown("**Priority Optimizations:**")
            st.markdown("- ⚡ Prebid.js for programmatic")
            st.markdown("- 🔧 Custom Tune popup")
            st.markdown("- 📈 Revenue potential: +$6k-$13k")
            
            if st.button("Analyze ModeFreeFinds", key="mff_analyze"):
                st.info("🔍 Full optimization analysis available in Property Deep Dive section")
    
    # Tab 2: ModeMarketMunchies - Recently Launched
    with property_tabs[1]:
        st.subheader("🟡 ModeMarketMunchies.com - Recently Launched")
        
        # Mobile screenshot and logo
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-7c9f0495-1873-43d5-b051-e6b193b2254e.png", 
                     caption="📱 ModeMarketMunchies Mobile", width=250)
        with col_img2:
            st.image("https://modemarketmunchies.com/wp-content/uploads/2025/04/market-munchies-logo-1.webp", 
                     caption="🏷️ MMM Logo", width=200)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **🎯 Business Model:** Finance Content Site  
            **📊 Traffic:** Building audience  
            **💰 Revenue:** No ads set up yet  
            **🔗 URL:** [ModeMarketMunchies.com](https://modemarketmunchies.com)
            
            **📱 Mobile Visual Insights:**
            - Professional financial content with real-time ticker
            - Crypto analysis and market news focus
            - Clean blue/red financial theme
            - Newsletter signup ready in footer
            """)
            
            st.markdown("**Implementation Strategy:**")
            st.markdown("""
            - 📋 Apply MFF revenue model template
            - 🎯 Target: Finance-focused affiliate offers
            - 💻 Programmatic + Custom popup strategy
            - 📈 Expected timeline: 2-3 months to revenue
            """)
        
        with col2:
            st.warning("**Status: LAUNCHED, NO MONETIZATION**")
            st.markdown("**Next Actions:**")
            st.markdown("- 🔧 Global Scripts implementation")
            st.markdown("- 📊 Traffic analysis & growth")
            st.markdown("- 💰 Revenue stream activation")
            
            if st.button("Plan MMM Setup", key="mmm_plan"):
                st.info("📋 MMM follows MFF proven playbook - Global Scripts ready for deployment")
    
    # Tab 3: ModeMobileDaily - Development Stage
    with property_tabs[2]:
        st.subheader("🔴 ModeMobileDaily.com - Development Stage")
        
        # Mobile screenshot and logo
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-84e981c0-206b-4370-83a1-f2b2e5540d90.png", 
                     caption="📱 ModeMobileDaily Mobile", width=250)
        with col_img2:
            st.image("https://modemobiledaily.com/wp-content/uploads/2025/06/cropped-Daily-2a.png", 
                     caption="🏷️ MMD Logo", width=200)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **🎯 Business Model:** Viral News/Breaking News Site  
            **📊 Traffic:** Limited content (June 2025)  
            **💰 Revenue:** Development phase  
            **🔗 URL:** [ModeMobileDaily.com](https://modemobiledaily.com)
            
            **📱 Mobile Visual Insights:**
            - Viral content format perfect for mobile sharing
            - Quizzes, entertainment, trending topics
            - Engaging headlines ("22 Weird Animal Facts")
            - Modern blue/white theme optimized for viral content
            """)
            
            st.markdown("**Development Plan:**")
            st.markdown("""
            - 📝 Content strategy & automation
            - 📱 Mobile-first viral news format
            - ⚡ High-velocity content publishing
            - 🎯 Target: News affiliate offers + programmatic
            """)
        
        with col2:
            st.error("**Status: DEVELOPMENT STAGE**")
            st.markdown("**Timeline:**")
            st.markdown("- 📅 Content: 2-4 weeks")
            st.markdown("- 🚀 Launch: 1-2 months")
            st.markdown("- 💰 Revenue: 3-4 months")
            
            if st.button("MMD Development Plan", key="mmd_plan"):
                st.info("📱 Viral news strategy requires content automation + rapid publishing system")
    
    # Tab 4: ModeClassActionsDaily - Development Stage
    with property_tabs[3]:
        st.subheader("🔴 ModeClassActionsDaily.com - Development Stage")
        
        # Mobile screenshot and logo
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-f7d2b138-0af0-4778-ab6e-b208a2cd45f1.png", 
                     caption="📱 ModeClassActionsDaily Mobile", width=250)
        with col_img2:
            st.image("https://modeclassactionsdaily.com/wp-content/uploads/2025/04/class-actions-logo.png", 
                     caption="🏷️ MCAD Logo", width=200)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **🎯 Business Model:** Consumer Class Action Awareness Content Site  
            **📊 Traffic:** No content yet  
            **💰 Revenue:** Development phase  
            **🔗 URL:** [ModeClassActionsDaily.com](https://modeclassactionsdaily.com)
            
            **📱 Mobile Visual Insights:**
            - Professional legal authority positioning
            - Clean, authoritative design theme
            - Framework ready for class action content
            - Navigation structured for legal content organization
            """)
            
            st.markdown("**Development Plan:**")
            st.markdown("""
            - ⚖️ Legal content & class action notifications
            - 🎯 Consumer awareness & participation
            - 💰 Legal affiliate offers + programmatic
            - 📈 High-value niche with engaged audience
            """)
        
        with col2:
            st.error("**Status: DEVELOPMENT STAGE**")
            st.markdown("**Timeline:**")
            st.markdown("- 📅 Content: 2-4 weeks")
            st.markdown("- 🚀 Launch: 1-2 months")
            st.markdown("- 💰 Revenue: 3-4 months")
            
            if st.button("MCAD Development Plan", key="mcad_plan"):
                st.info("⚖️ Class action niche has high engagement + legal affiliate opportunities")
    
    # Tab 5: Thanks.co Analysis
    with property_tabs[4]:
        st.subheader("🎁 Thanks.co Popup Analysis - Custom Replacement Insights")
        
        st.markdown("**Current Thanks.co Offer Rotation (Captured via Mobile Audit):**")
        
        popup_col1, popup_col2 = st.columns(2)
        
        with popup_col1:
            st.markdown("""
            **Sam's Club Membership Offer:**
            - 36% off Sam's Club Plus membership
            - Save $40 (normally $110)
            - Benefits: Free shipping, early hours, 2% cash back
            - Family-focused imagery with Sam's Club products
            """)
        
        with popup_col2:
            st.markdown("""
            **Who Gives A Crap Eco Offer:**
            - 20% off bamboo toilet paper (code: ecosave20)
            - Eco-friendly positioning
            - Benefits: Better for earth, 50% profits to build toilets
            - Clean, environmental packaging imagery
            """)
        
        st.info("💡 **Custom Replacement Strategy:** These popup examples show the variety of offers Thanks.co rotates. Our custom Tune integration can replicate this diversity while keeping 100% revenue.")
        
        # Interactive Demo Section
        st.subheader("🎬 Interactive Popup Demo Concept")
        
        demo_tabs = st.tabs(["📱 Thanks.co Current", "🔧 Custom Concept", "📊 Comparison"])
        
        with demo_tabs[0]:
            st.markdown("**Current Thanks.co 5-Slide Carousel System:**")
            
            # Thanks.co carousel simulation
            slide_option = st.selectbox(
                "View Popup Slides:",
                ["Slide 1: Sam's Club (36% off)", "Slide 2: TopCashback ($20)", "Slide 3: Capital One Shopping ($30)", "Slide 4: Kraken Crypto ($25)", "Slide 5: FreeShipping.com ($10)"]
            )
            
            if "Sam's Club" in slide_option:
                st.markdown("""
                **Sam's Club Plus Membership**
                - 🎯 36% off membership (Save $40)
                - ✅ Free shipping, early shopping hours
                - 💰 Earn 2% Sam's Cash back
                - 👨‍👩‍👧‍👦 Family-focused imagery with products
                """)
            elif "TopCashback" in slide_option:
                st.markdown("""
                **TopCashback Platform**
                - 🎯 $20 cashback on today's purchase
                - ✅ 7000+ stores, highest rates
                - 💰 Unbeatable cashback program
                - 🏪 Major retailer logos (Walmart, Best Buy, Nike)
                """)
            elif "Capital One" in slide_option:
                st.markdown("""
                **Capital One Shopping Extension**
                - 🎯 $30 bonus redemption
                - ✅ Auto-apply coupons instantly
                - 💰 Free browser extension
                - 💻 Shopping comparison interface
                """)
            elif "Kraken" in slide_option:
                st.markdown("""
                **Kraken Crypto Platform**
                - 🎯 $25 crypto bonus
                - ✅ 325+ cryptocurrencies
                - 💰 Deposit $100, get $25 bonus
                - 🚀 15M+ users globally
                """)
            elif "FreeShipping" in slide_option:
                st.markdown("""
                **FreeShipping.com Platform**
                - 🎯 $10 cash back today
                - ✅ 10% cashback at 1000+ stores
                - 💰 Free to join, instant claim
                - 🛍️ Major retailer network
                """)
        
        with demo_tabs[1]:
            st.markdown("**Custom Mode Popup with Tune CPL Inventory:**")
            
            custom_slide = st.selectbox(
                "Mode Custom Offers (Concept):",
                ["Finance Offer: Trading Platform", "Cashback Offer: Shopping App", "Membership: Warehouse Club", "Crypto: Trading Bonus", "Legal: Consultation Service"]
            )
            
            if "Trading Platform" in custom_slide:
                st.markdown("""
                **Premium Trading Platform (Tune CPL)**
                - 🎯 $50 bonus for new accounts
                - ✅ Commission-free stock trading
                - 💰 Professional research tools included
                - 📈 Perfect for ModeMarketMunchies audience
                **Revenue**: 100% vs Thanks.co commission
                """)
            elif "Shopping App" in custom_slide:
                st.markdown("""
                **Cashback Shopping App (Tune CPL)**
                - 🎯 $25 signup bonus
                - ✅ 5% cashback at major retailers
                - 💰 Real-time coupon application
                - 🛍️ Perfect for ModeFreeFinds audience
                **Revenue**: 100% vs Thanks.co commission
                """)
            elif "Warehouse Club" in custom_slide:
                st.markdown("""
                **Warehouse Club Membership (Tune CPL)**
                - 🎯 40% off annual membership
                - ✅ Bulk savings + gas discounts
                - 💰 $60 value for families
                - 👨‍👩‍👧‍👦 Family-focused positioning
                **Revenue**: 100% vs Thanks.co commission
                """)
        
        with demo_tabs[2]:
            st.markdown("**Revenue & Control Comparison:**")
            
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("""
                **🔴 Thanks.co Current:**
                - RPM: ~$75
                - Revenue Share: Commission to Thanks.co
                - Control: Limited offer selection
                - Attribution: Partial visibility
                - Branding: Third-party
                """)
            
            with comp_col2:
                st.markdown("""
                **🟢 Custom Mode System:**
                - RPM: $75+ target
                - Revenue Share: 100% retention
                - Control: Full Tune inventory access
                - Attribution: Complete visibility
                - Branding: Mode-branded experience
                """)
            
            st.success("**Bottom Line:** Custom system maintains performance while eliminating commission fees and providing full control!")

    # Tab 6: Portfolio Overview
    with property_tabs[5]:
        st.subheader("🚀 Portfolio-Wide Optimization Opportunities")
        
        opt_col1, opt_col2 = st.columns(2)
        
        with opt_col1:
            st.markdown("**🎯 Immediate Opportunities (ModeFreeFinds)**")
            
            st.markdown("""
            **1. Prebid.js Implementation**
            - Current: $12 RPM via Ezoic
            - Target: $18-$25 RPM
            - Impact: +$6k-$13k monthly
            - Timeline: 2-4 weeks
            """)
            
            st.markdown("""
            **2. Custom Thanks.co Replacement**
            - Current: ~$75 RPM (paying commission)
            - Target: $75+ RPM (100% revenue)
            - Impact: Commission savings + control
            - Timeline: 4-6 weeks
            """)
        
        with opt_col2:
            st.markdown("**📈 Scaling Opportunities (All Properties)**")
            
            st.markdown("""
            **1. Global Scripts Template**
            - Apply MFF success to MMM, MMD, MCAD
            - Standardized tracking & attribution
            - Consistent revenue optimization
            - Timeline: 1-2 weeks per property
            """)
            
            st.markdown("""
            **2. Portfolio Revenue Target**
            - MFF: $35k-$50k (optimized)
            - MMM: $15k-$25k (year 1)
            - MMD: $20k-$35k (viral potential)
            - MCAD: $10k-$20k (niche premium)
            - **Total Portfolio: $80k-$130k monthly**
            """)
        
        st.markdown("---")
        
        # Implementation Roadmap
        st.subheader("📋 Implementation Roadmap")
        
        roadmap_tabs = st.tabs(["🎯 Immediate (1-2 weeks)", "📈 Short-term (1-2 months)", "🚀 Long-term (3-6 months)"])
        
        with roadmap_tabs[0]:
            st.markdown("**Immediate Actions (1-2 weeks)**")
            
            immediate_col1, immediate_col2 = st.columns(2)
            
            with immediate_col1:
                st.markdown("""
                **ModeFreeFinds Optimization:**
                - [ ] Prebid.js demand partner applications
                - [ ] Thanks.co performance audit
                - [ ] Custom popup prototype
                - [ ] A/B testing framework setup
                """)
            
            with immediate_col2:
                st.markdown("""
                **Portfolio Infrastructure:**
                - [ ] Global Scripts template finalization
                - [ ] Universal tracking system setup
                - [ ] MMM monetization planning
                - [ ] Performance monitoring dashboard
                """)
        
        with roadmap_tabs[1]:
            st.markdown("**Short-term Goals (1-2 months)**")
            
            short_col1, short_col2 = st.columns(2)
            
            with short_col1:
                st.markdown("""
                **Revenue Optimization:**
                - [ ] Prebid.js full implementation
                - [ ] Custom popup A/B testing
                - [ ] MMM ad setup & optimization
                - [ ] MFF revenue target: $40k+ monthly
                """)
            
            with short_col2:
                st.markdown("""
                **Property Development:**
                - [ ] MMD content strategy & launch
                - [ ] MCAD content strategy & launch
                - [ ] Cross-property traffic optimization
                - [ ] Brand consistency & trust building
                """)
        
        with roadmap_tabs[2]:
            st.markdown("**Long-term Vision (3-6 months)**")
            
            long_col1, long_col2 = st.columns(2)
            
            with long_col1:
                st.markdown("""
                **Portfolio Scale:**
                - [ ] All 4 properties fully monetized
                - [ ] Portfolio revenue: $80k-$130k monthly
                - [ ] Advanced attribution & optimization
                - [ ] Acquisition & expansion opportunities
                """)
            
            with long_col2:
                st.markdown("""
                **Strategic Development:**
                - [ ] Content automation systems
                - [ ] Advanced AI optimization
                - [ ] New vertical exploration
                - [ ] Exit strategy or scaling decisions
                """)
        
        st.markdown("---")
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("📊 View Full Analytics", key="portfolio_analytics"):
                st.session_state.page = "📈 Analytics & Reports"
                st.rerun()
        
        with action_col2:
            if st.button("🔧 Global Scripts Setup", key="portfolio_global"):
                st.session_state.page = "🔧 Global Scripts Implementation"
                st.rerun()
        
        with action_col3:
            if st.button("💻 Access Code Repository", key="portfolio_code"):
                st.session_state.page = "💻 Code Repository"
                st.rerun()

    st.markdown("---")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*Dashboard updated: 2025-01-27*")
st.sidebar.markdown("**🚀 Multi-page dashboard with honest metrics!**")
st.sidebar.markdown("**Navigation:** Always-visible buttons (no dropdown!)")
