# MANDATORY DEPLOYMENT CHECKLIST - CHECK EVERY BOX

## BEFORE ANY CHANGE:
- [ ] Check current Railway logs with `mcp_Railway_get-logs`
- [ ] Verify current state: campaigns exist, popup works, no CORS errors
- [ ] Document what's working NOW before making changes

## WHEN USING EMERGENCY RESTORE:
- [ ] Verify golden backup files exist in git: `GOLDEN_campaigns_20251002_181029.json` and `GOLDEN_properties_20251002_181029.json`
- [ ] Check emergency restore code loads FROM golden backup (not hardcoded data)
- [ ] Emergency restore path must be `Path(__file__).parent.parent / "backups"` (NOT `parent / "backups"`)
- [ ] Response must show: `"source": "GOLDEN_campaigns_20251002_181029.json"`

## AFTER RESTORE:
- [ ] Call `/api/emergency-restore-12-campaigns` and verify JSON response
- [ ] Check campaigns: `curl /api/campaigns/mff | jq length` returns 6+
- [ ] Check for broken images: look at actual campaign logo_url and main_image_url
- [ ] Verify properties: check that campaign_properties table exists
- [ ] Test popup on live site: https://mode-thankyou.netlify.app/

## IF SOMETHING BREAKS:
- [ ] DON'T make 3+ rapid changes
- [ ] Use Railway MCP: `mcp_Railway_get-logs` to see ACTUAL error
- [ ] Check git reflog to find last working commit (don't guess!)
- [ ] Test rollback target BEFORE force push

## CURRENT GOLDEN BACKUP INFO:
- Location: `popup-system/backups/`
- Files: `GOLDEN_campaigns_20251002_181029.json` (12 campaigns with real image URLs)
- Files: `GOLDEN_properties_20251002_181029.json` (all property settings)
- Created: Oct 2, 2025 at 6:10pm from working production

