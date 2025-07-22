import streamlit as st
import json
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Mode Optimization Dashboard", 
    page_icon="🚀",
    layout="wide"
)

# Custom CSS with black header
st.markdown("""
<style>
    .main > div {
        background-color: black;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .info-pill {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: 1px solid #bee5eb;
        max-width: 50%;
        margin: 0.5rem 0;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Header with main Mode logo
st.markdown("""
<div style="background-color: black; padding: 1rem 0; margin-bottom: 2rem; text-align: center;">
    <img src="https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg" width="200">
</div>
""", unsafe_allow_html=True)

st.title("🚀 Mode Optimization Dashboard")
st.markdown("*Real-time insights for Lead Revenue Optimization*")

# Load corrected data
try:
    with open("memory-bank/project-memories-corrected.json") as f:
        data = json.load(f)
except:
    # Fallback to original if corrected doesn't exist yet
    with open("memory-bank/project-memories.json") as f:
        data = json.load(f)

# Property Status Cards - UPDATED LAYOUT
# 📊 DATA OVERVIEW SECTION
st.header("Property Status")

# Row 1: MFF and MM (with more space for MM traffic data)
col1, col2 = st.columns(2)

properties = data.get('properties', {})

# MFF Card
with col1:
    st.image("https://lh3.googleusercontent.com/hOi8rYWOfLYZQ0YjqAJlRLw-NRsDd3_s1YAp6XkUTwV4d2C5W1opPn4E1gSFlrlAXZaF3bTUl8vKuXkgNgf1kfFXrQmDzZRlS4I=w383", 
             width=150)
    
    mff = properties.get('mode_free_finds', {})
    st.metric(
        label="ModeFreeFinds (MFF)",
        value="$0.45 CPL",
        delta="⚠️ Breaking Even",
        delta_color="normal"
    )
    st.warning("📊 Just breaking even")
    st.text("Revenue: $40k/month")
    st.text("List: 1.5M subscribers")
    if 'leadpages_example' in mff:
        st.markdown(f"🔗 [View Flow]({mff['leadpages_example']})")

# MM Card - EXPANDED with traffic breakdown
with col2:
    st.image("https://lh3.googleusercontent.com/lt64vW20ku4h6VAEOduskIyi9yv8tg5WHZX8vU9znMdwQAaLpNOQWbJqLA1F_cP4NA8WC4GqD3GoyoLPqXqpvK6FC81KHiuO3Yc=w1064", 
             width=150)
    
    st.metric(
        label="ModeMarketMunchies (MM)",
        value="TRAFFIC SPLIT",
        delta="See breakdown below"
    )
    
    # Create two sub-columns for traffic data
    traffic_col1, traffic_col2 = st.columns(2)
    
    with traffic_col1:
        st.success("🔥 **AFFILIATE TRAFFIC**")
        st.metric("CPL", "$1.50", delta="+$3.00 profit/lead")
        st.text("ROI: 200%")
        st.text("Status: CRUSHING IT")
    
    with traffic_col2:
        st.error("💸 **META TRAFFIC**")
        st.metric("CPL", "$5-10", delta="-$3.00 loss/lead")
        st.text("ROI: -40% to -122%")
        st.text("Status: BLEEDING MONEY")
    
    st.text("List: 900k subscribers")
    if 'leadpages_example' in properties.get('mode_market_munchies', {}):
        st.markdown(f"🔗 [View Flow]({properties['mode_market_munchies']['leadpages_example']})")

# Add spacing between rows
st.markdown("<br>", unsafe_allow_html=True)

# Row 2: MCAD and MMD  
col3, col4 = st.columns(2)

# MCAD Card
with col3:
    st.image("https://modeclassactionsdaily.com/wp-content/uploads/2025/04/class-actions-logo.png",
             width=150)

    st.metric(
        label="ModeClassActionsDaily",
        value="TO BUILD",
        delta="1M list waiting"
    )
    st.markdown('<div class="info-pill">📋 Missing signup/TY flows</div>', unsafe_allow_html=True)
    st.text("List: 1M subscribers")
    st.text("Revenue: $0 (no setup)")

# MMD Card
with col4:
    st.image("https://modemobiledaily.com/wp-content/uploads/2025/06/cropped-Daily-2a.png",
             width=150)
    
    st.metric(
        label="ModeMobileDaily",
        value="TO BUILD", 
        delta="50k DAU potential"
    )
    st.markdown('<div class="info-pill">📱 Missing email setup</div>', unsafe_allow_html=True)
    st.text("App Users: 50k daily")
    st.text("Revenue: $0 (no setup)")


# MM TRAFFIC ANALYSIS SECTION
st.markdown("---")
# 🔍 ANALYSIS SECTION
st.header("**MM Traffic Performance Analysis**")

analysis_col1, analysis_col2, analysis_col3 = st.columns(3)

with analysis_col1:
    st.subheader("Affiliate Traffic (WINNING)")
    st.success("**CRUSHING IT - $3 profit per lead**")
    
    affiliate_data = {
        'Metric': ['Cost per Lead', 'Revenue per Lead', 'Profit per Lead', 'ROI'],
        'Value': ['$1.50', '$4.50', '$3.00', '200%']
    }
    st.dataframe(pd.DataFrame(affiliate_data), use_container_width=True)
    
    st.markdown("**✅ Why it works:**")
    st.markdown("- Pre-warmed, high-intent users")
    st.markdown("- Trust established by referrer")
    st.markdown("- Financial niche understanding")

with analysis_col2:
    st.subheader("Meta Traffic (PROBLEM)")
    st.error("**BLEEDING MONEY - losing $3-5.50/lead**")
    
    meta_data = {
        'Metric': ['Cost per Lead', 'Revenue per Lead', 'Profit per Lead', 'ROI'],
        'Value': ['$5-10', '$4.50', '-$0.50 to -$5.50', '-11% to -122%']
    }
    st.dataframe(pd.DataFrame(meta_data), use_container_width=True)
    
    st.markdown("**❌ Why it fails:**")
    st.markdown("- Cold audience from social scrolling")
    st.markdown("- Zero trust or context")
    st.markdown("- Need immediate value clarity")

with analysis_col3:
    st.subheader("Target Opportunity")
    st.info("**Get Meta to match Affiliate performance**")
    
    target_data = {
        'Metric': ['Target Meta CPL', 'Target Profit', 'Monthly Potential', 'Mike\'s Budget'],
        'Value': ['$1.50', '$3.00/lead', '$2M+', '$1M available']
    }
    st.dataframe(pd.DataFrame(target_data), use_container_width=True)
    
    st.markdown("**🚀 If we crack it:**")
    st.markdown("- Unlimited profitable scaling")
    st.markdown("- $1M+/month spend capacity")  
    st.markdown("- Industry-leading ROI")

# CORRECTED PRIORITIES SECTION
st.markdown("---")
st.header("**Optimization Priorities**")

priorities = data.get('corrected_priorities', data.get('immediate_priorities', []))

for i, priority in enumerate(priorities[:4]):
    priority_col1, priority_col2, priority_col3 = st.columns([1, 2, 1])
    
    with priority_col1:
        if i == 0:
            st.error(f"🥇 **Priority {priority['priority']}**")
        elif i == 1:
            st.warning(f"🥈 **Priority {priority['priority']}**")
        else:
            st.info(f"🥉 **Priority {priority['priority']}**")
    
    with priority_col2:
        st.markdown(f"**{priority['task']}**")
        st.text(f"Impact: {priority['impact']}")
        st.text(f"Timeline: {priority['timeline']}")
        
        if 'focus' in priority:
            st.markdown(f"*Focus: {priority['focus']}*")
    
    with priority_col3:
        if 'goal' in priority:
            st.metric("Goal", priority['goal'])
        elif 'expected_week_1_cpl' in priority:
            st.metric("Week 1 Target", priority['expected_week_1_cpl'])

# Today's Optimization Checklist - SINGLE LIST
st.markdown("---")
# ⚡ ACTION SECTION
st.header("✅ Today's Optimization Checklist")

# Single unified checklist
st.checkbox("Review corrected strategy document", value=False)
st.checkbox("Approve Meta-specific MM approach", value=False) 
st.checkbox("Share current affiliate vs Meta data", value=False)
st.checkbox("Set Week 1 Meta optimization budget", value=False)
st.checkbox("Research cold traffic psychology for financial offers", value=False)
st.checkbox("Design Meta-specific MM landing page", value=False)
st.checkbox("Set up traffic source segmentation", value=False) 
st.checkbox("Plan API integration for Tune + Meta data", value=False)

st.text_input("Add new task:", placeholder="Future: Mike can add via @mode-optimizer")

# Meta Optimization Strategy Section
st.markdown("---")
st.header("**Meta Traffic Optimization Strategy**")

strategy_col1, strategy_col2 = st.columns(2)

with strategy_col1:
    st.subheader("Cold Traffic Psychology")
    st.markdown("**Key Differences from Affiliate Traffic:**")
    st.markdown("- ❄️ **Cold audience** - no prior financial interest")
    st.markdown("- 🚫 **Zero trust** - never heard of MM before")
    st.markdown("- ⚡ **Instant gratification** - need immediate value clarity")
    st.markdown("- 👀 **Social scrolling mode** - distracted mindset")
    st.markdown("- 🎯 **Beginner-friendly** - avoid financial jargon")

with strategy_col2:
    st.subheader("Implementation Approach")
    st.markdown("**Meta-Specific Optimizations:**")
    st.markdown("- 📸 **Social proof visuals** - real success stories")
    st.markdown("- 💰 **Instant value promise** - clear financial benefit")
    st.markdown("- 🏆 **Trust signals** - testimonials, numbers, social proof")
    st.markdown("- 📱 **VIP positioning** - phone field as exclusive access")
    st.markdown("- 🎨 **Consistent creative** - ad to landing page alignment")

# Business Impact Section
st.markdown("---")
st.header("**Business Impact Potential**")

impact_col1, impact_col2, impact_col3 = st.columns(3)

with impact_col1:
    st.metric("Current MM Affiliate ROI", "200%", delta="$3 profit per $1.50 spend")
    st.success("✅ Keep this working!")

with impact_col2:
    st.metric("Current MM Meta ROI", "-40% to -122%", delta="Losing money", delta_color="inverse")
    st.error("🎯 Fix this = massive opportunity")

with impact_col3:
    st.metric("Potential Monthly Profit", "$2M+", delta="If Meta matches affiliate")
    st.info("💡 Mike's $1M budget available")

# Quick Stats
st.markdown("---")
# 📈 METRICS SECTION
st.header("Quick Stats")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Email Subscribers", "3.45M", delta="Across all properties")

with stat_col2:
    st.metric("Monthly Pageviews", "1M+", delta="MFF primary traffic")

with stat_col3:
    st.metric("Active Properties", "4", delta="2 revenue generating")

with stat_col4:
    st.metric("Optimization Potential", "$1M+/month", delta="Meta CPL optimization")


# Quick Links Section
st.markdown("---")
# 🔗 RESOURCES SECTION
st.header("Quick Links")

# Organize links by category
links_col1, links_col2, links_col3, links_col4 = st.columns(4)

with links_col1:
    st.subheader("**Landing Pages**")
    st.markdown("**[LeadPages Dashboard](https://my.leadpages.com/#/dashboard)**")
    st.markdown("- [MFF Signup Flow](https://join.modefreefinds.com/mff-signup-affiliate/)")
    st.markdown("- [MM Signup Flow](https://signups.modemobile.com/mm-signup-affv1/)")

with links_col2:
    st.subheader("**AI & Optimization**")
    st.markdown("**[Revmatics.ai](https://revmatics.ai/)**")
    st.markdown("*AI-powered landing page optimization*")

with links_col3:
    st.subheader("**Revenue & Tracking**")
    st.markdown("**[Tune (HasOffers)](https://modemobile.go2cloud.org/)**")
    st.markdown("*Affiliate platform & revenue attribution*")
    st.markdown("**[Meta Business Manager](https://business.facebook.com/)**")
    st.markdown("*Meta Ads management*")

with links_col4:
    st.subheader("**Properties**")
    st.markdown("**[ModeFreeFinds.com](https://modefreefinds.com/)**")
    st.markdown("**[ModeMarketMunchies.com](https://modemarketmunchies.com/)**")
    st.markdown("**[ModeClassActionsDaily.com](https://modeclassactionsdaily.com/)**")
    st.markdown("**[ModeMobileDaily.com](https://modemobiledaily.com/)**")
    st.markdown("**[Mode Earn App](https://play.google.com/store/apps/details?id=us.current.android&hl=en_CA)**")



# Footer
st.markdown("---")
st.markdown("*Dashboard updated: 2025-01-27 with corrected business reality*")
st.markdown("**🚀 Ready to unlock the $1M+/month Meta traffic opportunity!**")
