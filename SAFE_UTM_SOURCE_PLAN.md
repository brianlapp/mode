# SAFE utm_source → aff_sub3 Implementation Plan
## ✅ Lessons Learned from Production Break

### What Broke:
1. ❌ Missing imports caused API crash
2. ❌ Database schema changes not tested
3. ❌ No backup/restore verification
4. ❌ Deployed during unavailable time

### Safe Implementation Strategy:

## PHASE 1: Preparation (Do First, No Deploy)
- [ ] Create feature branch: `feature/utm-source-tracking`
- [ ] Test locally with actual database copy
- [ ] Verify all imports present
- [ ] Test rollback procedure

## PHASE 2: Database Schema (Separate PR)
**File:** `popup-system/api/database.py`
```python
# Add aff_sub3 column if missing (idempotent)
cursor = conn.execute("PRAGMA table_info(clicks)")
columns = [row[1] for row in cursor.fetchall()]

if 'aff_sub3' not in columns:
    conn.execute("ALTER TABLE clicks ADD COLUMN aff_sub3 TEXT DEFAULT 'direct'")
    conn.commit()
    print("✅ Added aff_sub3 column")
```

**Test:**
1. Deploy ONLY this change
2. Verify clicks table has aff_sub3 column
3. Verify existing tracking still works
4. Wait 24 hours, monitor for issues

## PHASE 3: Frontend Changes (Separate PR)
**File:** `popup-system/scripts/popup.js`
```javascript
// In handleCTAClick function
const utm_source = this.trackingData.source || 'direct';
const separator = campaign.tune_url.includes('?') ? '&' : '?';
const trackingUrl = `${campaign.tune_url}${separator}aff_sub3=${encodeURIComponent(utm_source)}`;
window.open(trackingUrl, '_blank');
```

**Test:**
1. Load popup with `?utm_source=test`
2. Click campaign
3. Verify opened URL includes `&aff_sub3=test`
4. Verify popup still works without utm_source

## PHASE 4: Backend Tracking (Separate PR)
**File:** `popup-system/api/routes/campaigns.py`

**CRITICAL: Add missing import FIRST**
```python
from fastapi import HTTPException, Request  # ← ADD Request HERE
```

**Then update click tracking:**
```python
@router.post("/click")
async def track_click(request: Request):
    data = await request.json()
    utm_source = data.get("source", "direct")[:100]
    
    # Store with aff_sub3 = utm_source
    conn.execute("""
        INSERT INTO clicks (..., aff_sub3)
        VALUES (..., ?)
    """, (..., utm_source))
```

**Test:**
1. Send test click with source='meta_test'
2. Query clicks table, verify aff_sub3='meta_test'
3. Verify clicks without source still work (default='direct')

## PHASE 5: Tune API Integration (Separate PR)
**File:** `popup-system/api/tune_api_integration.py`
```python
params = {
    'fields[]': [..., 'Stat.aff_sub3'],
    'group_by[]': ['Stat.offer_id', 'Stat.aff_sub3']
}
```

**Test:**
1. Call Tune API
2. Verify aff_sub3 field returned
3. Verify existing reports still work

---

## Testing Checklist (Before Each Deploy)

### Local Tests:
- [ ] `curl http://localhost:8000/api/campaigns/mff` works
- [ ] `curl http://localhost:8000/health` returns healthy
- [ ] Popup loads in browser
- [ ] Click tracking works
- [ ] Admin panel loads campaigns

### Production Tests (After Deploy):
- [ ] Wait for Railway deployment (check logs)
- [ ] Test `/api/campaigns/mff` returns 6 campaigns
- [ ] Test popup at mode-thankyou.netlify.app
- [ ] Test admin at mode-dash-production.up.railway.app
- [ ] Check Railway logs for errors

### Rollback Ready:
- [ ] Know last working commit: `90495eb`
- [ ] Backup command ready: `git revert HEAD && git push`
- [ ] Emergency restore ready: `/api/emergency-restore-12-campaigns`

---

## Safe Deployment Process

### Before Starting:
1. **You must be available** for 2 hours to monitor
2. **Check Railway status** - no ongoing incidents
3. **Verify current site working** - popup loads, campaigns show
4. **Create backup** of current working state

### During Deployment:
1. Deploy ONE phase at a time
2. Wait 5 minutes between phases
3. Test thoroughly after each phase
4. If ANY error → rollback immediately

### Emergency Contacts:
- Railway logs: Check for "ERROR" or "failed" 
- Health check: `https://mode-dash-production.up.railway.app/health`
- Campaigns test: `https://mode-dash-production.up.railway.app/api/campaigns`

---

## What NOT To Do:
- ❌ NO deploying when unavailable
- ❌ NO changing multiple files at once
- ❌ NO force-push without testing
- ❌ NO assuming backups work (test restore!)
- ❌ NO skipping import checks

---

## Emergency Rollback Commands

```bash
# If something breaks:
cd /Users/brianlapp/Documents/GitHub/mode
git log --oneline -5  # Find last working commit
git revert HEAD --no-commit
git commit -m "EMERGENCY: Rollback breaking changes"
git push

# Wait 60 seconds for Railway deployment

# Restore campaigns if needed:
curl -X POST https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns

# Verify working:
curl https://mode-dash-production.up.railway.app/api/campaigns/mff | jq length
# Should return: 6
```

---

## Timeline (When You're Back)

### Day 1: Test Locally
- Pull repo
- Create feature branch
- Implement Phase 1 (schema)
- Test on local database
- Verify no breaking changes

### Day 2: Deploy Schema Only
- Morning: Deploy Phase 1
- Monitor for 4 hours
- Afternoon: Verify stable
- Evening: Test Phase 2 locally

### Day 3: Deploy Frontend
- Morning: Deploy Phase 2 (popup.js)
- Test with `?utm_source=test`
- Monitor for 4 hours
- Verify Tune URLs include aff_sub3

### Day 4: Deploy Backend Tracking
- Morning: Deploy Phase 3
- Test click tracking
- Verify database stores aff_sub3
- Monitor for 4 hours

### Day 5: Deploy Tune API
- Morning: Deploy Phase 4
- Test Tune API calls
- Verify reports show aff_sub3
- Celebrate! 🎉

---

## Success Criteria

Implementation is successful when:
1. ✅ Popup still loads and works
2. ✅ Campaigns show in admin panel
3. ✅ Clicks tracked with utm_source
4. ✅ Tune URLs include aff_sub3 parameter
5. ✅ Tune API returns aff_sub3 data
6. ✅ Zero production incidents
7. ✅ Can calculate CPL by traffic source

---

## Current Status (Oct 2, 2025 4:40pm)

✅ **Site Working:**
- 12 campaigns restored
- Popup functional
- Admin panel working
- Money.com present (ID 1)

❌ **utm_source NOT Implemented:**
- Rolled back all changes
- No aff_sub3 tracking active
- Tune URLs do NOT include traffic source
- Reports do NOT show source breakdown

📅 **Next Session:**
- Review this plan
- Start with Phase 1 (schema only)
- Test locally first
- Deploy ONLY when available to monitor

---

**Created:** Oct 2, 2025 4:40pm  
**Status:** Ready for implementation when you return  
**Risk Level:** LOW (if following phased approach)  
**Estimated Time:** 5 days (safe, tested deployment)

