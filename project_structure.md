# Mode Email UA & Web Projects - Project Structure

## Recommended Directory Structure

```
/mode-mobile/
├── README.md                          # Project overview and quick start
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore patterns
├── memory-bank/                       # Central memory management
│   ├── daily-logs/                   # Daily work logs by date
│   ├── conversion-data/              # CPL tracking and conversion metrics
│   ├── revenue-attribution/          # Revenue flow tracking
│   ├── optimization-wins/            # Successful optimization patterns
│   └── project-memories.json         # Key insights and learnings
├── projects/                          # Individual site projects
│   ├── mode-free-finds/              # ModeFreeFinds.com
│   │   ├── current-metrics.md        # Current performance baseline
│   │   ├── leadpages-flows/          # LeadPages signup/TY flows
│   │   ├── optimization-tests/       # A/B tests and experiments
│   │   └── code-snippets/            # Custom scripts and integrations
│   ├── mode-market-munchies/         # ModeMarketMunchies.com
│   │   ├── current-metrics.md        # Performance tracking
│   │   ├── cpl-optimization/         # Focus on reducing $5-10 CPL
│   │   ├── leadpages-flows/          
│   │   └── code-snippets/
│   ├── mode-class-actions/           # ModeClassActionsDaily.com
│   │   ├── setup-tasks.md            # Missing signup/TY flows to build
│   │   ├── target-metrics.md         # Performance goals
│   │   └── development-notes/
│   └── mode-mobile-daily/            # ModeMobileDaily.com
│       ├── setup-tasks.md            # Missing flows to build
│       ├── app-integration/          # Mode Earn App connection
│       └── development-notes/
├── shared-resources/                  # Cross-project resources
│   ├── code-snippets/                # Reusable code patterns
│   │   ├── url-parameter-passing/
│   │   ├── field-prepopulation/
│   │   ├── tune-hasoffers-integration/
│   │   └── dynamic-content-injection/
│   ├── leadpages-templates/          # Standard LeadPages setups
│   ├── affiliate-tracking/           # Tune/HasOffers configurations
│   └── revenue-attribution/          # Attribution flow documentation
├── tools-and-integrations/           # External tool configurations
│   ├── revmatics-ai/                # AI optimization platform
│   ├── tune-hasoffers/              # Affiliate platform setup
│   ├── meta-ads/                    # Facebook/Meta advertising
│   └── programmatic-ads/            # Display advertising setup
├── optimization-playbook/            # Standard operating procedures
│   ├── cpl-optimization-guide.md    # CPL reduction strategies
│   ├── leadpages-best-practices.md  # LeadPages optimization
│   ├── a-b-testing-framework.md     # Testing methodology
│   └── revenue-attribution-setup.md # Attribution implementation
└── reporting-dashboards/             # Performance tracking
    ├── weekly-performance-reports/
    ├── monthly-revenue-summaries/
    └── optimization-impact-tracking/
```

## Key Focus Areas by Priority

### 🔥 Immediate Priorities (Week 1-2)
1. **Fix MMM CPL** ($5-10 → $0.45 target)
2. **Build missing flows** for Class Actions & Mobile Daily
3. **Optimize MFF flow** (1M pageviews = massive impact potential)

### 🎯 Ongoing Optimization (Continuous)
1. **Revenue attribution tracking** (Tune/HasOffers validation)
2. **A/B testing framework** implementation
3. **Revmatics.ai integration** and testing

### 📊 Success Metrics to Track
- **CPL by property** (target vs actual)
- **Conversion rates** by funnel step
- **Revenue attribution accuracy**
- **Page load speeds** and user experience metrics
- **Email list growth rates**

## Memory Bank Categories

### Daily Logs Format
```
YYYY-MM-DD-daily-log.md
- Morning priorities
- Tasks completed
- Conversion data updates
- Optimization discoveries
- Tomorrow's focus
```

### Optimization Wins Database
```json
{
  "optimization_id": "unique-identifier",
  "property": "ModeFreeFinds|ModeMarketMunchies|etc",
  "test_type": "A/B|Multivariate|Copy Change",
  "baseline_metric": "previous_value",
  "optimized_metric": "new_value",
  "improvement_percent": "percentage_change",
  "implementation_details": "what_was_changed",
  "date_implemented": "YYYY-MM-DD",
  "revenue_impact": "dollar_amount"
}
```

## Code Snippet Organization

### Reusable Patterns
- **URL Parameter Passing**: Dynamic source attribution
- **Field Prepopulation**: LeadPages form optimization  
- **Tune Integration**: Revenue attribution validation
- **Dynamic Content**: Personalization based on traffic source

### Testing Framework
- **A/B Test Setup**: Statistical significance tracking
- **Conversion Tracking**: Event-based analytics
- **Performance Monitoring**: Page speed and UX metrics

This structure will help you maintain organization across 4 different properties while building a knowledge base of what works for future optimization projects! 