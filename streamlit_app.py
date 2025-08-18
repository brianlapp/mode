import streamlit as st
import json
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Mode Optimization Dashboard v2.0", 
    page_icon="🚀",
    layout="wide"
)

# Import and execute the main dashboard
exec(open('streamlit-dashboard.py').read()) 