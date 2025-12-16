# main.py - UPDATED FLOW
import streamlit as st
import os
import asyncio
import nest_asyncio

# Apply nest_asyncio for async support
nest_asyncio.apply()

# Import from modules
from utils.session_manager import initialize_session_state
from ui.sidebar import render_sidebar
from ui.main_content import render_main_content, render_research_findings, render_platform_outputs, render_history, render_footer
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

# ==========================================
# AUTO-INITIALIZE AGENTS FROM SECRETS (PRIORITY)
# ==========================================
if not st.session_state.get('agents_initialized', False):
    try:
        # Try to get API keys from Streamlit Secrets
        google_api_key = st.secrets.get("GOOGLE_GEMINI_API_KEY", "")
        groq_api_key = st.secrets.get("GROQ_API_KEY", "")
        
        if google_api_key and groq_api_key:
            # Set API keys in environment
            os.environ["GOOGLE_API_KEY"] = google_api_key
            os.environ["GROQ_API_KEY"] = groq_api_key
            
            # Create pipeline
            pipeline_agent = create_multi_platform_pipeline()
            
            # Create runner
            runner = InMemoryRunner(agent=pipeline_agent)
            
            # Store in session state
            st.session_state.runner = runner
            st.session_state.agents_initialized = True
            st.session_state.secrets_initialized = True
            
        else:
            st.session_state.secrets_initialized = False
            
    except Exception as e:
        st.session_state.secrets_initialized = False

# ==========================================
# RENDER SIDEBAR (with conditional API inputs)
# ==========================================
render_sidebar()

# ==========================================
# MANUAL INITIALIZATION HANDLING
# ==========================================
if st.session_state.get('initialize_clicked', False):
    # Get API keys from session state (manual input)
    google_api_key = st.session_state.get('google_api_key_input', '')
    groq_api_key = st.session_state.get('groq_api_key_input', '')
    
    if google_api_key and groq_api_key:
        with st.sidebar:
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
                    st.session_state.secrets_initialized = True
                    
                    st.markdown('<div class="success-box">✅ <strong>4 Agents Initialized!</strong><br>Research + 3 Platform Writers ready</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Setup failed: {str(e)}")
    else:
        with st.sidebar:
            st.warning("Please enter both API keys")
    
    # Clear the flag
    st.session_state.initialize_clicked = False

# ==========================================
# MAIN CONTENT GENERATION FLOW
# ==========================================
# Render topic input and platform selection
research_topic, linkedin_enabled, facebook_enabled, whatsapp_enabled = render_main_content()

# Generate button (positioned below platform selection)
if st.button("🚀 **Generate All Platform Content**", type="primary", use_container_width=True, key="generate_button"):
    if not st.session_state.get('agents_initialized', False):
        st.warning("Please initialize the pipeline first (sidebar)")
    elif not research_topic.strip():
        st.warning("Please enter a research topic")
    else:
        with st.spinner("🔍 Researching topic and creating platform content..."):
            try:
                # Clear ALL outputs BEFORE running pipeline
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
                from utils.formatters import clean_agent_response
                
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
                            research_output = clean_agent_response(content)
                            st.session_state.current_outputs['research'] = research_output
                        
                        # LinkedIn agent
                        elif 'linkedin_agent' in event_str or '#9jaai_farmer' in content.lower():
                            linkedin_output = clean_agent_response(content)
                            st.session_state.current_outputs['linkedin'] = linkedin_output
                        
                        # Facebook agent
                        elif 'facebook_agent' in event_str or 'read more' in content.lower():
                            facebook_output = clean_agent_response(content)
                            st.session_state.current_outputs['facebook'] = facebook_output
                        
                        # WhatsApp agent
                        elif 'whatsapp_agent' in event_str or '[link_' in content.lower():
                            whatsapp_output = clean_agent_response(content)
                            st.session_state.current_outputs['whatsapp'] = whatsapp_output
                
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

# ==========================================
# DISPLAY OUTPUTS IN NEW ORDER
# ==========================================
# 1. Research Findings (FIRST on main page)
render_research_findings()

# 2. Platform Outputs (in new order: LinkedIn → Facebook → WhatsApp)
render_platform_outputs(linkedin_enabled, facebook_enabled, whatsapp_enabled)

# 3. History
#render_history()

# 4. Footer
render_footer()
