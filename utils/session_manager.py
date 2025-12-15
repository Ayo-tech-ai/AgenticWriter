# utils/session_manager.py - UPDATED
import streamlit as st

def initialize_session_state():
    """Initialize all session state variables."""
    if 'agents_initialized' not in st.session_state:
        st.session_state.agents_initialized = False
    if 'pipeline_history' not in st.session_state:
        st.session_state.pipeline_history = []
    if 'runner' not in st.session_state:
        st.session_state.runner = None
    if 'current_outputs' not in st.session_state:
        st.session_state.current_outputs = {
            'research': '',
            'linkedin': '',
            'facebook': '',
            'whatsapp': ''
        }
    # Add new session state variables
    if 'secrets_initialized' not in st.session_state:
        st.session_state.secrets_initialized = False
    if 'initialize_clicked' not in st.session_state:
        st.session_state.initialize_clicked = False
    if 'example_topic' not in st.session_state:
        st.session_state.example_topic = ""

def clear_session_state():
    """Clear all session state except initialization."""
    st.session_state.pipeline_history = []
    st.session_state.current_outputs = {'research': '', 'linkedin': '', 'facebook': '', 'whatsapp': ''}
    # Note: We keep agents_initialized and runner so users don't have to re-initialize
