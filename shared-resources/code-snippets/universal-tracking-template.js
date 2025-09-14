/**
 * Universal Mode Properties Tracking Template
 * Based on Mike's proven $0.45 CPL MFF implementation
 * Designed for LeadPages Global Scripts
 * 
 * Properties: MFF, MMM, MCAD, MMD
 * Performance: Proven $0.45 CPL foundation
 */

// ============================================================================
// UNIVERSAL CONFIGURATION
// ============================================================================
const MODE_PROPERTIES_CONFIG = {
    mff: {
        name: 'ModeFreeFinds',
        meta_pixel: '1153754019617349', // Mike's production pixel
        tune_config: 'mff_settings',
        facebook_page: 'https://www.facebook.com/modefreefinds/',
        domain_match: 'modefreefinds',
        thank_you_params: ['email', 'first_name', 'last_name', 'source'],
        trust_elements: ['facebook_widget', 'navigation']
    },
    mmm: {
        name: 'ModeMarketMunchies',
        meta_pixel: '[MMM_PIXEL_ID]', // To be added
        tune_config: 'mmm_settings',
        facebook_page: 'https://www.facebook.com/modemarketmunchies/', // If exists
        domain_match: 'modemarketmunchies',
        thank_you_params: ['email', 'first_name', 'last_name', 'phone', 'source'],
        trust_elements: ['subscriber_count', 'testimonials', 'earnings_proof']
    },
    mcad: {
        name: 'ModeClassActionsDaily',
        meta_pixel: '[MCAD_PIXEL_ID]', // To be added
        tune_config: 'mcad_settings',
        domain_match: 'modeclassactionsdaily',
        thank_you_params: ['email', 'first_name', 'last_name', 'source'],
        trust_elements: ['legal_badges', 'case_count', 'navigation']
    },
    mmd: {
        name: 'ModeMobileDaily',
        meta_pixel: '[MMD_PIXEL_ID]', // To be added
        tune_config: 'mmd_settings',
        domain_match: 'modemobiledaily',
        thank_you_params: ['email', 'first_name', 'last_name', 'source'],
        trust_elements: ['viral_stats', 'app_downloads', 'navigation']
    }
};

const UNIVERSAL_CONFIG = {
    tune_domain: 'https://track.modemobile.com',
    smart_recognition_url: 'https://portal.smartrecognition.com/js/libcode3.js',
    facebook_sdk_version: 'v22.0'
};

// ============================================================================
// UNIVERSAL TRACKING MANAGER
// ============================================================================
class UniversalModeTracking {
    constructor() {
        this.property = this.detectProperty();
        this.config = MODE_PROPERTIES_CONFIG[this.property];
        
        if (!this.config) {
            console.warn('🚨 Unknown property, defaulting to MFF config');
            this.config = MODE_PROPERTIES_CONFIG.mff;
        }
        
        console.log(`🚀 ${this.config.name} Tracking Initialized`);
        this.initializeAllTracking();
    }
    
    detectProperty() {
        const hostname = window.location.hostname.toLowerCase();
        
        for (const [key, config] of Object.entries(MODE_PROPERTIES_CONFIG)) {
            if (hostname.includes(config.domain_match)) {
                return key;
            }
        }
        
        // Default to MFF if detection fails
        return 'mff';
    }
    
    initializeAllTracking() {
        this.initializeMetaPixel();
        this.initializeTuneSDK();
        this.initializeSmartRecognition();
        this.initializeFacebookSDK();
        this.initializeFormEnhancement();
    }
    
    initializeMetaPixel() {
        if (!this.config.meta_pixel || this.config.meta_pixel.includes('[') || this.config.meta_pixel.includes(']')) {
            console.warn(`⚠️ Meta Pixel not configured for ${this.config.name}`);
            return;
        }
        
        // Mike's proven Meta Pixel implementation
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        
        fbq('init', this.config.meta_pixel);
        fbq('track', 'PageView');
        
        // Add noscript fallback
        const noscript = document.createElement('noscript');
        noscript.innerHTML = `<img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=${this.config.meta_pixel}&ev=PageView&noscript=1" />`;
        document.head.appendChild(noscript);
        
        console.log(`✅ Meta Pixel initialized for ${this.config.name}: ${this.config.meta_pixel}`);
    }
    
    initializeTuneSDK() {
        // Mike's proven Tune SDK implementation
        !function(){var o=window.tdl=window.tdl||[];if(o.invoked)window.console&&console.error&&console.error("Tune snippet has been included more than once.");else{o.invoked=!0,o.methods=["init","identify","convert"],o.factory=function(n){return function(){var e=Array.prototype.slice.call(arguments);return e.unshift(n),o.push(e),o}};for(var e=0;e<o.methods.length;e++){var n=o.methods[e];o[n]=o.factory(n)}o.init=function(e){var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src="https://js.go2sdk.com/v2/tune.js";var t=document.getElementsByTagName("script")[0];t.parentNode.insertBefore(n,t),o.domain=e}}}();
        
        tdl.init(UNIVERSAL_CONFIG.tune_domain);
        tdl.identify();
        
        console.log(`✅ Tune SDK initialized for ${this.config.name}`);
    }
    
    initializeSmartRecognition() {
        var _avp = _avp || [];
        (function() {
            var s = document.createElement('script');
            s.type = 'text/javascript'; 
            s.async = true; 
            s.src = UNIVERSAL_CONFIG.smart_recognition_url;
            var x = document.getElementsByTagName('script')[0];
            x.parentNode.insertBefore(s, x);
        })();
        
        console.log(`✅ Smart Recognition initialized for ${this.config.name}`);
    }
    
