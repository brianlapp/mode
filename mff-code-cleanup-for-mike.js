/**
 * ModeFreeFinds Landing Page - CLEANED UP VERSION
 * Original: Mike's production code
 * Cleanup: Uniform formatting, clear comments, functional improvements
 * Purpose: Test candidate for LeadPages Global Scripts
 */

// ============================================================================
// HEAD SECTION - TRACKING & ANALYTICS
// ============================================================================

// Meta Pixel - Facebook Tracking
(function initializeMetaPixel() {
    !function(f,b,e,v,n,t,s) {
        if(f.fbq) return;
        n = f.fbq = function() {
            n.callMethod ? n.callMethod.apply(n,arguments) : n.queue.push(arguments)
        };
        if(!f._fbq) f._fbq = n;
        n.push = n;
        n.loaded = !0;
        n.version = '2.0';
        n.queue = [];
        t = b.createElement(e);
        t.async = !0;
        t.src = v;
        s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    
    fbq('init', '1153754019617349'); // MFF Meta Pixel ID
    fbq('track', 'PageView');
    
    console.log('✅ Meta Pixel initialized');
})();

// Tune SDK - Revenue Attribution
(function initializeTuneSDK() {
    !function() {
        var o = window.tdl = window.tdl || [];
        if(o.invoked) {
            window.console && console.error && console.error("Tune snippet has been included more than once.");
        } else {
            o.invoked = !0;
            o.methods = ["init", "identify", "convert"];
            o.factory = function(n) {
                return function() {
                    var e = Array.prototype.slice.call(arguments);
                    return e.unshift(n), o.push(e), o
                }
            };
            for(var e = 0; e < o.methods.length; e++) {
                var n = o.methods[e];
                o[n] = o.factory(n)
            }
            o.init = function(e) {
                var n = document.createElement("script");
                n.type = "text/javascript";
                n.async = !0;
                n.src = "https://js.go2sdk.com/v2/tune.js";
                var t = document.getElementsByTagName("script")[0];
                t.parentNode.insertBefore(n, t);
                o.domain = e
            }
        }
    }();
    
    tdl.init("https://track.modemobile.com");
    tdl.identify();
    
    console.log('✅ Tune SDK initialized');
})();

// Form Enhancement - Data Capture & Thank You URL Population
(function initializeFormEnhancement() {
    document.addEventListener("DOMContentLoaded", function () {
        console.log("📝 ModeFreeFinds Form Enhancement Loading");

        const form = document.querySelector("form");
        if (!form) {
            console.error("❌ No form found");
            return;
        }

        const originalThankYouURL = form.getAttribute("data-thank-you") || "";
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get("source") || "";

        // Utility: Find input by placeholder text (Mike's genius method)
        function findInputByPlaceholder(placeholderText) {
            return [...form.querySelectorAll("input")].find(input =>
                (input.placeholder || "").toLowerCase().includes(placeholderText.toLowerCase())
            );
        }

        // Form submission handler
        form.addEventListener("submit", function () {
            // Collect form data
            const formData = {
                email: findInputByPlaceholder("email")?.value.trim() || "",
                firstName: findInputByPlaceholder("first")?.value.trim() || "",
                lastName: findInputByPlaceholder("last")?.value.trim() || "",
                phone: findInputByPlaceholder("phone")?.value.trim() || ""
            };

            try {
                const thankYouURL = new URL(originalThankYouURL);
                
                // Add form data to Thank You URL
                if (formData.email) thankYouURL.searchParams.set("email", formData.email);
                if (formData.firstName) thankYouURL.searchParams.set("first_name", formData.firstName);
                if (formData.lastName) thankYouURL.searchParams.set("last_name", formData.lastName);
                if (formData.phone) thankYouURL.searchParams.set("phone", formData.phone);
                if (source) thankYouURL.searchParams.set("source", source);

                // Update form action
                form.setAttribute("data-thank-you", thankYouURL.toString());
                console.log("🚀 Thank You URL updated:", thankYouURL.toString());
                
                // Track lead conversion
                if (window.fbq) {
                    fbq('track', 'Lead');
                }
                
            } catch (error) {
                console.error("⚠️ Failed to update Thank You URL:", error);
            }
        }, { once: true });

        console.log("✅ Form enhancement active");
    });
})();

// Smart Recognition - Additional Tracking
(function initializeSmartRecognition() {
    var _avp = _avp || [];
    (function() {
        var script = document.createElement('script');
        script.type = 'text/javascript'; 
        script.async = true; 
        script.src = 'https://portal.smartrecognition.com/js/libcode3.js';
        var firstScript = document.getElementsByTagName('script')[0];
        firstScript.parentNode.insertBefore(script, firstScript);
    })();
    
    console.log('✅ Smart Recognition initialized');
})();

// ============================================================================
// BODY SECTION - FACEBOOK SDK
// ============================================================================

// Facebook SDK Integration (goes immediately after opening <body> tag)
function initializeFacebookSDK() {
    // Create fb-root div if it doesn't exist
    if (!document.getElementById('fb-root')) {
        const fbRoot = document.createElement('div');
        fbRoot.id = 'fb-root';
        document.body.insertBefore(fbRoot, document.body.firstChild);
    }
    
    // Load Facebook SDK
    const script = document.createElement('script');
    script.async = true;
    script.defer = true;
    script.crossOrigin = 'anonymous';
    script.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v22.0';
    document.head.appendChild(script);
    
    console.log('✅ Facebook SDK initialized');
}

// Auto-initialize Facebook SDK when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeFacebookSDK);
} else {
    initializeFacebookSDK();
}

