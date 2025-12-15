# ui/main_content.py - RESTRUCTURED
import streamlit as st
from utils.formatters import format_platform_content, clean_agent_response
from config.constants import FOOTER_HTML

def render_main_content():
    """Render the main content area."""
    # Title
    st.markdown('<h1 class="main-header">🌱 Agri-Tech Multi-Platform Content Creator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.1rem;">Generate platform-optimized content from AI research • One research → Three platforms</p>', unsafe_allow_html=True)
    
    # Main Content Area
    st.header("📝 **Generate Multi-Platform Content**")
    
    # Get topic input
    if 'example_topic' in st.session_state:
        default_topic = st.session_state.example_topic
        del st.session_state.example_topic
    else:
        default_topic = ""
    
    research_topic = st.text_input(
        "**Enter agriculture technology topic:**",
        value=default_topic,
        placeholder="e.g., 'AI for soil health monitoring' or 'IoT in Nigerian agriculture'",
        help="Focus on agriculture technology topics for best results",
        key="main_research_input"
    )
    
    # Platform selection
    st.markdown("### 🌐 **Platform Selection**")
    col1, col2, col3 = st.columns(3)
    with col1:
        linkedin_enabled = st.checkbox("LinkedIn Article", value=True, key="linkedin_check")
    with col2:
        facebook_enabled = st.checkbox("Facebook Post", value=True, key="facebook_check")
    with col3:
        whatsapp_enabled = st.checkbox("WhatsApp Message", value=True, key="whatsapp_check")
    
    return research_topic, linkedin_enabled, facebook_enabled, whatsapp_enabled

def render_research_findings():
    """Display research findings on main page."""
    if st.session_state.current_outputs['research']:
        st.markdown("---")
        st.header("🔍 **Research Findings**")
        
        clean_research = clean_agent_response(st.session_state.current_outputs['research'])
        
        # Display full research content (no truncation)
        st.markdown(f'<div class="content-box">{clean_research}</div>', unsafe_allow_html=True)
        
        # Clear Research Button (clears current research + outputs only)
        if st.button("🗑️ Clear Current Research & Outputs", key="clear_current_research", use_container_width=True):
            st.session_state.current_outputs = {'research': '', 'linkedin': '', 'facebook': '', 'whatsapp': ''}
            st.rerun()

def render_platform_outputs(linkedin_enabled=True, facebook_enabled=True, whatsapp_enabled=True):
    """Display the platform content outputs in new order."""
    # Check if any platform content exists
    platform_outputs_exist = (
        (st.session_state.current_outputs['linkedin'] and linkedin_enabled) or
        (st.session_state.current_outputs['facebook'] and facebook_enabled) or
        (st.session_state.current_outputs['whatsapp'] and whatsapp_enabled)
    )
    
    if platform_outputs_exist:
        st.markdown("---")
        st.header("📱 **Platform Content Ready**")
        
        # 1. LinkedIn Article (First)
        if st.session_state.current_outputs['linkedin'] and linkedin_enabled:
            linkedin_content = format_platform_content(st.session_state.current_outputs['linkedin'], "linkedin")
            if linkedin_content:
                st.markdown(f"""
                <div class="platform-card linkedin">
                    <div class="platform-header">
                        <h3 class="platform-title">🌐 LinkedIn Article</h3>
                        <span class="platform-stats">{{:,}} chars</span>
                    </div>
                </div>
                """.format(len(linkedin_content)), unsafe_allow_html=True)
                
                st.markdown(f'<div class="content-box">{linkedin_content}</div>', unsafe_allow_html=True)
                
                # Copy button
                if st.button("📋 Copy LinkedIn Article", key="copy_linkedin", use_container_width=True):
                    st.code(linkedin_content, language="markdown")
                    st.success("✅ LinkedIn article copied! Paste into LinkedIn")
        
        # 2. Facebook Post (Second)
        if st.session_state.current_outputs['facebook'] and facebook_enabled:
            facebook_content = format_platform_content(st.session_state.current_outputs['facebook'], "facebook")
            if facebook_content:
                st.markdown(f"""
                <div class="platform-card facebook">
                    <div class="platform-header">
                        <h3 class="platform-title">👍 Facebook Post</h3>
                        <span class="platform-stats">{{:,}} chars</span>
                    </div>
                </div>
                """.format(len(facebook_content)), unsafe_allow_html=True)
                
                st.markdown(f'<div class="content-box">{facebook_content}</div>', unsafe_allow_html=True)
                
                if st.button("📋 Copy Facebook Post", key="copy_facebook", use_container_width=True):
                    st.code(facebook_content, language="markdown")
                    st.success("✅ Facebook post copied! Paste into Facebook")
        
        # 3. WhatsApp Message (Third)
        if st.session_state.current_outputs['whatsapp'] and whatsapp_enabled:
            whatsapp_content = format_platform_content(st.session_state.current_outputs['whatsapp'], "whatsapp")
            if whatsapp_content:
                st.markdown(f"""
                <div class="platform-card whatsapp">
                    <div class="platform-header">
                        <h3 class="platform-title">💬 WhatsApp Message</h3>
                        <span class="platform-stats">{{:,}} chars</span>
                    </div>
                </div>
                """.format(len(whatsapp_content)), unsafe_allow_html=True)
                
                st.markdown(f'<div class="content-box">{whatsapp_content}</div>', unsafe_allow_html=True)
                
                if st.button("📋 Copy WhatsApp Message", key="copy_whatsapp", use_container_width=True):
                    st.code(whatsapp_content, language="markdown")
                    st.success("✅ WhatsApp message copied! Paste into WhatsApp")

def render_history():
    """Display the content history."""
    if st.session_state.pipeline_history:
        st.markdown("---")
        st.header("📚 **Content History**")
        
        for i, entry in enumerate(reversed(st.session_state.pipeline_history)):
            with st.expander(f"📄 {entry['topic'][:40]}... ({entry['timestamp']})", key=f"history_{i}"):
                hist_col1, hist_col2, hist_col3 = st.columns(3)
                
                with hist_col1:
                    if entry['outputs'].get('linkedin'):
                        st.markdown("**LinkedIn:**")
                        preview = clean_agent_response(entry['outputs']['linkedin'])[:200] + "..."
                        st.text(preview)
                
                with hist_col2:
                    if entry['outputs'].get('facebook'):
                        st.markdown("**Facebook:**")
                        preview = clean_agent_response(entry['outputs']['facebook'])[:150] + "..."
                        st.text(preview)
                
                with hist_col3:
                    if entry['outputs'].get('whatsapp'):
                        st.markdown("**WhatsApp:**")
                        preview = clean_agent_response(entry['outputs']['whatsapp'])[:100] + "..."
                        st.text(preview)

def render_footer():
    """Render the footer."""
    st.markdown("---")
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)
