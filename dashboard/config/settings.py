"""
Dashboard Configuration and Settings
Extracted from main dashboard for modular architecture
"""

import streamlit as st

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Mode Optimization Dashboard", 
        page_icon="🚀",
        layout="centered"
    )

def apply_custom_css():
    """Apply custom CSS styles to the dashboard"""
    st.markdown("""
    <style>
        .main > div {
            background-color: black;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        .stSelectbox > div > div {
            background-color: #f0f2f6;
        }
        .metric-card {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #007bff;
        }
        .code-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .risk-low { border-left: 4px solid #28a745; }
        .risk-medium { border-left: 4px solid #ffc107; }
        .risk-high { border-left: 4px solid #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# Constants
LOGO_PATH = "img/logo.svg"
LOGO_WIDTH = 200

# Page identifiers
PAGES = {
    "OVERVIEW": "🏠 Overview Dashboard",
    "GLOBAL_SCRIPTS": "🔧 Global Scripts Implementation", 
    "CODE_REPOSITORY": "💻 Code Repository",
    "PROPERTIES_HUB": "🏢 Mode Properties Hub",
    "ANALYTICS": "📈 Analytics & Reports"
}

# URL parameter mappings
URL_PARAM_MAPPINGS = {
    "code": PAGES["CODE_REPOSITORY"],
    "global": PAGES["GLOBAL_SCRIPTS"],
    "analytics": PAGES["ANALYTICS"],
    "properties": PAGES["PROPERTIES_HUB"],
    "portfolio": PAGES["PROPERTIES_HUB"]
} 