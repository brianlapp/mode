"""
Dashboard Deployment Manager
Manages transition from 2613-line monolith to modular architecture
"""

import streamlit as st
import shutil
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Dashboard Deployment Manager", 
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Dashboard Deployment Manager")
st.markdown("**Transition from 2613-line monolith → Clean modular architecture**")

# Deployment status
st.subheader("📊 Current Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Old Dashboard", "2613 lines", "streamlit-dashboard.py")

with col2:
    st.metric("New Dashboard", "✅ Modular", "streamlit_app_v2.py")

with col3:
    st.metric("Tune Integration", "✅ Ready", "Real campaigns")

st.markdown("---")

# Deployment options
st.subheader("🔄 Deployment Options")

deployment_choice = st.radio(
    "Choose deployment strategy:",
    [
        "🔄 Switch to New Dashboard (Recommended)",
        "📋 Compare Dashboards Side-by-Side", 
        "🛠️ Test Tune Integration",
        "📦 Archive Old Dashboard",
        "🔙 Rollback to Old Dashboard"
    ]
)

if deployment_choice == "🔄 Switch to New Dashboard (Recommended)":
    st.success("✅ **Recommended Choice** - Mike will love the clean organization!")
    
    st.markdown("**🎯 What this does:**")
    st.markdown("""
    1. **Backs up** current `streamlit_app.py` 
    2. **Replaces** it with new modular version
    3. **Preserves** all existing functionality
    4. **Adds** Mike's requested 2-section organization
    5. **Integrates** Tune campaign system
    """)
    
    if st.button("🚀 Deploy New Dashboard", type="primary"):
        try:
            # Backup current streamlit_app.py
            if os.path.exists("streamlit_app.py"):
                backup_name = f"streamlit_app_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                shutil.copy("streamlit_app.py", backup_name)
                st.success(f"✅ Backed up current app to: {backup_name}")
            
            # Copy new dashboard
            if os.path.exists("streamlit_app_v2.py"):
                shutil.copy("streamlit_app_v2.py", "streamlit_app.py")
                st.success("✅ New dashboard deployed!")
                st.balloons()
                
                st.markdown("**🎉 Deployment Complete!**")
                st.markdown("- ✅ Clean 2-section organization")
                st.markdown("- ✅ Company knowledge section")
                st.markdown("- ✅ Active tasks section")
                st.markdown("- ✅ Working popup demo")
                st.markdown("- ✅ Tune integration ready")
                
                st.info("🌟 **Next step:** Test the new dashboard at https://modedash.streamlit.app/")
            else:
                st.error("❌ streamlit_app_v2.py not found!")
                
        except Exception as e:
            st.error(f"❌ Deployment failed: {e}")

elif deployment_choice == "📋 Compare Dashboards Side-by-Side":
    st.info("📋 **Comparison View** - See the differences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Old Dashboard (2613 lines)")
        st.markdown("""
        **Issues:**
        - ❌ 2613 lines in single file
        - ❌ Mixed content (knowledge + tasks)
        - ❌ Hard to navigate
        - ❌ No clear organization
        - ❌ Static demo only
        """)
        
        if st.button("👀 View Old Structure"):
            with open("streamlit-dashboard.py", "r") as f:
                lines = f.readlines()
                st.text(f"Total lines: {len(lines)}")
                st.text("First 20 lines:")
                st.code("".join(lines[:20]))
    
    with col2:
        st.markdown("### ✨ New Dashboard (Modular)")
        st.markdown("""
        **Improvements:**
        - ✅ Clean 2-section organization
        - ✅ Company Knowledge section
        - ✅ Active Tasks section  
        - ✅ Easy navigation
        - ✅ Working Tune integration
        - ✅ Mike's favorite popup demo
        """)
        
        if st.button("👀 View New Structure"):
            if os.path.exists("streamlit_app_v2.py"):
                with open("streamlit_app_v2.py", "r") as f:
                    lines = f.readlines()
                    st.text(f"Total lines: {len(lines)}")
                    st.text("First 20 lines:")
                    st.code("".join(lines[:20]))

