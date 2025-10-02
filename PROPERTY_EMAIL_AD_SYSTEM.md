# Property-Based Email Ad Management System

## 🎯 **Overview**
Create a property-specific email ad management system that serves standalone, complete email advertisements (not screenshots of popups). Each property (MFF, MMM, etc.) can have multiple email ads that rotate based on percentage settings.

## 📋 **Requirements**

### 1. **Database Schema Updates**
Add email ad management tables:

```sql
-- Email ads table
CREATE TABLE email_ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_code TEXT NOT NULL,           -- 'mff', 'mmm', 'mcad', 'mmd'
    name TEXT NOT NULL,                    -- "MFF Finance Newsletter Ad #1"
    desktop_image_url TEXT NOT NULL,       -- Desktop version (600px wide)
    mobile_image_url TEXT,                 -- Mobile version (320px wide, optional)
    click_url TEXT NOT NULL,               -- Where email click goes
    description TEXT,                      -- Internal description
    visibility_percentage INTEGER DEFAULT 100,  -- 0-100% rotation weight
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_code) REFERENCES properties(code)
);

-- Email ad analytics
CREATE TABLE email_ad_impressions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_ad_id INTEGER NOT NULL,
    property_code TEXT NOT NULL,
    variant TEXT NOT NULL,                 -- 'desktop' or 'mobile'
    recipient_hash TEXT,                   -- Anonymized recipient ID
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_ad_id) REFERENCES email_ads(id) ON DELETE CASCADE
);

CREATE TABLE email_ad_clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_ad_id INTEGER NOT NULL,
    property_code TEXT NOT NULL,
    variant TEXT NOT NULL,
    recipient_hash TEXT,
    revenue_estimate DECIMAL(10,2) DEFAULT 0.25,  -- Lower than popup clicks
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_ad_id) REFERENCES email_ads(id) ON DELETE CASCADE
);
```

### 2. **Updated Email API Endpoints**

#### **Primary Email Ad Endpoint**
```python
@app.get("/api/email/ad.png")
async def serve_email_ad(
    property: str = "mff",
    variant: str = "desktop",  # 'desktop' or 'mobile'
    recipient: str = None      # Optional recipient tracking
):
    """
    Serve rotating email ad for property
    - Gets active email ads for property
    - Applies visibility percentage rotation
    - Tracks impression
    - Returns redirect to selected ad image
    """
```

#### **Email Ad Click Tracking**
```python
@app.get("/api/email/click/{email_ad_id}")
async def track_email_click(
    email_ad_id: int,
    property: str,
    variant: str = "desktop",
    recipient: str = None
):
    """
    Track email ad click and redirect to destination
    - Records click analytics
    - Returns redirect to click_url
    """
```

### 3. **Admin Dashboard Integration**

#### **Property Management Tab**
Add new tab to existing admin dashboard:
- **"Email Ads"** tab next to "Campaign Management"
- Property selector dropdown (MFF, MMM, MCAD, MMD)
- Similar UI pattern as campaign management screenshot

#### **Email Ad Management Interface**
Based on the campaign management UI pattern shown:

**Left Panel - Email Ad Details:**
- Email Ad Name (text input)
- Property Code (dropdown: MFF, MMM, MCAD, MMD)
- Description (textarea)
- Click URL (text input - where email clicks go)
- Desktop Image URL (text input + upload button)
- Mobile Image URL (text input + upload button)
- Visibility Percentage (0-100 slider)
- Active toggle (checkbox)

**Right Panel - Live Preview:**
- Desktop preview (600px width)
- Mobile preview (320px width)
- Toggle between desktop/mobile views
- Click tracking URL preview

#### **Email Ads List View**
- Table showing all email ads per property
- Columns: Name, Property, Desktop Image, Mobile Image, Visibility %, Active, Actions
- Edit/Delete/Duplicate actions
- Bulk enable/disable functionality

### 4. **Email Integration HTML**

#### **Email Template Snippet**
Provide HTML snippet for email templates:

```html
<!-- Desktop Version -->
<div class="desktop-only" style="display:block;">
    <a href="https://mode-dash-production.up.railway.app/api/email/click/{{ad_id}}?property=mff&variant=desktop&recipient={{recipient_id}}">
        <img src="https://mode-dash-production.up.railway.app/api/email/ad.png?property=mff&variant=desktop&recipient={{recipient_id}}"
             alt="Mode Offer"
             style="max-width:600px;width:100%;height:auto;">
    </a>
</div>

<!-- Mobile Version -->
<div class="mobile-only" style="display:none;">
    <a href="https://mode-dash-production.up.railway.app/api/email/click/{{ad_id}}?property=mmm&variant=mobile&recipient={{recipient_id}}">
        <img src="https://mode-dash-production.up.railway.app/api/email/ad.png?property=mmm&variant=mobile&recipient={{recipient_id}}"
             alt="Mode Offer"
             style="max-width:320px;width:100%;height:auto;">
    </a>
</div>
```

### 5. **Rotation Logic**

#### **Visibility Percentage Algorithm**
- Same logic as popup campaigns
- Weight ads by visibility percentage
- Random selection based on weights
- Ensure different ads show to different recipients

#### **Analytics Integration**
- Track impressions per email ad
- Track clicks per email ad
- Revenue attribution per email ad
- Property-specific reporting

### 6. **Default Email Ads**

#### **Seed Data for Each Property**
Create default email ads for each property:

**MFF (ModeFreeFinds):**
- "Free Samples Newsletter Ad"
- "Daily Deals Email Banner"
- "Lifestyle Offers Email Ad"

**MMM (ModeMarketMunchies):**
- "Trading Tips Email Banner"
- "Financial Newsletter Ad"
- "Stock Broker Comparison Ad"

### 7. **Implementation Phases**

#### **Phase 1: Core System**
- Database schema updates
- Basic email ad CRUD operations
- Simple email serving endpoint

#### **Phase 2: Admin Dashboard**
- Email ad management UI
- Property-specific management
- Live preview functionality

#### **Phase 3: Analytics & Optimization**
- Click tracking implementation
- Impression analytics
- Performance reporting
- A/B testing capabilities

## 🎯 **Success Criteria**

1. **Email ads serve instantly** (no screenshot delays)
2. **Property-specific ad rotation** working
3. **Desktop/mobile variants** supported
4. **Click tracking** functional
5. **Admin dashboard** intuitive and similar to campaign management
6. **Analytics** showing email ad performance
7. **Revenue attribution** per email ad

## 🔧 **Technical Notes**

- **No screenshot dependencies** - Pure image serving
- **Existing database patterns** - Follows campaign/property structure
- **Consistent UI patterns** - Matches existing admin dashboard
- **Performance optimized** - Image redirects, not proxying
- **Scalable design** - Can handle multiple properties and ads

## 🚀 **Implementation Ready**

This design leverages existing patterns and infrastructure while providing a clean, manageable solution for email advertising without the complexity of real-time screenshot generation.