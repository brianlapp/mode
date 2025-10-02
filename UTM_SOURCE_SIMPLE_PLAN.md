# utm_source → aff_sub3 Implementation Plan
**Simple 4-Line Fix | 30 Minutes | Low Risk**

## Current State ✅
- Frontend ALREADY captures `utm_source` from URLs
- Backend ALREADY stores it in `source` column
- Database ALREADY has `source` column in clicks/impressions tables
- Tune API client ALREADY makes requests

## What We Need (Literally 4 Lines)

### 1. Frontend: Append to Tune URL (2 lines)
**File:** `popup-system/scripts/popup.js`
**Location:** In `handleCTAClick()` function (~line 720)

```javascript
// BEFORE (current):
window.open(campaign.tune_url, '_blank');

// AFTER (add 2 lines):
const source = this.trackingData.source || 'direct';
const trackingUrl = `${campaign.tune_url}&aff_sub3=${encodeURIComponent(source)}`;
window.open(trackingUrl, '_blank');
```

### 2. Backend: Request aff_sub3 from Tune API (2 lines)
**File:** `popup-system/api/tune_api_integration.py`
**Location:** In `_make_hasoffers_request()` method (~line 50)

```python
# BEFORE (current):
'fields[]': ['Stat.clicks', 'Stat.conversions', 'Stat.payout', 'Stat.revenue', 'Stat.offer_id'],
'group_by[]': ['Stat.offer_id'],

# AFTER (add aff_sub3):
'fields[]': ['Stat.clicks', 'Stat.conversions', 'Stat.payout', 'Stat.revenue', 'Stat.offer_id', 'Stat.aff_sub3'],
'group_by[]': ['Stat.offer_id', 'Stat.aff_sub3'],
```

## That's It! 🎉

The `source` field is already being captured and stored. We're just:
1. Appending it to Tune URLs
2. Requesting it back from Tune API for reports

---

## Testing Checklist

### Local Test (5 mins):
```bash
# 1. Check imports work
python -c "from popup-system.api.main import app; print('✅ Imports OK')"

# 2. Start local server
cd popup-system/api && uvicorn main:app --reload

# 3. Test popup with utm_source
# Open: http://localhost:8000/api/campaigns/mff
# Open popup with: ?utm_source=test_meta
# Click campaign → verify URL includes &aff_sub3=test_meta
```

### Production Test (10 mins):
```bash
# 1. Deploy to Railway (auto-deploys on push)
git add -A
git commit -m "feat: Map utm_source to aff_sub3 for Tune reporting"
git push

# 2. Wait 60 seconds for Railway deployment

# 3. Test production popup
# Open: https://mode-thankyou.netlify.app/?utm_source=meta_test
# Click any campaign
# Verify opened URL includes: &aff_sub3=meta_test

# 4. Check Railway logs for errors
# https://railway.app → mode-dash-production → Deployments → View Logs

# 5. Verify campaigns still work
curl https://mode-dash-production.up.railway.app/api/campaigns/mff | jq length
# Should return: 6
```

### Tune Dashboard Test (24 hours later):
1. Login to HasOffers dashboard
2. Navigate to Reports
3. Check if `aff_sub3` column shows traffic sources
4. Verify "meta" vs "direct" vs other sources appearing

---

## Rollback Plan (If Something Breaks)

```bash
# Revert the changes
cd /Users/brianlapp/Documents/GitHub/mode
git log --oneline -3  # Find commit hash before utm_source
git revert HEAD --no-commit
git commit -m "Rollback utm_source implementation"
git push

# Wait 60 seconds for Railway

# Verify site working
curl https://mode-dash-production.up.railway.app/api/campaigns/mff | jq length
```

---

## Files Being Modified

1. **popup-system/scripts/popup.js** (2 lines)
   - Risk: LOW
   - Already has trackingData.source
   - Just appending to URL before opening

2. **popup-system/api/tune_api_integration.py** (2 lines)
   - Risk: LOW  
   - Just requesting additional field from API
   - No database changes
   - No logic changes

**NO changes to:**
- ❌ Database schema (already has source column)
- ❌ Campaign data (stays untouched)
- ❌ Property settings (stays untouched)
- ❌ Import statements (no new imports needed)
- ❌ Emergency restore (disabled, won't trigger)

---

## What This Achieves

### Before:
```
Meta Ads traffic → popup.js captures utm_source=meta
                 → Stored in DB as source='meta'
                 → Tune URL: ...?offer_id=7521&aff_id=43092
                 → Tune reports: All traffic looks the same
```

### After:
```
Meta Ads traffic → popup.js captures utm_source=meta
                 → Stored in DB as source='meta'  
                 → Tune URL: ...?offer_id=7521&aff_id=43092&aff_sub3=meta
                 → Tune reports: Shows traffic by source
                 → Can calculate: Meta CPL = $7.50, Affiliate CPL = $1.50
```

---

## Why This is Safe

1. **No database migrations** - source column already exists
2. **No imports added** - all functions already imported
3. **No new endpoints** - using existing tracking
4. **Backward compatible** - defaults to 'direct' if no utm_source
5. **Frontend only adds parameter** - doesn't break if backend fails
6. **Backend only requests field** - Tune API already supports it
7. **Emergency restore disabled** - won't accidentally trigger
8. **Golden backup exists** - can restore if needed

---

## Timeline

**Now (when you're available):**
- [ ] Read this plan
- [ ] Make the 4 line changes
- [ ] Test locally (5 mins)
- [ ] Commit and push
- [ ] Wait for Railway deploy (60 seconds)
- [ ] Test production (10 mins)
- [ ] Monitor for 1 hour

**Tomorrow:**
- [ ] Check Railway logs for any errors
- [ ] Test a few more clicks with different utm_sources
- [ ] Verify tracking data in database

**Next Week:**
- [ ] Check Tune dashboard for aff_sub3 data
- [ ] Calculate CPL by traffic source
- [ ] Celebrate differentiating $7.50 CPL from $1.50 CPL! 🎉

---

## If You See This Error:

**"ModePopup is not defined"**
→ Problem with popup.js syntax. Revert immediately.

**"500 Internal Server Error"**  
→ Check Railway logs. Might be Python syntax error.

**"CORS policy error"**
→ Backend crashed. Check Railway logs for Python traceback.

**"Campaigns missing"**
→ Emergency restore triggered somehow. Call `/api/emergency-restore-12-campaigns`

**"Tune API error"**
→ Tune API might not support aff_sub3. Check Tune API docs.

---

## Success Criteria

✅ Popup still loads  
✅ Campaigns still display  
✅ Clicks still track  
✅ Tune URLs include &aff_sub3={source}  
✅ Tune API returns aff_sub3 field  
✅ Can segment traffic by source in reports  
✅ Zero production incidents  

---

**Created:** Oct 2, 2025 6:15pm  
**Status:** Ready to implement  
**Risk Level:** LOW  
**Estimated Time:** 30 minutes total  
**Complexity:** 4 lines of code

