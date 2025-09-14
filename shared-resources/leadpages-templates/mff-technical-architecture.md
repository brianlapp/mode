# ModeFreeFinds LeadPages Technical Architecture
## **Current Implementation (Mike's Testing Setup)**

*Based on Mike's email: January 27, 2025*  
*Status: Production - Testing on Meta Ads*

---

## 🏗️ **LANDING PAGE ARCHITECTURE**

### **Settings > Analytics Configuration**

#### **HEAD Section Scripts:**
```html
<!-- Meta Pixel - Facebook Tracking -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{PIXEL_ID}'); 
fbq('track', 'PageView');
</script>
<!-- End Meta Pixel -->

<!-- Tune SDK Conversion Script - Revenue Attribution -->
<script>
(function() {
    var tune_script = document.createElement('script');
    tune_script.src = 'https://sdk.tune.com/scripts/tune-sdk.js';
    tune_script.async = true;
    document.head.appendChild(tune_script);
    
    tune_script.onload = function() {
        // Initialize Tune tracking
        Tune.init({
            advertiser_id: '{ADVERTISER_ID}',
            conversion_key: '{CONVERSION_KEY}'
        });
    };
})();
</script>
<!-- End Tune SDK -->

<!-- Form Listener - Capture Data → Thank You URL -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Capture form data
            const formData = new FormData(form);
            const params = new URLSearchParams();
            
            // Build URL parameters for Thank You page
            for (let [key, value] of formData.entries()) {
                params.append(key, value);
            }
            
            // Add source attribution
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('utm_source')) {
                params.append('source', urlParams.get('utm_source'));
            }
            if (urlParams.get('utm_campaign')) {
                params.append('campaign', urlParams.get('utm_campaign'));
            }
            
            // Store for Thank You page
            sessionStorage.setItem('signup_data', params.toString());
        });
    }
});
</script>
<!-- End Form Listener -->
```

#### **BODY Section Scripts:**
```html
<!-- Meta/Facebook Connect/Verification -->
<script>
// Facebook verification and connect functionality
// Enables social login and verification features
fbq('track', 'Lead');
</script>
```

### **Form Configuration (Sidebar Settings)**

#### **Form Fields:**
- Email (required)
- First Name (required)  
- Last Name (required)

#### **Integrations Available:**
- Zapier (for CRM/email automation)
- Webhook endpoints
- Custom API integrations

#### **Form Actions (Post-Submission):**
- Redirect to Thank You page
- Pass form data via URL parameters
- Trigger pixel/conversion events

---

## 🎯 **THANK YOU PAGE ARCHITECTURE**

### **Settings > Analytics Configuration**

#### **HEAD Section Scripts:**
```html
<!-- Meta Conversion Pixel - Track Conversions -->
<script>
// Track conversion completion
fbq('track', 'CompleteRegistration');

// Track custom conversion event
fbq('trackCustom', 'MFF_Signup', {
    content_name: 'Free Finds Newsletter',
    value: 1.00,
    currency: 'USD'
});
</script>

<!-- Tune SDK Conversion Script - Revenue Attribution -->
<script>
// Initialize conversion tracking
Tune.recordConversion({
    action: 'signup',
    revenue: 1.00,
    currency: 'USD',
    advertiser_ref_id: new URLSearchParams(window.location.search).get('ref_id')
});
</script>
```

