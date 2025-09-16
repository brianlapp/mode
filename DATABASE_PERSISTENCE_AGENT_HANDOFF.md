# 🔒 Database Persistence & Auto-Restore Agent - CRITICAL HANDOFF

## 🚨 **CRITICAL ISSUE: DATABASE RESETS ON EVERY DEPLOY**

Your mission is to **permanently solve the database reset problem** and ensure campaigns persist across Railway deployments. This is the #1 blocker causing endless frustration.

## 🔥 **THE PROBLEM**

### **Current Situation**
- Every Railway deployment wipes the SQLite database
- Campaigns disappear, requiring manual restoration
- User has to run `/api/emergency-restore-12-campaigns` after EVERY deploy
- This breaks email generation, analytics, everything

### **User Quote**: 
> "restore campaigns ASAP... every gosh darn deploy"

## 🔍 **ROOT CAUSE ANALYSIS**

Based on previous investigations:

1. **Railway Volume Issue**
   - SQLite file at `/app/popup-system/api/popup_campaigns.db`
   - Railway may not be persisting this path
   - Or volume mount is misconfigured

2. **Startup Overwrite**
   - Database might be recreated on startup
   - Init scripts may be wiping existing data

3. **File Path Mismatch**
   - Code expects one path, Railway provides another
   - Backup system works but doesn't prevent resets

## 🎯 **TWO-PART SOLUTION STRATEGY**

### **Part 1: Immediate Auto-Restore** (URGENT)
Implement bulletproof auto-restoration on startup:

```python
# Add to main.py startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and auto-restore if needed"""
    init_db()
    
    # Check if campaigns exist
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
    campaign_count = cursor.fetchone()[0]
    conn.close()
    
    # Auto-restore if empty or corrupted
    if campaign_count < 12:  # Should have exactly 12 campaigns
        logger.warning(f"Found only {campaign_count} campaigns, auto-restoring...")
        
        # Use the working restoration logic
        from emergency_restore_endpoint import restore_campaigns_from_backup
        result = restore_campaigns_from_backup()
        
        logger.info(f"Auto-restore complete: {result}")
    else:
        logger.info(f"Database healthy with {campaign_count} campaigns")
```

### **Part 2: Permanent Persistence** (HIGH PRIORITY)

#### **Option A: Railway Volume Fix**
1. **Research Railway volume configuration**:
   ```toml
   # railway.toml
   [[mounts]]
   source = "popup_campaigns_volume"
   destination = "/app/popup-system/api/data"
   ```

2. **Update database path**:
   ```python
   def get_db_path():
       # Use volume-mounted directory
       data_dir = Path("/app/popup-system/api/data")
       data_dir.mkdir(exist_ok=True)
       return str(data_dir / "popup_campaigns.db")
   ```

3. **Verify with Railway CLI**:
   ```bash
   railway volume list
   railway volume create popup_campaigns_volume
   railway link
   ```

#### **Option B: PostgreSQL Migration**
Since SQLite + Railway volumes are problematic:

1. **Add PostgreSQL to Railway**:
   ```bash
   railway add postgresql
   ```

2. **Update database code**:
   ```python
   # Use SQLAlchemy for compatibility
   from sqlalchemy import create_engine
   
   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///popup_campaigns.db")
   engine = create_engine(DATABASE_URL)
   ```

3. **Migrate existing data**:
   ```python
   def migrate_to_postgres():
       # Export from SQLite
       sqlite_conn = sqlite3.connect("popup_campaigns.db")
       campaigns = sqlite_conn.execute("SELECT * FROM campaigns").fetchall()
       
       # Import to PostgreSQL
       pg_conn = psycopg2.connect(DATABASE_URL)
       cursor = pg_conn.cursor()
       
       for campaign in campaigns:
           cursor.execute(
               "INSERT INTO campaigns (...) VALUES (...)",
               campaign
           )
       
       pg_conn.commit()
   ```

#### **Option C: External Backup Service**
Use cloud storage for persistence:

1. **S3/R2 Backup**:
   ```python
   import boto3
   
   def backup_to_cloud():
       s3 = boto3.client('s3')
       with open(get_db_path(), 'rb') as f:
           s3.put_object(
               Bucket='mode-backups',
               Key='popup_campaigns_latest.db',
               Body=f
           )
   
   def restore_from_cloud():
       s3 = boto3.client('s3')
       obj = s3.get_object(
           Bucket='mode-backups',
           Key='popup_campaigns_latest.db'
       )
       
       with open(get_db_path(), 'wb') as f:
           f.write(obj['Body'].read())
   ```

## 🔧 **IMPLEMENTATION STEPS**

