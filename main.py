# main.py - Main orchestration file
import streamlit as st
import os
import asyncio
import nest_asyncio

# Apply nest_asyncio for async support
nest_asyncio.apply()

# Import from modules
from utils.session_manager import initialize_session_state, clear_session_state
from utils.formatters import clean_agent_response
from ui.sidebar import render_sidebar, get_api_keys
from ui.main_content import render_main_content, render_platform_outputs, render_history, render_footer
from config.constants import CUSTOM_CSS
from pipeline.pipeline_creator import create_multi_platform_pipeline
from google.adk.runners import InMemoryRunner

# Set page config
st.set_page_config(
    page_title="Agri-Tech Multi-Platform Content Creator",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Render sidebar
render_sidebar()

# Sidebar buttons and logic
with st.sidebar:
    # Initialize button
    if st.button("🚀 **Initialize All Agents**", type="primary", use_container_width=True):
        google_api_key, groq_api_key = get_api_keys()
        
        if google_api_key and groq_api_key:
            with st.spinner("Setting up 4 specialized agents..."):
                try:
                    # Set API keys
                    os.environ["GOOGLE_API_KEY"] = google_api_key
                    os.environ["GROQ_API_KEY"] = groq_api_key
                    
                    # Create pipeline
                    pipeline_agent = create_multi_platform_pipeline()
                    
                    # Create runner
                    runner = InMemoryRunner(agent=pipeline_agent)
                    
                    # Store in session state
                    st.session_state.runner = runner
                    st.session_state.agents_initialized = True
                    
                    st.markdown('<div class="success-box">✅ <strong>4 Agents Initialized!</strong><br>Research + 3 Platform Writers ready</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Setup failed: {str(e)}")
        else:
            st.warning("Please enter both API keys")
    
    # Clear button
    if st.button("🗑️ **Clear All**", use_container_width=True):
        clear_session_state()
        st.rerun()

# Render main content
research_topic, linkedin_enabled, facebook_enabled, whatsapp_enabled = render_main_content()

# Generate button
if st.button("🚀 **Generate All Platform Content**", type="primary", use_container_width=True):
    if not st.session_state.get('agents_initialized', False):
        st.warning("Please initialize the pipeline first (sidebar)")
    elif not research_topic.strip():
        st.warning("Please enter a research topic")
    else:
        with st.spinner("🔍 Researching topic and creating platform content..."):
            try:
                # Clear previous outputs
                st.session_state.current_outputs = {'research': '', 'linkedin': '', 'facebook': '', 'whatsapp': ''}
                
                # Run pipeline
                async def run_pipeline():
                    return await st.session_state.runner.run_debug(research_topic)
                
                # Create new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    events = loop.run_until_complete(run_pipeline())
                finally:
                    loop.close()
                
                # Extract outputs by agent
                research_output = ""
                linkedin_output = ""
                facebook_output = ""
                whatsapp_output = ""
                
                for event in events:
                    if hasattr(event, 'content'):
                        content = str(event.content)
                        event_str = str(event).lower()
                        
                        # Research agent
                        if 'research_agent' in event_str or 'TOPIC:' in content:
                            research_output = content
                            st.session_state.current_outputs['research'] = content
                        
                        # LinkedIn agent
                        elif 'linkedin_agent' in event_str or '#9jaai_farmer' in content.lower():
                            linkedin_output = content
                            st.session_state.current_outputs['linkedin'] = content
                        
                        # Facebook agent
                        elif 'facebook_agent' in event_str or 'read more' in content.lower():
                            facebook_output = content
                            st.session_state.current_outputs['facebook'] = content
                        
                        # WhatsApp agent
                        elif 'whatsapp_agent' in event_str or '[link_' in content.lower():
                            whatsapp_output = content
                            st.session_state.current_outputs['whatsapp'] = content
                
                # Add to history
                st.session_state.pipeline_history.append({
                    "topic": research_topic,
                    "timestamp": "Now",
                    "outputs": {
                        'linkedin': linkedin_output,
                        'facebook': facebook_output,
                        'whatsapp': whatsapp_output
                    }
                })
                
                st.success(f"✅ Generated content for {research_topic}!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display platform outputs
render_platform_outputs(linkedin_enabled, facebook_enabled, whatsapp_enabled)

# Display history
render_history()

# Display footer
render_footer()
