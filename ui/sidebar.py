# ui/sidebar.py - SIMPLIFIED (no research display)
import streamlit as st
from config.constants import EXAMPLE_TOPICS

def render_sidebar():
    """Render the entire sidebar UI."""
    with st.sidebar:
        # Only show manual API inputs if secrets weren't loaded
        if not st.session_state.get('secrets_initialized', True):
            st.markdown("### ⚙️ **Manual API Configuration**")
            st.caption("(Secrets not loaded - using manual input)")
            
            # API Keys - create once with unique keys
            google_api_key = st.text_input(
                "**Google Gemini API Key:**",
                type="password",
                help="Get from: https://aistudio.google.com/app/apikeys",
                key="sidebar_google_key"
            )
            
            groq_api_key = st.text_input(
                "**Groq API Key:**",
                type="password",
                help="Get from: https://console.groq.com/keys",
                key="sidebar_groq_key"
            )
            
            # Store keys in session state
            if google_api_key:
                st.session_state.google_api_key_input = google_api_key
            if groq_api_key:
                st.session_state.groq_api_key_input = groq_api_key
            
            # Initialize button - only show if manual input needed
            if st.button("🚀 **Initialize All Agents**", type="primary", use_container_width=True):
                # Set a flag that main.py will check
                st.session_state.initialize_clicked = True
            
            st.markdown("---")
        else:
            # Show status when using secrets
            st.markdown("### ⚙️ **API Status**")
            st.markdown('<div class="success-box">✅ <strong>Using API Keys from Secrets</strong><br>Agents ready</div>', unsafe_allow_html=True)
            st.markdown("---")
        
        st.markdown("### 💡 **Example Topics**")
        
        for example in EXAMPLE_TOPICS:
            if st.button(example, use_container_width=True, key=f"example_{example}"):
                topic = example.split(" ", 1)[1] if " " in example else example
                st.session_state.example_topic = topic
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 **Quick Stats**")
        if st.session_state.get('agents_initialized', False):
            st.markdown(f"""
            <div style="background: #F8F9FA; padding: 1rem; border-radius: 10px;">
            <span class="agent-pill">Research Agent</span>
            <span class="agent-pill">LinkedIn Agent</span>
            <span class="agent-pill">Facebook Agent</span>
            <span class="agent-pill">WhatsApp Agent</span>
            <br><br>
            <strong>Runs Completed:</strong> {len(st.session_state.pipeline_history)}
            </div>
            """, unsafe_allow_html=True)
        
        # Clear All button (clears everything including history)
        if st.button("🗑️ **Clear All (Full Reset)**", use_container_width=True, key="clear_all_button"):
            st.session_state.pipeline_history = []
            st.session_state.current_outputs = {'research': '', 'linkedin': '', 'facebook': '', 'whatsapp': ''}
            st.rerun()
