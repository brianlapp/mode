/**
 * MODE PROPERTIES - THANK YOU PAGE GLOBAL SCRIPTS
 * Clean, uniform code ready for LeadPages Global Scripts feature
 * Based on Mike's proven $0.45 CPL MFF Thank You page
 * 
 * IMPLEMENTATION ORDER (safest to riskiest):
 * 1. Tune Conversion Tracking (universal across properties)
 * 2. URL Parameter Injection (universal revenue logic)
 * 3. Email.js Error Monitoring (universal system)
 * 4. Facebook SDK (universal social integration)
 * 5. Mode UA API Integration (property-specific endpoints)
 * 6. Meta Conversion Pixel (property-specific pixel IDs)
 */

// ============================================================================
// SECTION 1: TUNE CONVERSION TRACKING (IMPLEMENT FIRST - LOWEST RISK)
// Label: "Tune Conversion - Revenue Attribution"
// Usage: Copy this entire section to Global Scripts (same across properties)
// Risk: LOW - Same conversion tracking across all properties
// ============================================================================
(function initializeTuneConversion() {
    // Clean Tune SDK implementation (same as landing page)
    !function(){var o=window.tdl=window.tdl||[];if(o.invoked)window.console&&console.error&&console.error("Tune snippet already loaded");else{o.invoked=!0,o.methods=["init","identify","convert"],o.factory=function(n){return function(){var e=Array.prototype.slice.call(arguments);return e.unshift(n),o.push(e),o}};for(var e=0;e<o.methods.length;e++){var n=o.methods[e];o[n]=o.factory(n)}o.init=function(e){var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src="https://js.go2sdk.com/v2/tune.js";var t=document.getElementsByTagName("script")[0];t.parentNode.insertBefore(n,t),o.domain=e}}}();
    
    // Initialize Tune tracking
    tdl.init("https://track.modemobile.com");
    tdl.convert(); // KEY: Track conversion, not just identification
    
    console.log('✅ Tune conversion tracking initialized');
})();

// ============================================================================
// SECTION 2: URL PARAMETER INJECTION (IMPLEMENT SECOND - LOW RISK)
// Label: "Universal Link Monetization"
// Usage: Copy this entire section to Global Scripts (universal revenue logic)
// Risk: LOW - Revenue attribution logic works across all properties
// ============================================================================
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

// ============================================================================
// SECTION 3: EMAIL.JS ERROR MONITORING (IMPLEMENT THIRD - LOW RISK)
// Label: "Universal Error Monitoring"
// Usage: Copy this entire section to Global Scripts (universal system)
// Risk: LOW - Error monitoring system, improves reliability
// ============================================================================
(function initializeErrorMonitoring() {
    // Initialize Email.js for error notifications
    const script = document.createElement('script');
    script.src = 'https://cdn.emailjs.com/dist/email.min.js';
    script.onload = function() {
        // Initialize EmailJS service
        emailjs.init("service_twy8maf");
        
        // Create global error alert function
        window.sendErrorAlert = function({ fromName, message, pageUrl, errorType }) {
            emailjs.send("service_twy8maf", "template_02ts48r", {
                from_name: fromName,
                message: message,
                page_url: pageUrl,
                error_type: errorType
            }).then(() => {
                console.log("📧 Error alert sent successfully");
            }).catch((err) => {
                console.error("❌ Failed to send error alert:", err);
            });
        };
        
        // Set up global error handler
        window.addEventListener('error', function(event) {
            const errorInfo = {
                fromName: 'Thank You Page Error',
                message: event.message,
                pageUrl: window.location.href,
                errorType: 'JavaScript Error'
            };
            
            if (window.sendErrorAlert) {
                window.sendErrorAlert(errorInfo);
            }
        });
        
        console.log('✅ Email.js error monitoring initialized');
    };
    
    document.head.appendChild(script);
})();

// ============================================================================
// SECTION 4: FACEBOOK SDK INTEGRATION (IMPLEMENT FOURTH - MEDIUM RISK)
// Label: "Facebook SDK - Social Integration"
// Usage: Copy this entire section to Global Scripts (universal social features)
// Risk: MEDIUM - Social integration, could affect page functionality
// ============================================================================
(function initializeFacebookSDK() {
    function setupFacebookSDK() {
        // Create fb-root div if it doesn't exist
        if (!document.getElementById('fb-root')) {
            const fbRoot = document.createElement('div');
            fbRoot.id = 'fb-root';
            document.body.insertBefore(fbRoot, document.body.firstChild);
        }
        
        // Load Facebook SDK
        const fbScript = document.createElement('script');
        fbScript.async = true;
        fbScript.defer = true;
        fbScript.crossOrigin = 'anonymous';
        fbScript.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v22.0';
        document.head.appendChild(fbScript);
        
        console.log('✅ Facebook SDK initialized for Thank You page');
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupFacebookSDK);
    } else {
        setupFacebookSDK();
    }
})();

