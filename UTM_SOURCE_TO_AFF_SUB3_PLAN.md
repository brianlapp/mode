# UTM Source → Tune aff_sub3 Mapping Implementation Plan

## 🎯 Goal
Map `utm_source` values from incoming URLs into Tune API's `aff_sub3` parameter for detailed traffic source reporting.

## 📊 Why This Matters
- Track which traffic sources (Meta Ads, Affiliates, Email) drive best performance
- Separate $1.50 CPL affiliate traffic from $7.50 CPL Meta traffic in reporting
- Optimize campaigns based on actual source performance data
- Justify budget allocation across channels

---

## 🗺️ Data Flow Architecture

```
Incoming URL with utm_source
    ↓
JavaScript captures utm_source on page load
    ↓
Store in sessionStorage (persist across thank-you page)
    ↓
User sees popup → Impression tracked with utm_source
    ↓
User clicks campaign → Click tracked with utm_source
    ↓
Append aff_sub3=utm_source to Tune tracking URL
    ↓
Tune records conversion with aff_sub3 value
    ↓
Pull Tune reports with aff_sub3 field
    ↓
Dashboard shows performance by traffic source
```

---

## 📋 PHASE 1: Capture UTM Source

### 1.1 JavaScript URL Parameter Capture

**File:** `/popup-system/static/popup.js` (or new `utm-tracker.js`)

```javascript
/**
 * UTM Source Tracker
 * Captures utm_source from URL and persists for tracking
 */
class UTMTracker {
    constructor() {
        this.storageKey = 'mode_utm_source';
        this.init();
    }
    
    init() {
        // Capture utm_source from current URL
        const urlParams = new URLSearchParams(window.location.search);
        const utmSource = urlParams.get('utm_source');
        
        if (utmSource) {
            // Store in sessionStorage (persists across page loads in session)
            sessionStorage.setItem(this.storageKey, utmSource);
            
            // Also store in localStorage with timestamp for longer tracking
            const trackingData = {
                source: utmSource,
                timestamp: Date.now(),
                landing_page: window.location.pathname
            };
            localStorage.setItem(this.storageKey, JSON.stringify(trackingData));
        }
    }
    
    getSource() {
        // Try sessionStorage first (most recent)
        let source = sessionStorage.getItem(this.storageKey);
        
        // Fallback to localStorage
        if (!source) {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                try {
                    const data = JSON.parse(stored);
                    // Use if less than 24 hours old
                    if (Date.now() - data.timestamp < 86400000) {
                        source = data.source;
                    }
                } catch (e) {
                    console.error('Error parsing UTM data:', e);
                }
            }
        }
        
        return source || 'direct'; // Default to 'direct' if no source found
    }
    
    // Clear tracking data (optional, for testing)
    clear() {
        sessionStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.storageKey);
    }
}

// Initialize on page load
const utmTracker = new UTMTracker();
```

### 1.2 Integration Points

**LeadPages Signup Pages:**
- Add `utm-tracker.js` to global scripts
- Ensure utm_source persists from ad click → signup → thank-you page

**Thank-You Pages (Netlify):**
- Popup.js already loads here
- Add UTM tracker initialization before popup init
- Include utm_source in impression/click tracking calls

---

## 📋 PHASE 2: Database Schema Updates

### 2.1 Add utm_source to Tracking Tables

**File:** `/popup-system/api/database.py`

```python
def init_db():
    """Initialize database with updated schema"""
    conn = get_db_connection()
    
    # Update impressions table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS impressions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            property_code TEXT NOT NULL,
            placement TEXT DEFAULT 'thankyou',
            utm_source TEXT DEFAULT 'direct',  -- NEW: Traffic source
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)
    
    # Update clicks table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            property_code TEXT NOT NULL,
            placement TEXT DEFAULT 'thankyou',
            utm_source TEXT DEFAULT 'direct',  -- NEW: Traffic source
            aff_sub3 TEXT,  -- NEW: Tune parameter value
            revenue_estimate REAL DEFAULT 0.45,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)
    
    conn.commit()
    conn.close()
```

### 2.2 Migration for Existing Tables

**File:** `/popup-system/api/migrations/add_utm_tracking.py`

