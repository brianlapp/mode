import streamlit as st

# Simple redirect to main dashboard
st.set_page_config(
    page_title="Mode Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Mode Properties Dashboard")
st.markdown("**Redirecting to main dashboard...**")

# Import and run the main dashboard
exec(open('streamlit-dashboard.py').read()) 