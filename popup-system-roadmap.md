# 🎯 Mode Popup System - 4-Day Roadmap

## 📋 **PROJECT OVERVIEW**
**Goal:** Campaign management dashboard + embeddable popup script  
**Timeline:** 4 days  
**Budget:** $5/month hosting  
**Revenue Impact:** Immediate popup monetization for Mike's 400k monthly impressions  

---

## 🎨 **CRITICAL DESIGN REQUIREMENTS**
**⚠️ MUST PRESERVE EXACT TEMPLATE DESIGN ⚠️**
- **Dual Image System:** Logo circle (top-left) + Main offer image
- **Mode Branding:** Pink/blue color scheme exactly as approved
- **Layout:** Maintain exact spacing, typography, and interactions from demo
- **Mobile Responsive:** Preserve design integrity across all devices

---

## 🗓️ **DAY-BY-DAY ROADMAP**

### **Day 1: Backend Foundation** ⚡
**Goal:** Working API for campaign management
- [ ] FastAPI project setup + Railway deployment
- [ ] SQLite database (campaigns + campaign_properties tables)  
- [ ] **Updated Schema:** Add logo_url + main_image_url fields
- [ ] Core CRUD endpoints (add/edit/delete campaigns)
- [ ] Property assignment endpoints
- [ ] Basic campaign fetching API for popup script

**Success:** Mike can add/edit campaigns with dual images via API

### **Day 2: Admin Dashboard** 🎛️
**Goal:** User-friendly interface for Mike
- [ ] Simple HTML/CSS admin interface
- [ ] Campaign add/edit forms with **dual image upload**:
  - Logo/Brand Image (for top-left circle)
  - Main Offer Image (for campaign display)
- [ ] **Image preview** showing exact popup layout
- [ ] Property controls (MFF, MMM, MCAD, MMD toggles)
- [ ] Visibility percentage sliders (0-100%)
- [ ] Integration code display (copy-paste script)

**Success:** Mike can manage campaigns with proper image preview

### **Day 3: Popup Script** 🚀
**Goal:** Production-ready embeddable script with EXACT design template
- [ ] Lightweight popup.js (no dependencies)
- [ ] **Exact Mode design replication:**
  - Logo circle positioning (top-left)
  - Main image display area
  - Typography and spacing matching demo
  - Mode pink/blue color scheme
- [ ] Mobile responsive (preserving design integrity)
- [ ] Property-specific campaign fetching
- [ ] Smart campaign rotation (weighted by visibility %)
- [ ] Session frequency respect
- [ ] Simple impression tracking

**Success:** Popup matches approved design template exactly

### **Day 4: Polish & Launch** 🎉
**Goal:** Production deployment + Mike validation
- [ ] Mike testing and feedback on design accuracy
- [ ] Bug fixes and UX improvements
- [ ] **Design template validation** (pixel-perfect matching)
- [ ] Production deployment optimization
- [ ] MFF integration testing
- [ ] Monitoring and alerts setup

**Success:** Live popup with exact approved design generating revenue

---

## 🎨 **UPDATED DATABASE SCHEMA**
```sql
campaigns (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    tune_url TEXT NOT NULL,
    logo_url TEXT NOT NULL,      -- NEW: For top-left circle
    main_image_url TEXT NOT NULL, -- NEW: For main offer display
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

campaign_properties (
    id INTEGER PRIMARY KEY,
    campaign_id INTEGER,
    property_code TEXT,
    visibility_percentage INTEGER DEFAULT 100,
    active BOOLEAN DEFAULT true,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
)
```

## 🎨 **ADMIN INTERFACE UPDATE**
```
┌─ Add New Campaign ─────────────────────────────────────────┐
│ Campaign Name: [Tesla Stock Alert]                         │
│ Tune URL: [https://track.modemobile.com/aff_ad?camp...]    │
│                                                            │
│ Logo/Brand Image (Circle): [Choose File] [Preview]        │
│ Main Offer Image: [Choose File] [Preview]                 │
│                                                            │
│ ┌─ Popup Preview ────────────────────────────────────────┐ │
│ │ [●] [Tesla Logo]          [×]                          │ │
│ │                                                        │ │
│ │     [Main Tesla Stock Image]                           │ │
│ │                                                        │ │
│ │ Tesla Down 50% - Insider Alert                        │ │
│ │ Get trading intel now...                               │ │
│ │ [Get Trading Intel]                                    │ │
│ └────────────────────────────────────────────────────────┘ │
│ [Save Campaign]                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 **SUCCESS CRITERIA**
1. Mike adds campaign with dual images in <2 minutes ✅
2. Popup shows EXACT approved design template ✅
3. Logo circle and main image display correctly ✅
4. Clicks go to Tune URLs properly ✅
5. Property controls work (on/off, percentages) ✅
6. Mobile responsive design preserved ✅
7. System handles 15k daily impressions ✅

---

## 📦 **DELIVERABLES**
- **API:** `popup-api.railway.app`
- **Admin:** `popup-api.railway.app/admin`  
- **Script:** `popup-api.railway.app/popup.js`
- **Documentation:** Integration guide for each property
- **Design Template:** Pixel-perfect popup matching approved demo

---

## 💰 **ROI CALCULATION**
- **Development:** 4 days
- **Hosting:** $5/month  
- **Current Traffic:** 400k impressions/month
- **Target CPL:** $0.45 (proven MFF rate)
- **Potential Revenue:** $180k/month
- **ROI:** 36,000x monthly return on hosting costs

---

## 🚨 **CRITICAL SUCCESS FACTOR**
**The design template is what got everyone excited!** Preserving the exact layout, branding, and user experience from the demo is essential for project success. Any deviation from the approved design could impact stakeholder confidence and conversion rates. 