```python
def migrate_add_utm_source():
    """Add utm_source columns to existing tables"""
    conn = get_db_connection()
    
    try:
        # Check if columns already exist
        cursor = conn.execute("PRAGMA table_info(impressions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'utm_source' not in columns:
            conn.execute("ALTER TABLE impressions ADD COLUMN utm_source TEXT DEFAULT 'direct'")
            print("✅ Added utm_source to impressions table")
        
        cursor = conn.execute("PRAGMA table_info(clicks)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'utm_source' not in columns:
            conn.execute("ALTER TABLE clicks ADD COLUMN utm_source TEXT DEFAULT 'direct'")
            print("✅ Added utm_source to clicks table")
            
        if 'aff_sub3' not in columns:
            conn.execute("ALTER TABLE clicks ADD COLUMN aff_sub3 TEXT")
            print("✅ Added aff_sub3 to clicks table")
        
        conn.commit()
        print("✅ Migration completed successfully")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()
```

---

## 📋 PHASE 3: Update Tracking Endpoints

### 3.1 Impression Tracking with utm_source

**File:** `/popup-system/api/main.py`

```python
@app.post("/api/impression")
async def track_impression(request: Request):
    """Track popup impression with utm_source"""
    try:
        data = await request.json()
        campaign_id = data.get('campaign_id')
        property_code = data.get('property_code', 'unknown')
        utm_source = data.get('utm_source', 'direct')  # NEW: Accept utm_source from frontend
        
        from database import get_db_connection
        conn = get_db_connection()
        
        # Insert impression with utm_source
        conn.execute("""
            INSERT INTO impressions (campaign_id, property_code, placement, utm_source, timestamp)
            VALUES (?, ?, 'thankyou', ?, CURRENT_TIMESTAMP)
        """, (campaign_id, property_code, utm_source))
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success", 
            "message": "Impression tracked",
            "utm_source": utm_source
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to track impression: {e}"}
```

### 3.2 Click Tracking with aff_sub3

**File:** `/popup-system/api/main.py`

```python
@app.post("/api/click")
async def track_click(request: Request):
    """Track popup click with utm_source and aff_sub3"""
    try:
        data = await request.json()
        campaign_id = data.get('campaign_id')
        property_code = data.get('property_code', 'unknown')
        utm_source = data.get('utm_source', 'direct')  # NEW: Accept utm_source
        
        from database import get_db_connection
        conn = get_db_connection()
        
        # Get campaign details to build Tune URL
        campaign = conn.execute(
            "SELECT * FROM campaigns WHERE id = ?", 
            (campaign_id,)
        ).fetchone()
        
        if campaign:
            # Build Tune tracking URL with aff_sub3
            tune_url = (
                f"https://track.modemobile.com/aff_ad?"
                f"campaign_id={campaign['tune_campaign_id']}&"
                f"aff_id={campaign['tune_aff_id']}&"
                f"aff_sub3={utm_source}&"  # NEW: Pass utm_source as aff_sub3
                f"format=iframe"
            )
            
            # Store click with utm_source and aff_sub3
            conn.execute("""
                INSERT INTO clicks (campaign_id, property_code, placement, utm_source, aff_sub3, revenue_estimate, timestamp)
                VALUES (?, ?, 'thankyou', ?, ?, 0.45, CURRENT_TIMESTAMP)
            """, (campaign_id, property_code, utm_source, utm_source))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success", 
                "message": "Click tracked",
                "utm_source": utm_source,
                "aff_sub3": utm_source,
                "redirect_url": tune_url
            }
        else:
            return {"status": "error", "message": "Campaign not found"}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to track click: {e}"}
```

### 3.3 Frontend Click Handler Update

**File:** `/popup-system/static/popup.js`

```javascript
async function trackClick(campaignId, propertyCode) {
    // Get utm_source from tracker
    const utmSource = utmTracker.getSource();
    
    try {
        const response = await fetch(`${API_BASE}/api/click`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                campaign_id: campaignId,
                property_code: propertyCode,
                utm_source: utmSource  // NEW: Send utm_source to backend
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success' && data.redirect_url) {
            // Open Tune campaign URL with aff_sub3 parameter
            window.open(data.redirect_url, '_blank');
        }
        
        return data;
    } catch (error) {
        console.error('Click tracking error:', error);
    }
}

async function trackImpression(campaignId, propertyCode) {
    // Get utm_source from tracker
    const utmSource = utmTracker.getSource();
    
    try {
        await fetch(`${API_BASE}/api/impression`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                campaign_id: campaignId,
                property_code: propertyCode,
                utm_source: utmSource  // NEW: Send utm_source to backend
            })
        });
    } catch (error) {
        console.error('Impression tracking error:', error);
    }
}
```

---

## 📋 PHASE 4: Tune API Integration Updates

### 4.1 Request aff_sub3 in Tune Reports

**File:** `/popup-system/api/tune_api_integration.py`

