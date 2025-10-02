# 🧪 UTM Source → aff_sub3 Testing Guide

## ✅ Implementation Complete!

We just shipped utm_source to aff_sub3 mapping in **4 simple changes**:

1. ✅ Frontend captures utm_source (was already working!)
2. ✅ Frontend appends `&aff_sub3={utm_source}` to Tune URLs
3. ✅ Backend stores aff_sub3 in clicks table
4. ✅ Tune API requests Stat.aff_sub3 field for reporting

---

## 🧪 How to Test

### Test 1: Verify UTM Capture & Tune URL Generation

**Step 1:** Visit your thank-you page with utm_source:
```
https://mode-thankyou.netlify.app/?utm_source=meta_test_campaign
```

**Step 2:** Open browser console (F12) and check:
```javascript
// The popup should capture utm_source
console.log(window.ModePopup.trackingData.source);
// Should show: "meta_test_campaign"
```

**Step 3:** Click a popup campaign CTA button

**Step 4:** Check the console debug log (if debug enabled):
```
[ModePopup] Opening Tune URL with aff_sub3: 
https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips&aff_sub3=meta_test_campaign
```

✅ **Expected:** Tune URL includes `&aff_sub3=meta_test_campaign`

---

### Test 2: Verify Database Storage

**After clicking a campaign, check the database:**

```bash
# SSH into Railway or access database
sqlite3 /app/popup-system/api/data/popup_campaigns.db

# Check latest click record
SELECT campaign_id, source, aff_sub3, timestamp 
FROM clicks 
ORDER BY timestamp DESC 
LIMIT 5;
```

✅ **Expected Output:**
```
campaign_id | source              | aff_sub3            | timestamp
------------|---------------------|---------------------|---------------------------
2           | meta_test_campaign  | meta_test_campaign  | 2025-10-02 15:58:00
```

---

### Test 3: Verify Tune HasOffers Dashboard

**After clicks with utm_source flow through:**

1. Log into Tune HasOffers dashboard: `https://currentpublisher.api.hasoffers.com`
2. Go to **Reports** → **Conversions** or **Performance**
3. Add column: **Sub ID 3** (aff_sub3)
4. Filter by your popup offer IDs: 6998, 7521, 7389, 7385, 7390

✅ **Expected:** You'll see aff_sub3 values like:
- `meta_test_campaign`
- `affiliate_partner_123`
- `email_newsletter`
- `direct` (for traffic without utm_source)

---

### Test 4: Different Traffic Sources

Test with different utm_source values to verify segmentation:

**Meta Ads:**
```
?utm_source=meta_cold_traffic
?utm_source=meta_retargeting
?utm_source=meta_lookalike
```

**Affiliate Traffic:**
```
?utm_source=affiliate_partner_name
?utm_source=affiliate_network_123
```

**Email Campaigns:**
```
?utm_source=email_newsletter
?utm_source=email_promotional
```

**Direct Traffic (no utm_source):**
```
https://mode-thankyou.netlify.app/
```
- Should default to `aff_sub3=direct`

---

### Test 5: Verify Tune API Reports

**Run a test API call to verify aff_sub3 is returned:**

```python
# In Python shell or test script
from popup-system.api.tune_api_integration import tune_client

# Get stats (will now include aff_sub3)
result = tune_client.get_stats()

# Check if aff_sub3 is in the response
print(result['raw_data']['response']['data'])

# Should see Stat.aff_sub3 field in each record
```

✅ **Expected:** Response includes aff_sub3 values for each conversion

---

## 🎯 Real-World Testing Scenarios

### Scenario 1: Meta Ads Campaign

1. Create Meta ad with utm_source:
   ```
   https://join.modefreefinds.com/mff-signup-affiliate/?utm_source=meta_oct_2025
   ```

2. User completes signup → lands on thank-you page (utm_source persists in URL)

3. Popup shows → user clicks campaign

4. Check Tune dashboard → conversions show `aff_sub3=meta_oct_2025`

5. Calculate Meta CPL from Tune data filtered by aff_sub3

---

### Scenario 2: Affiliate Traffic

1. Affiliate sends traffic with their ID:
   ```
   ?utm_source=affiliate_partner_abc
   ```

2. Same flow as above

