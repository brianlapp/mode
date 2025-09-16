# 🗃️ Campaign Data Manager - AGENT 3 HANDOFF

## 🎯 **MISSION: Ensure Stable Campaign Data**

Your job is to **permanently fix the campaign reset problem** and maintain stable, high-quality campaign data that doesn't get wiped on every Railway deployment.

## 📋 **HANDOFF FROM PREVIOUS AGENTS**

### **Agent 1 (Railway)**: Should have fixed deployment/routing issues
### **Agent 2 (PNG Generation)**: Building PNG generation system

**Your work is CRITICAL** - without stable campaigns, the PNG generation will keep breaking!

## 🚨 **CRITICAL PROBLEMS TO SOLVE**

### **Problem 1: Campaign Database Resets** (URGENT)
- **Current Issue**: Every Railway deployment wipes the campaign database
- **Impact**: Email generation breaks, shows "No campaigns found"
- **User Frustration**: Constant manual restoration required
- **Root Cause**: Railway volume mount or database persistence issue

### **Problem 2: "Prizies" Campaign Contamination**
- **Current Issue**: "Prizies" campaign keeps appearing in restore scripts
- **Impact**: Email ads show crappy placeholder instead of professional campaigns
- **Location**: Multiple restore scripts contain Prizies data
- **Need**: Permanent removal from ALL restore mechanisms

### **Problem 3: Inconsistent Campaign Count**
- **Expected**: 13 campaigns consistently
- **Actual**: Varies between 11-13 depending on restore
- **Issue**: Some campaigns missing or duplicated

## 🗃️ **CURRENT DATABASE SYSTEM**

### **Database Location**
- **Railway Path**: `/app/popup-system/api/popup_campaigns.db`
- **Local Path**: `popup-system/api/popup_campaigns.db`
- **Backup Directory**: `popup-system/backups/`

### **Backup System** (WORKING but not preventing resets)
- **Auto-backup**: Triggers before every git commit
- **File**: `popup-system/api/auto_backup.py`
- **Storage**: `popup_campaigns_backup_YYYYMMDD_HHMMSS.db`
- **Latest**: `popup_campaigns_backup_20250915_214412.db`

### **Restoration System** (WORKING but manual)
- **Endpoint**: `POST /api/emergency-restore-12-campaigns`
- **File**: `popup-system/api/emergency_restore_endpoint.py` (embedded in main.py)
- **Response**: `{"status":"success","campaigns_restored":13,"mmm_campaigns":5,"mff_campaigns":7}`

## 📊 **CAMPAIGN DATA SPECIFICATIONS**

### **GOOD Campaigns to Keep** (12 total)
```json
[
  {"id": 1, "name": "Trading Tips", "property": "mmm", "cta_text": "Get Trading Tips"},
  {"id": 2, "name": "Behind The Markets", "property": "mmm", "cta_text": "Learn More"},
  {"id": 3, "name": "Brownstone Research", "property": "mmm", "cta_text": "View Research"},
  {"id": 4, "name": "Hotsheets", "property": "mmm", "cta_text": "Get Hotsheets"},
  {"id": 5, "name": "Best Gold", "property": "mmm", "cta_text": "Learn About Gold"},
  {"id": 6, "name": "Daily Goodie Box", "property": "mff", "cta_text": "Claim Now!"},
  {"id": 7, "name": "Free Samples Guide", "property": "mff", "cta_text": "Claim Now!"},
  {"id": 9, "name": "Hulu - Hit Movies, TV and More!", "property": "mff", "cta_text": "Get Hulu!"},
  {"id": 10, "name": "Paramount", "property": "mff", "cta_text": "Get Paramount+!"},
  {"id": 11, "name": "Trend'n Daily", "property": "mff", "cta_text": "Get Box!"},
  {"id": 14, "name": "Money.com - Online Stock Brokers", "property": "mmm", "cta_text": "View Offer"},
  {"id": 8, "name": "UpLevel - Amazon Mystery Box", "property": "mff", "cta_text": "Get Box!"}
]
```

### **BAD Campaigns to Remove** (PERMANENTLY)
```json
[
  {"id": 12, "name": "Prizies", "cta_text": "Win!", "description": "Win $1,000 Cashapp!"}
]
```

## 🔧 **SPECIFIC TASKS**

### **Task 1: Fix Database Persistence** (URGENT)
1. **Investigate Railway volume mounting**
   - Ensure `/app/popup-system/api/popup_campaigns.db` persists
   - Check if Railway is properly mounting the volume
   - Verify database file permissions and ownership

