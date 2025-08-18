# Thanks.co Integration Analysis & Custom Popup Strategy

## Current Thanks.co Implementation

### Revenue Performance
- **RPM**: ~$75 (extremely high compared to programmatic ~$12)
- **Placement**: Popup on ModeFreeFinds content/blog posts
- **Revenue Impact**: Significant contributor to $25k-$35k monthly revenue

### Technical Implementation
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

## Custom Popup Strategy Analysis

### Mike's Vision: Replace Thanks.co with Tune CPL Inventory

**Advantages:**
1. **100% Revenue Retention** - No commission to Thanks.co
2. **Existing Relationships** - Leverage proven Tune CPL partners
3. **Better Attribution** - Full control over tracking and attribution
4. **Brand Control** - Custom experience vs third-party widget

**Technical Requirements:**
1. **URL Parameter Parsing** - Already implemented (source, aff_sub)
2. **TraceId Generation** - Attribution system ready
3. **Popup Framework** - Need to build custom modal system
4. **Tune Integration** - API calls to Tune for offer delivery
5. **Performance Tracking** - RPM monitoring vs Thanks.co baseline

## Implementation Recommendations

### Phase 1: Analysis & Planning
- [ ] Audit current Thanks.co performance metrics
- [ ] Map Tune CPL inventory suitable for popup format
- [ ] Design custom popup UX/UI
- [ ] Plan A/B testing strategy (Thanks.co vs Custom)

### Phase 2: Development
- [ ] Build custom popup modal system
- [ ] Integrate Tune API for offer delivery
- [ ] Implement attribution tracking
- [ ] Add performance monitoring

### Phase 3: Testing & Optimization
- [ ] A/B test custom popup vs Thanks.co
- [ ] Monitor RPM performance
- [ ] Optimize offer targeting and rotation
- [ ] Scale to other Mode properties

## Revenue Optimization Potential

**Current State**: Thanks.co ~$75 RPM
**Target**: Maintain or exceed $75 RPM with 100% revenue retention
**Risk Mitigation**: Keep Thanks.co running during testing phase

## Next Steps

1. **Immediate**: Analyze Thanks.co widget behavior and user interaction
2. **Week 1**: Audit Tune CPL inventory for popup-suitable offers
3. **Week 2**: Design and prototype custom popup system
4. **Week 3**: Implement A/B testing framework
5. **Month 1**: Launch controlled test on subset of traffic 