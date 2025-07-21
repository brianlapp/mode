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

# Custom CSS for better card styling
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: white;
}

.priority-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: white;
}

.success-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: white;
}

.warning-card {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: white;
}

.build-card {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    color: #333;
}

.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.property-link {
    background: rgba(255,255,255,0.2);
    padding: 0.3rem 0.6rem;
    border-radius: 5px;
    text-decoration: none;
    color: white !important;
    display: inline-block;
    margin-top: 0.5rem;
    transition: all 0.3s ease;
}

.property-link:hover {
    background: rgba(255,255,255,0.3);
    transform: translateY(-2px);
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
    # Header with logo
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Mode Free Finds logo
        st.image("https://lh3.googleusercontent.com/hOi8rYWOfLYZQ0YjqAJlRLw-NRsDd3_s1YAp6XkUTwV4d2C5W1opPn4E1gSFlrlAXZaF3bTUl8vKuXkgNgf1kfFXrQmDzZRlS4I=w383", 
                 width=150, caption="ModeFreeFinds.com")
    
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Mode Optimization Dashboard</h1>
            <p>Lead Generation Empire • 3.4M+ Subscribers • Revenue Optimization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.metric("Properties", "4", delta="Active")
        st.metric("Target CPL", "$0.45")
    
    st.markdown(f"📅 **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")
    
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
        mff = properties.get('mode_free_finds', {})
        st.markdown(f"""
        <div class="success-card">
            <h3>📈 ModeFreeFinds.com</h3>
            <h2>CPL: {mff.get('meta_cpl', 'N/A')} ✅</h2>
            <p><strong>Revenue:</strong> {mff.get('monthly_revenue', 'N/A')}</p>
            <p><strong>Email List:</strong> {mff.get('email_list', 'N/A')}</p>
            <p><strong>Status:</strong> Target Met - Scaling Opportunity</p>
        </div>
        """, unsafe_allow_html=True)
        if 'leadpages_example' in mff:
            st.markdown(f'<a href="{mff["leadpages_example"]}" class="property-link" target="_blank">🔗 View Signup Flow</a>', unsafe_allow_html=True)
    
    # MMM Card  
    with col2:
        mmm = properties.get('mode_market_munchies', {})
        st.markdown(f"""
        <div class="warning-card">
            <h3>📊 ModeMarketMunchies.com</h3>
            <h2>CPL: {mmm.get('meta_cpl', 'N/A')} ⚠️</h2>
            <p><strong>Target:</strong> {mmm.get('target_cpl', 'N/A')}</p>
            <p><strong>Email List:</strong> {mmm.get('email_list', 'N/A')}</p>
            <p><strong>🚨 PRIORITY:</strong> CPL Optimization Required!</p>
            <p><strong>Impact:</strong> 90% cost reduction potential</p>
        </div>
        """, unsafe_allow_html=True)
        if 'leadpages_example' in mmm:
            st.markdown(f'<a href="{mmm["leadpages_example"]}" class="property-link" target="_blank">🔗 View Signup Flow</a>', unsafe_allow_html=True)
    
    # MCAD Card
    with col3:
        mcad = properties.get('mode_class_actions', {})
        st.markdown(f"""
        <div class="build-card">
            <h3>⚖️ ModeClassActionsDaily.com</h3>
            <h2>Status: Missing Flows 🔨</h2>
            <p><strong>Email List:</strong> {mcad.get('email_list', 'N/A')}</p>
            <p><strong>Focus:</strong> Class Action Alerts</p>
            <p><strong>Priority:</strong> Build Signup/TY Flows</p>
            <p><strong>Timeline:</strong> Week 2-3</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="https://modeclassactionsdaily.com" class="property-link" target="_blank">🔨 Build Signup Flow</a>', unsafe_allow_html=True)
    
    # MMD Card
    with col4:
        mmd = properties.get('mode_mobile_daily', {})
        st.markdown(f"""
        <div class="build-card">
            <h3>📱 ModeMobileDaily.com</h3>
            <h2>Status: Missing Setup 🔨</h2>
            <p><strong>Daily Active Users:</strong> {mmd.get('audience', 'N/A')}</p>
            <p><strong>Focus:</strong> Viral News & Trends</p>
            <p><strong>Priority:</strong> Build Email Integration</p>
            <p><strong>Timeline:</strong> Week 3-4</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="https://modemobiledaily.com" class="property-link" target="_blank">🔨 Build Signup Flow</a>', unsafe_allow_html=True)
    
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
    
    # Footer
    st.markdown("---")
    st.markdown("🚀 **Mode Optimization Dashboard** | Built for revenue optimization")

if __name__ == "__main__":
    main() 