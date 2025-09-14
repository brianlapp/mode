"""
Base Property Interface
Defines the standard interface that all Mode properties must implement
"""

from abc import ABC, abstractmethod
import streamlit as st

class BaseProperty(ABC):
    """Base class for all Mode properties"""
    
    def __init__(self, property_key: str, property_name: str, status: str):
        self.property_key = property_key
        self.property_name = property_name
        self.status = status
        self.logo_url = ""
        self.site_url = ""
        self.revenue = ""
        self.cpl = ""
        self.priority = ""
    
    @abstractmethod
    def render_overview_section(self):
        """Render the property overview with visuals and metrics"""
        pass
    
    @abstractmethod
    def render_optimization_strategy(self):
        """Render optimization strategy and roadmap"""
        pass
    
    @abstractmethod
    def render_implementation_timeline(self):
        """Render implementation timeline and phases"""
        pass
    
    def render_complete_tab(self):
        """Render the complete property tab (calls all sections)"""
        self.render_overview_section()
        st.markdown("---")
        self.render_optimization_strategy()
        st.markdown("---")
        self.render_implementation_timeline()
    
    def render_property_status_card(self):
        """Render a standardized property status card"""
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {self.property_name}")
                st.markdown(f"**Status:** {self.status}")
                if self.revenue:
                    st.markdown(f"**Revenue:** {self.revenue}")
                if self.cpl:
                    st.markdown(f"**CPL:** {self.cpl}")
                if self.site_url:
                    st.markdown(f"**URL:** [{self.site_url}]({self.site_url})")
            
            with col2:
                if self.priority:
                    if "HIGH" in self.priority.upper():
                        st.error(f"**{self.priority}**")
                    elif "MEDIUM" in self.priority.upper():
                        st.warning(f"**{self.priority}**")
                    else:
                        st.info(f"**{self.priority}**")

class PropertyManager:
    """Manages all properties and provides utility functions"""
    
    def __init__(self):
        self.properties = {}
    
    def register_property(self, property_key: str, property_instance: BaseProperty):
        """Register a property with the manager"""
        self.properties[property_key] = property_instance
    
    def get_property(self, property_key: str) -> BaseProperty:
        """Get a specific property instance"""
        return self.properties.get(property_key)
    
    def get_all_properties(self) -> dict:
        """Get all registered properties"""
        return self.properties
    
    def render_portfolio_overview(self):
        """Render portfolio overview with all properties"""
        st.header("📊 Portfolio Overview")
        
        # Portfolio metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Properties", "4", "Live: 1, Launched: 1, Development: 2")
        with col2:
            st.metric("💰 Monthly Revenue", "$25k-$35k", "ModeFreeFinds only")
        with col3:
            st.metric("👀 Monthly Pageviews", "1M+", "ModeFreeFinds traffic")
        with col4:
            st.metric("🎯 Revenue Potential", "$50k-$75k", "Optimized portfolio")
        
        st.markdown("---")
        
        # Property status cards
        st.subheader("🏢 Property Status Overview")
        
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            st.markdown("**🟢 Live & Profitable:**")
            for prop_key, prop in self.properties.items():
                if "🟢" in prop.status:
                    prop.render_property_status_card()
                    st.markdown("")
        
        with status_col2:
            st.markdown("**🟡 Development Stage:**")
            for prop_key, prop in self.properties.items():
                if "🟡" in prop.status or "🔴" in prop.status:
                    prop.render_property_status_card()
                    st.markdown("") 