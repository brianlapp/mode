/**
 * ModeFreeFinds Production Landing Page Code
 * Source: Mike Debutte - January 27, 2025
 * Status: Live on Meta Ads - PROVEN WORKING
 * Performance: $0.45 CPL
 */

// ============================================================================
// HEAD SECTION SCRIPTS
// ============================================================================

// Meta Pixel Code (Facebook Tracking)
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1153754019617349'); // MFF Meta Pixel ID
fbq('track', 'PageView');

// Meta Pixel NoScript Fallback
// <noscript><img height="1" width="1" style="display:none"
// src="https://www.facebook.com/tr?id=1153754019617349&ev=PageView&noscript=1"
// /></noscript>

// ============================================================================
// TUNE SDK - Revenue Attribution
// ============================================================================
!function(){var o=window.tdl=window.tdl||[];if(o.invoked)window.console&&console.error&&console.error("Tune snippet has been included more than once.");else{o.invoked=!0,o.methods=["init","identify","convert"],o.factory=function(n){return function(){var e=Array.prototype.slice.call(arguments);return e.unshift(n),o.push(e),o}};for(var e=0;e<o.methods.length;e++){var n=o.methods[e];o[n]=o.factory(n)}o.init=function(e){var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src="https://js.go2sdk.com/v2/tune.js";var t=document.getElementsByTagName("script")[0];t.parentNode.insertBefore(n,t),o.domain=e}}}();
tdl.init("https://track.modemobile.com")
tdl.identify()

// ============================================================================
// FORM DATA CAPTURE & THANK YOU URL POPULATION
// ============================================================================
document.addEventListener("DOMContentLoaded", function () {
    console.log("📝 ModeFreeFinds Signup Enhancer Loaded");

    const form = document.querySelector("form");
    if (!form) return console.error("❌ No form found.");

    const originalThankYouURL = form.getAttribute("data-thank-you") || "";
    const urlParams = new URLSearchParams(window.location.search);
    const source = urlParams.get("source") || "";

    // Utility: Match by input type + placeholder
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
            console.log("🚀 Updated MFF Thank You URL:", thankYouURL.toString());
        } catch (err) {
            console.error("⚠ Failed to update thank-you URL:", err);
        }
    }, { once: true });
});

// ============================================================================
// SMART RECOGNITION CODE
// ============================================================================
var _avp = _avp || [];
(function() {
  var s = document.createElement('script');
  s.type = 'text/javascript'; s.async = true; s.src = 'https://portal.smartrecognition.com/js/libcode3.js';
  var x = document.getElementsByTagName('script')[0];
  x.parentNode.insertBefore(s, x);
})();

// ============================================================================
// BODY SECTION SCRIPTS
// ============================================================================

// Facebook SDK Integration (Immediately after opening <body> tag)
// <div id="fb-root"></div>
// <script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v22.0"></script>

// ============================================================================
// NAVIGATION BAR COMPONENT
// ============================================================================
function createMFFNavigation() {
    return `
    <!-- NAVIGATION BAR START -->
    <nav class="lp-custom-nav">
      <!-- Hamburger icon (shown on mobile) -->
      <div class="menu-toggle" id="mobileMenuToggle">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>

      <!-- The navigation links -->
      <ul class="menu-links" id="navLinks">
        <li><a href="https://modefreefinds.com/" target="_blank" rel="noopener">Home</a></li>
        <li><a href="https://helpdesk.modemobile.com/hc/en-us" target="_blank" rel="noopener">Contact Us</a></li>
        <li><a href="https://modefreefinds.com/terms-of-service/" target="_blank" rel="noopener">T&Cs</a></li>
        <li><a href="https://modefreefinds.com/privacy-policy-2/" target="_blank" rel="noopener">Privacy</a></li>
      </ul>
    </nav>
    <!-- NAVIGATION BAR END -->`;
}

// Mobile Menu Toggle Handler
document.addEventListener("DOMContentLoaded", function() {
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const navLinks = document.getElementById('navLinks');

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', function() {
      // If the menu is hidden or not displayed, show it; otherwise hide it
      if (navLinks.style.display === "none" || navLinks.style.display === "") {
        navLinks.style.display = "flex";
      } else {
        navLinks.style.display = "none";
      }
    });
  }
});

// ============================================================================
// FACEBOOK PAGE WIDGET (Under form custom HTML)
// ============================================================================
function createFacebookPageWidget() {
    return `<div class="fb-page" data-href="https://www.facebook.com/modefreefinds/" data-tabs="" data-width="" data-height="" data-small-header="true" data-adapt-container-width="true" data-hide-cover="true" data-show-facepile="false"><blockquote cite="https://www.facebook.com/modefreefinds/" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/modefreefinds/">Mode Free Finds</a></blockquote></div>`;
}

// ============================================================================
// CONFIGURATION CONSTANTS
// ============================================================================
const MFF_CONFIG = {
    meta: {
        pixel_id: '1153754019617349',
        events: ['PageView', 'Lead']
    },
    tune: {
        domain: 'https://track.modemobile.com'
    },
    facebook: {
        app_id: 'v22.0',
        page_url: 'https://www.facebook.com/modefreefinds/'
    },
    smart_recognition: {
        script_url: 'https://portal.smartrecognition.com/js/libcode3.js'
    }
}; 