"""
Tune Campaign Management System
Backend interface for managing Tune CPL campaigns and creatives
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from tune_integration import TunePopupManager

# Page config
st.set_page_config(
    page_title="Tune Campaign Manager", 
    page_icon="🔗",
    layout="wide"
)

# Custom CSS for management interface
st.markdown("""
<style>
    .management-header {
        background: linear-gradient(135deg, #F7007C 0%, #07C8F7 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .campaign-card {
        background: white;
        border: 2px solid #F7007C;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-paused {
        color: #ffc107;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #07C8F7 0%, #F7007C 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="management-header">
    <h1>🔗 Tune Campaign Management System</h1>
    <p>Backend interface for Mike's Tune CPL campaigns and revenue tracking</p>
    <p><strong>🎯 Purpose:</strong> Manually add Tune links/impression pixels to popup units</p>
</div>
""", unsafe_allow_html=True)

# Initialize Tune manager
tune_manager = TunePopupManager()

# Sidebar navigation
st.sidebar.title("🧭 Management Menu")
page = st.sidebar.radio(
    "Select function:",
    ["📋 Campaign Dashboard", "➕ Add Campaign", "🔧 Campaign Editor", "📊 Analytics", "🔗 Tune Demo", "⚙️ Settings"],
    help="Navigate between management functions"
)

if page == "📋 Campaign Dashboard":
    st.header("📋 Campaign Dashboard")
    
    campaigns = tune_manager.campaigns
    
    if not campaigns:
        st.warning("No campaigns found. Add your first campaign!")
        if st.button("➕ Add First Campaign", type="primary"):
            st.switch_page("tune_management_app.py#add-campaign")
    else:
        # Overview metrics
        active_campaigns = [c for c in campaigns if c.get('active', True)]
        total_campaigns = len(campaigns)
        active_count = len(active_campaigns)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card"><h3>Total Campaigns</h3><h2>{}</h2></div>'.format(total_campaigns), unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card"><h3>Active</h3><h2>{}</h2></div>'.format(active_count), unsafe_allow_html=True)
        
        with col3:
            paused_count = total_campaigns - active_count
            st.markdown('<div class="metric-card"><h3>Paused</h3><h2>{}</h2></div>'.format(paused_count), unsafe_allow_html=True)
        
        with col4:
            impressions = len(st.session_state.get('tune_impressions', []))
            st.markdown('<div class="metric-card"><h3>Impressions</h3><h2>{}</h2></div>'.format(impressions), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Campaign list
        st.subheader("📝 Campaign Overview")
        
        for i, campaign in enumerate(campaigns):
            with st.expander(f"📈 {campaign['name']} - Campaign ID: {campaign['id']}", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Campaign ID:** {campaign['id']}")
                    st.markdown(f"**Affiliate ID:** {campaign['aff_id']}")
                    st.markdown(f"**Dimensions:** {campaign['width']}x{campaign['height']}")
                    st.markdown(f"**Created:** {campaign.get('created', 'Unknown')}")
                
                with col2:
                    status = "✅ Active" if campaign.get('active', True) else "⏸️ Paused"
                    st.markdown(f"**Status:** {status}")
                    
                    if st.button(f"{'⏸️ Pause' if campaign.get('active', True) else '▶️ Activate'}", 
                               key=f"toggle_status_{i}"):
                        tune_manager.campaigns[i]['active'] = not campaign.get('active', True)
                        st.session_state.tune_campaigns = tune_manager.campaigns
                        st.rerun()
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_{i}"):
                        st.session_state.edit_campaign_id = campaign['id']
                        st.session_state.page = "🔧 Campaign Editor"
                        st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        if st.session_state.get(f"confirm_delete_{i}", False):
                            # Actually delete
                            tune_manager.campaigns.pop(i)
                            st.session_state.tune_campaigns = tune_manager.campaigns
                            st.success(f"Campaign '{campaign['name']}' deleted!")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{i}"] = True
                            st.warning("Click again to confirm deletion!")
                
                # Show iframe code
                iframe_url = tune_manager.get_iframe_url(campaign['id'], campaign['aff_id'])
                st.markdown("**Generated iframe code:**")
                st.code(f"""<iframe src="{iframe_url}" scrolling="no" frameborder="0" marginheight="0" marginwidth="0" width="{campaign['width']}" height="{campaign['height']}"></iframe>""", 
                       language="html")

elif page == "➕ Add Campaign":
    st.header("➕ Add New Campaign")
    st.info("🎯 **Mike's Request:** Backend system to manually add Tune links/impression pixels")
    
    with st.form("add_new_campaign", clear_on_submit=True):
        st.subheader("📝 Campaign Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Campaign Name*", 
                               placeholder="e.g., Trading Platform Signup",
                               help="Internal campaign name")
            
            display_title = st.text_input("Display Title*", 
                                        placeholder="e.g., 50% off Premium Trading Platform",
                                        help="Title shown in popup")
            
            campaign_id = st.number_input("Campaign ID*", 
                                        min_value=1, 
                                        value=14,
                                        help="Tune campaign identifier")
            
            aff_id = st.number_input("Affiliate ID*", 
                                   min_value=1, 
                                   value=43045,
                                   help="Your Tune affiliate ID")
        
        with col2:
            tagline = st.text_input("Tagline", 
                                   placeholder="e.g., Build your wealth & the future",
                                   help="Small text above title")
            
            description = st.text_area("Description*", 
                                     placeholder="e.g., Start trading commission-free stocks with professional research tools...",
                                     help="Main description text",
                                     height=100)
            
            cta_text = st.text_input("CTA Button Text", 
                                    value="View Campaign",
                                    help="Text on the main button")
        
        # Campaign content and settings
        col3, col4 = st.columns(2)
        
        with col3:
            logo_url = st.text_input("Logo URL (Optional)", 
                                    placeholder="https://example.com/logo.png",
                                    help="URL to campaign logo image")
            
            image_url = st.text_input("Campaign Image URL*", 
                                     placeholder="https://example.com/campaign-image.jpg",
                                     help="URL to main campaign image (replaces 🔗 icon)")
            
            width = st.number_input("Iframe Width (px)", 
                                  min_value=100, 
                                  max_value=1200, 
                                  value=600,
                                  help="Iframe width in pixels")
            
            active = st.checkbox("Active", value=True, help="Start campaign immediately")
        
        with col4:
            uploaded_logo = st.file_uploader("Upload Logo", 
                                            type=['png', 'jpg', 'jpeg', 'svg'],
                                            help="Upload campaign logo")
            
            uploaded_image = st.file_uploader("Upload Campaign Image", 
                                            type=['png', 'jpg', 'jpeg'],
                                            help="Upload main campaign image")
            
            height = st.number_input("Iframe Height (px)", 
                                   min_value=100, 
                                   max_value=800, 
                                   value=400,
                                   help="Iframe height in pixels")
            
            priority = st.slider("Priority", 1, 10, 5, 
                                help="Higher priority campaigns show first in rotation")
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            custom_params = st.text_area("Custom URL Parameters", 
                                       placeholder="e.g., &source=popup&placement=main",
                                       help="Additional parameters to append to iframe URL")
            
            notes = st.text_area("Notes", 
                                placeholder="Internal notes about this campaign...",
                                help="Internal documentation")
        
        # Preview section
        st.subheader("👀 Preview")
        if name and display_title and campaign_id and aff_id and description:
            preview_url = tune_manager.get_iframe_url(campaign_id, aff_id)
            if custom_params:
                preview_url += custom_params
            
            # Show popup preview
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Popup Preview:**")
                st.markdown(f"**Title:** {display_title}")
                st.markdown(f"**Tagline:** {tagline or f'Campaign ID: {campaign_id}'}")
                st.markdown(f"**Description:** {description}")
                st.markdown(f"**CTA:** {cta_text}")
                if logo_url:
                    st.markdown(f"**Logo:** {logo_url}")
                if image_url:
                    st.markdown(f"**📸 Campaign Image:** {image_url}")
                    try:
                        st.image(image_url, width=200, caption="Campaign Image Preview")
                    except:
                        st.warning("Could not load image preview")
            
            with col2:
                st.markdown("**Generated iframe URL:**")
                st.code(preview_url, language="url")
                
                st.markdown("**Complete iframe code:**")
                st.code(f"""<iframe src="{preview_url}" scrolling="no" frameborder="0" marginheight="0" marginwidth="0" width="{width}" height="{height}"></iframe>""", 
                       language="html")
        
        submitted = st.form_submit_button("🚀 Add Campaign", type="primary")
        
        if submitted:
            if name and display_title and campaign_id and aff_id and description:
                # Check for duplicate campaign ID
                existing_ids = [c['id'] for c in tune_manager.campaigns]
                if campaign_id in existing_ids:
                    st.error(f"❌ Campaign ID {campaign_id} already exists! Please use a different ID.")
                else:
                    # Handle file uploads
                    final_logo_url = logo_url
                    final_image_url = image_url
                    
                    if uploaded_logo is not None:
                        # In a real implementation, you'd upload to a CDN
                        final_logo_url = f"uploaded_{uploaded_logo.name}"
                        st.info(f"📁 Logo uploaded: {uploaded_logo.name} (Note: In production, this would be uploaded to CDN)")
                    
                    if uploaded_image is not None:
                        # In a real implementation, you'd upload to a CDN
                        final_image_url = f"uploaded_{uploaded_image.name}"
                        st.info(f"📸 Campaign image uploaded: {uploaded_image.name} (Note: In production, this would be uploaded to CDN)")
                    
                    new_campaign = {
                        "id": campaign_id,
                        "aff_id": aff_id,
                        "name": name,
                        "display_title": display_title,
                        "tagline": tagline,
                        "description": description,
                        "cta_text": cta_text,
                        "logo_url": final_logo_url,
                        "image_url": final_image_url,
                        "width": width,
                        "height": height,
                        "active": active,
                        "priority": priority,
                        "custom_params": custom_params,
                        "notes": notes,
                        "created": datetime.now().isoformat(),
                        "impressions": 0,
                        "clicks": 0
                    }
                    
                    tune_manager.add_campaign(new_campaign)
                    st.success(f"✅ Campaign '{name}' added successfully!")
                    st.balloons()
                    
                    # Show success details
                    with st.expander("📋 Campaign Added", expanded=True):
                        st.json(new_campaign)
            else:
                st.error("❌ Please fill in all required fields (*)")

elif page == "🔧 Campaign Editor":
    st.header("🔧 Campaign Editor")
    
    if 'edit_campaign_id' in st.session_state:
        edit_id = st.session_state.edit_campaign_id
        campaign_to_edit = next((c for c in tune_manager.campaigns if c['id'] == edit_id), None)
        
        if campaign_to_edit:
            st.info(f"Editing: **{campaign_to_edit['name']}** (ID: {edit_id})")
            
            # Edit form
            with st.form("edit_campaign"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Campaign Name", value=campaign_to_edit['name'])
                    aff_id = st.number_input("Affiliate ID", value=campaign_to_edit['aff_id'], min_value=1)
                    width = st.number_input("Width (px)", value=campaign_to_edit['width'], min_value=100)
                
                with col2:
                    active = st.checkbox("Active", value=campaign_to_edit.get('active', True))
                    height = st.number_input("Height (px)", value=campaign_to_edit['height'], min_value=100)
                    priority = st.slider("Priority", 1, 10, campaign_to_edit.get('priority', 5))
                
                custom_params = st.text_area("Custom URL Parameters", 
                                           value=campaign_to_edit.get('custom_params', ''))
                notes = st.text_area("Notes", value=campaign_to_edit.get('notes', ''))
                
                col1, col2 = st.columns(2)
                with col1:
                    save_changes = st.form_submit_button("💾 Save Changes", type="primary")
                with col2:
                    cancel_edit = st.form_submit_button("❌ Cancel")
                
                if save_changes:
                    # Update campaign
                    for i, campaign in enumerate(tune_manager.campaigns):
                        if campaign['id'] == edit_id:
                            tune_manager.campaigns[i].update({
                                'name': name,
                                'aff_id': aff_id,
                                'width': width,
                                'height': height,
                                'active': active,
                                'priority': priority,
                                'custom_params': custom_params,
                                'notes': notes,
                                'modified': datetime.now().isoformat()
                            })
                            break
                    
                    st.session_state.tune_campaigns = tune_manager.campaigns
                    st.success("✅ Campaign updated successfully!")
                    del st.session_state.edit_campaign_id
                    st.rerun()
                
                if cancel_edit:
                    del st.session_state.edit_campaign_id
                    st.rerun()
        else:
            st.error("Campaign not found!")
    else:
        st.info("Select a campaign to edit from the Campaign Dashboard")

elif page == "📊 Analytics":
    st.header("📊 Campaign Analytics")
    tune_manager.render_analytics()
    
    # Additional analytics
    impressions = st.session_state.get('tune_impressions', [])
    if impressions:
        st.subheader("📈 Performance Trends")
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(impressions)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Daily impressions
        daily_impressions = df.groupby('date').size().reset_index()
        daily_impressions.columns = ['Date', 'Impressions']
        
        st.line_chart(daily_impressions.set_index('Date'))
        
        # Campaign performance
        st.subheader("🎯 Campaign Performance")
        campaign_performance = df['campaign_id'].value_counts().reset_index()
        campaign_performance.columns = ['Campaign ID', 'Impressions']
        
        # Add campaign names
        campaign_names = {c['id']: c['name'] for c in tune_manager.campaigns}
        campaign_performance['Campaign Name'] = campaign_performance['Campaign ID'].map(campaign_names)
        
        st.dataframe(campaign_performance)

elif page == "🔗 Tune Demo":
    st.header("🔗 Tune Demo Interface")
    
    demo_type = st.selectbox("Choose demo type:", [
        "🔄 Cycling Popup with Tune Campaigns (Yesterday's Layout!)",
        "🔗 Basic Tune Iframe (Raw iframe display)",
        "📱 Mobile Preview",
        "🧪 A/B Test Preview"
    ], index=0)
    
    if demo_type == "🔄 Cycling Popup with Tune Campaigns (Yesterday's Layout!)":
        tune_manager.render_cycling_popup_with_tune()
        
    elif demo_type == "🔗 Basic Tune Iframe (Raw iframe display)":
        tune_manager.render_tune_popup_demo()
    
    elif demo_type == "📱 Mobile Preview":
        st.info("📱 Mobile-optimized popup preview")
        st.markdown("*Coming soon: Mobile-responsive popup testing*")
    
    elif demo_type == "🧪 A/B Test Preview":
        st.info("🧪 A/B testing interface")
        st.markdown("*Coming soon: A/B test different popup variations*")

elif page == "⚙️ Settings":
    st.header("⚙️ System Settings")
    
    st.subheader("🔧 Global Configuration")
    
    with st.form("settings"):
        default_width = st.number_input("Default iframe width", value=600, min_value=100)
        default_height = st.number_input("Default iframe height", value=400, min_value=100)
        default_aff_id = st.number_input("Default affiliate ID", value=43045, min_value=1)
        
        tracking_enabled = st.checkbox("Enable impression tracking", value=True)
        auto_rotate = st.checkbox("Auto-rotate campaigns", value=False)
        rotation_interval = st.number_input("Rotation interval (seconds)", value=10, min_value=5)
        
        save_settings = st.form_submit_button("💾 Save Settings", type="primary")
        
        if save_settings:
            settings = {
                'default_width': default_width,
                'default_height': default_height,
                'default_aff_id': default_aff_id,
                'tracking_enabled': tracking_enabled,
                'auto_rotate': auto_rotate,
                'rotation_interval': rotation_interval
            }
            st.session_state.tune_settings = settings
            st.success("✅ Settings saved!")
    
    # Export/Import
    st.subheader("📤 Export/Import")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Campaigns"):
            campaigns_json = json.dumps(tune_manager.campaigns, indent=2)
            st.download_button(
                "⬇️ Download campaigns.json",
                campaigns_json,
                "tune_campaigns.json",
                "application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📤 Import Campaigns", type="json")
        if uploaded_file is not None:
            try:
                imported_campaigns = json.load(uploaded_file)
                if st.button("✅ Confirm Import"):
                    st.session_state.tune_campaigns = imported_campaigns
                    st.success("✅ Campaigns imported successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error importing file: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔗 <strong>Tune Campaign Management System</strong> - Built for Mike's Tune CPL Revenue</p>
    <p>🎯 Manually add Tune links/impression pixels • 📊 Track performance • 🚀 Maximize revenue</p>
</div>
""", unsafe_allow_html=True) 