## Mode Perks: Properties Toggles, Featured Offer, and Analytics Truthfulness — Implementation Spec

### Objectives
- Fix property-level offer display (on/off) so it persists correctly and reflects true state in UI.
- Stabilize featured offer per property; ensure single featured per property, consistent UI/DB behavior.
- Make analytics truth-only: remove local fallbacks and placeholders, show N/A with explicit Tune error when unavailable.
- Compute real per-offer metrics (CTR, RPM, RPC) using Tune clicks/revenue and internal impressions; no fabricated values.
- Preserve and verify data integrity with backups before/after, and restore on Railway as required.

### Non‑Negotiables
- Never fabricate analytics. If Tune API errors, surface N/A and a visible error badge; provide Retry.
- Never deploy without: (1) pre-deploy backup, (2) immediate restoration of campaigns/settings on Railway post-deploy, (3) live verification of endpoints and UI.
- Protect Mike’s live campaigns at all times (no destructive operations without current backup).

---

## 1) Backups and Verification

Run prior to any changes:
- DB snapshot + analysis (timestamped .db, JSON summary)
- Full data export JSON (impressions, clicks, campaigns)
- Live API snapshots (tune-style-report, attribution)
- Git branch + tag + tarball archive

Artifacts (example):
- `popup-system/api/backups/popup_campaigns_backup_YYYYMMDD_HHMMSS.db`
- `popup-system/api/backups/backup_analysis_YYYYMMDD_HHMMSS.json`
- `popup-system/api/mike_data_backup_YYYYMMDD_HHMMSS.json`
- `popup-system/api/backups/tune_report_pre.json`, `.../attribution_pre.json`
- git branch: `chore/backup-YYYYMMDD`, tag: `backup-YYYYMMDD`
- tarball: `popup-system/api/backups/popup-system-code-YYYYMMDD.tar.gz`

Post-deploy Railway rule: after code deploy, immediately restore campaigns/settings if needed (Railway resets). Verify analytics endpoints return success from Tune.

---

## 2) Backend Changes

### 2.1 Remove analytics fallbacks; add health ping
- Files: `popup-system/api/routes/campaigns.py`
- Endpoints impacted:
  - `/api/analytics/tune-style-report`
  - `/api/analytics/attribution`

Changes:
- If Tune client missing or API request fails: return `{ success: false, data: [], summary: {}, source: 'Tune API error|unavailable', error: '<details>' }`. Do NOT call local fallbacks (`_get_local_tune_style_report` or `_get_local_attribution_analytics`). Keep helpers for dev-only use but not called by these endpoints.
- Add `/api/analytics/tune-health` to perform a minimal Tune connectivity check and return `{ ok: true|false, error?: string, timestamp }`.

### 2.2 Real per-offer metrics (no placeholders)
- Replace fixed CTR (6.67%) and synthetic impressions in analytics with real values:
  - Revenue, clicks: from Tune (HasOffers) per offer_id.
  - Impressions: from local `impressions` table for the requested date range; count by `campaign_id` and (optionally) by `property_code` if filters are added later.
  - CTR = clicks / impressions * 100 (0 if impressions = 0)
  - RPM = revenue / impressions * 1000 (0 if impressions = 0)
  - RPC = revenue / clicks (0 if clicks = 0)
  - Profit = revenue − payout (payout from Tune if available; else 0)

Implementation details:
- Cross-link HasOffers rows to our campaigns via `campaigns.offer_id`.
- For time-bounded queries: derive SQLite date filter for `impressions.timestamp` matching the selected preset (today, last_7_days, last_30_days, etc.).
- Shape responses to match current frontend expectations, but all numeric values must reflect true counts.

### 2.3 Featured campaign integrity
- Ensure `properties.featured_campaign_id` column exists on startup (already in `init_db()`), and add a defensive migration call in startup sequence if needed.
- `/properties/{code}/featured` already sets a single campaign id per property; enforce that setting featured does not depend on `campaigns.featured` (campaign-level featured must not be used for rotation anymore).

### 2.4 Property settings persistence
- Endpoint `POST /campaigns/{campaign_id}/properties` upserts a dict keyed by property codes (works today). Validate and normalize payload:
  - Coerce `active` to 0/1
  - Clamp `visibility_percentage` to [0, 100]
  - Allow `impression_cap_daily`, `click_cap_daily` to be nullable
- Ensure index coverage remains (existing indexes OK).

---

## 3) Frontend Changes (Admin UI)

File: `popup-system/frontend/assets/js/admin.js`