```python
def _make_hasoffers_request(self, method: str = 'getStats', **additional_params) -> Dict:
    """Make authenticated request with aff_sub3 field"""
    
    params = {
        'NetworkToken': self.api_key,
        'Target': 'Report',
        'Method': method,
        'fields[]': [
            'Stat.clicks', 
            'Stat.conversions', 
            'Stat.payout', 
            'Stat.revenue', 
            'Stat.offer_id',
            'Stat.aff_sub3'  # NEW: Request aff_sub3 (utm_source) from Tune
        ],
        'filters[Stat.offer_id][conditional]': 'EQUAL_TO',
        'filters[Stat.offer_id][values][]': popup_offer_ids,
        'group_by[]': ['Stat.offer_id', 'Stat.aff_sub3'],  # NEW: Group by source
        'totals': 1,
        'limit': 1000,
        **additional_params
    }
    
    # Rest of implementation...
```

### 4.2 Process aff_sub3 in Reports

```python
def get_stats_by_source(self, start_date: str = None, end_date: str = None) -> Dict:
    """
    Get statistics grouped by traffic source (aff_sub3)
    """
    api_result = self._make_hasoffers_request(
        method='getStats',
        data_start=start_date or (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        data_end=end_date or datetime.now().strftime('%Y-%m-%d')
    )
    
    if not api_result.get('success'):
        return {'success': False, 'error': api_result.get('error')}
    
    # Extract data grouped by aff_sub3 (utm_source)
    raw_data = api_result['raw_data']
    campaign_data = raw_data['response']['data'].get('data', [])
    
    source_performance = {}
    
    for row in campaign_data:
        stats = row.get('Stat', {})
        source = stats.get('aff_sub3', 'direct')
        
        if source not in source_performance:
            source_performance[source] = {
                'clicks': 0,
                'conversions': 0,
                'revenue': 0,
                'payout': 0
            }
        
        source_performance[source]['clicks'] += int(stats.get('clicks', 0))
        source_performance[source]['conversions'] += int(stats.get('conversions', 0))
        source_performance[source]['revenue'] += float(stats.get('revenue', 0))
        source_performance[source]['payout'] += float(stats.get('payout', 0))
    
    return {
        'success': True,
        'by_source': source_performance,
        'source': 'Tune API with aff_sub3'
    }
```

---

## 📋 PHASE 5: Reporting Dashboard Updates

### 5.1 New Analytics Endpoint - By Source

**File:** `/popup-system/api/main.py`

```python
@app.get("/api/analytics/by-source")
async def analytics_by_source(
    preset: str = "last_7_days",
    property: str = "all",
    start_date: str = None,
    end_date: str = None
):
    """Get analytics grouped by traffic source (utm_source)"""
    
    try:
        from database import get_db_connection
        import datetime as dt
        
        # Parse date range
        if preset == "last_7_days":
            start = (dt.datetime.now() - dt.timedelta(days=7)).strftime('%Y-%m-%d')
            end = dt.datetime.now().strftime('%Y-%m-%d')
        elif preset == "last_30_days":
            start = (dt.datetime.now() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
            end = dt.datetime.now().strftime('%Y-%m-%d')
        else:
            start = start_date
            end = end_date
        
        conn = get_db_connection()
        
        # Get impressions by source
        impressions_query = """
            SELECT 
                utm_source,
                COUNT(*) as impressions
            FROM impressions
            WHERE timestamp BETWEEN ? AND ?
        """
        
        if property != "all":
            impressions_query += " AND property_code = ?"
            impressions_params = (start, end, property)
        else:
            impressions_params = (start, end)
        
        impressions_query += " GROUP BY utm_source"
        
        impressions_data = conn.execute(impressions_query, impressions_params).fetchall()
        
        # Get clicks by source
        clicks_query = """
            SELECT 
                utm_source,
                COUNT(*) as clicks,
                SUM(revenue_estimate) as revenue
            FROM clicks
            WHERE timestamp BETWEEN ? AND ?
        """
        
        if property != "all":
            clicks_query += " AND property_code = ?"
            clicks_params = (start, end, property)
        else:
            clicks_params = (start, end)
        
        clicks_query += " GROUP BY utm_source"
        
        clicks_data = conn.execute(clicks_query, clicks_params).fetchall()
        
        # Combine data
        source_stats = {}
        
        for row in impressions_data:
            source = row['utm_source']
            source_stats[source] = {
                'source': source,
                'impressions': row['impressions'],
                'clicks': 0,
                'revenue': 0,
                'ctr': 0,
                'rpm': 0,
                'rpc': 0
            }
        
        for row in clicks_data:
            source = row['utm_source']
            if source not in source_stats:
                source_stats[source] = {
                    'source': source,
                    'impressions': 0,
                    'clicks': 0,
                    'revenue': 0
                }
            
            source_stats[source]['clicks'] = row['clicks']
            source_stats[source]['revenue'] = round(row['revenue'] or 0, 2)
            
            # Calculate metrics
            impressions = source_stats[source]['impressions']
            clicks = source_stats[source]['clicks']
            revenue = source_stats[source]['revenue']
            
            if impressions > 0:
                source_stats[source]['ctr'] = round((clicks / impressions) * 100, 2)
                source_stats[source]['rpm'] = round((revenue / impressions) * 1000, 2)
            
            if clicks > 0:
                source_stats[source]['rpc'] = round(revenue / clicks, 2)
        
        conn.close()
        
        return {
            'success': True,
            'period': f"{start} to {end}",
            'data': list(source_stats.values()),
            'summary': {
                'total_sources': len(source_stats),
                'total_impressions': sum(s['impressions'] for s in source_stats.values()),
                'total_clicks': sum(s['clicks'] for s in source_stats.values()),
                'total_revenue': round(sum(s['revenue'] for s in source_stats.values()), 2)
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
```