// ============================================================================
// UI COMPONENTS - NAVIGATION & WIDGETS
// ============================================================================

// Mobile Navigation Toggle Handler
(function initializeMobileNav() {
    document.addEventListener("DOMContentLoaded", function() {
        const toggleBtn = document.getElementById('mobileMenuToggle');
        const navLinks = document.getElementById('navLinks');

        if (toggleBtn && navLinks) {
            toggleBtn.addEventListener('click', function() {
                // Toggle mobile menu visibility
                const isHidden = navLinks.style.display === "none" || navLinks.style.display === "";
                navLinks.style.display = isHidden ? "flex" : "none";
            });
            
            console.log('✅ Mobile navigation initialized');
        }
    });
})();

// ============================================================================
// HTML COMPONENTS (for reference)
// ============================================================================

// Navigation HTML (Custom Header HTML)
const NAVIGATION_HTML = `
<!-- NAVIGATION BAR -->
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

// Facebook Page Widget (Under Form Custom HTML)
const FACEBOOK_WIDGET_HTML = `
<div class="fb-page" 
     data-href="https://www.facebook.com/modefreefinds/" 
     data-tabs="" 
     data-width="" 
     data-height="" 
     data-small-header="true" 
     data-adapt-container-width="true" 
     data-hide-cover="true" 
     data-show-facepile="false">
    <blockquote cite="https://www.facebook.com/modefreefinds/" class="fb-xfbml-parse-ignore">
        <a href="https://www.facebook.com/modefreefinds/">Mode Free Finds</a>
    </blockquote>
</div>`;

// NoScript fallback for Meta Pixel
const META_PIXEL_NOSCRIPT = `
<noscript>
    <img height="1" width="1" style="display:none"
         src="https://www.facebook.com/tr?id=1153754019617349&ev=PageView&noscript=1" />
</noscript>`;

// ============================================================================
// GLOBAL SCRIPTS CANDIDATE SECTIONS
// ============================================================================

/*
POTENTIAL GLOBAL SCRIPTS (for LeadPages Global Scripts feature):

1. META PIXEL + TUNE SDK (universal tracking foundation)
2. FORM ENHANCEMENT SYSTEM (works across all properties) 
3. FACEBOOK SDK (universal social integration)
4. SMART RECOGNITION (additional tracking layer)
5. ERROR HANDLING & LOGGING (debugging system)

PROPERTY-SPECIFIC (keep per-page):
- Navigation links (different per property)
- Facebook page widgets (property-specific pages)
- Meta Pixel IDs (different per property)
- Thank You URL parameters (property-specific)
*/ 