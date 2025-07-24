"""
Mode Properties Optimization Dashboard - Modular Version
Main entry point for the refactored dashboard
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path

# Import our modular components
from config.settings import configure_page, apply_custom_css, PAGES
from config.navigation import (
    render_sidebar_navigation, 
    handle_url_parameters, 
    initialize_session_state, 
    get_current_page,
    render_footer
)
from pages.overview import render_overview_page
from data.property_data import load_project_data

def main():
    """Main dashboard application"""
    # Configure page and apply styling
    configure_page()
    apply_custom_css()
    
    # Handle navigation
    render_sidebar_navigation()
    handle_url_parameters()
    initialize_session_state()
    
    # Get current page
    page = get_current_page()
    
    # Load project data (temporary - will be moved to data layer)
    try:
        properties = load_project_data().get('properties', {})
    except:
        properties = {}
    
    # Route to appropriate page
    if page == PAGES["OVERVIEW"]:
        render_overview_page()
        
    elif page == PAGES["GLOBAL_SCRIPTS"]:
        # TODO: Extract to pages/global_scripts.py
        render_global_scripts_page_legacy(properties)
        
    elif page == PAGES["CODE_REPOSITORY"]:
        # TODO: Extract to pages/code_repository.py
        render_code_repository_page_legacy()
        
    elif page == PAGES["PROPERTIES_HUB"]:
        # TODO: Extract to pages/properties_hub.py
        render_properties_hub_page_legacy(properties)
        
    elif page == PAGES["ANALYTICS"]:
        # TODO: Extract to pages/analytics_reports.py
        render_analytics_page_legacy(properties)
    
    # Render footer
    render_footer()

# Temporary legacy functions (will be extracted in next phases)
def render_global_scripts_page_legacy(properties):
    """Temporary function - will be extracted to pages/global_scripts.py"""
    st.title("🔧 LeadPages Global Scripts Implementation")
    st.markdown("**Step-by-step guide to implement Mike's cleaned code**")
    st.info("🚧 This page will be modularized in Phase 2 of the refactoring")
    
    # Implementation Status
    st.header("Implementation Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.metric("Setup Process", "Add → Save → Done", "applies to ALL content")
    with status_col2:
        st.metric("Universal Coverage", "ALL assets", "landing pages, pop-ups, sites") 
    with status_col3:
        st.metric("Implementation", "Copy-Paste Ready", "13 sections prepared")

def render_code_repository_page_legacy():
    """Temporary function - will be extracted to pages/code_repository.py"""
    st.title("💻 Clean Code Repository")
    st.markdown("**Copy-paste ready code sections for Global Scripts**")
    st.info("🚧 This page will be modularized in Phase 2 of the refactoring")

def render_properties_hub_page_legacy(properties):
    """Temporary function - will be extracted to pages/properties_hub.py"""
    st.title("🏢 Mode Properties Hub")
    st.markdown("Complete portfolio management with visual insights, optimization strategies, and implementation roadmaps")
    st.info("🚧 This page will be modularized in Phase 3 of the refactoring")

def render_analytics_page_legacy(properties):
    """Temporary function - will be extracted to pages/analytics_reports.py"""
    st.title("📈 Analytics & Performance Reports")
    st.info("🚧 This page will be modularized in Phase 2 of the refactoring")

if __name__ == "__main__":
    main() 