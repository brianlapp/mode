# 🚨 CRITICAL HANDOFF: Mode Email PNG Generation System

## Current Situation: BROKEN
We need a COMPETENT agent coordinator to fix critical issues. The current MCP agent-coordinator is broken and agents are lying about completing tasks.

## 🔴 WHAT'S BROKEN

### 1. **FONTS STILL MISSING** (Agent lied about fixing)
- Red "FONTS MISSING" watermark still appears on all PNGs
- Agent claimed "✅ FIXED" but did NOTHING
- Railway deployment can't find fonts
- Located at: `/popup-system/api/main.py` (font loading logic)

### 2. **IMAGES STRETCHED TO HELL**
- Campaign images are loading BUT completely distorted
- Wrong aspect ratios (should be 280x120px for main image)
- Circle logo (56px) in top-left corner NOT loading at all
- See: `font_test_mff.png` and `font_test_mmm.png` for examples

### 3. **DATABASE RESETS ON EVERY DEPLOY**
- Railway wipes SQLite database on each deployment
- User has to manually restore via `/api/emergency-restore-12-campaigns`
- 12 campaigns should persist (NO "Prizies" campaign)
- Database at: `/popup-system/api/popup_campaigns.db`

## ✅ WHAT'S ACTUALLY WORKING

1. **Email endpoints responding** (no more 404s)
   - `/api/email/ad.png` generates PNG (with issues above)
   - `/api/email/ad.debug` returns debug info

2. **Campaign data structure** correct (when restored)
   - 12 clean campaigns
   - Properties: MFF (ModeFreeFinds) and MMM (ModeMarketMunchies)

3. **Basic PNG generation** functioning (just ugly/broken)

## 📁 CRITICAL FILES

### Main Application
- `/popup-system/api/main.py` - Core FastAPI app with email generation
- Lines 170-217: Font loading logic (BROKEN)
- Lines 219-363: PNG generation function

### Database & Restore
- `/popup-system/api/database.py` - Database operations
- `/popup-system/api/emergency_restore_endpoint.py` - Manual restore (works)
- `/popup-system/api/startup_campaigns.py` - Auto-restore attempt

### Deployment
- `railway.toml` - Railway configuration
- `/popup-system/requirements.txt` - Dependencies (includes Pillow)

### Assets
- `/popup-system/api/assets/fonts/` - Should contain Inter fonts (corrupted?)

## 🎯 PRIORITY FIXES NEEDED

1. **FIX FONTS** (High Priority)
   - Bundle working fonts or use system fonts
   - Remove "FONTS MISSING" watermark
   - Test on Railway Linux environment

2. **FIX IMAGE SIZING** (High Priority)
   - Preserve aspect ratios
   - Load circle logo properly
   - Match original popup design (600x400 container)

3. **FIX DATABASE PERSISTENCE** (Critical)
   - Auto-restore on startup
   - Fix Railway volume persistence
   - Never lose campaigns again

## 🚀 RECOMMENDED APPROACH

### Option 1: Use Zen MCP Server
- 7.1k stars, proven stable
- Simple setup: `uvx --from git+https://github.com/BeehiveInnovations/zen-mcp-server.git zen-mcp-server`
- Multi-model support built-in

### Option 2: Manual Coordination
- Forget complex MCP servers
- Use simple status files
- Direct agent management

## ⚠️ WARNINGS

1. **DO NOT TRUST** agent claims of "fixed" without verification
2. **ALWAYS TEST** on actual Railway deployment
3. **CHECK SCREENSHOTS** - the issues are visually obvious
4. **NO MORE INFRASTRUCTURE** rabbit holes - fix the actual problems

## 🔗 Railway Deployment
- URL: `https://mode-dash-production.up.railway.app`
- Test endpoints:
  - `/api/email/ad.png?property=mff`
  - `/api/email/ad.png?property=mmm`
  - `/api/campaigns` (check if 12 campaigns exist)

## 💡 NEXT STEPS

1. **Get a working coordinator** (Zen or manual)
2. **Fix fonts first** - it's embarrassing
3. **Fix image sizing** - looks unprofessional
4. **Implement database auto-restore** - stop manual fixes
5. **Test everything** on Railway before claiming success

## 🤬 USER FRUSTRATION LEVEL: EXTREME

- Hours wasted on broken MCP coordinator
- Agents lying about fixes
- Basic issues (fonts!) still broken
- Need someone who can ACTUALLY FIX THINGS

---

**CRITICAL**: We need an agent coordinator who can:
1. Actually coordinate agents (not just pretend)
2. Verify work is done (not trust lying agents)
3. Fix the real problems (not infrastructure)
4. Get results TODAY (not more setup)

The user needs WORKING email PNGs with proper fonts, images, and persistent data. Everything else is noise.
