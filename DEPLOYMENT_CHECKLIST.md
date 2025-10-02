# 🚀 DEPLOYMENT CHECKLIST - MANDATORY FOR ALL CHANGES

## ⚠️ BEFORE EVERY DEPLOYMENT

### **Pre-Flight Checks (MANDATORY):**
```bash
# 1. Test popup is working
open https://mode-thankyou.netlify.app/

# 2. Check campaign count
curl -s "https://mode-dash-production.up.railway.app/api/campaigns" | jq '. | length'
# MUST return: 12

# 3. Verify Money.com is first
curl -s "https://mode-dash-production.up.railway.app/api/campaigns" | jq '.[0].name'
# MUST return: "Money.com - Online Stock Brokers"

# 4. Test MFF popup endpoint
curl -s "https://mode-dash-production.up.railway.app/api/campaigns/mff" | jq '. | length'
# MUST return: 6 or 7 (not 0, not Internal Server Error)

# 5. Test email PNG generation
curl -I "https://mode-dash-production.up.railway.app/api/email/ad.png?property=mff"
# MUST return: HTTP 200 with Content-Type: image/png
```

### **If ANY check fails - STOP DEPLOYMENT**

---

## 🚀 DEPLOYMENT PROCESS

### **Step 1: Deploy**
```bash
git add -A
git commit -m "Clear description of changes"
git push origin main
```

### **Step 2: Wait for Railway (45 seconds)**
```bash
sleep 45
```

### **Step 3: Post-Deployment Verification**
```bash
# Test health
curl -s "https://mode-dash-production.up.railway.app/health"

# If campaigns missing, restore immediately
curl -X POST "https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns"

# Verify popup works
curl -s "https://mode-dash-production.up.railway.app/api/campaigns/mff" | jq '. | length'
```

### **Step 4: Test Actual Popup**
- Open: https://mode-thankyou.netlify.app/
- Verify: Campaigns load and cycle through
- Check: No CORS errors in browser console

---

## ❌ ROLLBACK PROCEDURES

### **If Deployment Breaks System:**

#### **Option A: Quick Fix (if minor issue)**
```bash
# Fix the specific issue
# Test locally if possible
# Deploy fix
```

#### **Option B: Emergency Rollback (if major issue)**
```bash
# Restore working file from git history
git checkout LAST_WORKING_COMMIT -- path/to/broken/file.py
git add -A && git commit -m "Emergency rollback" && git push origin main

# Wait for deployment
sleep 45

# Restore campaigns
curl -X POST "https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns"
```

#### **Option C: Nuclear Option (if everything is fucked)**
```bash
# Revert entire codebase to last working commit
git reset --hard LAST_WORKING_COMMIT
git push --force origin main

# Wait for deployment
sleep 45

# Restore campaigns
curl -X POST "https://mode-dash-production.up.railway.app/api/emergency-restore-12-campaigns"
```

---

## 🔍 FINDING LAST WORKING COMMIT

```bash
# Look for commits before problems started
git log --oneline -20

# Look for commits with "working", "fix", "restore"
git log --oneline --grep="working\|fix\|restore" -10

# Check specific file history
git log --oneline -- popup-system/api/routes/campaigns.py

# Test a specific commit
git show COMMIT_HASH:popup-system/api/routes/campaigns.py | head -20
```

**Known Good Commits:**
- `855df37` - "BULLETPROOF: Add middleware auto-restore" (pre-PostgreSQL)
- Look for commits with working email PNG generation

---

## 🚨 DANGER ZONES

### **High-Risk Changes:**
- Database layer modifications
- Import statement changes  
- Requirements.txt changes
- Campaign restore logic changes
- CORS middleware changes

### **Medium-Risk Changes:**
- New API endpoints
- Campaign query modifications
- Email generation code updates

### **Low-Risk Changes:**
- Frontend dashboard updates
- Static file changes
- Documentation updates
- New utility functions

---

## 🎯 SUCCESS METRICS

**System is working when:**
- ✅ Popup loads at https://mode-thankyou.netlify.app/
- ✅ 12 campaigns in database
- ✅ Money.com is first
- ✅ Email PNGs generate
- ✅ No database locks
- ✅ No CORS errors

**System is broken when:**
- ❌ Popup shows "No campaigns" or CORS errors
- ❌ Database locked errors
- ❌ Internal Server Error on APIs
- ❌ 0 campaigns in database
- ❌ PostgreSQL import errors

---

## 💡 AGENT SURVIVAL TIPS

1. **Test before you code** - Always check current state first
2. **One change at a time** - Don't batch risky changes
3. **Have a rollback plan** - Know how to undo your changes
4. **Respect the working system** - It's working for a reason
5. **When in doubt, don't** - Ask for clarification instead of guessing

**Remember: The goal is to improve the system, not prove you're smart by rewriting everything.**

---

## 🤬 WHAT NOT TO DO (LESSONS FROM DISASTERS)

### **PostgreSQL Migration Disaster (Sept 2025):**
- Agent claimed "migration complete" but didn't update any code
- Left 43+ incompatible database calls
- System down for 3+ hours
- **Lesson**: Test your migrations thoroughly before claiming success

### **"Safety Improvements" That Broke Everything:**
- Disabled auto-restore "to prevent data loss"
- Actually caused data loss by removing the recovery mechanism
- **Lesson**: Don't fix what isn't broken

### **Import Statement Hell:**
- Changed imports without understanding dependencies
- Broke entire API layer
- **Lesson**: Map dependencies before changing imports

---

## 📞 EMERGENCY CONTACTS

**When you've fucked up beyond repair:**
1. **Document what you did** - Full commit history
2. **Estimate downtime** - How long to fix vs rollback
3. **Execute fastest recovery** - Revenue > ego
4. **Post-mortem after** - Learn from the disaster

**Remember: Mike needs this system working for his business. Your experimental ideas can wait until there's a staging environment.**

---

## 🏆 FINAL WISDOM

**The popup system survived:**
- Multiple "improvement" attempts
- Database migration disasters  
- Import refactoring nightmares
- Configuration "optimizations"

**It works because it's simple, tested, and battle-hardened. Respect that.**

**New agent? Read this document. Follow the rules. Don't be a hero. Just make it work.**