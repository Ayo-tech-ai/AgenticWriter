# agents/linkedin_agent.py
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from config.constants import LINKEDIN_AGENT_INSTRUCTION

def create_linkedin_agent():
    """Create and return the LinkedIn agent."""
    linkedin_agent = Agent(
        name="linkedin_agent",
        model=LiteLlm(model="groq/llama-3.3-70b-versatile"),
        description="Professional LinkedIn writer for agriculture tech",
        instruction=LINKEDIN_AGENT_INSTRUCTION,
    )
    return linkedin_agent