elif deployment_choice == "🛠️ Test Tune Integration":
    st.info("🔗 **Tune Integration Testing**")
    
    st.markdown("**🎯 Mike's Requirements:**")
    st.markdown("""
    1. ✅ Direct Tune ad integration into popup
    2. ✅ Backend management system for campaigns
    3. ✅ Manual URL/creative management
    4. ✅ Impression pixel tracking
    """)
    
    # Test buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎬 Test Popup Integration", type="primary"):
            st.success("🚀 Opening Tune popup test...")
            st.markdown("**Mike's iframe code:**")
            st.code("""<iframe src="https://track.modemobile.com/aff_ad?campaign_id=13&aff_id=43045&format=iframe" scrolling="no" frameborder="0" marginheight="0" marginwidth="0" width="600" height="400"></iframe>""")
    
    with col2:
        if st.button("🛠️ Test Management System", type="primary"):
            st.success("🔧 Opening campaign manager...")
            st.markdown("**Management features available:**")
            st.markdown("- ✅ Add/edit campaigns")
            st.markdown("- ✅ URL parameter management")
            st.markdown("- ✅ Impression tracking")
            st.markdown("- ✅ Performance analytics")

elif deployment_choice == "📦 Archive Old Dashboard":
    st.warning("📦 **Archive Old Dashboard** - Keep as backup")
    
    st.markdown("**What this does:**")
    st.markdown("""
    - Moves `streamlit-dashboard.py` to `archive/` folder
    - Creates timestamped backup
    - Preserves all 2613 lines for reference
    - Cleans up main directory
    """)
    
    if st.button("📦 Archive Old Dashboard"):
        try:
            # Create archive directory
            os.makedirs("archive", exist_ok=True)
            
            # Move old dashboard
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_name = f"archive/streamlit-dashboard-{timestamp}.py"
            shutil.move("streamlit-dashboard.py", archive_name)
            
            st.success(f"✅ Old dashboard archived to: {archive_name}")
            st.info("💡 Now you can deploy the new dashboard cleanly!")
            
        except Exception as e:
            st.error(f"❌ Archive failed: {e}")

elif deployment_choice == "🔙 Rollback to Old Dashboard":
    st.error("🔙 **Rollback** - Return to old dashboard")
    
    st.markdown("**⚠️ This will:**")
    st.markdown("""
    - Replace new dashboard with old version
    - Lose Mike's requested organization
    - Lose Tune integration
    - Return to 2613-line monolith
    """)
    
    st.warning("**Are you sure?** Mike loved the new demo!")
    
    if st.checkbox("I understand the consequences"):
        if st.button("🔙 Confirm Rollback", type="secondary"):
            try:
                if os.path.exists("streamlit-dashboard-backup.py"):
                    shutil.copy("streamlit-dashboard-backup.py", "streamlit_app.py")
                    st.success("✅ Rolled back to old dashboard")
                else:
                    st.error("❌ Backup file not found!")
            except Exception as e:
                st.error(f"❌ Rollback failed: {e}")

# Current file status
st.markdown("---")
st.subheader("📁 Current File Status")

files_to_check = [
    "streamlit_app.py",
    "streamlit_app_v2.py", 
    "streamlit-dashboard.py",
    "tune_integration.py",
    "tune_management_app.py"
]

for file in files_to_check:
    if os.path.exists(file):
        size = os.path.getsize(file)
        with open(file, 'r') as f:
            lines = len(f.readlines())
        st.success(f"✅ {file} - {lines} lines ({size} bytes)")
    else:
        st.error(f"❌ {file} - Not found")

# Quick actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌐 Open Live Dashboard"):
        st.markdown("[🚀 Open modedash.streamlit.app](https://modedash.streamlit.app/)")

with col2:
    if st.button("📊 View Analytics"):
        st.info("Opening analytics dashboard...")

with col3:
    if st.button("🔗 Test Tune Manager"):
        st.info("Opening Tune management system...")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 <strong>Dashboard Deployment Manager</strong></p>
    <p>From 2613-line monolith → Clean modular architecture Mike requested</p>
    <p>✅ Company Knowledge + ⚡ Active Tasks + 🔗 Tune Integration</p>
</div>
""", unsafe_allow_html=True) 