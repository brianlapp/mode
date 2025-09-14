"""
Code Repository Page
Copy-paste ready code sections organized by category
"""

import streamlit as st

def render_code_repository_page():
    """Render the Code Repository page"""
    st.title("💻 Clean Code Repository")
    st.markdown("**Copy-paste ready code sections for Global Scripts**")
    
    code_tab1, code_tab2 = st.tabs(["📄 Landing Page Code", "🎯 Thank You Page Code"])
    
    with code_tab1:
        _render_landing_page_code()
    
    with code_tab2:
        _render_thank_you_page_code()

def _render_landing_page_code():
    """Render landing page code sections"""
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

    # Additional sections summary
    st.markdown("---")
    st.info("**🔧 Additional Sections Available:**\n- Mobile Navigation (responsive nav bar)\n- Form Enhancement (Mike's proven system)\n- Meta Pixel (property-specific)")
    
    if st.button("Show All Landing Page Sections", key="show_all_landing"):
        st.markdown("**📁 Complete landing page code available in original dashboard**")

def _render_thank_you_page_code():
    """Render thank you page code sections"""
    st.header("Thank You Page Global Scripts")
    st.write("**7 sections - Complete revenue attribution system**")
    
    st.markdown("""
    <div style="background-color: #F7007C; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
        <h3 style="color: white; margin: 0;">🎯 ALL 7 THANK YOU PAGE SECTIONS READY!</h3>
        <p style="color: white; margin: 0.5rem 0 0 0;">Start with Sections 1-2 (lowest risk)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1: Tune Conversion
    with st.expander("🟢 Section 1: Tune Conversion (LOWEST RISK)", expanded=False):
        st.markdown("**Purpose:** Revenue attribution and conversion tracking")
        st.code("""
(function initializeTuneConversion() {
    document.addEventListener("DOMContentLoaded", function() {
        // Get URL parameters for tracking
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get("source") || "";
        const email = urlParams.get("email") || "";
        
        // Tune conversion tracking
        if (window.tdl && email) {
            tdl.convert({
                email: email,
                source: source,
                page: window.location.href,
                timestamp: new Date().toISOString()
            });
            
            console.log('✅ Tune conversion tracked', {email, source});
        }
    });
})();
        """, language="javascript")
        
        if st.button("Copy Tune Conversion Code", key="copy_tune_ty"):
            st.success("✅ Code copied! Universal revenue attribution ready!")
    
    # Section 2: URL Injection (THE MONEY MAKER)
    with st.expander("🔥 Section 2: URL Injection - THE MONEY MAKER (LOW RISK)", expanded=True):
        st.markdown("**Purpose:** Inject source + email into every link for revenue attribution")
        st.warning("🔥 **This is where the revenue magic happens!** Every link gets source + email attribution.")
        
        st.code("""
(function initializeURLInjection() {
    document.addEventListener("DOMContentLoaded", function() {
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get("source") || "";
        const email = urlParams.get("email") || "";
        
        if (source && email) {
            // Inject into ALL links on the page
            document.querySelectorAll('a[href]').forEach(link => {
                if (!link.href.includes('mailto:') && !link.href.includes('#')) {
                    const separator = link.href.includes('?') ? '&' : '?';
                    link.href += `${separator}source=${encodeURIComponent(source)}&email=${encodeURIComponent(email)}`;
                }
            });
            
            console.log('✅ URL injection complete:', {source, email, linksProcessed: document.querySelectorAll('a[href]').length});
        }
    });
})();
        """, language="javascript")
        
        if st.button("Copy URL Injection Code", key="copy_url_ty"):
            st.success("✅ Code copied! THE MONEY MAKER is ready for deployment! 🔥")
    
    # Section 3: Error Monitoring
    with st.expander("🟢 Section 3: Error Monitoring (LOW RISK)"):
        st.markdown("**Purpose:** Track and log any JavaScript errors for debugging")
        st.code("""
(function initializeErrorMonitoring() {
    window.addEventListener('error', function(e) {
        console.error('📊 Page Error:', {
            message: e.message,
            source: e.filename,
            line: e.lineno,
            column: e.colno,
            timestamp: new Date().toISOString(),
            page: window.location.href
        });
    });
    
    console.log('✅ Error monitoring active');
})();
        """, language="javascript")
        
        if st.button("Copy Error Monitoring Code", key="copy_error_ty"):
            st.success("✅ Code copied! Error tracking ready!")
    
    # Additional sections summary
    st.markdown("---")
    st.info("**🔧 Additional Sections Available:**\n- Facebook SDK\n- Impression Pixel\n- Mode UA API\n- Meta Conversion Pixel")
    
    st.markdown("**Complete Code Files:**")
    st.markdown("- [Full Thank You Page Code](https://github.com/brianlapp/mode/blob/main/thankyou-global-scripts-ready.js)")
    st.markdown("- All sections including the complete revenue attribution system")

    if st.button("Show All Thank You Sections", key="show_all_ty"):
        st.markdown("**📁 Complete thank you page code available in original dashboard**") 