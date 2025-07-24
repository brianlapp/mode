"""
Overview Dashboard Page
Clean landing page with navigation and portfolio snapshot
"""

import streamlit as st
from ..config.settings import PAGES

def render_overview_page():
    """Render the Overview Dashboard page"""
    st.title("🎯 Mode Properties Optimization Dashboard")
    st.markdown("**Complete portfolio analysis, mobile optimization, and revenue tracking for Mike's 4 Mode properties**")
    
    # Quick Navigation Cards
    st.header("🗂️ Dashboard Sections")
    
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        if st.button("🏢 Mode Properties Hub\n\nComplete portfolio management with visual insights, optimization strategies, and implementation roadmaps for all 4 Mode properties.", 
                     use_container_width=True, key="nav_properties", type="primary"):
            st.session_state.page = PAGES["PROPERTIES_HUB"]
            st.rerun()
    
    with nav_col2:
        if st.button("🔧 Global Scripts\n\nLeadPages implementation guide with Mike's optimized tracking code ready for deployment.", 
                     use_container_width=True, key="nav_global", type="primary"):
            st.session_state.page = PAGES["GLOBAL_SCRIPTS"]
            st.rerun()
    
    with nav_col3:
        if st.button("💻 Code Repository\n\nAll optimization code, scripts, and technical implementations organized by property and function.", 
                     use_container_width=True, key="nav_code", type="primary"):
            st.session_state.page = PAGES["CODE_REPOSITORY"]
            st.rerun()

    # Quick Stats
    st.markdown("---")
    st.header("📊 Portfolio Snapshot")
    
    snapshot_col1, snapshot_col2, snapshot_col3, snapshot_col4 = st.columns(4)
    
    with snapshot_col1:
        st.metric(
            label="🟢 Active Revenue",
            value="$25k-$35k",
            delta="ModeFreeFinds monthly"
        )
    
    with snapshot_col2:
        st.metric(
            label="📊 Total Properties", 
            value="4",
            delta="1 Live, 1 Launched, 2 Development"
        )
    
    with snapshot_col3:
        st.metric(
            label="🎯 Optimization Target",
            value="$50k-$75k",
            delta="Portfolio potential"
        )
    
    with snapshot_col4:
        st.metric(
            label="📧 Email Subscribers",
            value="3.45M",
            delta="Across all properties"
        )

    # Key Insights
    st.markdown("---")
    st.header("💡 Key Portfolio Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.success("**🎯 MFF Success Formula Proven**")
        st.markdown("- CPL: $0.45 (Target achieved)")
        st.markdown("- Revenue: $25k-$35k monthly")
        st.markdown("- Template ready for replication")
        
        st.info("**⚡ Immediate Opportunity**")
        st.markdown("- Prebid.js implementation")
        st.markdown("- Revenue lift: +$6k-$13k")
        st.markdown("- Timeline: 2-3 weeks")
    
    with insight_col2:
        st.warning("**📈 MMM Optimization Needed**")
        st.markdown("- Current CPL: $5-10 (unprofitable)")
        st.markdown("- Target CPL: $1.50 (affiliate baseline)")
        st.markdown("- Strategy: Apply MFF foundation")
        
        st.error("**🔧 Development Properties**")
        st.markdown("- MMD & MCAD: No flows built yet")
        st.markdown("- Revenue potential: $10k-$40k each")
        st.markdown("- Priority: Foundation setup")

    # External Links
    st.markdown("---")
    st.header("🔗 Quick Links & Resources")
    
    link_col1, link_col2, link_col3 = st.columns(3)
    
    with link_col1:
        st.markdown("**🌐 Live Properties**")
        st.markdown("- [ModeFreeFinds.com](https://modefreefinds.com/)")
        st.markdown("- [ModeMarketMunchies.com](https://modemarketmunchies.com/)")
        st.markdown("- [ModeMobileDaily.com](https://modemobiledaily.com/)")
        st.markdown("- [ModeClassActionsDaily.com](https://modeclassactionsdaily.com/)")

    with link_col2:
        st.markdown("**📊 Tracking & Analytics**")
        st.markdown("- [Tune (HasOffers)](https://modemobile.go2cloud.org/)")
        st.markdown("- [Meta Business Manager](https://business.facebook.com/)")
        st.markdown("- [Revmatics.ai](https://revmatics.ai/)")

    with link_col3:
        st.markdown("**💻 Development Resources**")
        st.markdown("- [GitHub Repository](https://github.com/brianlapp/mode)")
        st.markdown("- [Direct Dashboard Links](https://modedash.streamlit.app/)")
        st.markdown("- [Support Documentation](https://helpdesk.modemobile.com/)")

    # Quick Actions
    st.markdown("---")
    st.header("⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🎬 View Thanks.co Demo", use_container_width=True):
            st.session_state.page = PAGES["PROPERTIES_HUB"]
            st.rerun()
    
    with action_col2:
        if st.button("📈 Check Property Analytics", use_container_width=True):
            st.session_state.page = PAGES["ANALYTICS"]
            st.rerun()
    
    with action_col3:
        if st.button("🔧 Start Property Setup", use_container_width=True):
            st.session_state.page = PAGES["PROPERTIES_HUB"]
            st.rerun() 