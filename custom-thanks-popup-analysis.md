# Custom Thanks.co Replacement Analysis & Development Plan

## Thanks.co Popup System Analysis

### 🎯 Current Performance
- **RPM**: ~$75 (Mike's reported performance)
- **Format**: 5-slide carousel popup system
- **Placement**: ModeFreeFinds thank you page
- **Integration**: URL parameter tracking (source, aff_sub → traceId)

### 📱 Popup Carousel Structure (Captured via Screenshots)

#### Slide 1: Sam's Club Membership
- **Offer**: 36% off Sam's Club Plus membership
- **Value**: Save $40 (normally $110)
- **Benefits**: Free shipping, early hours, 2% Sam's Cash
- **Imagery**: Family with Sam's Club grocery products
- **CTA**: "Claim offer" (white button)
- **Branding**: Sam's Club logo prominent

#### Slide 2: TopCashback
- **Offer**: $20 cashback on today's purchase
- **Value**: Join free, earn highest cashback
- **Benefits**: 7000+ stores, unbeatable rates, $20 bonus
- **Imagery**: Brand logos grid (Walmart, Best Buy, Nike, etc.)
- **CTA**: "Claim your $20" (white button)
- **Branding**: TopCashback logo

#### Slide 3: Capital One Shopping
- **Offer**: Get coupons applied to orders instantly
- **Value**: $30 bonus redemption
- **Benefits**: Free browser extension, automatic coupons
- **Imagery**: Shopping comparison interface screenshot
- **CTA**: "Redeem $30 Bonus" (white button)
- **Branding**: Capital One Shopping logo

#### Slide 4: Kraken Crypto
- **Offer**: $25 in crypto bonus
- **Value**: Deposit & trade $100 to get $25
- **Benefits**: 325+ cryptocurrencies, 15M+ users
- **Imagery**: Abstract crypto-themed graphics
- **CTA**: "Claim now" (white button)
- **Branding**: Kraken logo

#### Slide 5: FreeShipping.com
- **Offer**: $10 cash back on today's purchase
- **Value**: 10% cash back at 1000+ stores
- **Benefits**: Free to join, immediate $10 claim
- **Imagery**: Retailer brand logos (Best Buy, Walmart, Home Depot, etc.)
- **CTA**: "Claim your $10" (white button)
- **Branding**: FreeShipping.com logo

### 🔧 Technical Implementation (Mike's Code)

```html
<html>
  <div id="thanks-widget"></div>
  <script>
    // Function to get the value of a URL parameter
    function getUrlParameter(name) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(name) || ''; // Return empty string if not found
    }

    // Get 'source' and 'aff_sub' from URL
    const source = getUrlParameter('source');
    const affSub = getUrlParameter('aff_sub');

    // Construct traceId as "source-aff_sub", fallback if either is missing
    const traceId = `${source}-${affSub}`.replace(/^-|-$/g, '').replace(/--+/g, '-');

    console.log("Trace ID:", traceId);

    // Widget config
    __thanks = {
      partnerId: 'plat28b62ac9-0624-4c1a-bb09-2ef507ed',
      traceId: traceId || 'default-traceid'
    };
  </script>

  <script src="https://s.thanks.is/v1/widget.js" defer></script>
</html>
```

## 🚀 Custom Popup Strategy - Tune CPL Integration

### Revenue Opportunity Analysis
- **Current**: ~$75 RPM via Thanks.co (paying commission)
- **Custom Target**: $75+ RPM with 100% revenue retention
- **Monthly Impact**: Eliminate commission fees + full attribution control
- **Scale Potential**: Apply to all Mode properties (MMM, MMD, MCAD)

### Custom Implementation Architecture

#### 1. Popup Container System
```html
<div id="mode-offers-popup" class="mode-popup-overlay">
  <div class="mode-popup-container">
    <div class="mode-popup-header">
      <span class="mode-popup-title">Exclusive Offers</span>
      <button class="mode-popup-close">&times;</button>
    </div>
    <div class="mode-popup-carousel">
      <!-- Dynamic offer slides -->
    </div>
    <div class="mode-popup-navigation">
      <div class="mode-popup-dots"></div>
      <button class="mode-popup-next">Next ></button>
    </div>
  </div>
</div>
```

#### 2. Tune CPL Integration
```javascript
// Mode Custom Popup System
class ModeOffersPopup {
  constructor(config) {
    this.partnerId = config.partnerId || 'mode-default';
    this.traceId = this.generateTraceId();
    this.offers = [];
    this.currentSlide = 0;
  }

  generateTraceId() {
    const source = this.getUrlParameter('source');
    const affSub = this.getUrlParameter('aff_sub');
    return `${source}-${affSub}`.replace(/^-|-$/g, '').replace(/--+/g, '-') || 'default-traceid';
  }

  async loadTuneOffers() {
    // Fetch offers from Tune API based on user profile/source
    const offers = await fetch('/api/tune-offers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        traceId: this.traceId,
        source: this.getUrlParameter('source'),
        vertical: 'freefinds' // or 'finance', 'viral', 'legal'
      })
    });
    
    this.offers = await offers.json();
    this.renderCarousel();
  }

  renderCarousel() {
    // Build carousel with Tune offers
    // Track impressions and clicks
    // Handle offer redemption
  }
}
```

#### 3. Tune Offer Categories by Property

**ModeFreeFinds Offers:**
- Cashback apps (TopCashback, Rakuten alternatives)
- Membership deals (Sam's Club, Costco via Tune partners)
- Shopping tools (Capital One Shopping alternatives)
- Free sample/trial offers

**ModeMarketMunchies Offers:**
- Financial services (trading platforms, banking)
- Credit monitoring services
- Investment apps and tools
- Crypto trading platforms

**ModeMobileDaily Offers:**
- Entertainment subscriptions
- Gaming platforms
- Social media tools
- Viral content apps

**ModeClassActionsDaily Offers:**
- Legal consultation services
- Document preparation tools
- Insurance quote services
- Financial recovery services

### Design System Replication

#### Visual Elements
- **Modal Overlay**: Dark semi-transparent background
- **Container**: Rounded corners, white background, centered
- **Header**: Title + close button (X)
- **Content Area**: Full-width imagery + text content
- **CTA Buttons**: White background, rounded, prominent
- **Navigation**: Dot indicators + "Next >" button
- **Branding**: Partner logos prominently displayed

#### Mobile Optimization
- **Responsive Design**: Adapts to mobile viewport
- **Touch Gestures**: Swipe between slides
- **Fast Loading**: Optimized images and minimal JavaScript
- **Accessibility**: ARIA labels, keyboard navigation

### Implementation Timeline

#### Phase 1: MVP Development (2-3 weeks)
- [ ] Basic popup modal system
- [ ] Single offer display
- [ ] Tune API integration
- [ ] URL parameter tracking
- [ ] Click attribution

#### Phase 2: Carousel System (1-2 weeks)
- [ ] Multi-slide carousel
- [ ] Navigation controls
- [ ] Auto-advance timing
- [ ] Mobile swipe gestures

#### Phase 3: A/B Testing (2-3 weeks)
- [ ] Custom popup vs Thanks.co split test
- [ ] Performance monitoring
- [ ] RPM comparison
- [ ] Conversion tracking

#### Phase 4: Portfolio Rollout (2-4 weeks)
- [ ] Apply to ModeMarketMunchies
- [ ] Customize for viral content (ModeMobileDaily)
- [ ] Legal vertical offers (ModeClassActionsDaily)
- [ ] Cross-property analytics

### Success Metrics

#### Primary KPIs
- **RPM Performance**: Match or exceed $75 baseline
- **Revenue Attribution**: 100% vs Thanks.co commission
- **Click-through Rate**: Maintain current engagement
- **Conversion Rate**: Track offer completion

#### Technical Metrics
- **Load Speed**: <2 seconds popup display
- **Mobile Performance**: Smooth carousel on mobile
- **API Response**: <500ms Tune offer loading
- **Error Rate**: <1% popup loading failures

### Competitive Advantages

#### vs Thanks.co
1. **100% Revenue Retention** - No commission fees
2. **Full Attribution Control** - Complete tracking visibility
3. **Custom Offer Curation** - Tune inventory optimization
4. **Brand Integration** - Mode-branded experience
5. **Cross-Property Synergy** - Portfolio-wide optimization

#### Technical Benefits
1. **Direct Tune Integration** - Existing partner relationships
2. **Custom Targeting** - Property-specific offer matching
3. **Advanced Analytics** - Full funnel visibility
4. **A/B Testing Control** - Optimize without vendor dependency
5. **Scalable Architecture** - Easy portfolio deployment

## 📊 Dashboard Demo Integration

### Properties Portfolio Enhancement
Add interactive popup demo showing:
- **Thanks.co Current System** - Screenshot carousel
- **Custom Replacement Concept** - Mockup with Tune offers
- **Side-by-side Comparison** - Revenue retention benefits
- **Implementation Timeline** - Development roadmap

This analysis shows building a custom popup system is absolutely feasible and could provide significant revenue upside while maintaining the high-converting format that's already proven successful! 