### 3.1 N/A + error badge for analytics
- In `loadAnalyticsData()`:
  - If either analytics endpoint returns `success: false`, surface a red badge: “Tune API error” with `error` detail.
  - Show N/A in the metrics and table row stating “Tune API unavailable: <error> — displaying N/A”.
  - Provide a Retry button; optional auto-retry (2 attempts over ~30–60s). No fabricated values.
  - Optional (feature flag): display last-good cached Tune data with “Cached at HH:MM” label (default: disabled; we will start with strict N/A).

### 3.2 Real metric rendering
- Table columns: use returned `impressions`, `clicks`, `ctr`, `revenue`, `rpm`, `rpc`, `payout`, `profit` as computed on the server. Remove any remaining UI-side placeholders.

### 3.3 Property toggles clarity and persistence
- In the property modal:
  - Do NOT render active checkboxes as checked by default. Render unchecked until `loadPropertySettings()` populates true values. This prevents the “always on” visual default.
  - If a campaign lacks a `campaign_properties` row for a property, default UI to unchecked and visibility 100%; when the user clicks Save, create the row via POST.
  - After Save, show success toast and close modal; a subsequent reopen must reflect the persisted values from the server.

### 3.4 Featured toggle UX
- Keep the per-property featured toggle. After a successful PUT, reload the featured status for that property and campaign to ensure UI reflects DB. Make non-featured toggles appear off. The DB’s single `featured_campaign_id` guarantees only one featured per property.

### 3.5 Global deactivate vs per-property off
- Clarify in UI labels/tooltips:
  - “Deactivate campaign” toggles `campaigns.active` (global).
  - Property “Active” toggles only that `campaign_properties.active` row (per property).
  - On global deactivate, property rows are effectively ignored by fetching queries (already filtered by `c.active = 1`).

---

## 4) Tests

Add/extend tests under `popup-system/`:
- Property settings:
  - Create campaign; set per-property `active=false`; verify `/properties/{property}/campaigns` excludes it.
  - Toggle back to `active=true`; verify inclusion.
- Featured:
  - Set featured for `mff`; GET featured; ensure id matches; ensure only that id is returned as featured.
- Deactivate:
  - PUT `/campaigns/{id}` `{ active:false }`; verify `/campaigns/by-host` excludes it.
- Analytics:
  - Force Tune call failure (mock); verify API returns `success:false` and frontend shows N/A (component test or integration test stub).
  - With sample Tune response + local impressions, verify CTR/RPM/RPC are computed correctly per offer.

---

## 5) Deployment & Verification

Sequence:
1. Pre-deploy backups (DB snapshot, JSON export, API snapshots, git tag).
2. Deploy code.
3. Immediately restore campaigns/settings if Railway reset occurred.
4. Live verification:
   - `/api/analytics/tune-style-report?preset=last_7_days` returns `success:true`, source indicates Tune.
   - `/api/analytics/attribution?preset=last_7_days` returns `success:true` (or `success:false` with N/A if Tune temporarily down).
   - Admin dashboard shows real numbers or N/A with error badge; no placeholders.
   - Property modal reflects persisted states; toggles work; featured is consistent.
5. Save post-deploy API snapshots for change audit.

Rollback plan:
- Revert to `backup-YYYYMMDD` tag/branch.
- Restore DB from latest snapshot if needed.

---

## 6) Acceptance Criteria
- Properties modal:
  - Active checkboxes reflect true server state on open; saving updates rows and persists after reload.
  - Featured toggle sets exactly one campaign per property and reflects accurately after save.
- Global deactivate:
  - Campaign disappears from property listings and optimized host endpoints when deactivated.
- Analytics:
  - No local fallback; UI shows N/A + error on Tune failures.
  - CTR/RPM/RPC per offer are computed from real data (Tune revenue/clicks + internal impressions) over the selected range.
  - No ROI field rendered without real spend data.
- Backups & deployment:
  - Backups taken, verified, and restorable; Railway restore procedure executed on deploy as required.

---

## 7) Out of Scope (for this batch)
- Conversion webhook ingestion from Tune (future: populate `conversions` table and track actual payouts per conversion).
- Advanced caching/queuing layers; we start with strict N/A policy (optional short-lived cache is a follow-up switch).

---

## 8) Implementation Notes
- Keep `_get_local_tune_style_report` and `_get_local_attribution_analytics` for dev/testing utilities but ensure production endpoints never call them.
- Document a lightweight runbook: common Tune errors, how to read the health endpoint, and expected N/A behavior.


