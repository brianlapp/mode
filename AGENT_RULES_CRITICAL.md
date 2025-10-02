# CRITICAL AGENT RULES - NEVER BREAK THESE

## Rule 1: VERIFY BEFORE ROLLBACK
- **NEVER** rollback to a commit without checking if it's actually working
- **ALWAYS** check git log to see if the target commit has fixes AFTER it
- **TEST** the rollback locally before force pushing

## Rule 2: TEST BEFORE DECLARING SUCCESS
- **NEVER** say "it's working" without testing the API endpoints
- **ALWAYS** verify:
  1. `/health` returns 200
  2. `/api/campaigns/mff` returns actual campaigns
  3. Popup loads without CORS errors
  4. Railway logs show no errors

## Rule 3: ONE CHANGE AT A TIME
- **NEVER** make multiple changes in rapid succession without testing
- **ALWAYS** wait for Railway deploy AND test before next change
- **STOP** after 3 failed deploys and reassess strategy

## Rule 4: KNOW YOUR WORKING BASELINE
- **ALWAYS** identify the last known working commit FIRST
- **DOCUMENT** what "working" means (has campaigns, popup loads, etc)
- **NEVER** assume a recent commit is working

## Rule 5: USE RAILWAY MCP TO CHECK LOGS
- **BEFORE** making changes, check what the actual error is
- **AFTER** deploy, check logs to verify success
- **DON'T** rely on HTTP status codes alone

## Rule 6: STOP WHEN CONFUSED
- If you've rolled back 3+ times, **STOP**
- If you're guessing which commit works, **STOP**
- If Railway keeps failing, **STOP** and check logs
- **ASK** the user for help instead of guessing

## Current Situation (Oct 2, 2025):
- Popup has CORS errors
- Campaigns are gone AGAIN
- Need to find ACTUAL working commit from 2+ weeks ago
- Current commit `a120e76` still broken

## Next Steps:
1. Check Railway logs for actual error
2. Roll back to commit `42ca891` (2 weeks ago - "Fix campaign deletion")
3. TEST before declaring success
4. If that doesn't work, go to `90495eb` (2 weeks ago - "Fix email router")

