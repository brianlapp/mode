# 🚂 Railway Deployment Agent - URGENT HANDOFF

## 🚨 **CRITICAL ISSUES TO RESOLVE**

### **Primary Problem**: All new email endpoints returning 404 "Not Found"
- `/api/email/ad.png` → 404
- `/api/email/ad.debug` → 404  
- `/api/email/preview.html` → 404

### **Secondary Problem**: Campaign database resets on every deployment
- Campaigns get wiped during Railway deployments
- Requires manual restoration via `/api/emergency-restore-12-campaigns`
- Backup system exists but not preventing resets

## 📊 **CURRENT STATE**

### ✅ **Working Systems**
- Main FastAPI app loads: `https://mode-dash-production.up.railway.app/`
- Campaigns API works: `/api/campaigns` (when campaigns exist)
- Emergency restore works: `POST /api/emergency-restore-12-campaigns`
- Database backup system active (creates backups before commits)

### ❌ **Broken Systems**  
- **ALL email routes return 404** despite being in main.py
- **Campaign database resets** on every deployment
- **Old email system** still serving "Prizies" placeholder (source unknown)

## 🔧 **DEPLOYMENT CONFIGURATION**

### **Railway Config** (`railway.toml`)
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "cd popup-system/api && uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2"
```

### **Dependencies** (`popup-system/requirements.txt`)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
jinja2==3.1.2
aiofiles==23.2.1
requests==2.31.0
httpx==0.25.2 
Pillow==10.2.0
```

### **Environment Variables**
- `PUBLIC_BASE_URL=https://mode-dash-production.up.railway.app`

## 🗃️ **DATABASE BACKUP SYSTEM**

### **Automatic Backup System** (WORKING)
- Located in: `popup-system/api/auto_backup.py`
- Triggers: Before every git commit
- Storage: `popup-system/backups/popup_campaigns_backup_YYYYMMDD_HHMMSS.db`
- Latest backup: `popup_campaigns_backup_20250915_214412.db`

### **Emergency Restoration** (WORKING)
- Endpoint: `POST /api/emergency-restore-12-campaigns`
- Restores 13 campaigns with property attribution
- Response: `{"status":"success","campaigns_restored":13,"mmm_campaigns":5,"mff_campaigns":7}`

### **CRITICAL REQUEST**: Fix database persistence
The backup system works but **campaigns still get wiped on deployment**. Need to:
- Ensure Railway volume mount is working: `/app/popup-system/api/popup_campaigns.db`
- Fix whatever is causing database resets during deployment
- Make the backup system restore automatically on startup if DB is empty

## 🐛 **EMAIL ROUTE DEBUGGING**

### **Routes Defined in main.py** (lines 262-302)
```python
@app.get("/api/email/ad.png")
async def working_email_ad_png(property: str = "mff", w: int = 600, h: int = 400, send: str = "qa"):
    # ... working code here ...

@app.get("/api/email/ad.debug") 
async def direct_email_ad_debug(property: str = "mff", w: int = 600, h: int = 400, send: str = "qa"):
    # ... working code here ...
```

### **Import Issues Suspected**
- Email router import disabled due to PIL issues: `# app.include_router(email_router, prefix="/api", tags=["email"])`
- Direct routes added to main.py to bypass routing
- **Still returning 404** - suggests app isn't loading properly

## 🎯 **SPECIFIC TASKS FOR RAILWAY AGENT**

### **Task 1: Fix 404 Email Endpoints** (URGENT)
1. **Investigate why email routes return 404** despite being in main.py
2. **Check Railway deployment logs** for import errors or startup failures
3. **Verify FastAPI app is loading** all routes properly
4. **Test route registration** - are the email endpoints actually being registered?

### **Task 2: Fix Database Persistence** (HIGH PRIORITY)
1. **Ensure Railway volume mount** is working for `/app/popup-system/api/popup_campaigns.db`
2. **Fix database resets** during deployment
3. **Implement auto-restore** on startup if database is empty
4. **Test backup/restore cycle** to ensure data persistence

### **Task 3: Deployment Health Check** (MEDIUM)
1. **Verify all dependencies** are installing correctly (especially Pillow)
2. **Check Python version compatibility** on Railway
3. **Test import chain** - can all modules load without errors?
4. **Optimize startup command** if needed

## 📝 **TESTING CHECKLIST**

After fixes, these should work:
- [ ] `GET /api/email/ad.png?property=mff&w=600&h=400` → Returns PNG or text
- [ ] `GET /api/email/ad.debug?property=mff&w=600&h=400` → Returns JSON debug info
- [ ] `GET /api/email/preview.html` → Returns HTML preview
- [ ] `POST /api/emergency-restore-12-campaigns` → Restores campaigns
- [ ] **Database persists** after deployment (no resets)

## 🔄 **HANDOFF BACK TO ORCHESTRATOR**

When Railway deployment is fixed and endpoints are working:
1. **Confirm email endpoints respond** (not 404)
2. **Verify database persistence** (campaigns don't reset)
3. **Hand back to PNG Generation Agent** to implement actual image generation
4. **Provide deployment logs** if any issues found

## ⚠️ **CRITICAL NOTES**
- **User is frustrated** with endless cycles - need working solution ASAP
- **Campaigns reset frequently** - this MUST be fixed
- **Old "Prizies" system** still interfering - may need separate investigation
- **PIL/Pillow issues** on Railway causing import problems

**Priority: GET ENDPOINTS WORKING FIRST, then worry about PNG quality**