### **Step 1: Add Startup Auto-Restore** (DO THIS FIRST)
1. Modify `popup-system/api/main.py`:
   ```python
   # Import restoration logic
   from emergency_restore_endpoint import restore_campaigns_from_backup
   
   @app.on_event("startup")
   async def startup_event():
       """Auto-restore campaigns if database is empty"""
       init_db()
       
       # Check campaign count
       conn = sqlite3.connect(get_db_path())
       cursor = conn.cursor()
       
       try:
           cursor.execute("SELECT COUNT(*) FROM campaigns WHERE active = 1")
           count = cursor.fetchone()[0]
           
           if count < 12:
               logger.warning(f"Only {count} campaigns found, restoring...")
               
               # Clear any bad data
               cursor.execute("DELETE FROM campaigns WHERE name = 'Prizies'")
               conn.commit()
               
               # Restore good campaigns
               result = restore_campaigns_from_backup()
               logger.info(f"Restored: {result}")
               
       except Exception as e:
           logger.error(f"Startup check failed: {e}")
           # Force restoration on any error
           result = restore_campaigns_from_backup()
           logger.info(f"Emergency restore: {result}")
       
       finally:
           conn.close()
   ```

### **Step 2: Remove Prizies Permanently**
Update restoration data to exclude Prizies:

```python
# In emergency_restore_endpoint.py
CAMPAIGNS_DATA = [
    # Only the 12 good campaigns, NO PRIZIES
    {"id": 1, "name": "Trading Tips", "property": "mmm", ...},
    {"id": 2, "name": "Behind The Markets", "property": "mmm", ...},
    # ... other 10 campaigns
    # NO ENTRY FOR PRIZIES
]
```

### **Step 3: Test Persistence Solutions**

1. **Test Railway Volume**:
   ```bash
   # Deploy with volume mount
   railway up
   
   # Check if data persists
   curl https://mode-dash-production.up.railway.app/api/campaigns | jq length
   
   # Deploy again
   railway up
   
   # Check if still there
   curl https://mode-dash-production.up.railway.app/api/campaigns | jq length
   ```

2. **Monitor logs**:
   ```bash
   railway logs -f | grep -E "(campaigns|restore|database)"
   ```

## 🌐 **RESEARCH TASKS** (Use Internet Search)

### **Railway Persistence Research**
Search for:
- "Railway SQLite volume persistence"
- "Railway database resets on deployment"
- "Railway persistent storage best practices"
- "Railway PostgreSQL vs SQLite"

### **Alternative Solutions**
Research:
- "Cloudflare D1 for edge databases"
- "Supabase for Railway apps"
- "PlanetScale serverless MySQL"
- "Turso SQLite edge database"

## 🧪 **TESTING PROTOCOL**

### **Auto-Restore Test**
```bash
# 1. Deploy with auto-restore
railway up

# 2. Check campaigns loaded automatically
curl https://mode-dash-production.up.railway.app/api/campaigns | jq length
# Should return 12

# 3. Check no Prizies
curl https://mode-dash-production.up.railway.app/api/campaigns | jq '.[] | select(.name == "Prizies")'
# Should return nothing
```

### **Persistence Test**
```bash
# 1. Add test campaign
curl -X POST https://mode-dash-production.up.railway.app/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Campaign", "property": "mff"}'

# 2. Deploy
railway up

# 3. Check if test campaign persists
curl https://mode-dash-production.up.railway.app/api/campaigns | jq '.[] | select(.name == "Test Campaign")'
```

## 📁 **FILES TO MODIFY**

### **Critical Files**
- `popup-system/api/main.py` - Add startup auto-restore
- `popup-system/api/database.py` - Fix path for persistence
- `popup-system/api/emergency_restore_endpoint.py` - Remove Prizies
- `railway.toml` - Add volume configuration

### **New Files**
- `popup-system/api/utils/auto_restore.py` - Dedicated restoration logic
- `popup-system/api/utils/cloud_backup.py` - Cloud backup option
- `popup-system/scripts/migrate_to_postgres.py` - Migration script

## 🎯 **SUCCESS CRITERIA**

### **MUST ACHIEVE**
- [ ] **Auto-restore on startup** - No manual intervention needed
- [ ] **Campaigns persist** across deployments
- [ ] **No more Prizies** - Permanently removed
- [ ] **Exactly 12 campaigns** consistently
- [ ] **No user frustration** - It just works!

### **Stretch Goals**
- [ ] Move to PostgreSQL for reliability
- [ ] Cloud backup system
- [ ] Real-time sync to backup
- [ ] Database health monitoring

## 🚀 **QUICK WIN PATH**

If time is critical, do this MINIMUM:

1. **Add startup auto-restore** (30 min)
2. **Remove Prizies from restore data** (10 min)
3. **Deploy and test** (20 min)

This ensures campaigns are ALWAYS available, even if persistence isn't fixed yet.

## ⚠️ **CRITICAL NOTES**

1. **User is EXTREMELY frustrated** - This has been broken too long
2. **This blocks EVERYTHING** - No campaigns = no email generation
3. **Manual restore is NOT acceptable** - Must be automatic
4. **Test thoroughly** - One more failure will break trust

## 🔄 **HANDOFF BACK**

When complete:
1. **Demonstrate auto-restore working**
2. **Show persistence solution** (if implemented)
3. **Provide deployment instructions**
4. **Document any remaining issues**

**PRIORITY: Make campaigns survive deployments - permanently!**
