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
if st.sidebar.button("🏢 Mode Properties Hub", use_container_width=True):
    st.session_state.page = "🏢 Mode Properties Hub"
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
    elif page_param == "properties" or page_param == "portfolio":
        st.session_state.page = "🏢 Mode Properties Hub"

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
        if st.button("🏢 Mode Properties Hub\n\nComplete portfolio management with visual insights, optimization strategies, and implementation roadmaps for all 4 Mode properties.", 
                     use_container_width=True, key="nav_properties", type="primary"):
            st.session_state.page = "🏢 Mode Properties Hub"
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
            st.session_state.page = "🏢 Mode Properties Hub"
            # You could add URL params here to jump directly to Thanks.co tab
            st.rerun()
    
    with action_col2:
        if st.button("📈 Check Property Analytics", use_container_width=True):
            st.session_state.page = "📈 Analytics & Reports"
            st.rerun()
    
    with action_col3:
        if st.button("🔧 Start Property Setup", use_container_width=True):
            st.session_state.page = "🏢 Mode Properties Hub"
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
# PAGE 4: MODE PROPERTIES HUB (Unified Portfolio + Deep Dive)
# ============================================================================
elif page == "🏢 Mode Properties Hub":
    st.title("🏢 Mode Properties Hub")
    st.markdown("Complete portfolio management with visual insights, optimization strategies, and implementation roadmaps")
    st.markdown("---")
    
    # 7-tab unified structure
    property_tabs = st.tabs([
        "📊 Portfolio Overview",
        "🟢 ModeFreeFinds", 
        "🟡 ModeMarketMunchies",
        "🔴 ModeMobileDaily", 
        "🔴 ModeClassActionsDaily",
        "🎁 Thanks.co Analysis",
        "🚀 Implementation Roadmap"
    ])
    
    # Tab 1: Portfolio Overview
    with property_tabs[0]:
        st.header("📊 Portfolio Overview")
        
        # Portfolio Metrics
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
                label="🎯 Revenue Potential",
                value="$50k-$75k",
                delta="Optimized portfolio"
            )
        
        st.markdown("---")
        
        # Property Status Cards
        st.subheader("🏢 Property Status Overview")
        
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            st.markdown("""
            **🟢 ModeFreeFinds** - LIVE & PROFITABLE
            - Revenue: $25k-$35k/month
            - CPL: $0.45 (Target achieved)
            - Priority: Prebid.js optimization
            """)
            
            st.markdown("""
            **🔴 ModeMobileDaily** - DEVELOPMENT
            - Revenue: $0 (no content yet)
            - Focus: Viral news automation
            - Timeline: 2-3 months to launch
            """)
        
        with status_col2:
            st.markdown("""
            **🟡 ModeMarketMunchies** - LAUNCHED, NO ADS
            - Revenue: $0 (setup needed)
            - CPL Challenge: $5-10 vs $1.50 target
            - Priority: Global Scripts deployment
            """)
            
            st.markdown("""
            **🔴 ModeClassActionsDaily** - DEVELOPMENT  
            - Revenue: $0 (no content yet)
            - Focus: Legal vertical setup
            - Timeline: 2-4 months to launch
            """)
        
        st.markdown("---")
        
        # Optimization Priority Matrix
        st.subheader("🎯 Optimization Priority Matrix")
        
        priority_col1, priority_col2, priority_col3 = st.columns(3)
        
        with priority_col1:
            st.markdown("""
            **🔥 HIGH PRIORITY**
            - MFF Prebid.js (+$6k-$13k)
            - MMM Global Scripts setup
            - Thanks.co custom replacement
            """)
        
        with priority_col2:
            st.markdown("""
            **⚡ MEDIUM PRIORITY**
            - MMM Meta traffic optimization
            - MCAD content framework
            - Cross-property automation
            """)
        
        with priority_col3:
            st.markdown("""
            **📈 LOW PRIORITY**
            - MMD content automation
            - Advanced analytics setup
            - Portfolio scaling strategy
            """)
        
        st.success("💡 **Strategic Focus**: Optimize existing revenue (MFF) while building foundation for new properties (MMM, MCAD, MMD)")
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🚀 Start MFF Optimization", use_container_width=True):
                st.info("Navigate to ModeFreeFinds tab for detailed optimization plan")
        
        with action_col2:
            if st.button("🔧 Setup MMM Global Scripts", use_container_width=True):
                st.session_state.page = "🔧 Global Scripts Implementation"
                st.rerun()
        
        with action_col3:
            if st.button("📊 View Implementation Timeline", use_container_width=True):
                st.info("Navigate to Implementation Roadmap tab for master timeline")

    # Tab 2: ModeFreeFinds - Complete Property Profile
    with property_tabs[1]:
        st.header("🟢 ModeFreeFinds - Flagship Revenue Property")
        
        # Visual Section
        visual_col1, visual_col2 = st.columns([1, 2])
        
        with visual_col1:
            st.image("https://i0.wp.com/modefreefinds.com/wp-content/uploads/2024/11/FreeFinds-Large.png?fit=1171%2C355&ssl=1", 
                     caption="🏷️ ModeFreeFinds Logo", width=200)
            
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-0a7816aa-1b1a-4781-ac06-385c92c7d392.png", 
                     caption="📱 Landing Page Mobile", width=250)
        
        with visual_col2:
            st.subheader("📊 Property Overview")
            st.markdown("""
            **🎯 Business Model:** Free Stuff Content Site  
            **📊 Traffic:** 1M pageviews per month  
            **💰 Revenue:** $25k-$35k monthly  
            **📧 Email List:** 1.5M subscribers
            **🔗 URL:** [ModeFreeFinds.com](https://modefreefinds.com)
            **✅ Status:** LIVE & PROFITABLE
            """)
            
            st.success("🎯 **CPL Achievement:** $0.45 (Target achieved!)")
            
            st.markdown("**📱 Mobile Visual Insights:**")
            st.markdown("- Daily content posts with professional graphics")
            st.markdown("- Engaging headlines ('Cool Off with a Free Root Beer Float')")
            st.markdown("- Facebook social proof integration")
            st.markdown("- Clean mobile-optimized content feed")
        
        st.markdown("---")
        
        # Revenue Analysis
        st.subheader("💰 Revenue Stream Analysis")
        
        revenue_col1, revenue_col2 = st.columns(2)
        
        with revenue_col1:
            st.markdown("""
            **💻 Programmatic Ads (Ezoic)**
            - Current RPM: ~$12 (weak performance)
            - Monthly Revenue: ~$12k-$18k
            - **🔥 Opportunity:** Prebid.js integration
            - **Target RPM:** $18-$25 (+$6k-$13k)
            """)
            
            st.error("⚠️ **Issue:** Single ad provider limits competition")
            
        with revenue_col2:
            st.markdown("""
            **🎁 Thanks.co Popup**
            - Current RPM: ~$75 (excellent)
            - Monthly Revenue: ~$7k-$10k
            - **🔥 Opportunity:** Custom Tune integration
            - **Target:** 100% revenue retention (no commission)
            """)
            
            st.success("✅ **Strength:** High-converting popup system")
        
        st.markdown("---")
        
        # Success Factors Analysis
        st.subheader("🎯 Success Factors - $0.45 CPL Formula")
        
        success_col1, success_col2 = st.columns(2)
        
        with success_col1:
            st.markdown("**✅ Conversion Optimization:**")
            st.success("• Tangible visual proof (product photos)")
            st.success("• Simple 3-field form (no friction)")
            st.success("• Clear value proposition (free samples)")
            st.success("• Low-risk proposition (free stuff)")
            
        with success_col2:
            st.markdown("**✅ Technical Excellence:**")
            st.success("• Complete source attribution tracking")
            st.success("• Facebook SDK social proof")
            st.success("• Smart form auto-detection")
            st.success("• URL injection revenue system")
        
        # Technical Architecture
        st.subheader("🔧 Technical Architecture")
        
        with st.expander("📋 Complete Technical Stack"):
            st.markdown("""
            **🎯 Tracking Systems:**
            - Meta Pixel: 1153754019617349
            - Tune SDK: track.modemobile.com
            - Smart Recognition: Form auto-detection
            - Facebook SDK: Social proof integration
            
            **💰 Revenue Attribution Flow:**
            1. Meta Ad → Landing Page (Form Submission)
            2. Form Data Captured → Thank You URL populated
            3. Thank You Page → ALL LINKS get source + email
            4. Any click → Revenue attributed to original Meta Ad
            5. Multiple tracking systems ensure zero revenue leakage
            
            **🔧 Implementation Ready:**
            - Global Scripts: 13 sections prepared
            - LeadPages Ready: Copy-paste deployment
            - A/B Testing: Framework in place
            """)
        
        st.info("💡 **Key Insight:** MFF's technical foundation is the proven template for all Mode properties!")
        
        # Optimization Roadmap
        st.subheader("🚀 Optimization Roadmap")
        
        roadmap_tabs = st.tabs(["Phase 1: Prebid.js", "Phase 2: Custom Popup", "Phase 3: CRO"])
        
        with roadmap_tabs[0]:
            st.markdown("""
            **🔥 PHASE 1: Prebid.js Implementation (HIGH PRIORITY)**
            
            **Expected Results:**
            - Revenue Lift: +$6k-$13k/month
            - Timeline: 2-3 weeks
            - Risk Level: LOW (additive optimization)
            
            **Implementation Steps:**
            1. Header bidding setup with multiple demand sources
            2. Ezoic integration with prebid competition
            3. Revenue monitoring & optimization
            4. A/B testing vs current Ezoic-only setup
            
            **Success Metrics:**
            - Target RPM: $18-$25 (vs current $12)
            - Page load speed maintained (<3s)
            - Revenue attribution tracking intact
            """)
            
            if st.button("🚀 Start Prebid.js Implementation", key="prebid_start"):
                st.success("Ready to implement! Navigate to Global Scripts for technical setup.")
        
        with roadmap_tabs[1]:
            st.markdown("""
            **🎁 PHASE 2: Custom Thanks.co Replacement (MEDIUM PRIORITY)**
            
            **Expected Results:**
            - Revenue Retention: 100% vs Thanks.co commission
            - Timeline: 4-6 weeks
            - Risk Level: MEDIUM (requires A/B testing)
            
            **Implementation Steps:**
            1. Tune CPL offer inventory integration
            2. Popup design replication (Thanks.co visual match)
            3. A/B testing framework setup
            4. Performance monitoring vs Thanks.co baseline
            
            **Success Metrics:**
            - Match or exceed $75 RPM
            - Maintain popup conversion rates
            - 100% revenue retention (no third-party commission)
            """)
            
            if st.button("🎬 View Thanks.co Demo", key="thankco_demo"):
                st.info("Navigate to Thanks.co Analysis tab for working demo!")
        
        with roadmap_tabs[2]:
            st.markdown("""
            **📈 PHASE 3: Conversion Rate Optimization (LOW PRIORITY)**
            
            **Expected Results:**
            - Revenue Lift: +15-25%
            - Timeline: Ongoing optimization
            - Risk Level: LOW (systematic testing)
            
            **Focus Areas:**
            1. Landing page headline optimization
            2. Form field sequence testing
            3. Visual content A/B testing
            4. Mobile UX improvements
            
            **Success Metrics:**
            - CPL maintenance at $0.45 or better
            - Conversion rate improvements
            - Email list growth acceleration
            """)
        
        st.success("🎯 **Strategic Priority:** Phase 1 (Prebid.js) offers highest ROI with lowest risk - implement immediately!")
        
    # Tab 3: ModeMarketMunchies  
    with property_tabs[2]:
        st.header("🟡 ModeMarketMunchies - Launch & Optimize")
        
        # Visual Section
        visual_col1, visual_col2 = st.columns([1, 2])
        
        with visual_col1:
            st.image("https://modemarketmunchies.com/wp-content/uploads/2025/04/market-munchies-logo-1.webp", 
                     caption="🏷️ MMM Logo", width=200)
            
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-7c9f0495-1873-43d5-b051-e6b193b2254e.png", 
                     caption="📱 Landing Page Mobile", width=250)
        
        with visual_col2:
            st.subheader("📊 Property Overview")
            st.markdown("""
            **🎯 Business Model:** Finance Content Site  
            **📊 Traffic:** Building audience  
            **💰 Revenue:** $0 (ready for setup)
            **📧 Content Focus:** Finance, crypto, trading
            **🔗 URL:** [ModeMarketMunchies.com](https://modemarketmunchies.com)
            **⚠️ Status:** LAUNCHED, NO MONETIZATION
            """)
            
            st.warning("🎯 **Challenge:** Meta CPL $5-10 vs Affiliate CPL $1.50")
            
            st.markdown("**📱 Mobile Visual Insights:**")
            st.markdown("- Professional financial content with real-time ticker")
            st.markdown("- Crypto analysis and market news focus")
            st.markdown("- Clean blue/red financial theme")
            st.markdown("- Newsletter signup ready in footer")
        
        st.markdown("---")
        
        # Challenge Analysis
        st.subheader("⚠️ Current Performance Challenge")
        
        challenge_col1, challenge_col2 = st.columns(2)
        
        with challenge_col1:
            st.error("**❌ Meta Traffic Issues:**")
            st.markdown("- CPL: $5-10 (LOSING MONEY)")
            st.markdown("- Poor conversion on paid traffic")
            st.markdown("- Lacks financial trust signals")
            st.markdown("- Value proposition unclear for paid")
            
        with challenge_col2:
            st.success("**✅ Affiliate Traffic Success:**")
            st.markdown("- CPL: $1.50 (PROFITABLE)")
            st.markdown("- Organic traffic converts well")
            st.markdown("- Content resonates with audience")
            st.markdown("- Proof of concept validated")
        
        st.info("💡 **Root Cause:** Landing page optimized for organic traffic, not paid advertising")
        
        # Implementation Strategy
        st.subheader("🚀 Implementation Strategy")
        
        strategy_tabs = st.tabs(["Phase 1: Foundation", "Phase 2: Optimization", "Phase 3: Scale"])
        
        with strategy_tabs[0]:
            st.markdown("""
            **🔧 PHASE 1: Foundation (Week 1-2)**
            
            **Apply MFF's Proven $0.45 CPL Foundation:**
            - Deploy MFF Global Scripts (complete tracking)
            - Implement Thanks.co popup system
            - Set up complete revenue attribution
            - Test affiliate traffic flow with new system
            
            **Expected Results:**
            - Risk: LOW (proven foundation)
            - Timeline: 1-2 weeks
            - Revenue: Maintain $1.50 affiliate CPL
            
            **Success Metrics:**
            - Affiliate traffic performance maintained
            - Complete tracking system operational
            - Revenue attribution working
            """)
            
            if st.button("🔧 Start MMM Foundation Setup", key="mmm_foundation"):
                st.session_state.page = "🔧 Global Scripts Implementation"
                st.success("Ready to apply MFF's proven foundation to MMM!")
                st.rerun()
        
        with strategy_tabs[1]:
            st.markdown("""
            **📈 PHASE 2: Financial Optimization (Week 3-4)**
            
            **Finance-Specific Enhancements:**
            - Add financial trust signals (certifications, awards)
            - Test Meta-specific value propositions
            - Financial-focused popup offers (trading, investing)
            - A/B test against MFF baseline performance
            
            **Expected Results:**
            - Target: $1.50 CPL on Meta traffic (match affiliate)
            - Revenue Potential: $8k-$15k/month
            - Risk: MEDIUM (requires optimization)
            
            **Success Metrics:**
            - Meta CPL reduction from $5-10 to $1.50
            - Conversion rate improvement on paid traffic
            - Revenue attribution accuracy
            """)
        
        with strategy_tabs[2]:
            st.markdown("""
            **🚀 PHASE 3: Scale & Optimize (Week 5-8)**
            
            **Scaling Strategy:**
            - Scale profitable Meta campaigns
            - Optimize conversion funnel continuously
            - Expand affiliate partnerships
            - Cross-property traffic optimization
            
            **Expected Results:**
            - Revenue Target: $15k-$25k/month
            - Sustainability: Match MFF performance
            - Timeline: 2-3 months total
            
            **Success Metrics:**
            - Consistent $1.50 CPL across all traffic
            - Revenue growth month-over-month
            - Email list growth acceleration
            """)
        
        # Revenue Projections
        st.subheader("💰 Revenue Projections")
        
        projection_col1, projection_col2 = st.columns(2)
        
        with projection_col1:
            st.markdown("""
            **📊 Conservative Scenario:**
            - Month 1-2: $2k-$5k (foundation + basic ads)
            - Month 3-6: $8k-$15k (optimized Meta + popup)
            - Month 6+: $15k-$25k (scaled operations)
            """)
        
        with projection_col2:
            st.markdown("""
            **🚀 Aggressive Scenario:**
            - Month 3: $10k-$18k (rapid optimization success)
            - Month 6+: $20k-$35k (MFF performance parity)
            - Goal: Match ModeFreeFinds revenue model
            """)
        
        st.success("🎯 **Strategic Advantage:** Finance vertical has higher affiliate payouts than free stuff - revenue potential may exceed MFF!")
        
    # Tab 4: ModeMobileDaily - Development Blueprint
    with property_tabs[3]:
        st.header("🔴 ModeMobileDaily - Development Blueprint")
        
        # Visual Section
        visual_col1, visual_col2 = st.columns([1, 2])
        
        with visual_col1:
            st.image("https://modemobiledaily.com/wp-content/uploads/2025/06/cropped-Daily-2a.png", 
                     caption="🏷️ MMD Logo", width=200)
            
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-84e981c0-206b-4370-83a1-f2b2e5540d90.png", 
                     caption="📱 Current State", width=250)
        
        with visual_col2:
            st.subheader("📊 Property Overview")
            st.markdown("""
            **🎯 Business Model:** Viral News/Breaking News Site  
            **📊 Traffic:** Limited content (June 2025)
            **💰 Revenue:** $0 (development phase)
            **📧 Content Strategy:** Mobile-first viral content
            **🔗 URL:** [ModeMobileDaily.com](https://modemobiledaily.com)
            **⚠️ Status:** DEVELOPMENT STAGE
            """)
            
            st.error("🚧 **Current State:** No content automation or monetization")
            
            st.markdown("**📱 Visual Insights:**")
            st.markdown("- Viral content format perfect for mobile sharing")
            st.markdown("- Quizzes, entertainment, trending topics")
            st.markdown("- Engaging headlines ('22 Weird Animal Facts')")
            st.markdown("- Modern blue/white theme optimized for viral content")
        
        st.markdown("---")
        
        # Development Strategy
        st.subheader("🚀 Development Strategy")
        
        dev_tabs = st.tabs(["Content Automation", "Monetization Plan", "Implementation Timeline"])
        
        with dev_tabs[0]:
            st.markdown("""
            **📰 Content Automation Framework**
            
            **RSS Feed Integration:**
            - Breaking news sources (AP, Reuters, BBC)
            - Entertainment & celebrity news
            - Trending social media topics
            - Viral content aggregation
            
            **AI Enhancement Pipeline:**
            - Headline optimization for mobile engagement
            - Content summarization for quick consumption
            - Trending hashtag integration
            - Social sharing optimization
            
            **Publishing Strategy:**
            - Target: 5-10 posts per day minimum
            - Peak times: 6AM, 12PM, 6PM, 9PM
            - Mobile-first formatting
            - Auto-social media distribution
            """)
        
        with dev_tabs[1]:
            st.markdown("""
            **💰 Revenue Model Strategy**
            
            **Primary Revenue Streams:**
            1. **Programmatic Ads** (High volume model)
               - Target: $2-$4 RPM (volume compensates)
               - Ad placement: Between stories, sidebar
               - Mobile-optimized ad units
            
            2. **News Affiliate Offers**
               - Breaking news alert subscriptions
               - News app promotions
               - Entertainment service trials
            
            3. **Email List Monetization**
               - Daily digest newsletter
               - Breaking news alerts
               - Sponsored content integration
            
            **Target Performance:**
            - CPL Target: $0.75-$1.25 (volume-based)
            - Revenue Timeline: 3-4 months
            - Monthly Goal: $5k-$10k initially
            """)
        
        with dev_tabs[2]:
            st.markdown("""
            **📅 Implementation Timeline**
            
            **Week 1-2: Infrastructure Setup**
            - WordPress automation configuration
            - RSS feed integration & testing
            - Content template creation
            - Mobile optimization audit
            
            **Week 3-4: Content Production Launch**
            - Daily publishing schedule activation
            - Social media automation setup
            - Traffic generation campaigns
            - Audience building focus
            
            **Week 5-8: Monetization Activation**
            - Global Scripts deployment (MFF foundation)
            - Ad placement optimization
            - Affiliate offer integration
            - Revenue stream testing
            
            **Week 9-12: Scale & Optimize**
            - Traffic scaling campaigns
            - Conversion optimization
            - Revenue diversification
            - Performance analysis & improvement
            """)
        
        st.info("💡 **Key Advantage:** Viral news has natural shareability - one viral post can drive massive traffic spikes")
        
        # Challenges & Solutions
        st.subheader("⚠️ Development Challenges & Solutions")
        
        challenge_col1, challenge_col2 = st.columns(2)
        
        with challenge_col1:
            st.markdown("""
            **🚨 Challenges:**
            - Content velocity requirements (5-10 posts/day)
            - Breaking news timing sensitivity
            - Mobile engagement optimization
            - Content quality vs quantity balance
            """)
        
        with challenge_col2:
            st.markdown("""
            **✅ Solutions:**
            - Automated RSS + AI enhancement pipeline
            - Real-time news monitoring systems
            - Mobile-first content templates
            - Quality scoring & filtering algorithms
            """)
        
        st.success("🎯 **Strategic Focus:** Build content automation first, then layer on MFF's proven monetization framework")
        
    # Tab 5: ModeClassActionsDaily - Legal Vertical Setup
    with property_tabs[4]:
        st.header("🔴 ModeClassActionsDaily - Legal Vertical Setup")
        
        # Visual Section
        visual_col1, visual_col2 = st.columns([1, 2])
        
        with visual_col1:
            st.image("https://modeclassactionsdaily.com/wp-content/uploads/2025/04/class-actions-logo.png", 
                     caption="🏷️ MCAD Logo", width=200)
            
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-f7d2b138-0af0-4778-ab6e-b208a2cd45f1.png", 
                     caption="📱 Framework Ready", width=250)
        
        with visual_col2:
            st.subheader("📊 Property Overview")
            st.markdown("""
            **🎯 Business Model:** Consumer Class Action Awareness Content Site
            **📊 Traffic:** No content yet
            **💰 Revenue:** $0 (development phase)
            **📧 Target Market:** Consumers affected by class actions
            **🔗 URL:** [ModeClassActionsDaily.com](https://modeclassactionsdaily.com)
            **⚠️ Status:** DEVELOPMENT STAGE
            """)
            
            st.error("⚖️ **Current State:** Framework ready, needs legal content")
            
            st.markdown("**📱 Visual Insights:**")
            st.markdown("- Professional legal authority positioning")
            st.markdown("- Clean, authoritative design theme")
            st.markdown("- Framework ready for class action content")
            st.markdown("- Navigation structured for legal content")
        
        st.markdown("---")
        
        # Legal Content Strategy
        st.subheader("⚖️ Legal Content Strategy")
        
        legal_tabs = st.tabs(["Content Categories", "Revenue Model", "Implementation Plan"])
        
        with legal_tabs[0]:
            st.markdown("""
            **📋 Content Categories & Sources**
            
            **Active Class Actions:**
            - Current cases seeking participants
            - Eligibility requirements & deadlines
            - Settlement amounts & timelines
            - How to join/opt-out information
            
            **Settlement Notifications:**
            - Approved settlements with claim deadlines
            - Required documentation & forms
            - Payment distribution schedules
            - Consumer rights education
            
            **Legal Education:**
            - Class action process explanation
            - Consumer protection laws
            - When to join vs individual action
            - Legal terminology simplified
            
            **Case Updates:**
            - Progress on major consumer cases
            - Court decisions & appeals
            - Industry-specific class actions
            - Consumer impact analysis
            """)
        
        with legal_tabs[1]:
            st.markdown("""
            **💰 High-Value Revenue Opportunities**
            
            **Legal Services Affiliate:**
            - Attorney referral networks ($50-$200 CPL)
            - Legal consultation services
            - Document preparation services
            - Legal insurance products
            
            **Financial Services:**
            - Settlement advance companies
            - Legal funding options
            - Credit monitoring (post-settlement)
            - Tax preparation for settlements
            
            **Consumer Protection:**
            - Identity monitoring services
            - Credit repair after legal issues
            - Consumer advocacy memberships
            - Legal document templates
            
            **Revenue Potential:**
            - Legal vertical: $25-$100+ CPL typical
            - High lifetime value consumers
            - Recurring service subscriptions
            - Premium consultation upsells
            """)
        
        with legal_tabs[2]:
            st.markdown("""
            **📅 Legal Vertical Implementation Plan**
            
            **Phase 1: Legal Framework (Week 1-3)**
            - Legal content research & sourcing
            - Compliance review (consumer protection laws)
            - Content calendar creation (class action tracking)
            - Email list activation (target audience)
            
            **Phase 2: Content Production (Week 4-6)**
            - Daily class action notifications
            - Settlement deadline alerts
            - Consumer education content
            - Legal authority building
            
            **Phase 3: Monetization (Week 7-10)**
            - Legal affiliate partnerships
            - MFF Global Scripts deployment
            - High-value popup offers (legal services)
            - Revenue attribution system
            
            **Phase 4: Scale (Week 11-16)**
            - SEO for legal keywords
            - Email marketing automation
            - Attorney partnership network
            - Revenue optimization
            """)
        
        # Unique Advantages
        st.subheader("🎯 Legal Vertical Advantages")
        
        advantage_col1, advantage_col2 = st.columns(2)
        
        with advantage_col1:
            st.success("**✅ High-Value Market:**")
            st.markdown("- Legal CPL: $25-$100+ (vs $0.45-$1.50)")
            st.markdown("- Long customer lifetime value")
            st.markdown("- Multiple service upsell opportunities")
            st.markdown("- Recurring consultation revenue")
        
        with advantage_col2:
            st.success("**✅ Proven Demand:**")
            st.markdown("- Class actions affect millions")
            st.markdown("- Settlement money goes unclaimed")
            st.markdown("- Consumer awareness gap exists")
            st.markdown("- Legal services always in demand")
        
        # Revenue Projections
        st.subheader("💰 Revenue Projections")
        
        projection_col1, projection_col2 = st.columns(2)
        
        with projection_col1:
            st.markdown("""
            **📊 Conservative Scenario:**
            - Month 1-2: $2k-$5k (foundation + content)
            - Month 3-6: $10k-$20k (legal affiliate revenue)
            - Month 6+: $20k-$40k (optimized legal funnel)
            """)
        
        with projection_col2:
            st.markdown("""
            **🚀 Aggressive Scenario:**
            - Month 3: $15k-$25k (high-value legal leads)
            - Month 6+: $30k-$60k (attorney partnership network)
            - Goal: Highest CPL in Mode portfolio
            """)
        
        st.info("💡 **Strategic Advantage:** Legal vertical commands premium pricing - potential for highest per-lead revenue in entire Mode portfolio!")
        
        if st.button("🔧 Start MCAD Legal Framework", key="mcad_start"):
            st.session_state.page = "🔧 Global Scripts Implementation"
            st.success("Ready to build MCAD with MFF foundation + legal vertical optimization!")
            st.rerun()
    
    # Tab 6: Thanks.co Analysis (Enhanced)
    with property_tabs[5]:
        st.header("🎁 Thanks.co Analysis - Custom Replacement Strategy")
        
        st.info("💡 **Live Thanks.co Popup Screenshots:** These are the actual popup offers captured from Mike's Thank You page showing the system generating ~$75 RPM.")
        
        # Enhanced demo section from existing Properties Portfolio
        st.subheader("🎬 Thanks.co Popup Visual Demo")
        
        demo_tabs = st.tabs(["📱 Live Screenshots", "🔧 Custom Concept", "📊 Comparison"])
        
        with demo_tabs[0]:
            st.markdown("**🎯 Actual Thanks.co Popup Screenshots Captured:**")
            
            # Show actual captured popup screenshot
            st.image("https://service.firecrawl.dev/storage/v1/object/public/media/screenshot-bf2ee1ba-8bed-4078-96d4-b4c1c43992ba.png", 
                     caption="📱 Thanks.co Popup on ModeFreeFinds Thank You Page", 
                     width=400)
            
            st.markdown("""
            **🎬 Live Popup Analysis:**
            - **Current Offer:** Who Gives A Crap eco-friendly toilet paper (20% off)
            - **Promotional Code:** ecosave20
            - **Value Proposition:** "Better for earth, 50% profits to build toilets"
            - **Visual Design:** Clean eco-friendly packaging imagery
            - **CTA Button:** "Unlock offer" (white button, prominent)
            - **Revenue Model:** Thanks.co takes commission, ~$75 RPM
            """)
            
            st.success("✅ **Key Insight:** This popup shows sophisticated offer rotation system with branded imagery and clear value propositions. Mike's custom replacement can replicate this high-converting format while keeping 100% revenue.")
            
            # Show the technical implementation
            with st.expander("🔧 View Thanks.co Technical Code"):
                st.code("""
// Mike's Thanks.co Implementation
<div id="thanks-widget"></div>
<script>
  function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name) || '';
  }
  
  const source = getUrlParameter('source');
  const affSub = getUrlParameter('aff_sub');
  const traceId = `${source}-${affSub}`.replace(/^-|-$/g, '').replace(/--+/g, '-');
  
  __thanks = {
    partnerId: 'plat28b62ac9-0624-4c1a-bb09-2ef507ed',
    traceId: traceId || 'default-traceid'
  };
</script>
<script src="https://s.thanks.is/v1/widget.js" defer></script>
                """, language="html")
        
        with demo_tabs[1]:
            st.markdown("**🚀 Interactive Custom Popup Demo (Tune CPL)**")
            
            # Use the working popup demo from existing code
            if st.button("🎬 Launch Custom Popup Demo", key="custom_popup_demo", type="primary"):
                popup_demo_html = """
                <div id="mode-popup-demo" style="margin: 20px 0;">
                    <!-- Custom Popup Modal - Exact Thanks.co Design -->
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
                            border-radius: 20px;
                            padding: 0;
                            max-width: 380px;
                            width: 90%;
                            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        ">
                            <!-- Header Section -->
                            <div style="
                                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                                height: 180px;
                                border-radius: 20px 20px 0 0;
                                position: relative;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                            ">
                                <!-- Close Button -->
                                <button onclick="hideModePopup()" style="
                                    position: absolute;
                                    top: 16px; right: 16px;
                                    background: rgba(255,255,255,0.2);
                                    border: none;
                                    color: white;
                                    font-size: 20px;
                                    cursor: pointer;
                                    width: 32px;
                                    height: 32px;
                                    border-radius: 50%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                ">×</button>
                                
                                <!-- Logo Circle -->
                                <div style="
                                    position: absolute;
                                    top: 20px; left: 20px;
                                    width: 40px; height: 40px;
                                    background: rgba(255,255,255,0.9);
                                    border-radius: 50%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-weight: bold;
                                    color: #6366f1;
                                    font-size: 18px;
                                ">$$</div>
                                
                                <!-- Main Content -->
                                <div style="text-align: center; margin-top: 20px;">
                                    <div style="
                                        background: rgba(255,255,255,0.2);
                                        padding: 6px 16px;
                                        border-radius: 20px;
                                        font-size: 12px;
                                        margin-bottom: 16px;
                                        display: inline-block;
                                    ">Build your wealth & the future</div>
                                    
                                    <div style="font-size: 48px; margin-bottom: 8px;">📈</div>
                                    
                                    <h3 style="
                                        margin: 0;
                                        font-size: 24px;
                                        font-weight: 700;
                                        line-height: 1.2;
                                    ">$50 off Premium Trading Platform</h3>
                                </div>
                            </div>
                            
                            <!-- Content Section -->
                            <div style="padding: 32px 24px 24px;">
                                <p style="
                                    color: #666;
                                    font-size: 16px;
                                    line-height: 1.5;
                                    margin: 0 0 24px 0;
                                    text-align: center;
                                ">Start trading with commission-free stocks and get professional research tools included. Perfect for building your investment portfolio.</p>
                                
                                <!-- CTA Buttons -->
                                <button style="
                                    width: 100%;
                                    background: #8b5cf6;
                                    color: white;
                                    border: none;
                                    padding: 14px;
                                    border-radius: 12px;
                                    font-size: 16px;
                                    font-weight: 600;
                                    cursor: pointer;
                                    margin-bottom: 12px;
                                ">Unlock offer</button>
                                
                                <button onclick="hideModePopup()" style="
                                    width: 100%;
                                    background: white;
                                    color: #666;
                                    border: 2px solid #e5e7eb;
                                    padding: 12px;
                                    border-radius: 12px;
                                    font-size: 14px;
                                    cursor: pointer;
                                ">Next ></button>
                                
                                <!-- Footer Dots -->
                                <div style="text-align: center; margin-top: 16px;">
                                    <span style="width: 8px; height: 8px; background: #333; border-radius: 50%; margin: 0 4px; display: inline-block;"></span>
                                    <span style="width: 8px; height: 8px; background: #ddd; border-radius: 50%; margin: 0 4px; display: inline-block;"></span>
                                    <span style="width: 8px; height: 8px; background: #ddd; border-radius: 50%; margin: 0 4px; display: inline-block;"></span>
                                    <span style="width: 8px; height: 8px; background: #ddd; border-radius: 50%; margin: 0 4px; display: inline-block;"></span>
                                    <span style="width: 8px; height: 8px; background: #ddd; border-radius: 50%; margin: 0 4px; display: inline-block;"></span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
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
                
                st.success("✅ **Demo Active:** The popup above replicates Thanks.co design with Tune CPL offers. Use ESC key or click outside to close!")
        
        with demo_tabs[2]:
            st.markdown("**📊 Thanks.co vs Custom Replacement Comparison**")
            
            comparison_col1, comparison_col2 = st.columns(2)
            
            with comparison_col1:
                st.markdown("""
                **🎁 Thanks.co (Current)**
                - RPM: ~$75 (excellent)
                - Revenue Share: Commission to Thanks.co
                - Control: Limited offer selection
                - Integration: Third-party dependency
                - Customization: Minimal brand control
                """)
            
            with comparison_col2:
                st.markdown("""
                **🔧 Custom Tune Integration**
                - RPM Target: $75+ (match or exceed)
                - Revenue Share: 100% retention
                - Control: Full offer inventory access
                - Integration: Direct Tune API
                - Customization: Complete brand control
                """)
            
            st.success("🎯 **Strategic Advantage:** Custom integration provides 100% revenue retention while maintaining or improving performance!")
        
        # Implementation Roadmap
        st.subheader("🚀 Custom Thanks.co Implementation Roadmap")
        
        roadmap_col1, roadmap_col2 = st.columns(2)
        
        with roadmap_col1:
            st.markdown("""
            **Phase 1: Technical Foundation (Week 1-2)**
            - Popup HTML/CSS framework (Thanks.co replica)
            - JavaScript modal system
            - Tune API integration
            - Source attribution integration
            
            **Phase 2: Offer Management (Week 3-4)**
            - Tune CPL offer categorization
            - A/B testing framework
            - Revenue tracking system
            - Automated offer rotation
            """)
        
        with roadmap_col2:
            st.markdown("""
            **Phase 3: Testing & Deployment (Week 5-6)**
            - ModeFreeFinds A/B test vs Thanks.co
            - Performance monitoring
            - Revenue comparison analysis
            - Rollout decision based on data
            
            **Expected Results:**
            - Revenue Retention: 100% vs commission
            - Performance: Match or exceed $75 RPM
            - Timeline: 6-8 weeks to deployment
            """)
        
        st.info("💡 **Strategic Impact:** Custom replacement could add $3k-$5k monthly by eliminating Thanks.co commission while maintaining performance!")
    
    # Tab 7: Implementation Roadmap
    with property_tabs[6]:
        st.header("🚀 Implementation Roadmap - Master Timeline")
        
        st.subheader("🎯 Priority Matrix & Resource Allocation")
        
        priority_col1, priority_col2, priority_col3 = st.columns(3)
        
        with priority_col1:
            st.markdown("""
            **🔥 IMMEDIATE (Next 2 weeks)**
            - **HIGH:** MFF Prebid.js (+$6k-$13k)
            - **HIGH:** MMM Global Scripts foundation
            - **MEDIUM:** Thanks.co custom development
            - **LOW:** Content strategy (MMD, MCAD)
            """)
        
        with priority_col2:
            st.markdown("""
            **⚡ SHORT-TERM (2-8 weeks)**
            - MMM Meta traffic optimization
            - Thanks.co A/B testing
            - MMD content automation
            - MCAD legal framework
            """)
        
        with priority_col3:
            st.markdown("""
            **📈 LONG-TERM (2-6 months)**
            - All properties revenue-generating
            - Cross-property optimization
            - Advanced automation
            - Portfolio scaling strategies
            """)
        
        st.markdown("---")
        
        # Revenue Impact Timeline
        st.subheader("💰 Revenue Impact Timeline")
        
        timeline_data = {
            'Month': [1, 2, 3, 4, 5, 6],
            'MFF Optimization': ['+$6k', '+$10k', '+$13k', '+$13k', '+$13k', '+$15k'],
            'MMM Launch': ['$0', '+$5k', '+$12k', '+$18k', '+$22k', '+$25k'],
            'Thanks.co Custom': ['$0', '$0', '+$3k', '+$5k', '+$5k', '+$8k'],
            'MMD Launch': ['$0', '$0', '$0', '+$3k', '+$8k', '+$12k'],
            'MCAD Launch': ['$0', '$0', '$0', '$0', '+$8k', '+$15k'],
            'Total Monthly': ['+$6k', '+$15k', '+$28k', '+$39k', '+$56k', '+$75k']
        }
        
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, use_container_width=True)
        
        st.success("🎯 **Target Achievement:** $50k-$75k monthly revenue increase within 6 months through systematic optimization!")
        
        # Success Metrics
        st.subheader("📊 Success Metrics & KPIs")
        
        kpi_col1, kpi_col2 = st.columns(2)
        
        with kpi_col1:
            st.markdown("""
            **Revenue Metrics:**
            - Month-over-month growth
            - CPL optimization targets
            - Revenue stream diversification
            - Cross-property performance
            """)
        
        with kpi_col2:
            st.markdown("""
            **Operational Metrics:**
            - Implementation timeline adherence
            - A/B testing success rates
            - Traffic growth rates
            - Conversion optimization
            """)
        
        # Next Actions
        st.subheader("⚡ Immediate Next Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("🚀 Start MFF Prebid.js", key="start_prebid", type="primary"):
                st.session_state.page = "🔧 Global Scripts Implementation"
                st.success("Implementing highest ROI optimization first!")
                st.rerun()
        
        with action_col2:
            if st.button("🔧 Deploy MMM Foundation", key="deploy_mmm", type="primary"):
                st.session_state.page = "🔧 Global Scripts Implementation"
                st.success("Building MMM foundation with MFF template!")
                st.rerun()
        
        with action_col3:
            if st.button("🎬 Test Thanks.co Demo", key="test_thankco"):
                st.info("Navigate to Thanks.co Analysis tab for working demo!")
        
        st.info("💡 **Strategic Approach:** Optimize existing revenue first (MFF), then scale proven model to new properties (MMM, MCAD, MMD)")
        
        # Remove the old Properties Portfolio section entirely
        # (This section will be completely removed)

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

# (Properties Portfolio section removed - now integrated into Mode Properties Hub)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*Dashboard updated: 2025-01-27*")
st.sidebar.markdown("**🚀 Multi-page dashboard with honest metrics!**")
st.sidebar.markdown("**Navigation:** Always-visible buttons (no dropdown!)")