### 5.2 Dashboard UI - Traffic Source Section

**File:** `/popup-system/dashboard/src/components/SourcePerformance.tsx` (or similar)

```javascript
// React/Vue component for traffic source dashboard

function SourcePerformanceTable({ data }) {
    return (
        <div className="source-performance">
            <h3>📊 Performance by Traffic Source</h3>
            <table>
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Impressions</th>
                        <th>Clicks</th>
                        <th>CTR</th>
                        <th>Revenue</th>
                        <th>RPM</th>
                        <th>RPC</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map(source => (
                        <tr key={source.source}>
                            <td><strong>{source.source}</strong></td>
                            <td>{source.impressions.toLocaleString()}</td>
                            <td>{source.clicks.toLocaleString()}</td>
                            <td>{source.ctr}%</td>
                            <td>${source.revenue}</td>
                            <td>${source.rpm}</td>
                            <td>${source.rpc}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            
            {/* Highlight key insights */}
            <div className="insights">
                <div className="insight meta">
                    <h4>🎯 Meta Ads Performance</h4>
                    <p>CPL: ${calculateCPL(data, 'meta')}</p>
                    <p>Revenue: ${getSourceRevenue(data, 'meta')}</p>
                </div>
                
                <div className="insight affiliate">
                    <h4>🤝 Affiliate Performance</h4>
                    <p>CPL: ${calculateCPL(data, 'affiliate')}</p>
                    <p>Revenue: ${getSourceRevenue(data, 'affiliate')}</p>
                </div>
                
                <div className="insight email">
                    <h4>📧 Email Performance</h4>
                    <p>RPM: ${getSourceRPM(data, 'email')}</p>
                    <p>Revenue: ${getSourceRevenue(data, 'email')}</p>
                </div>
            </div>
        </div>
    );
}
```

---

## 📋 PHASE 6: Testing & Validation

### 6.1 Test URLs

Create test campaigns with specific utm_source values:

```
# Meta Ads Test
https://join.modefreefinds.com/mff-signup-affiliate/?utm_source=meta_cold_traffic

# Affiliate Traffic Test  
https://join.modefreefinds.com/mff-signup-affiliate/?utm_source=affiliate_partner_123

# Email Campaign Test
https://join.modefreefinds.com/mff-signup-affiliate/?utm_source=email_newsletter_oct
```

### 6.2 Validation Checklist

- [ ] UTM tracker captures utm_source correctly
- [ ] utm_source persists from landing page → thank-you page
- [ ] Impressions tracked with correct utm_source
- [ ] Clicks tracked with correct utm_source
- [ ] Tune URL includes aff_sub3 parameter
- [ ] Tune API returns aff_sub3 in reports
- [ ] Dashboard shows traffic source breakdown
- [ ] Meta vs Affiliate performance clearly visible
- [ ] Revenue attribution matches Tune dashboard

### 6.3 Data Quality Checks

```python
# Run this query to verify utm_source tracking
def validate_utm_tracking():
    """Validate utm_source is being tracked correctly"""
    conn = get_db_connection()
    
    # Check unique sources
    sources = conn.execute("""
        SELECT DISTINCT utm_source, COUNT(*) as count
        FROM impressions
        GROUP BY utm_source
        ORDER BY count DESC
    """).fetchall()
    
    print("📊 UTM Sources in Database:")
    for row in sources:
        print(f"  - {row['utm_source']}: {row['count']} impressions")
    
    # Check for missing sources
    missing = conn.execute("""
        SELECT COUNT(*) as count
        FROM impressions
        WHERE utm_source IS NULL OR utm_source = ''
    """).fetchone()
    
    if missing['count'] > 0:
        print(f"⚠️  Warning: {missing['count']} impressions missing utm_source")
    
    conn.close()
```