// ============================================================================
// SECTION 5: IMPRESSION PIXEL TRACKING (IMPLEMENT FIFTH - MEDIUM RISK)
// Label: "Affiliate Impression Tracking"
// Usage: Copy this section to Global Scripts (universal tracking)
// Risk: MEDIUM - Revenue tracking, property-specific offer IDs
// ============================================================================
(function initializeImpressionPixel() {
    document.addEventListener("DOMContentLoaded", function() {
        console.log("📊 Impression Pixel Loading");
        
        // Parse source from URL
        const urlParams = new URLSearchParams(window.location.search);
        const sourceVal = urlParams.get('source') || '';
        
        // Find the impression pixel
        const pixelImg = document.getElementById('modefree-pixel');
        if (!pixelImg) {
            console.warn("⚠️ Impression pixel element not found");
            return;
        }
        
        // Get pixel URL template
        const rawUrl = pixelImg.getAttribute('data-pixel-url');
        if (!rawUrl) {
            console.warn("⚠️ data-pixel-url missing on pixel element");
            return;
        }
        
        try {
            // Replace source placeholder with actual value
            const finalUrl = rawUrl.replace("{source}", sourceVal);
            
            // Fire impression pixel
            pixelImg.src = finalUrl;
            
            console.log('✅ Impression pixel fired:', finalUrl);
            
        } catch (error) {
            console.error("❌ Failed to fire impression pixel:", error);
            
            // Send error alert if available
            if (window.sendErrorAlert) {
                window.sendErrorAlert({
                    fromName: 'Impression Pixel Error',
                    message: error.message,
                    pageUrl: window.location.href,
                    errorType: 'Impression Pixel Failure'
                });
            }
        }
    });
})();

// ============================================================================
// SECTION 6: MODE UA API INTEGRATION (IMPLEMENT SIXTH - HIGH RISK)
// Label: "CRM/Email Integration"
// Usage: Copy this section to Global Scripts (property-specific endpoints)
// Risk: HIGH - Property-specific API endpoints and parameters
// ============================================================================
(function initializeModeUAAPI() {
    document.addEventListener("DOMContentLoaded", function() {
        console.log("🧠 Mode UA API Integration Loading");
        
        function sendToModeUA() {
            // Parse user data from URL
            const params = new URLSearchParams(window.location.search);
            const email = params.get("email") || "";
            const firstName = params.get("first_name") || "";
            const lastName = params.get("last_name") || "";
            const phone = params.get("phone") || "";
            const source = params.get("source") || "";
            
            // Validate required data
            if (!email) {
                console.warn("⚠️ No email in URL parameters - skipping Mode UA API");
                return;
            }
            
            try {
                // Build API URL (property-specific configuration needed)
                const apiUrl = `https://nodejs-serverless-connector.vercel.app/api/mode_ua_leadgen?action=add` +
                    `&email=${encodeURIComponent(email)}` +
                    `&lead_source=${encodeURIComponent("Leadpages")}` +
                    `&campaign=${encodeURIComponent("ModeFreeFinds")}` + // TODO: Make property-specific
                    `&country=${encodeURIComponent("United States")}` +
                    `&type=${encodeURIComponent("opt-in")}`;
                
                console.log("📡 Sending to Mode UA API:", apiUrl);
                
                // Make API call
                fetch(apiUrl)
                    .then(response => response.json())
                    .then(data => {
                        if (data?.success) {
                            console.log("✅ Mode UA API Success:", data);
                        } else {
                            console.warn("⚠️ Mode UA API responded but failed:", data);
                        }
                    })
                    .catch(error => {
                        console.error("❌ Mode UA API call failed:", error);
                        
                        // Send error alert
                        if (window.sendErrorAlert) {
                            window.sendErrorAlert({
                                fromName: 'Mode UA API Error',
                                message: error.message,
                                pageUrl: window.location.href,
                                errorType: 'API Integration Failure'
                            });
                        }
                    });
                    
            } catch (error) {
                console.error("❌ Failed to build Mode UA API request:", error);
            }
        }
        
        // Delay API call to avoid blocking page load
        if ("requestIdleCallback" in window) {
            requestIdleCallback(sendToModeUA, { timeout: 3000 });
        } else {
            setTimeout(sendToModeUA, 3000);
        }
    });
})();

