# Testing utm_source → aff_sub3 Implementation

## ✅ DEPLOYED: Oct 2, 2025

### What Was Implemented:
1. **Frontend (popup.js):** Appends `&aff_sub3={source}` to Tune URLs
2. **Backend (tune_api_integration.py):** Requests `aff_sub3` field from Tune API

---

## Manual Testing Steps:

### Test 1: Popup with utm_source parameter
1. Open: https://mode-thankyou.netlify.app/?utm_source=meta_test
2. Open browser DevTools (F12) → Console tab
3. Wait for popup to appear
4. Click any campaign CTA button
5. **VERIFY:** New tab opens with URL containing `&aff_sub3=meta_test`

**Expected URL format:**
```
https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946&aff_sub3=meta_test
```

### Test 2: Popup without utm_source (default)
1. Open: https://mode-thankyou.netlify.app/
2. Click any campaign CTA button
3. **VERIFY:** URL contains `&aff_sub3=direct`

### Test 3: Different traffic sources
- `?utm_source=facebook` → `&aff_sub3=facebook`
- `?utm_source=google_ads` → `&aff_sub3=google_ads`
- `?source=affiliate` → `&aff_sub3=affiliate`

### Test 4: Tune API reporting (24 hours later)
1. Login to HasOffers dashboard
2. Navigate to Reports
3. Check if `aff_sub3` column appears
4. Verify traffic sources are segmented

---

## Rollback Instructions:

If popup breaks or errors occur:

```bash
cd /Users/brianlapp/Documents/GitHub/mode
./ROLLBACK_IF_BROKEN.sh
```

This will:
- Revert to commit `0deb21f` (before utm_source)
- Restore campaigns
- Test that site is working

---

## Console Debug Commands:

```javascript
// Check what source is being captured
console.log(document.querySelector('script[src*="popup.js"]'));

// Manually test URL building
const testUrl = "https://track.modemobile.com/aff_c?offer_id=123&aff_id=456";
const source = "meta_test";
const separator = testUrl.includes('?') ? '&' : '?';
const trackingUrl = `${testUrl}${separator}aff_sub3=${encodeURIComponent(source)}`;
console.log(trackingUrl);
// Should output: https://track.modemobile.com/aff_c?offer_id=123&aff_id=456&aff_sub3=meta_test
```

---

## What to Look For:

### ✅ SUCCESS Indicators:
- Popup loads normally
- Clicking campaigns opens new tab
- URL includes `&aff_sub3=` parameter
- Source value matches utm_source from URL
- No JavaScript errors in console
- Impression tracking still works

### ❌ FAILURE Indicators:
- Popup doesn't load (white screen)
- Clicking campaigns does nothing
- JavaScript errors in console
- "ModePopup is not defined" error
- URLs don't include aff_sub3

---

## Current Status:

**Frontend Changes:**
- File: `popup-system/scripts/popup.js`
- Lines: 550-553 (handleCTAClick function)
- Change: Appends aff_sub3 to Tune URL before opening

**Backend Changes:**
- File: `popup-system/api/tune_api_integration.py`  
- Lines: 30, 33
- Change: Added 'Stat.aff_sub3' to fields and group_by

**Commit Hash:** `dafb46f`
**Previous Working:** `0deb21f`

---

## Next Steps:

1. ✅ Test popup works (basic functionality)
2. ⏳ Test utm_source is captured and appended
3. ⏳ Verify URLs contain aff_sub3
4. ⏳ Wait 24 hours for Tune dashboard data
5. ⏳ Check if traffic is segmented by source
6. ⏳ Calculate CPL by traffic source

---

**Created:** Oct 2, 2025 6:43pm  
**Status:** Deployed, awaiting testing  
**Rollback:** Ready if needed

