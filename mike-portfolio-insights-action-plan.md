# Mike's Portfolio Insights & Action Plan

## Email Summary (Latest Update)

**Date:** Today  
**From:** Mike Debutte  
**Key Insights:** Complete portfolio overview with revenue models and optimization opportunities

### ModeFreeFinds.com - Flagship Revenue Property

**Performance Metrics:**
- **Traffic:** 1M pageviews per month
- **Revenue:** $25k-$35k monthly (proven model)
- **Business Model:** Free Stuff Content Site

**Revenue Streams:**
1. **Programmatic (Ezoic):** ~$12 RPM (Mike calls this "weak")
2. **Thanks.co Popup:** ~$75 RPM (excellent performance)

**Mike's Questions & Opportunities:**
- **Prebid.js Integration:** "Can we add prebid.js to include more demand sources for programmatic optimization? Any experience with this?"
- **Custom Popup Development:** Exploring building own version of Thanks.co using Tune CPL inventory

### Portfolio Development Pipeline

**ModeMarketMunchies.com**
- **Status:** Finance content site, just went live
- **Monetization:** No ads set up yet
- **Strategy:** Apply MFF proven model to finance vertical

**ModeMobileDaily.com**
- **Status:** Viral news/breaking news site
- **Content:** No content or ads yet
- **Potential:** High-velocity viral content model

**ModeClassActionsDaily.com**
- **Status:** Consumer class action awareness content site
- **Content:** No content or ads yet
- **Opportunity:** High-value legal niche

## Immediate Action Plan

### 1. Prebid.js Optimization (ModeFreeFinds)

**Problem:** $12 RPM from Ezoic is weak performance
**Solution:** Header bidding with multiple demand sources
**Expected Impact:** 50-100% RPM improvement ($18-$25 target)

**Implementation Steps:**
1. **Week 1:** Research & apply to premium demand partners
   - Google Ad Manager
   - Amazon TAM (Transparent Ad Marketplace)
   - Index Exchange
   - Rubicon Project
   - AppNexus

2. **Week 2:** Prebid.js configuration & testing
   - Set up header bidding auction
   - Configure ad units and bidders
   - Implement timeout optimization

3. **Week 3:** A/B testing launch
   - 50/50 traffic split (Ezoic vs Prebid)
   - Monitor RPM performance
   - Track page speed impact

4. **Week 4:** Performance analysis & optimization
   - Optimize bidder timeouts
   - Adjust floor prices
   - Scale winning configuration

**Revenue Impact:** +$6k-$13k monthly potential

### 2. Custom Thanks.co Replacement Strategy

**Current:** Thanks.co popup generating ~$75 RPM
**Opportunity:** Build custom popup using Tune CPL inventory
**Benefits:** 100% revenue retention + full control

**Mike's Code Analysis:**
```javascript
// Current Thanks.co implementation
const source = getUrlParameter('source');
const affSub = getUrlParameter('aff_sub');
const traceId = `${source}-${affSub}`.replace(/^-|-$/g, '').replace(/--+/g, '-');

__thanks = {
  partnerId: 'plat28b62ac9-0624-4c1a-bb09-2ef507ed',
  traceId: traceId || 'default-traceid'
};
```

**Custom Implementation Plan:**
1. **Phase 1:** Audit current Thanks.co performance & user behavior
2. **Phase 2:** Map Tune CPL inventory suitable for popup format
3. **Phase 3:** Build custom popup modal with Tune integration
4. **Phase 4:** A/B test custom vs Thanks.co
5. **Phase 5:** Scale to all Mode properties

### 3. Portfolio Scaling Strategy

**Global Scripts Template Application:**
- Deploy MFF tracking success to MMM, MMD, MCAD
- Standardized attribution across all properties
- Consistent optimization framework

**Property Development Priority:**
1. **MMM (Finance):** Immediate monetization setup
2. **MMD (Viral News):** Content strategy & automation
3. **MCAD (Legal):** Niche content & legal affiliate focus

## Revenue Projections

### Current State (ModeFreeFinds Only)
- **Monthly Revenue:** $25k-$35k
- **Source:** Single property optimization

### Optimized Portfolio Target (6-12 months)
- **ModeFreeFinds:** $35k-$50k (prebid + custom popup)
- **ModeMarketMunchies:** $15k-$25k (finance vertical)
- **ModeMobileDaily:** $20k-$35k (viral potential)
- **ModeClassActionsDaily:** $10k-$20k (premium niche)
- **Total Portfolio:** $80k-$130k monthly

## Technical Implementation Priority

### Immediate (1-2 weeks)
1. **Prebid.js demand partner applications** - Start long approval process
2. **Thanks.co performance audit** - Baseline metrics for custom replacement
3. **Global Scripts template finalization** - Ready for MMM deployment
4. **MMM monetization planning** - First property to scale

### Short-term (1-2 months)
1. **Prebid.js full implementation & optimization**
2. **Custom popup A/B testing**
3. **MMM ad setup using MFF template**
4. **MMD & MCAD content strategy development**

### Long-term (3-6 months)
1. **All properties fully monetized**
2. **Advanced attribution & optimization systems**
3. **Content automation for viral properties**
4. **Portfolio-level strategic decisions**

## Questions for Mike

### Prebid.js Implementation
1. **Demand Partner Preferences:** Any existing relationships with Google Ad Manager, Amazon, etc.?
2. **Page Speed Priorities:** How important is Core Web Vitals vs revenue optimization?
3. **A/B Testing Approach:** Conservative gradual rollout vs aggressive testing?

### Custom Popup Strategy
1. **Tune Inventory:** Which CPL offers work best for popup format?
2. **User Experience:** Match Thanks.co style or create new branded experience?
3. **Attribution:** How important is maintaining current traceId system?

### Portfolio Development
1. **Content Strategy:** In-house team vs outsourced content creation?
2. **Launch Timeline:** Aggressive simultaneous launch vs sequential rollout?
3. **Brand Consistency:** Unified Mode branding vs distinct property identities?

## Success Metrics & Monitoring

### KPIs to Track
1. **RPM Performance:** Ezoic baseline vs prebid optimization
2. **Revenue Attribution:** Source/aff_sub tracking accuracy
3. **User Experience:** Page speed, engagement, bounce rates
4. **Portfolio Growth:** Property-by-property revenue scaling

### Reporting Dashboard
- Real-time RPM monitoring across all properties
- Attribution tracking with source breakdown
- A/B testing performance comparison
- Portfolio-level revenue trending

## Next Steps

1. **Today:** Update dashboard with Properties Portfolio section ✅
2. **Tomorrow:** Begin prebid.js demand partner research & applications
3. **This Week:** Audit Thanks.co performance & plan custom replacement
4. **Next Week:** MMM Global Scripts implementation planning

This action plan transforms Mike's portfolio insights into executable optimization strategy with clear timelines and revenue targets. 