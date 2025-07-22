#!/usr/bin/env python3
"""
Mode Optimization Dashboard - Streamlit Version
Web-based dashboard that can be shared with Mike
Deploy with: streamlit run streamlit-dashboard.py
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Mode Optimization Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Minimal styling for clean look with black header
st.markdown("""
<style>
.main-content {
    max-width: 1200px;
    margin: 0 auto;
}
.header-section {
    background-color: #000000;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
}
.header-title {
    color: white;
    margin-bottom: 0.5rem;
}
.header-subtitle {
    color: #cccccc;
    margin-bottom: 0.5rem;
}
.header-timestamp {
    color: #999999;
    font-size: 0.9em;
}
</style>
""", unsafe_allow_html=True)

def load_project_data():
    """Load project data from memory bank"""
    try:
        with open("memory-bank/project-memories.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("⚠️ Memory bank not found. Make sure to run from project root directory.")
        return {}

def main():
    # Header with black background and centered logo
    st.markdown("""
    <div class="header-section">
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <img src="https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg" 
                 width="250" style="max-width: 100%; height: auto;">
        </div>
        <h1 class="header-title">🚀 Mode Optimization Dashboard</h1>
        <p class="header-subtitle"><strong>Lead Generation Empire • 3.4M+ Subscribers • Revenue Optimization</strong></p>
        <p class="header-timestamp">📅 <strong>Last Updated:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    data = load_project_data()
    
    if not data:
        st.warning("No project data found. Please check memory bank file.")
        return
    
    # Property Status Cards
    st.header("🏢 Property Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    properties = data.get('properties', {})
    
    # MFF Card
    with col1:
        # MFF Logo
        st.image("https://lh3.googleusercontent.com/hOi8rYWOfLYZQ0YjqAJlRLw-NRsDd3_s1YAp6XkUTwV4d2C5W1opPn4E1gSFlrlAXZaF3bTUl8vKuXkgNgf1kfFXrQmDzZRlS4I=w383", 
                 width=150)
        
        mff = properties.get('mode_free_finds', {})
        st.metric(
            label="ModeFreeFinds.com",
            value=mff.get('meta_cpl', 'N/A'),
            delta="✅ Target Met"
        )
        st.text(f"Revenue: {mff.get('monthly_revenue', 'N/A')}")
        st.text(f"List: {mff.get('email_list', 'N/A')}")
        if 'leadpages_example' in mff:
            st.markdown(f"🔗 [View Signup Flow]({mff['leadpages_example']})")
    
    # MMM Card  
    with col2:
        # MMM Logo
        st.image("https://lh3.googleusercontent.com/lt64vW20ku4h6VAEOduskIyi9yv8tg5WHZX8vU9znMdwQAaLpNOQWbJqLA1F_cP4NA8WC4GqD3GoyoLPqXqpvK6FC81KHiuO3Yc=w1064", 
                 width=150)
        
        mmm = properties.get('mode_market_munchies', {})
        st.metric(
            label="ModeMarketMunchies.com", 
            value=mmm.get('meta_cpl', 'N/A'),
            delta=f"Target: {mmm.get('target_cpl', 'N/A')}",
            delta_color="inverse"
        )
        st.text(f"List: {mmm.get('email_list', 'N/A')}")
        st.error("🚨 PRIORITY: CPL too high!")
        if 'leadpages_example' in mmm:
            st.markdown(f"🔗 [View Signup Flow]({mmm['leadpages_example']})")
    
    # MCAD Card
    with col3:
        # MCAD Logo
        st.image("https://modeclassactionsdaily.com/wp-content/uploads/2025/04/class-actions-logo.png", 
                 width=150)
        
        mcad = properties.get('mode_class_actions', {})
        st.metric(
            label="ModeClassActionsDaily.com",
            value="Missing Flows",
            delta="🔨 To Build"
        )
        st.text(f"List: {mcad.get('email_list', 'N/A')}")
        st.markdown("🔗 [Build Signup Flow](https://modeclassactionsdaily.com) 🔨")
    
    # MMD Card
    with col4:
        # MMD Logo
        st.image("https://modemobiledaily.com/wp-content/uploads/2025/06/cropped-Daily-2a.png", 
                 width=150)
        
        mmd = properties.get('mode_mobile_daily', {})
        st.metric(
            label="ModeMobileDaily.com",
            value="Missing Setup", 
            delta="🔨 To Build"
        )
        st.text(f"DAU: {mmd.get('audience', 'N/A')}")
        st.markdown("🔗 [Build Signup Flow](https://modemobiledaily.com) 🔨")
    
    st.markdown("---")
    
    # Priorities Section
    st.header("🎯 Immediate Priorities")
    
    priorities = data.get('immediate_priorities', [])
    
    for priority in priorities:
        priority_num = priority.get('priority', '?')
        task = priority.get('task', 'Unknown task')
        timeline = priority.get('timeline', 'No timeline')
        impact = priority.get('impact', 'Unknown impact')
        
        with st.expander(f"Priority {priority_num}: {task}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"⏰ **Timeline:** {timeline}")
            with col2:
                st.write(f"💰 **Impact:** {impact}")
    
    st.markdown("---")
    
    # Quick Stats
    st.header("📊 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Subscribers", "3.4M+")
    
    with col2:
        st.metric("Properties", "4")
    
    with col3:
        st.metric("MFF Monthly Revenue", "~$40k")
    
    with col4:
        st.metric("Target CPL", "$0.45")
    
    st.markdown("---")
    
    # Today's Checklist
    st.header("✅ Today's Optimization Checklist")
    
    checklist_items = [
        "Check MMM CPL performance",
        "Review MFF conversion metrics", 
        "Update daily log with discoveries",
        "Log any code snippets created",
        "Validate attribution tracking",
        "Document optimization wins"
    ]
    
    for item in checklist_items:
        st.checkbox(item)
    
    st.markdown("---")
    
    # Memory Bank Status
    st.header("🧠 Memory Bank Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        daily_logs_dir = Path("memory-bank/daily-logs")
        if daily_logs_dir.exists():
            log_files = list(daily_logs_dir.glob("*.md"))
            st.metric("Daily Logs", len(log_files))
        else:
            st.metric("Daily Logs", "0", delta="Directory not found")
    
    with col2:
        wins_dir = Path("memory-bank/optimization-wins")
        if wins_dir.exists():
            win_files = list(wins_dir.glob("*"))
            st.metric("Optimization Wins", len(win_files))
        else:
            st.metric("Optimization Wins", "0", delta="Directory not found")
    
    # Landing Page Audit Section
    st.markdown("---")
    st.header("🕵️‍♂️ Landing Page Audit Findings")
    
    audit_col1, audit_col2 = st.columns(2)
    
    with audit_col1:
        st.subheader("🎯 Audit Summary")
        st.metric("CPL Gap Analysis", "10-20x Higher", delta="MMM vs MFF")
        st.metric("Critical Issues Found", "10", delta="High Impact")
        st.metric("Quick Wins Available", "3", delta="24-48hrs")
        
        st.markdown("**📊 Key Findings:**")
        st.markdown("- Phone field adds 20-30% friction")
        st.markdown("- Abstract value vs tangible proof")
        st.markdown("- Complex messaging dilutes focus")
        st.markdown("- Missing trust signals")
    
    with audit_col2:
        st.subheader("🚀 Optimization Roadmap")
        
        # Progress bars for implementation phases
        st.markdown("**Week 1: Quick Wins**")
        st.progress(0.0, text="Remove phone field (Ready)")
        
        st.markdown("**Week 2: Strategic Tests**")
        st.progress(0.0, text="A/B test headlines (Planned)")
        
        st.markdown("**Week 3-4: Advanced**")
        st.progress(0.0, text="Mobile optimization (Planned)")
        
        st.markdown("**🎯 Expected Impact:**")
        st.metric("Target CPL Reduction", "60-80%", delta="$5-10 → $0.45-1.00")
    
    # Detailed audit findings expander
    with st.expander("📋 View Detailed Audit Findings", expanded=False):
        st.markdown("### 🔥 High-Impact Fixes (24-48 hours)")
        
        fix_col1, fix_col2, fix_col3 = st.columns(3)
        
        with fix_col1:
            st.markdown("**1. Remove Phone Field**")
            st.markdown("- Current: 4 fields")
            st.markdown("- Fix: Match MFF's 3 fields")
            st.markdown("- Impact: 20-30% improvement")
        
        with fix_col2:
            st.markdown("**2. Simplify Value Prop**")
            st.markdown("- Current: Complex investment")
            st.markdown("- Fix: 'Daily Financial Opportunities'")
            st.markdown("- Impact: 15-25% clarity boost")
        
        with fix_col3:
            st.markdown("**3. Add Trust Elements**")
            st.markdown("- Current: Text-heavy")
            st.markdown("- Fix: Testimonials, social proof")
            st.markdown("- Impact: 10-20% trust increase")
        
        st.markdown("---")
        st.markdown("### 📈 Success Pattern Analysis")
        
        comparison_data = {
            'Factor': ['Visual Trust', 'Form Friction', 'Message Clarity', 'Risk Perception', 'Social Proof'],
            'MFF (Winner)': ['Product photos', '3 fields', 'Single benefit', 'No-risk freebies', 'Facebook integration'],
            'MMM (Problem)': ['Abstract concept', '4 fields + phone', 'Multiple concepts', 'Financial risk', 'Missing'],
            'Impact Level': ['HIGH', 'CRITICAL', 'HIGH', 'CRITICAL', 'MEDIUM']
        }
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("**💡 Key Insight:** MFF succeeds with tangible, simple, low-risk value proposition. MMM needs systematic friction removal.")
        
        # Link to full audit document
        st.markdown("📄 **Complete audit report available in project files** for detailed analysis and implementation steps.")

    # Footer
    st.markdown("---")
    st.markdown("🚀 **Mode Optimization Dashboard** | Built for revenue optimization")

if __name__ == "__main__":
    main() 