3. Tune shows separate conversions for `aff_sub3=affiliate_partner_abc`

4. Compare Meta CPL ($7.50) vs Affiliate CPL ($1.50)

---

### Scenario 3: Email Campaign

1. Email link includes:
   ```
   ?utm_source=email_oct_newsletter
   ```

2. Track email-driven conversions separately

3. Measure email campaign ROI with aff_sub3 data

---

## 📊 Expected Business Impact

Once data flows through, you'll be able to answer:

### Question 1: "What's our CPL by traffic source?"
```sql
SELECT 
    aff_sub3 as traffic_source,
    COUNT(*) as clicks,
    SUM(revenue_estimate) as revenue,
    SUM(revenue_estimate) / COUNT(*) as cpl
FROM clicks
WHERE aff_sub3 IN ('meta_cold_traffic', 'affiliate_partner', 'email_newsletter')
GROUP BY aff_sub3
ORDER BY cpl DESC;
```

### Question 2: "Which source is most profitable?"
Check Tune dashboard grouped by aff_sub3 - compare:
- Meta: ~$7.50 CPL
- Affiliate: ~$1.50 CPL  
- Email: TBD
- Direct: TBD

### Question 3: "Where should we invest more budget?"
Based on aff_sub3 performance data, allocate more to profitable sources!

---

## 🔧 Troubleshooting

### Issue: aff_sub3 showing as NULL in database

**Cause:** Frontend not passing source parameter

**Fix:** Check browser console:
```javascript
console.log(window.ModePopup.trackingData);
// Should show: { source: 'your_utm_source', ... }
```

---

### Issue: Tune URL doesn't include aff_sub3

**Cause:** Old popup.js cached in browser

**Fix:** Hard refresh (Cmd+Shift+R or Ctrl+F5)
- Or clear browser cache
- Or add cache-busting: `popup.js?v=2`

---

### Issue: Tune dashboard doesn't show aff_sub3

**Cause:** Column not added to report view

**Fix:** In Tune dashboard:
1. Go to Reports
2. Click "Customize Columns"
3. Add "Sub ID 3" (aff_sub3)
4. Save view

---

### Issue: All traffic showing as "direct"

**Cause:** UTM parameters not in URL

**Fix:** 
- Ensure your Meta ads include utm_source
- Check LeadPages preserves URL parameters
- Test with manual URL: `?utm_source=test`

---

## ✅ Success Criteria

Implementation is successful when:

1. ✅ Popup captures utm_source from URL (check console)
2. ✅ Tune URLs include `&aff_sub3={utm_source}` (check opened link)
3. ✅ Database stores aff_sub3 (check clicks table)
4. ✅ Tune API returns aff_sub3 (check API response)
5. ✅ Tune dashboard shows traffic sources (check reports)
6. ✅ Can calculate CPL by source (run analytics query)

---

## 🚀 Next Steps

After verifying everything works:

1. **Add utm_source to all Meta campaigns**
   - Format: `utm_source=meta_{campaign_name}`
   - Example: `utm_source=meta_cold_oct_2025`

2. **Tag affiliate traffic**
   - Format: `utm_source=affiliate_{partner_name}`
   - Example: `utm_source=affiliate_network_abc`

3. **Tag email campaigns**
   - Format: `utm_source=email_{type}`
   - Example: `utm_source=email_newsletter_weekly`

4. **Build dashboard reports**
   - Add "Traffic Source Performance" section
   - Show CPL, conversions, revenue by source
   - Compare Meta vs Affiliate vs Email vs Direct

5. **Optimize based on data**
   - Increase budget on profitable sources
   - Reduce spend on expensive sources
   - Test new sources with utm_source tracking

---

## 📞 Questions?

If something isn't working:

1. Check browser console for JavaScript errors
2. Verify popup.js has latest code (check git commit)
3. Test with manual utm_source parameter
4. Check database for aff_sub3 column existence
5. Verify Tune API includes aff_sub3 in request

---

**Implementation Date:** October 2, 2025  
**Git Commit:** c4b586a  
**Status:** ✅ Deployed to GitHub, ready for Railway deployment  
**Estimated Impact:** Clear $7.50 vs $1.50 CPL visibility → Better budget allocation

