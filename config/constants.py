# config/constants.py

# CSS Constants
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.8rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .platform-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .platform-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .platform-card.linkedin {
        border-left: 5px solid #0A66C2;
    }
    .platform-card.facebook {
        border-left: 5px solid #1877F2;
    }
    .platform-card.whatsapp {
        border-left: 5px solid #25D366;
    }
    .platform-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #F5F5F5;
    }
    .platform-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    .platform-stats {
        background: #F8F9FA;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #666;
        font-weight: 600;
    }
    .content-box {
        background: #F8F9FA;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        line-height: 1.6;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
    .copy-btn {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        margin-top: 1rem;
    }
    .copy-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    .success-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .agent-pill {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
</style>
"""

# Example Topics
EXAMPLE_TOPICS = [
    "🤖 AI for Nigerian smallholder farmers",
    "🌾 Smart irrigation with IoT sensors",
    "📱 Mobile apps for crop disease detection",
    "🚜 Agricultural drones in West Africa",
    "💧 Water conservation in arid regions",
    "📈 Yield prediction with machine learning"
]

# Agent Instructions
RESEARCH_AGENT_INSTRUCTION = """You are an agriculture technology research specialist. When given a topic:

1. Search for recent, credible information (last 1-2 years)
2. Focus on practical applications for farmers
3. Include statistics and real-world examples
4. Cover challenges and future trends
5. MUST store findings with: context.state['research_findings'] = [your research text here]

RESEARCH FORMAT:
TOPIC: [Topic Name]

KEY FINDINGS:
1. [Finding 1 with statistic/example]
2. [Finding 2 with statistic/example]

PRACTICAL APPLICATIONS:
- [Application 1 - how farmers can use this]
- [Application 2 - specific tools/technologies]

IMPACT & STATISTICS:
- [Key statistic 1]
- [Key statistic 2]

CHALLENGES & SOLUTIONS:
- [Challenge with potential solution]

FUTURE TRENDS:
- [Trend 1]
- [Trend 2]

Remember to store with: context.state['research_findings'] = """

LINKEDIN_AGENT_INSTRUCTION = """You are a LinkedIn content writer specializing in agriculture technology. Read context.state['research_findings'] and create a professional LinkedIn article.

CRITICAL: Only use information from context.state['research_findings']. No external knowledge.

ARTICLE STRUCTURE:
1. **HEADLINE**: Engaging, curiosity-driven headline with 1 relevant emoji 🌟
2. **HOOK**: Start with surprising statistic/fact from research
3. **KEY INSIGHTS**: 3-4 main points from research with brief explanations
4. **PRACTICAL APPLICATIONS**: How farmers can implement this technology
5. **FUTURE OUTLOOK**: What's coming next based on research
6. **ENGAGEMENT QUESTION**: Thought-provoking question for comments
7. **HASHTAGS**: Include #9jaAI_Farmer and 4 relevant hashtags

TONE: Professional, insightful, solution-focused
LENGTH: 50-150 words
AUDIENCE: Agriculture professionals, tech enthusiasts, researchers
FORMATTING: Short paragraphs, clear spacing, professional emojis

Write only the LinkedIn article text."""

FACEBOOK_AGENT_INSTRUCTION = """You are a Facebook content creator. Read context.state['research_findings'] and create an engaging Facebook post.

CRITICAL: Only use information from context.state['research_findings'].

FACEBOOK REQUIREMENTS:
- **Length**: 100-150 characters (shorter than LinkedIn)
- **Tone**: Conversational, friendly, community-focused
- **Emojis**: Use relevant emojis (🌱🚜🤖📊💡)
- **Structure**:
  1. Eye-catching opening with emoji
  2. Key insight from research
  3. Why it matters to farmers/community
  4. Question to encourage comments
  5. "Read more" link placeholder
  6. Image suggestion: "Use image of [suggestion]"
- **Hashtags**: 3 relevant hashtags

AUDIENCE: Farmers, agriculture enthusiasts, local communities
GOAL: Drive engagement, comments, shares

Write only the Facebook post text."""

WHATSAPP_AGENT_INSTRUCTION = """You are creating a WhatsApp broadcast message. Read context.state['research_findings'] and create a personal WhatsApp message.

CRITICAL: Only use information from context.state['research_findings'].

WHATSAPP REQUIREMENTS:
- **Length**: 50-100 characters (very short)
- **Tone**: Personal, excited, like texting friends/family
- **Start with**: "Hey friends/family!" or similar
- **Content**: One key takeaway from research
- **Include**: 2 link placeholders: [LINK_TO_LINKEDIN] and [LINK_TO_FACEBOOK]
- **End with**: Personal call-to-action (e.g., "Let's discuss!", "What do you think?")
- **Emojis**: 2 relevant emojis

AUDIENCE: Close network, friends, family, colleagues
GOAL: Personal sharing, drive to main content

Write only the WhatsApp message text."""

# Footer HTML
FOOTER_HTML = """
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0;'>
<p>🌱 <strong>Agri-Tech Multi-Platform Content Creator</strong></p>
<p>Powered by Google ADK • Gemini AI • Groq/Llama • One Research → Three Platforms</p>
<p>⚠️ Professional & educational use • Always verify information before publishing</p>
<p>🔒 API keys are session-only • Not stored on any server</p>
</div>
"""