    initializeFacebookSDK() {
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
        fbScript.src = `https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=${UNIVERSAL_CONFIG.facebook_sdk_version}`;
        document.head.appendChild(fbScript);
        
        console.log(`✅ Facebook SDK initialized for ${this.config.name}`);
    }
    
    initializeFormEnhancement() {
        document.addEventListener("DOMContentLoaded", () => {
            this.enhanceForm();
        });
    }
    
    // Mike's proven form enhancement system - universalized
    enhanceForm() {
        console.log(`📝 ${this.config.name} Form Enhancement Loading`);
        
        const form = document.querySelector("form");
        if (!form) {
            console.error("❌ No form found.");
            return;
        }
        
        const originalThankYouURL = form.getAttribute("data-thank-you") || "";
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get("source") || "";
        
        // Mike's brilliant placeholder-based field detection
        const getInput = (placeholderText) => {
            return [...form.querySelectorAll("input")].find(input =>
                (input.placeholder || "").toLowerCase().includes(placeholderText.toLowerCase())
            );
        };
        
        form.addEventListener("submit", () => {
            const formData = {};
            
            // Collect data based on property configuration
            this.config.thank_you_params.forEach(param => {
                const input = getInput(param.replace('_', ' '));
                if (input) {
                    formData[param] = input.value.trim();
                }
            });
            
            // Always include source if available
            if (source) {
                formData.source = source;
            }
            
            try {
                const thankYouURL = new URL(originalThankYouURL);
                
                // Add all collected data to Thank You URL
                Object.entries(formData).forEach(([key, value]) => {
                    if (value) {
                        thankYouURL.searchParams.set(key, value);
                    }
                });
                
                form.setAttribute("data-thank-you", thankYouURL.toString());
                console.log(`🚀 Updated ${this.config.name} Thank You URL:`, thankYouURL.toString());
                
                // Track form submission
                if (window.fbq) {
                    fbq('track', 'Lead');
                }
                
            } catch (err) {
                console.error("⚠️ Failed to update thank-you URL:", err);
                this.handleError(err, 'Form Enhancement');
            }
        }, { once: true });
        
        console.log(`✅ ${this.config.name} form enhancement active`);
    }
    
    handleError(error, context) {
        console.error(`❌ ${this.config.name} ${context}:`, error);
        
        // Could integrate with email.js or monitoring service
        // For now, just log detailed error info
        const errorInfo = {
            property: this.config.name,
            context: context,
            error: error.message,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent
        };
        
        console.table(errorInfo);
    }
}

// ============================================================================
// PROPERTY-SPECIFIC TRUST ELEMENTS
// ============================================================================
class PropertyTrustElements {
    constructor(property, config) {
        this.property = property;
        this.config = config;
    }
    
    createMFFTrustElements() {
        // Mike's proven Facebook widget
        return `<div class="fb-page" data-href="${this.config.facebook_page}" data-tabs="" data-width="" data-height="" data-small-header="true" data-adapt-container-width="true" data-hide-cover="true" data-show-facepile="false"><blockquote cite="${this.config.facebook_page}" class="fb-xfbml-parse-ignore"><a href="${this.config.facebook_page}">Mode Free Finds</a></blockquote></div>`;
    }
    
    createMMMTrustElements() {
        return `
        <div class="mmm-trust-container">
            <div class="subscriber-count">900k+ Members Earning Daily</div>
            <div class="earning-proof">Members Earned $247K+ This Month</div>
            <div class="security-badges">🔒 100% Secure & Private</div>
        </div>`;
    }
    
    createMCADTrustElements() {
        return `
        <div class="mcad-trust-container">
            <div class="case-count">500+ Active Class Actions</div>
            <div class="legal-badge">⚖️ Legal Expert Verified</div>
            <div class="member-count">1M+ Members Protected</div>
        </div>`;
    }
    
    createMMDTrustElements() {
        return `
        <div class="mmd-trust-container">
            <div class="app-downloads">50k+ Daily App Users</div>
            <div class="viral-stats">📱 #1 Trending News App</div>
            <div class="update-frequency">Updated Every Hour</div>
        </div>`;
    }
}

// ============================================================================
// AUTO-INITIALIZATION
// ============================================================================
(function() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeUniversalTracking);
    } else {
        initializeUniversalTracking();
    }
    
    function initializeUniversalTracking() {
        try {
            window.ModeTracking = new UniversalModeTracking();
            console.log('🚀 Universal Mode Tracking System Active');
        } catch (error) {
            console.error('❌ Failed to initialize Universal Mode Tracking:', error);
        }
    }
})();

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================
function getCurrentProperty() {
    return window.ModeTracking ? window.ModeTracking.property : 'unknown';
}

function getPropertyConfig() {
    return window.ModeTracking ? window.ModeTracking.config : null;
}

function trackCustomEvent(eventName, parameters = {}) {
    if (window.fbq) {
        fbq('trackCustom', eventName, parameters);
    }
    
    if (window.tdl) {
        tdl.convert(eventName, parameters);
    }
    
    console.log(`📊 Custom event tracked: ${eventName}`, parameters);
}

// Export for use in property-specific scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { UniversalModeTracking, PropertyTrustElements, MODE_PROPERTIES_CONFIG };
} 