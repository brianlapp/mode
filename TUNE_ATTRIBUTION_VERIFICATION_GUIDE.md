# 📊 TUNE ATTRIBUTION VERIFICATION GUIDE

**How to verify that `utm_source` → `aff_sub3` attribution is working in Tune dashboard**

---

## 🎯 **PARAMETER CONFIRMATION:**

### **✅ YES - `aff_sub3` is CORRECT!**

**Tune/HasOffers Parameter Hierarchy:**
```
aff_sub   = Sub ID 1 (available for use)
aff_sub2  = Sub ID 2 (used by some MFF campaigns) 
aff_sub3  = Sub ID 3 ← UTM SOURCE GOES HERE
aff_sub4  = Sub ID 4 (available for use)
aff_sub5  = Sub ID 5 (used for campaign identifiers like popup_tradingTips)
```

### **🔍 Current Campaign Examples:**
```
Original: https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips

Facebook Traffic: https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips&aff_sub3=facebook

Google Traffic: https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips&aff_sub3=google

Email Traffic: https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips&aff_sub3=email
```

---

## 🧪 **IMMEDIATE VERIFICATION (Right Now!)**

### **Step 1: Test Attribution in Browser Console**
1. **Open**: https://mode-dash-production.up.railway.app/?utm_source=facebook&debug=true
2. **Press F12** → Console tab
3. **Wait for popup** → Click CTA button  
4. **Look for**: `[DEBUG] Opening attributed URL` message
5. **Verify**: `aff_sub3=facebook` in the attributedUrl

### **Step 2: Manual URL Check**
1. **Right-click** popup CTA → "Copy link address"
2. **Paste** into text editor
3. **Look for**: `&aff_sub3=facebook` parameter

---

## 📊 **TUNE DASHBOARD VERIFICATION (15-30 minutes delay)**

### **Where to Look in Tune:**
1. **Login** to your Tune/HasOffers account
2. **Navigate**: Reports → Conversions (or Clicks)
3. **Look for columns**: 
   - **Sub ID 3** or **aff_sub3** column
   - Should show: "facebook", "google", "email", etc.
4. **Filter by**: Today's date to see new attributed traffic

### **What Success Looks Like:**
```
Conversion Report:
Offer ID | Campaign | Sub ID 3 | Revenue | Date
6998     | Trading  | facebook | $0.45   | Today
7521     | Behind   | google   | $0.45   | Today  
6571     | Goodie   | email    | $0.45   | Today
```

---

## 🎯 **BUSINESS VALUE CONFIRMATION:**

### **Mike's New Attribution Power:**
- **Facebook ROI**: "Facebook popup clicks convert at $2.50 revenue each"
- **Google Performance**: "Google organic generates 40% of popup conversions"  
- **Email Effectiveness**: "Newsletter clicks have 3x higher conversion rate"
- **Budget Optimization**: "Invest more in Facebook, less in direct traffic"

### **Before vs After:**
```
BEFORE: "Someone clicked popup... 🤷‍♂️"
AFTER:  "Facebook user clicked popup and converted for $0.45! 🎯"
```

---

## ⚡ **QUICK TEST RIGHT NOW:**

**Test Facebook Attribution:**
```bash
# Open this URL and click popup CTA:
https://mode-dash-production.up.railway.app/?utm_source=facebook&utm_medium=cpc&debug=true

# Expected in browser console:
[DEBUG] Opening attributed URL {
  attributedUrl: "...&aff_sub3=facebook"
}
```

**Test Google Attribution:**  
```bash
# Open this URL and click popup CTA:
https://mode-dash-production.up.railway.app/?utm_source=google&utm_medium=organic&debug=true

# Expected in browser console:
[DEBUG] Opening attributed URL {
  attributedUrl: "...&aff_sub3=google" 
}
```

---

## 🚀 **PRODUCTION VERIFICATION COMPLETE WHEN:**

- [ ] ✅ **Browser Console**: Shows attributed URLs with aff_sub3
- [ ] ✅ **No JavaScript Errors**: Attribution works without breaking popups
- [ ] ✅ **Tune Dashboard**: Sub ID 3 column shows traffic sources  
- [ ] ✅ **Revenue Attribution**: Can filter conversions by traffic source
- [ ] ✅ **Mike's Happy**: Gets the attribution data he needs for optimization!

**The parameter `aff_sub3` is 100% correct for Tune/HasOffers! Test it now with the URLs above!** 🎯