---

## 🚀 Deployment Strategy

### Pre-Deployment
1. **Create database backup**
   ```bash
   cp /path/to/production.db /path/to/backup_before_utm_tracking.db
   ```

2. **Test in development environment**
   - Run migration on dev database
   - Test full flow: URL → capture → track → report
   - Verify no breaking changes

3. **Review all code changes**
   - Frontend: utm-tracker.js, popup.js updates
   - Backend: database.py, main.py, tune_api_integration.py
   - Ensure backward compatibility (existing data still works)

### Deployment Steps
1. **Deploy backend changes first** (API endpoints, database)
2. **Run database migration** (add utm_source columns)
3. **Deploy frontend changes** (utm-tracker.js, popup.js)
4. **Monitor for 24 hours** (check logs, verify tracking)
5. **Enable dashboard reporting** (once data is flowing)

### Post-Deployment
1. **Verify data flow**
   - Check that utm_source is being captured
   - Verify clicks include aff_sub3 in Tune
   - Confirm dashboard shows source breakdown

2. **Monitor for issues**
   - Check error logs
   - Verify no tracking failures
   - Ensure existing functionality still works

3. **Create documentation**
   - Document utm_source naming conventions
   - Create guide for campaign setup
   - Train team on new reporting features

---

## 📝 UTM Source Naming Conventions

Standardize utm_source values for consistent reporting:

### Meta Ads
```
utm_source=meta_cold_traffic
utm_source=meta_retargeting
utm_source=meta_lookalike
```

### Affiliate Traffic
```
utm_source=affiliate_{partner_name}
utm_source=affiliate_network_{network_name}
```

### Email Campaigns
```
utm_source=email_newsletter
utm_source=email_promotional
utm_source=email_reengagement
```

### Other Sources
```
utm_source=organic_search
utm_source=direct
utm_source=referral_{site_name}
```

---

## 💰 Expected Business Impact

### Immediate Benefits
- **Clear ROI visibility**: See exactly which traffic sources are profitable
- **Budget optimization**: Shift spend from $7.50 CPL Meta to $1.50 CPL affiliates
- **Performance tracking**: Measure impact of Meta cold traffic optimizations
- **Attribution accuracy**: Know which channels drive conversions

### Long-Term Value
- **Scaling decisions**: Confidently increase budget on profitable sources
- **Creative insights**: Test different approaches per traffic source
- **Partner negotiations**: Prove value to affiliate partners with data
- **Strategic planning**: Data-driven channel mix optimization

---

## 🔧 Maintenance & Iteration

### Regular Reviews
- **Weekly**: Check source performance, identify anomalies
- **Monthly**: Analyze trends, adjust budgets
- **Quarterly**: Review naming conventions, optimize tracking

### Future Enhancements
- Add `utm_medium`, `utm_campaign` for deeper insights
- Track full user journey across sessions
- A/B test landing pages by traffic source
- Predictive analytics for source performance

---

## ✅ Success Criteria

This implementation is successful when:

1. **Tracking Works**: 95%+ of impressions/clicks have valid utm_source
2. **Tune Integration**: aff_sub3 visible in Tune HasOffers dashboard
3. **Reporting Accurate**: Dashboard matches Tune data
4. **Business Insights**: Can answer "Which traffic source is most profitable?"
5. **Team Adoption**: Mike and team using source reports for decisions

---

## 📚 Resources & References

- **Tune HasOffers API Docs**: https://support.tune.com/hasoffers/api-documentation/
- **aff_sub Parameters**: https://support.tune.com/hasoffers/tracking-urls/#sub-id-parameters
- **UTM Best Practices**: https://ga-dev-tools.web.app/campaign-url-builder/
- **Current Tune Integration**: `/popup-system/api/tune_api_integration.py`
- **Current Dashboard**: `/popup-system/dashboard/`

---

## 🎯 Next Steps

1. **Review this plan** with Mike and team
2. **Approve implementation** approach
3. **Schedule deployment** window
4. **Execute Phase 1** (capture & database)
5. **Test thoroughly** before production
6. **Deploy & monitor** with rollback plan ready

---

**Plan Created**: October 2, 2025  
**Author**: Brian Lapp (with AI assistance)  
**Status**: Ready for Review → Implementation

