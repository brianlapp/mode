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

def load_project_data():
    """Load project data from memory bank"""
    try:
        with open("memory-bank/project-memories.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("⚠️ Memory bank not found. Make sure to run from project root directory.")
        return {}

def main():
    # Header
    st.title("🚀 Mode Optimization Dashboard")
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
        st.metric(
            label="📈 ModeFreeFinds",
            value=mff.get('meta_cpl', 'N/A'),
            delta="✅ Target Met"
        )
        st.text(f"Revenue: {mff.get('monthly_revenue', 'N/A')}")
        st.text(f"List: {mff.get('email_list', 'N/A')}")
        if 'leadpages_example' in mff:
            st.markdown(f"🔗 [View Signup Flow]({mff['leadpages_example']})")
    
    # MMM Card  
    with col2:
        mmm = properties.get('mode_market_munchies', {})
        st.metric(
            label="📊 ModeMarketMunchies", 
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
        mcad = properties.get('mode_class_actions', {})
        st.metric(
            label="⚖️ ModeClassActions",
            value="Missing Flows",
            delta="🔨 To Build"
        )
        st.text(f"List: {mcad.get('email_list', 'N/A')}")
        st.markdown("🔗 [Build Signup Flow](https://modeClassActionsDaily.com) 🔨")
    
    # MMD Card
    with col4:
        mmd = properties.get('mode_mobile_daily', {})
        st.metric(
            label="📱 ModeMobileDaily",
            value="Missing Setup", 
            delta="🔨 To Build"
        )
        st.text(f"DAU: {mmd.get('audience', 'N/A')}")
        st.markdown("🔗 [Build Signup Flow](https://modeMobileDaily.com) 🔨")
    
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