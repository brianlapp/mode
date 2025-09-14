/**
 * MODE PROPERTIES - GLOBAL SCRIPTS
 * Clean, uniform code ready for LeadPages Global Scripts feature
 * Based on Mike's proven $0.45 CPL MFF implementation
 * 
 * IMPLEMENTATION ORDER (safest to riskiest):
 * 1. Tune SDK (lowest risk - same config everywhere)
 * 2. Facebook SDK (universal social integration)
 * 3. Smart Recognition (additional tracking layer)
 * 4. Mobile Navigation (UI enhancement)
 * 5. Form Enhancement (most complex - test last)
 * 6. Meta Pixel (property-specific IDs - needs customization)
 */

// ============================================================================
// SECTION 1: TUNE SDK REVENUE ATTRIBUTION (IMPLEMENT FIRST - LOWEST RISK)
// Label: "Tune SDK - Revenue Tracking"
// Usage: Copy this entire section to Global Scripts (universal across properties)
// Risk: LOW - Same config across all properties
// ============================================================================
(function initializeTuneSDK() {
    // Clean Tune SDK implementation with error handling
    !function() {
        var o = window.tdl = window.tdl || [];
        
        // Prevent duplicate loading
        if(o.invoked) {
            window.console && console.error && console.error("Tune snippet already loaded");
            return;
        }
        
        // Mark as loaded and setup methods
        o.invoked = !0;
        o.methods = ["init", "identify", "convert"];
        
        // Create method factory
        o.factory = function(methodName) {
            return function() {
                var args = Array.prototype.slice.call(arguments);
                args.unshift(methodName);
                o.push(args);
                return o;
            };
        };
        
        // Setup all methods
        for(var i = 0; i < o.methods.length; i++) {
            var methodName = o.methods[i];
            o[methodName] = o.factory(methodName);
        }
        
        // Initialize Tune SDK
        o.init = function(domain) {
            var script = document.createElement("script");
            script.type = "text/javascript";
            script.async = !0;
            script.src = "https://js.go2sdk.com/v2/tune.js";
            
            var firstScript = document.getElementsByTagName("script")[0];
            firstScript.parentNode.insertBefore(script, firstScript);
            o.domain = domain;
        };
    }();
    
    // Initialize with Mode tracking domain (same across all properties)
    tdl.init("https://track.modemobile.com");
    tdl.identify();
    
    console.log('✅ Tune SDK initialized');
})();

