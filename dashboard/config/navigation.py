"""
Navigation and Routing Logic
Handles sidebar navigation and URL parameter routing
"""

import streamlit as st
from .settings import PAGES, URL_PARAM_MAPPINGS, LOGO_PATH, LOGO_WIDTH

def render_sidebar_navigation():
    """Render the sidebar navigation menu"""
    # Logo and header
    st.sidebar.image(LOGO_PATH, width=LOGO_WIDTH)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Navigation")

    # Navigation buttons
    if st.sidebar.button("🏠 Overview Dashboard", use_container_width=True):
        st.session_state.page = PAGES["OVERVIEW"]
        st.query_params.clear()
        st.rerun()
        
    if st.sidebar.button("🔧 Global Scripts Implementation", use_container_width=True):
        st.session_state.page = PAGES["GLOBAL_SCRIPTS"]
        st.query_params.clear()
        st.rerun()
        
    if st.sidebar.button("💻 Code Repository", use_container_width=True):
        st.session_state.page = PAGES["CODE_REPOSITORY"]
        st.query_params.clear()
        st.rerun()
        
    if st.sidebar.button("🏢 Mode Properties Hub", use_container_width=True):
        st.session_state.page = PAGES["PROPERTIES_HUB"]
        st.query_params.clear()
        st.rerun()
        
    if st.sidebar.button("📈 Analytics & Reports", use_container_width=True):
        st.session_state.page = PAGES["ANALYTICS"]
        st.query_params.clear()
        st.rerun()

def handle_url_parameters():
    """Handle direct navigation via URL parameters"""
    query_params = st.query_params
    if "page" in query_params:
        page_param = query_params["page"]
        if page_param in URL_PARAM_MAPPINGS:
            st.session_state.page = URL_PARAM_MAPPINGS[page_param]

def initialize_session_state():
    """Initialize session state with default page"""
    if 'page' not in st.session_state:
        st.session_state.page = PAGES["OVERVIEW"]

def get_current_page():
    """Get the current active page"""
    return st.session_state.page

def render_footer():
    """Render the sidebar footer"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("*Dashboard updated: 2025-01-27*")
    st.sidebar.markdown("**🚀 Multi-page dashboard with honest metrics!**")
    st.sidebar.markdown("**Navigation:** Always-visible buttons (no dropdown!)") 