// ============================================================================
// SECTION 7: META CONVERSION PIXEL (IMPLEMENT LAST - HIGHEST RISK)
// Label: "Meta Conversion Tracking"
// Usage: Copy this section to Global Scripts (property-specific pixel IDs)
// Risk: HIGH - Property-specific pixel IDs, needs customization
// ============================================================================
(function initializeMetaConversion() {
    // Clean Meta Pixel implementation
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
    
    // Initialize with MFF pixel ID (TODO: Add property detection)
    fbq('init', '1153754019617349'); // MFF Meta Pixel ID
    fbq('track', 'Lead'); // Track conversion, not PageView
    
    console.log('✅ Meta conversion pixel initialized');
})();

// ============================================================================
// PROPERTY-SPECIFIC CONFIGURATIONS (NOT for Global Scripts)
// Label: "Property Configs - Keep Per-Page"
// Usage: These stay in individual Thank You page Analytics sections
// ============================================================================

/*
// MFF-SPECIFIC (keep in MFF Thank You page):
const MFF_THANKYOU_CONFIG = {
    metaPixel: '1153754019617349',
    impressionPixelOfferId: '6571',
    impressionPixelAffId: '42946',
    thanksPartnerID: 'plat98cd0e46-c46b-4718-94ae-dcddb731',
    apiCampaign: 'ModeFreeFinds'
};

// MMM-SPECIFIC (for future MMM Thank You page):
const MMM_THANKYOU_CONFIG = {
    metaPixel: '[MMM_PIXEL_ID]',
    impressionPixelOfferId: '[MMM_OFFER_ID]',
    impressionPixelAffId: '[MMM_AFF_ID]',
    thanksPartnerID: '[MMM_THANKS_PARTNER_ID]',
    apiCampaign: 'ModeMarketMunchies'
};
*/

// ============================================================================
// HTML COMPONENTS FOR THANK YOU PAGES
// ============================================================================

/*
// IMPRESSION PIXEL HTML (property-specific offer/aff IDs):
<div style="display:none;">
    <img id="modefree-pixel"
         data-pixel-url="https://track.modemobile.com/aff_i?offer_id=6571&aff_id=42946&aff_sub2={source}"
         width="0" height="0" style="position:absolute;visibility:hidden;" border="0" />
</div>

// THANKS.IS WIDGET (property-specific partner ID):
<div id="thanks-widget"></div>
<script>
    const source = getUrlParameter('source') || 'default_source';
    __thanks = {
        partnerId: 'plat98cd0e46-c46b-4718-94ae-dcddb731',
        traceId: source
    };
</script>
<script src="https://s.thanks.is/v1/widget.js" defer></script>

// FACEBOOK SHARE BUTTON (property-specific URL):
<div class="fb-share-button" 
     data-href="https://join.modefreefinds.com/free-finds-thank-you-v2/" 
     data-layout="" 
     data-size="">
</div>
*/

// ============================================================================
// IMPLEMENTATION CHECKLIST - THANK YOU PAGES
// ============================================================================

/*
STEP-BY-STEP THANK YOU PAGE GLOBAL SCRIPTS:

✅ PHASE 1: Test with Simple Conversion Tracking
   1. Implement Section 1 (Tune Conversion) first
   2. Test conversion tracking still works
   3. Verify console logs appear

✅ PHASE 2: Add Revenue Attribution
   1. Implement Section 2 (URL Injection)
   2. Test that links get source/email parameters
   3. Check affiliate attribution works

✅ PHASE 3: Add Error Monitoring
   1. Implement Section 3 (Email.js)
   2. Test error notification system
   3. Verify alerts send on failures

✅ PHASE 4: Add Social Integration
   1. Implement Section 4 (Facebook SDK)
   2. Test social sharing functionality
   3. Check for conflicts

✅ PHASE 5: Add Impression Tracking
   1. Implement Section 5 (Impression Pixel)
   2. Test impression pixel fires correctly
   3. Verify source attribution

✅ PHASE 6: Add CRM Integration
   1. Implement Section 6 (Mode UA API)
   2. Test API calls work correctly
   3. Verify lead data gets captured

✅ PHASE 7: Add Meta Conversion (Advanced)
   1. Implement Section 7 (Meta Pixel)
   2. Add property detection logic
   3. Test with different pixel IDs

REVENUE VERIFICATION:
- Check Tune dashboard for conversions
- Verify Meta conversion events
- Test affiliate link attribution
- Confirm CRM lead capture
*/ 