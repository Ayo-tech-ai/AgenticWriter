# pipeline/pipeline_creator.py
from google.adk.agents import SequentialAgent
from agents.research_agent import create_research_agent
from agents.linkedin_agent import create_linkedin_agent
from agents.facebook_agent import create_facebook_agent
from agents.whatsapp_agent import create_whatsapp_agent

def create_multi_platform_pipeline():
    """Create and return the complete multi-platform pipeline."""
    # Create individual agents
    research_agent = create_research_agent()
    linkedin_agent = create_linkedin_agent()
    facebook_agent = create_facebook_agent()
    whatsapp_agent = create_whatsapp_agent()
    
    # Create sequential pipeline
    pipeline_agent = SequentialAgent(
        name="multi_platform_pipeline",
        sub_agents=[research_agent, linkedin_agent, facebook_agent, whatsapp_agent],
        description="Research → LinkedIn → Facebook → WhatsApp pipeline"
    )
    
    return pipeline_agent