#### **OPEN BODY Section Scripts:**
```html
<!-- Facebook Verification -->
<script>
// Additional Facebook verification/connect features
// Enables enhanced social integration
</script>

<!-- Script to Grab Data from Thank You URL -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Get data from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const sessionData = sessionStorage.getItem('signup_data');
    
    let userData = {};
    
    // Combine URL params and session data
    if (sessionData) {
        const sessionParams = new URLSearchParams(sessionData);
        sessionParams.forEach((value, key) => {
            userData[key] = value;
        });
    }
    
    urlParams.forEach((value, key) => {
        userData[key] = value;
    });
    
    // Store for offer URL injection
    window.signupData = userData;
});
</script>

<!-- Inject Data into Thank You Offer URLs -->
<script>
function populateOfferUrls() {
    if (window.signupData) {
        const offerLinks = document.querySelectorAll('.offer-link');
        offerLinks.forEach(link => {
            const url = new URL(link.href);
            
            // Add user data to offer URLs
            Object.keys(window.signupData).forEach(key => {
                url.searchParams.set(key, window.signupData[key]);
            });
            
            // Add unique offer tracking
            url.searchParams.set('offer_source', 'mff_thankyou');
            url.searchParams.set('timestamp', Date.now());
            
            link.href = url.toString();
        });
    }
}

// Wait for DOM and run population
document.addEventListener('DOMContentLoaded', populateOfferUrls);
</script>
```

#### **CLOSE BODY Section Scripts:**
```html
<!-- Impression Pixel Source Injection -->
<script>
// Track page impressions for attribution
const impressionPixel = new Image();
impressionPixel.src = 'https://tracking.partner.com/impression?user_id=' + 
    (window.signupData?.email || 'anonymous') + 
    '&timestamp=' + Date.now();
</script>

<!-- Email.js for Email Notifications if Page is Broken -->
<script src="https://cdn.emailjs.com/dist/email.min.js"></script>
<script>
(function() {
    emailjs.init('{EMAIL_JS_USER_ID}');
    
    // Error handling and notifications
    window.addEventListener('error', function(e) {
        // Send error notification email
        emailjs.send('{SERVICE_ID}', '{TEMPLATE_ID}', {
            error_message: e.message,
            page_url: window.location.href,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        });
    });
    
    // Success notification
    if (window.signupData) {
        emailjs.send('{SERVICE_ID}', '{SUCCESS_TEMPLATE_ID}', {
            user_email: window.signupData.email,
            signup_time: new Date().toISOString(),
            source: window.signupData.source || 'direct'
        });
    }
})();
</script>

<!-- API Call Script - Additional Tracking -->
<script>
// Additional API integrations
fetch('/api/signup-complete', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        user_data: window.signupData,
        page: 'thankyou',
        timestamp: Date.now()
    })
}).catch(console.error);
</script>
```

---

## 🔧 **OPTIMIZATION OPPORTUNITIES**

### **Global Scripts Migration Candidates:**
1. **Meta Pixel Base Code** (universal across properties)
2. **Tune SDK Initialization** (consistent setup)
3. **Error Handling & Email.js** (standard across all pages)
4. **URL Parameter Utilities** (reusable functions)

### **Code Standardization Needs:**
1. **Consistent variable naming** across scripts
2. **Error handling** for all API calls  
3. **Async loading** optimization
4. **Debug mode** toggle for testing
5. **Performance monitoring** additions

### **Template Variables to Define:**
```javascript
// Global configuration object
const LEADPAGES_CONFIG = {
    meta: {
        pixel_id: '{META_PIXEL_ID}',
        conversion_events: ['Lead', 'CompleteRegistration']
    },
    tune: {
        advertiser_id: '{TUNE_ADVERTISER_ID}',
        conversion_key: '{TUNE_CONVERSION_KEY}'
    },
    email: {
        service_id: '{EMAILJS_SERVICE_ID}',
        user_id: '{EMAILJS_USER_ID}'
    }
};
```

---

## 📊 **PERFORMANCE TRACKING**

### **Current Metrics to Monitor:**
- **Meta Pixel Events:** PageView, Lead, CompleteRegistration
- **Tune Conversions:** Signup revenue attribution
- **Email Notifications:** Error rates and success confirmations
- **API Response Times:** Signup completion API performance

### **Optimization Targets:**
- **Script Load Time:** < 2 seconds total
- **Form Submission:** < 1 second processing
- **Thank You Page:** < 3 seconds full load
- **Error Rate:** < 1% for all tracking scripts

---

**Status: Ready for optimization and standardization based on Mike's architecture!** ⚡ 