# ui/sidebar.py
import streamlit as st
import re
from utils.formatters import clean_agent_response
from config.constants import EXAMPLE_TOPICS

def render_sidebar():
    """Render the entire sidebar UI."""
    with st.sidebar:
        st.markdown("### ⚙️ **API Configuration**")
        
        # API Keys - create once with unique keys
        google_api_key = st.text_input(
            "**Google Gemini API Key:**",
            type="password",
            help="Get from: https://aistudio.google.com/app/apikeys",
            key="sidebar_google_key"  # Unique key
        )
        
        groq_api_key = st.text_input(
            "**Groq API Key:**",
            type="password",
            help="Get from: https://console.groq.com/keys",
            key="sidebar_groq_key"  # Unique key
        )
        
        # Store keys in session state
        if google_api_key:
            st.session_state.google_api_key_input = google_api_key
        if groq_api_key:
            st.session_state.groq_api_key_input = groq_api_key
        
        # Initialize button - just sets a flag for main.py to handle
        if st.button("🚀 **Initialize All Agents**", type="primary", use_container_width=True):
            # Set a flag that main.py will check
            st.session_state.initialize_clicked = True
        
        st.markdown("---")
        
        # Research Output Section
        with st.expander("🔍 **View Research Findings**", expanded=False):
            if st.session_state.current_outputs['research']:
                clean_research = clean_agent_response(st.session_state.current_outputs['research'])
                # Remove the context.state assignment line for display
                clean_research = re.sub(r'context\.state\[.*?\].*', '', clean_research)
                st.text_area("Research Summary", clean_research[:2000] + "..." if len(clean_research) > 2000 else clean_research, height=250)
            else:
                st.info("No research generated yet. Run a topic first.")
        
        st.markdown("---")
        st.markdown("### 💡 **Example Topics**")
        
        for example in EXAMPLE_TOPICS:
            if st.button(example, use_container_width=True, key=f"example_{example}"):
                # Extract topic without emoji
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
        
        # Clear button
        if st.button("🗑️ **Clear All**", use_container_width=True, key="clear_button"):
            st.session_state.pipeline_history = []
            st.session_state.current_outputs = {'research': '', 'linkedin': '', 'facebook': '', 'whatsapp': ''}
            st.rerun()
