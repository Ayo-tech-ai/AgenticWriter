# utils/formatters.py
import re

def clean_agent_response(raw_response):
    """Clean the raw agent response to remove parts=[Part( wrapper."""
    if not raw_response:
        return ""
    
    response_str = str(raw_response)
    
    # Remove parts=[Part( wrapper and extract text
    if 'parts=[Part(' in response_str:
        try:
            # Extract text between triple quotes
            text_matches = re.findall(r'text="""(.*?)"""', response_str, re.DOTALL)
            if text_matches:
                cleaned_text = text_matches[0].strip()
                # Also remove any remaining wrapper text
                cleaned_text = re.sub(r'^parts=\[Part\(.*?text="""', '', cleaned_text, flags=re.DOTALL)
                cleaned_text = re.sub(r'"""\)\] role=\'model\'$', '', cleaned_text)
                return cleaned_text.strip()
        except:
            pass
    
    # If already clean text
    return response_str.strip()

def format_platform_content(text, platform):
    """Format content for specific platform display."""
    if not text:
        return ""
    
    # Basic cleaning
    text = clean_agent_response(text)
    
    # Platform-specific formatting
    if platform == "linkedin":
        # Ensure hashtags are visible
        text = re.sub(r'(#\w+)', r'**\1**', text)
    elif platform == "facebook":
        # Highlight emojis and links
        text = text.replace('[link]', '[🔗 LINK TO ARTICLE]')
    elif platform == "whatsapp":
        # Format links clearly
        text = text.replace('[LINK_TO_LINKEDIN]', '[🌐 LinkedIn Article]')
        text = text.replace('[LINK_TO_FACEBOOK]', '[👍 Facebook Post]')
    
    return text
