# Multi-domain popup updates (EST caps) — 2025-08-09

- Backend
  - Added `properties` table (code, name, domain, popup settings) and seeded defaults.
  - Implemented `detect_property_code_from_host(hostname)` and `/api/properties/resolve`.
  - Enforced per-property daily caps (impressions/clicks) using EST day bounds in `get_active_campaigns_for_property`.
  - Ensured `/popup.js` serves canonical `popup-system/popup.js`.
- Admin UI
  - Property modal supports `visibility_percentage`, `impression_cap_daily`, `click_cap_daily`.
  - On create, defaults the current site to 100%, others 0%.
  - **Properties column** added to campaigns table in dashboard with visibility percentages.
  - Campaigns dashboard shows property-specific visibility settings per campaign.
- Popup
  - `ModePopup.init({ property: 'auto' })` defaults brandTargeting ON; auto-resolves by host and loads `/api/campaigns/{property}`.
  - Images optional; text-only ads supported (circle/main image hidden when URLs empty).
- Test plan
  - Deploy/restart → hit `/api/properties/resolve`, `/api/campaigns/mff`.
  - Set small cap in Admin; verify exclusion after cap reached.
- **Netlify Domain Previews** 
  - Created `netlify-demo-for-mike/` and `netlify-test/` folders for domain-based testing.
  - Both include **domain navigation UI** for switching between MFF/MMM/MCAD/MMD properties.
  - Real-time property switching with popup re-initialization for each domain.
  - Thank you page preview shows domain-specific branding and popup campaigns.

Status: ready to deploy and run MFF test.
