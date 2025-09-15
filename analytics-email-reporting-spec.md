## Analytics – Email Source Reporting Spec

### Purpose
Add reporting for `source=email` with a simple UI toggle (Popup | Email | All) and unified API filters.

### Source Filter (UI)
- Segmented control: default Popup, options Email and All.
- Query param: `source=popup|email|all` (persisted in URL and localStorage).

### API – Unified (Recommended)
Use one family of endpoints with `source_filter` query param.

- GET `/api/analytics/summary?preset=last_7_days&property=mff|mmm|mcad|all&source_filter=popup|email|all`
  - Returns: totals { impressions, clicks, revenue, rpm, rpc }.

- GET `/api/analytics/by-campaign?preset=...&property=...&source_filter=...`
  - Returns rows: { campaign_name, property_code, source, impressions, clicks, revenue, rpm, rpc }.

- GET `/api/analytics/by-property?preset=...&source_filter=...`
  - Returns rows: { property_code, impressions, clicks, revenue, rpm, rpc }.

Filtering rules
- `popup`: exclude rows where `source='email'`.
- `email`: include rows where `source='email'` only.
- `all`: no filter; include both; aggregate accordingly.

Metrics
- Impressions: count from `impressions` table.
- Clicks: count from `clicks` table.
- Revenue: sum `clicks.revenue_estimate`.
- RPM: revenue / impressions * 1000.
- RPC: revenue / clicks.

### Alternative – Separate Email Endpoints
If preferred, keep dedicated email endpoints and switch by UI toggle:
- `/api/analytics/email/summary`, `/api/analytics/email/by-campaign`, `/api/analytics/email/by-property`.
- For Popup/All, call existing endpoints or combine responses client-side.

### Data Quality
- Do not fabricate missing values. If impressions=0 but clicks>0, set RPM/CTR to null and include a `data_quality` flag.

### Notes
- No deploy until backups are created and verified.
- Verification: compare totals before/after with real API responses; no sample data.