// ============================================================================
// SECTION 2: FACEBOOK SDK INTEGRATION (IMPLEMENT SECOND - LOW RISK)
// Label: "Facebook SDK - Social Integration"  
// Usage: Copy this entire section to Global Scripts (universal across properties)
// Risk: LOW - Universal social integration
// ============================================================================
(function initializeFacebookSDK() {
    // Wait for DOM to be ready
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

// ============================================================================
// SECTION 3: SMART RECOGNITION TRACKING (IMPLEMENT THIRD - LOW RISK)
// Label: "Smart Recognition - Additional Tracking"
// Usage: Copy this entire section to Global Scripts (universal tracking layer)
// Risk: LOW - Additional tracking layer, won't break core functionality
// ============================================================================
(function initializeSmartRecognition() {
    // Initialize Smart Recognition tracking
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
// SECTION 4: MOBILE NAVIGATION HANDLER (IMPLEMENT FOURTH - MEDIUM RISK)
// Label: "Mobile Navigation - UI Enhancement"
// Usage: Copy this section to Global Scripts (universal UI component)
// Risk: MEDIUM - UI enhancement, could affect page layout
// ============================================================================
(function initializeMobileNavigation() {
    document.addEventListener("DOMContentLoaded", function() {
        // Find mobile menu toggle and navigation links
        const toggleBtn = document.getElementById('mobileMenuToggle');
        const navLinks = document.getElementById('navLinks');

        // Setup mobile menu toggle if elements exist
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
// SECTION 5: FORM ENHANCEMENT SYSTEM (IMPLEMENT FIFTH - HIGH RISK)
// Label: "Universal Form Enhancement"
// Usage: Copy this entire section to Global Scripts (works across all properties)
// Risk: HIGH - Complex form logic, test thoroughly
// ============================================================================
(function initializeFormEnhancement() {
    document.addEventListener("DOMContentLoaded", function() {
        console.log("📝 Form Enhancement Loading");

        // Find the main form on the page
        const form = document.querySelector("form");
        if (!form) {
            console.warn("⚠️ No form found on page");
            return;
        }

        // Get original Thank You URL and source attribution
        const originalThankYouURL = form.getAttribute("data-thank-you") || "";
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get("source") || "";

        // MIKE'S GENIUS METHOD: Find inputs by placeholder text (works across all templates)
        function findInputByPlaceholder(placeholderText) {
            return [...form.querySelectorAll("input")].find(input => {
                const placeholder = (input.placeholder || "").toLowerCase();
                return placeholder.includes(placeholderText.toLowerCase());
            });
        }

        // Form submission handler with data capture
        form.addEventListener("submit", function() {
            console.log("🚀 Form submission detected");

            // Collect form data using placeholder detection
            const formData = {
                email: findInputByPlaceholder("email")?.value.trim() || "",
                firstName: findInputByPlaceholder("first")?.value.trim() || "",
                lastName: findInputByPlaceholder("last")?.value.trim() || "",
                phone: findInputByPlaceholder("phone")?.value.trim() || ""
            };

            try {
                // Build enhanced Thank You URL with captured data
                const thankYouURL = new URL(originalThankYouURL);
                
                // Add form data to URL parameters
                if (formData.email) thankYouURL.searchParams.set("email", formData.email);
                if (formData.firstName) thankYouURL.searchParams.set("first_name", formData.firstName);
                if (formData.lastName) thankYouURL.searchParams.set("last_name", formData.lastName);
                if (formData.phone) thankYouURL.searchParams.set("phone", formData.phone);
                
                // Preserve source attribution
                if (source) thankYouURL.searchParams.set("source", source);

                // Update form's Thank You URL
                form.setAttribute("data-thank-you", thankYouURL.toString());
                console.log("✅ Thank You URL updated:", thankYouURL.toString());
                
                // Track lead conversion in Meta Pixel
                if (window.fbq) {
                    fbq('track', 'Lead');
                }
                
            } catch (error) {
                console.error("❌ Failed to update Thank You URL:", error);
            }
        }, { once: true }); // Only bind once

        console.log("✅ Form enhancement active");
    });
})();

// ============================================================================
// SECTION 6: META PIXEL TRACKING (IMPLEMENT LAST - HIGHEST RISK)
// Label: "Meta Pixel - Universal Tracking"
// Usage: Copy this entire section to Global Scripts
// Risk: HIGH - Property-specific pixel IDs, needs customization per property
// NOTE: Will need property detection logic or manual pixel ID management
// ============================================================================
(function initializeMetaPixel() {
    // Clean, uniform Meta Pixel implementation
    !function(f,b,e,v,n,t,s) {
        if(f.fbq) return; // Prevent double-loading
        
        n = f.fbq = function() {
            n.callMethod ? n.callMethod.apply(n,arguments) : n.queue.push(arguments);
        };
        
        if(!f._fbq) f._fbq = n;
        n.push = n;
        n.loaded = !0;
        n.version = '2.0';
        n.queue = [];
        
        // Load Facebook Events script asynchronously
        t = b.createElement(e);
        t.async = !0;
        t.src = v;
        s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    
    // Initialize with MFF pixel ID (update per property)
    // TODO: Add property detection logic for different pixel IDs
    fbq('init', '1153754019617349'); // MFF Meta Pixel ID
    fbq('track', 'PageView');
    
    console.log('✅ Meta Pixel initialized');
})();

// ============================================================================
// PROPERTY-SPECIFIC CONFIGURATIONS (NOT for Global Scripts)
// Label: "Property Configs - Keep Per-Page"
// Usage: These stay in individual page Analytics sections
// ============================================================================

/*
// MFF-SPECIFIC (keep in MFF page Analytics):
const MFF_CONFIG = {
    metaPixel: '1153754019617349',
    facebookPage: 'https://www.facebook.com/modefreefinds/',
    navigationLinks: [
        { text: 'Home', url: 'https://modefreefinds.com/' },
        { text: 'Contact Us', url: 'https://helpdesk.modemobile.com/hc/en-us' },
        { text: 'T&Cs', url: 'https://modefreefinds.com/terms-of-service/' },
        { text: 'Privacy', url: 'https://modefreefinds.com/privacy-policy-2/' }
    ]
};

// MMM-SPECIFIC (keep in MMM page Analytics):  
const MMM_CONFIG = {
    metaPixel: '[MMM_PIXEL_ID]', // To be added
    facebookPage: 'https://www.facebook.com/modemarketmunchies/', // If exists
    navigationLinks: [
        { text: 'Home', url: 'https://modemarketmunchies.com/' },
        // etc.
    ]
};
*/

// ============================================================================
// IMPLEMENTATION CHECKLIST
// ============================================================================

/*
STEP-BY-STEP GLOBAL SCRIPTS IMPLEMENTATION:

✅ PHASE 1: Test Global Scripts Feature
   1. Add simple test script: console.log('Global Scripts Working!');
   2. Verify it loads on MFF lander
   3. Check timing and scope

✅ PHASE 2: Implement Section 1 (Tune SDK)
   1. Copy Section 1 to Global Scripts
   2. Remove from MFF page Analytics
   3. Test tracking still works
   4. Verify console log appears

✅ PHASE 3: Implement Section 2 (Facebook SDK)
   1. Copy Section 2 to Global Scripts
   2. Test Facebook widgets still render
   3. Check for conflicts

✅ PHASE 4: Implement Section 3 (Smart Recognition)
   1. Copy Section 3 to Global Scripts
   2. Verify additional tracking loads

✅ PHASE 5: Implement Section 4 (Mobile Navigation)
   1. Copy Section 4 to Global Scripts
   2. Test mobile menu functionality

✅ PHASE 6: Implement Section 5 (Form Enhancement)
   1. Copy Section 5 to Global Scripts
   2. Test form submissions thoroughly
   3. Verify Thank You URL population

✅ PHASE 7: Implement Section 6 (Meta Pixel) - ADVANCED
   1. Add property detection logic first
   2. Test with MFF pixel ID
   3. Plan for MMM, MCAD, MMD pixel IDs

ROLLBACK PLAN: Keep original code as backup in case anything breaks
*/ 