# agents/research_agent.py
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.google_search_tool import GoogleSearchTool
from config.constants import RESEARCH_AGENT_INSTRUCTION

def create_research_agent():
    """Create and return the research agent."""
    research_agent = Agent(
        name="research_agent",
        model=Gemini(model="gemini-2.5-flash-lite"),
        description="Specialized researcher for agriculture technology",
        instruction=RESEARCH_AGENT_INSTRUCTION,
        tools=[GoogleSearchTool(bypass_multi_tools_limit=True)],
    )
    return research_agent