2. **Implement Auto-Restore on Startup**
   - Add database check to `@app.on_event("startup")`
   - If database empty/missing, auto-restore from latest backup
   - Log restoration events for debugging

3. **Test Deployment Persistence**
   - Deploy a test change
   - Verify campaigns survive the deployment
   - Document any remaining persistence issues

### **Task 2: Remove Prizies Permanently** (HIGH PRIORITY)
1. **Clean All Restore Scripts**
   - `popup-system/api/emergency_restore_endpoint.py` (lines 28, 32)
   - `popup-system/api/startup_campaigns.py` (lines 84, 124)
   - Any other files containing Prizies data

2. **Update Emergency Restore**
   - Remove Prizies from campaign restoration data
   - Ensure only 12 good campaigns are restored
   - Test that restoration never includes Prizies

3. **Database Cleanup**
   - Add endpoint to permanently delete Prizies campaigns
   - Ensure Prizies can't be re-added accidentally

### **Task 3: Campaign Data Quality** (MEDIUM)
1. **Standardize Campaign Count**
   - Ensure exactly 12 campaigns always restored
   - Fix any duplication or missing campaign issues
   - Validate campaign data integrity

2. **Improve Image URLs**
   - Fix broken imgur links (many return 404)
   - Update to working image URLs
   - Test image accessibility

3. **Property Attribution**
   - Ensure campaigns properly assigned to MFF/MMM
   - Verify property-specific campaign selection works

## 📁 **FILES TO MODIFY**

### **Primary Files**
- `popup-system/api/main.py` - Add startup auto-restore
- `popup-system/api/emergency_restore_endpoint.py` - Remove Prizies
- `popup-system/api/startup_campaigns.py` - Clean campaign data
- `popup-system/api/database.py` - Improve persistence

### **Backup Files** (for reference)
- `popup-system/backups/popup_campaigns_backup_20250915_214412.db` - Latest backup
- `popup-system/api/mike_data_backup_20250826_204923.json` - Historical data

## 🧪 **TESTING PROTOCOL**

### **Before Changes**
```bash
# Check current campaign count
curl "https://mode-dash-production.up.railway.app/api/campaigns" | jq 'length'

# Check for Prizies
curl "https://mode-dash-production.up.railway.app/api/campaigns" | jq '.[] | select(.name == "Prizies")'
```

### **After Changes**
```bash
# Verify 12 campaigns consistently
curl "https://mode-dash-production.up.railway.app/api/campaigns" | jq 'length'

# Verify no Prizies
curl "https://mode-dash-production.up.railway.app/api/campaigns" | jq '.[] | select(.name == "Prizies")'

# Test deployment persistence
# 1. Deploy a test change
# 2. Check campaigns still exist
# 3. Verify count remains 12
```

## 🎯 **SUCCESS CRITERIA**

### **MUST ACHIEVE**
- [ ] **Database persists** through Railway deployments
- [ ] **No more manual restoration** required
- [ ] **Prizies permanently eliminated** from all systems
- [ ] **Consistent 12 campaigns** always available
- [ ] **Auto-restore** on startup if database empty

### **DELIVERABLES**
1. **Fixed database persistence** - campaigns survive deployments
2. **Clean restore scripts** - no Prizies contamination
3. **Auto-restore system** - handles empty database gracefully
4. **Documentation** - how to maintain campaign data going forward

## 🚨 **CRITICAL NOTES**

### **User Frustration Level**: EXTREME
- **"restore campaigns ASAP"** - constant manual fixes required
- **"every gosh darn deploy"** - resets are happening too frequently
- **Need permanent solution** - not more manual workarounds

### **Dependencies**
- **Agent 1**: Must fix Railway deployment issues first
- **Agent 2**: Needs stable campaigns for PNG generation
- **Agent 4**: May find old systems that need campaign data

### **Coordination Required**
- **Don't break** what Agent 1 fixes
- **Ensure campaigns available** for Agent 2's PNG generation
- **Document changes** for other agents

## 🔄 **HANDOFF BACK TO ORCHESTRATOR**

When campaign data is stable:
1. **Confirm database persistence** through deployment cycle
2. **Verify 12 campaigns consistently available**
3. **Document auto-restore system**
4. **Report any remaining data issues**

**Priority: STOP THE ENDLESS CAMPAIGN RESETS!**
