# 🚨 CRITICAL AGENT RULES - READ THIS OR YOU'LL DESTROY EVERYTHING

## ⚠️ WARNING: THIS IS A LIVE REVENUE SYSTEM
**Mike's popup system generates REAL MONEY. Breaking it costs actual revenue. Treat this like you're handling nuclear launch codes.**

---

## 🛡️ GOLDEN RULES - NEVER BREAK THESE

### 1. **NEVER TOUCH PostgreSQL MIGRATION**
- ❌ **DO NOT** change imports from `database` to `database_postgres`
- ❌ **DO NOT** add `psycopg2-binary` to requirements.txt
- ❌ **DO NOT** try to "modernize" the database layer
- ✅ **SQLite works perfectly** - leave it alone

### 2. **CAMPAIGNS ARE SACRED**
- ❌ **NEVER DELETE** campaigns without explicit backup
- ❌ **NO PRIZIES** campaigns (corrupts the system)
- ✅ **Money.com must be first** (ID 1)
- ✅ **Exactly 12 campaigns** (5 MMM finance + 7 MFF lifestyle)
- ✅ **Use emergency restore**: `curl -X POST "https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns"`

### 3. **DATABASE LOCK PREVENTION**
- ❌ **NEVER** run multiple database operations simultaneously
- ❌ **NEVER** leave connections open
- ✅ **Always close connections**: `conn.close()`
- ✅ **If database locked**: Force fresh deployment to unlock

### 4. **POPUP IS THE HEART**
- 🎯 **Primary test URL**: https://mode-thankyou.netlify.app/
- 🎯 **API endpoint**: `/api/campaigns/mff` (must return 6+ campaigns)
- 🎯 **CORS must work** (Netlify → Railway)
- 🎯 **If popup broken, EVERYTHING is broken**

---

## 📋 BEFORE MAKING ANY CHANGES

### **MANDATORY PRE-FLIGHT CHECKS:**
1. **Test popup works**: https://mode-thankyou.netlify.app/
2. **Check campaigns count**: `curl -s "https://mode-dash-production.up.railway.app/api/campaigns" | jq '. | length'`
3. **Verify Money.com first**: `curl -s "https://mode-dash-production.up.railway.app/api/campaigns" | jq '.[0].name'`
4. **Test email PNGs**: https://mode-dash-production.up.railway.app/api/email/ad.png?property=mff

### **IF ANY OF THESE FAIL - STOP IMMEDIATELY**

---

## 🚨 EMERGENCY RECOVERY PROCEDURES

### **Symptom: Database Locked**
```bash
# Force fresh deployment
echo "# $(date)" >> popup-system/api/main.py
git add -A && git commit -m "Force restart" && git push origin main
# Wait 45 seconds, then restore campaigns
```

### **Symptom: 0 Campaigns**
```bash
curl -X POST "https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns"
```

### **Symptom: Internal Server Error**
```bash
# Restore working campaigns.py from GitHub
git checkout 855df37 -- popup-system/api/routes/campaigns.py
git add -A && git commit -m "Restore working campaigns.py" && git push origin main
```

### **Symptom: CORS Errors**
- CORS is configured correctly in main.py
- Issue is usually broken API endpoints, not CORS
- Fix the underlying API error first

---

## 📁 CRITICAL FILES - HANDLE WITH CARE

### **NEVER MODIFY THESE:**
- `popup-system/api/database.py` - Database layer (works perfectly)
- `popup-system/api/main.py` - Auto-restore logic (critical for Railway)
- `popup-system/backups/` - Backup files (lifeline when shit breaks)

### **SAFE TO MODIFY:**
- Email PNG generation code (lines 389-750 in main.py)
- Frontend dashboard files
- New endpoints (but test thoroughly)

### **MODIFY WITH EXTREME CAUTION:**
- `popup-system/api/routes/campaigns.py` - Popup depends on this
- Database queries (SQLite syntax only)
- Import statements (keep using `database`, not `database_postgres`)

---

## 🎯 THE POPUP SYSTEM ARCHITECTURE

### **Flow:**
1. **Netlify popup** (https://mode-thankyou.netlify.app/) calls Railway API
2. **Railway API** (`/api/campaigns/mff`) returns campaigns from SQLite
3. **Popup script** cycles through campaigns and tracks impressions
4. **Email system** generates PNGs from same campaign data

### **Critical Dependencies:**
- SQLite database with 12 campaigns
- CORS middleware allowing Netlify access
- Auto-restore system for Railway resets
- Campaign-property assignments (5 MMM, 7 MFF)

---

## 💰 BUSINESS CONTEXT

**This system generates Mike's revenue through:**
- Popup displays on ModeFreeFinds.com (1M+ pageviews)
- Email campaigns with PNG ads
- Tune tracking for affiliate commissions

**Every hour down = lost money. Every broken deployment = cancelled plans.**

---

## 🔧 DEBUGGING CHECKLIST

### **When Something Breaks:**

1. **Check health**: `curl https://mode-dash-production.up.railway.app/health`
2. **Check campaigns**: `curl https://mode-dash-production.up.railway.app/api/campaigns`
3. **Check popup endpoint**: `curl https://mode-dash-production.up.railway.app/api/campaigns/mff`
4. **Test actual popup**: https://mode-thankyou.netlify.app/
5. **If all fail**: Database is locked, force restart

### **Common Fixes:**
- **0 campaigns**: Run emergency restore
- **Database locked**: Force fresh deployment
- **Internal Server Error**: Restore campaigns.py from git
- **Import errors**: Check you're using `database` not `database_postgres`

---

## 🎓 LESSONS LEARNED

### **What Causes Disasters:**
1. **PostgreSQL migrations** - Complex, breaks everything
2. **"Improving" working systems** - If it works, don't touch it
3. **Complex database queries** - Simple queries = fewer bugs
4. **Multiple simultaneous changes** - Change one thing at a time

### **What Actually Works:**
1. **SQLite + auto-restore** - Bulletproof for Railway
2. **Simple API endpoints** - Less complexity = more reliability
3. **Emergency restore endpoints** - Fast recovery from disasters
4. **GitHub history** - Always have a way back

---

## 🚀 SUCCESS CRITERIA

**Before claiming victory, verify ALL of these:**
- ✅ Popup loads at https://mode-thankyou.netlify.app/
- ✅ Campaigns cycle through offers
- ✅ Dashboard shows 12 active campaigns
- ✅ Email PNGs generate properly
- ✅ Money.com is first campaign
- ✅ No database lock errors

**Only then can you say the system is working.**

---

## 🤬 FINAL WARNING

**This documentation exists because agents keep fucking up Mike's revenue system with "improvements" and "migrations" that break everything.**

**READ THIS DOCUMENT. FOLLOW THE RULES. DON'T BE THE AGENT THAT DESTROYS THE REVENUE MACHINE.**

**When in doubt: TEST THE POPUP FIRST.**