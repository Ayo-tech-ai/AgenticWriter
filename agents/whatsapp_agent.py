# agents/whatsapp_agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from config.constants import WHATSAPP_AGENT_INSTRUCTION

def create_whatsapp_agent():
    """Create and return the WhatsApp agent."""
    whatsapp_agent = Agent(
        name="whatsapp_agent",
        model=LiteLlm(model="groq/llama-3.3-70b-versatile"),
        description="Personal WhatsApp writer for close networks",
        instruction=WHATSAPP_AGENT_INSTRUCTION,
    )
    return whatsapp_agent
