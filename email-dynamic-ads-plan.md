## Email Dynamic Ads – Implementation Plan (Plan-First, No Deploy)

### Objectives
- Mobile-first email-safe offer card rendered server-side as PNG (no JS in email).
- Deterministic per-send rotation using featured-first then RPM ordering across properties `mff`, `mmm`, `mcad`.
- Clean attribution: `source=email`, `subsource={ESP}`, `utm_campaign={send}`.

### Rotation & Selection
- Order: featured campaign (if set for property) first, then by RPM DESC, then created_at DESC.
- Deterministic hash on `send` (or `sub` if chosen) → stable offer per blast.
- Properties covered: `mff`, `mmm`, `mcad`.

### Rendering (Email-Safe)
- Default: 300x250 PNG (mobile-first), optional 600x500 for high-DPI/desktop templates.
- HTML recommends width/height attributes and inline styles: `width:100%; max-width:300px; height:auto` for responsiveness.
- Card contents: title, image area (or proxied campaign image v2), CTA text.
- No co-brand overlay initially; room to add later.

### ESP Integration (SendGrid, CleverTap)
- URLs carry `send` (blast id) and optional `sub` (recipient id) to ensure deterministic stickiness and unique cache keys.
- We will map exact macros after confirming ESP channel/template mode.

### Endpoint Specs (Proposed)
- GET `/api/email/ad.png`
  - Query: `property` (mff|mmm|mcad), `send`, `sub` (optional), `esp` (sendgrid|clevertap|other), `w`, `h`.
  - Behavior: selects offer deterministically; logs impression with `source=email`, `subsource=esp`, `utm_campaign=send`; returns PNG.
  - Caching: private; rely on unique querystring to bust ESP/Gmail caches per send.
- GET `/api/email/click`
  - Query: `property`, `send`, `sub`, `esp`.
  - Behavior: logs click with same attribution fields; 302 to campaign tracking URL with appended UTM and source params.

### Caching & Deliverability
- Per-send stickiness ensures consistent creatives within a blast and stable cached image across opens.
- Use distinct URL params to avoid Gmail/Outlook image cache collisions.
- Filter bot opens via UA when feasible; measure performance on clicks primarily.

### Backup & Deployment (Required Sequence)
1) Create production backup including tables: campaigns, campaign_properties, properties (with `featured_campaign_id`), impressions, clicks.
2) Deploy code.
3) Immediately restore campaigns from backup (Railway startup wipes campaigns).
4) Run manual migration for `featured_campaign_id` if needed.
5) Verify analytics endpoints before marking success.

### Staging & Validation
- Implement behind feature flag; validate on staging DB clone.
- Send a controlled test via SendGrid/CleverTap to confirm:
  - PNG loads; click redirects; DB logs impression/click; UTMs present.
  - Deterministic rotation per-send works across multiple opens/recipients.

### Analytics Reporting (Email View)
- Goal: Secondary view or filter within existing analytics to isolate `source=email`.
- API (proposed):
  - GET `/api/analytics/email/summary?preset=last_7_days&property=mff|mmm|mcad` → totals: impressions, clicks, revenue, RPM, RPC.
  - GET `/api/analytics/email/by-campaign?preset=...&property=...` → per-campaign rows.
  - GET `/api/analytics/email/by-property?preset=...` → property aggregates.
- Metrics: 
  - Impressions: impressions.source='email'.
  - Clicks/Revenue: clicks.source='email', sum revenue_estimate.
  - RPM: revenue/impressions*1000; RPC: revenue/clicks.
- UI: Add an Email tab or a Source filter toggle in the existing dashboard to switch between Popup vs Email.
  - Start with toggle (less clutter); only add a separate tab if needed.

### Source Filter Toggle (UI & Routing)
- Three-state segmented control above analytics: `[Popup] [Email] [All]`.
  - Default: Popup (exclude `source=email`).
  - Email: include only `source=email`.
  - All: combine both; tables show a Source column; metric cards sum across both.
- Deep linking: add `?source=popup|email|all` to preserve state.
- Persistence: store last choice (e.g., `localStorage.analytics_source_filter`).
- API mapping options:
  - Unified endpoints with `source_filter` param: `popup|email|all`.
  - Or separate `/email/*` endpoints; UI selects endpoint based on toggle. Recommendation: unified param for simplicity.

### Approval Gates
- Confirm: mobile-first rendering, per-send rotation, properties in scope.
- Confirm: analytics as a filter (preferred) vs separate tab.
- Confirm: macro mapping for SendGrid/CleverTap.
- Proceed to staging only after sign-off.

### Open Questions
- Do we want a desktop-optimized image variant automatically selected by template, or manual toggle per campaign?
- Proxy and embed the actual campaign image in the PNG (v2), or keep stylized placeholder initially?

### ESP Snippets (Copy-Paste)

SendGrid – Dynamic Templates (API sends)

```html
<a href="https://mode-dash-production.up.railway.app/api/email/click?property=mmm&send={{send_id}}&sub={{user_id}}&esp=sendgrid">
  <img src="https://mode-dash-production.up.railway.app/api/email/ad.png?property=mmm&send={{send_id}}&sub={{user_id}}&esp=sendgrid&w=300&h=250"
       width="300" height="250" alt="Sponsored offer" style="display:block;border:0;width:100%;max-width:300px;height:auto;">
</a>
```

- Provide per-blast `send_id` and per-recipient `user_id` via `personalizations[n].dynamic_template_data`.
- Desktop variant: use `w=600&h=500`, set `width="600"` and `max-width:600px`.

SendGrid – Marketing Campaigns (UI sends)

```html
<a href="https://mode-dash-production.up.railway.app/api/email/click?property=mmm&send={{ contact.custom_fields.send_id }}&sub={{ contact.custom_fields.user_id }}&esp=sendgrid">
  <img src="https://mode-dash-production.up.railway.app/api/email/ad.png?property=mmm&send={{ contact.custom_fields.send_id }}&sub={{ contact.custom_fields.user_id }}&esp=sendgrid&w=300&h=250"
       width="300" height="250" alt="Sponsored offer" style="display:block;border:0;width:100%;max-width:300px;height:auto;">
</a>
```

- Create custom fields `send_id` and `user_id` in Marketing Campaigns and map them in your audience.

CleverTap – Final tokens (from Katie)

```html
<a href="https://mode-dash-production.up.railway.app/api/email/click?property=mmm&send={{ Campaign.campaignId }}&sub=$replacement$##y[none]$/replacement$&sub1={{Profile.customer_id|default:'none'}}&esp=clevertap">
  <img src="https://mode-dash-production.up.railway.app/api/email/ad.png?property=mmm&send={{ Campaign.campaignId }}&sub=$replacement$##y[none]$/replacement$&sub1={{Profile.customer_id|default:'none'}}&esp=clevertap&w=300&h=250"
       width="300" height="250" alt="Sponsored offer" style="display:block;border:0;width:100%;max-width:300px;height:auto;">
</a>
```

- Uses `send={{ Campaign.campaignId }}` and two subs:
  - `sub=$replacement$##y[none]$/replacement$` (email address; fallback none)
  - `sub1={{Profile.customer_id|default:'none'}}` (customer id)
- Backend will accept both parameters; `sub` is used for session identity and `sub1` recorded alongside for attribution. We can switch to hashed email later if required.


