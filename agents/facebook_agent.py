# agents/facebook_agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from config.constants import FACEBOOK_AGENT_INSTRUCTION

def create_facebook_agent():
    """Create and return the Facebook agent."""
    facebook_agent = Agent(
        name="facebook_agent",
        model=LiteLlm(model="groq/llama-3.3-70b-versatile"),
        description="Engaging Facebook writer for community discussion",
        instruction=FACEBOOK_AGENT_INSTRUCTION,
    )
    return facebook_agent
