from openai import OpenAI
import anthropic
import os
import dotenv
from agents.image_provider import ImageProvider
from agents.language_provider import LanguageProvider

dotenv.load_dotenv()

providers = {
    "OPENAI": LanguageProvider(
        base_url="https://api.openai.com/v1",
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    ),
    "ANTHROPIC": LanguageProvider(
        base_url="https://api.anthropic.com/v1",
        model="claude-3-5-sonnet-20240620",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    ),
    "XAI": LanguageProvider(
        base_url="https://api.x.ai/v1",
        model="grok-beta",
        api_key=os.getenv("XAI_API_KEY"),
        client=OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
    ),
    "GROQ8": LanguageProvider(
        base_url="https://api.groq.com/openai/v1",
        model="llama3-groq-8b-8192-tool-use-preview",
        api_key=os.getenv("GROQ_API_KEY"),
        client=OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    ),
    "GROQ70": LanguageProvider(
        base_url="https://api.groq.com/openai/v1",
        model="llama3-groq-70b-8192-tool-use-preview",
        api_key=os.getenv("GROQ_API_KEY"),
        client=OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    ),
    "IMAGE": ImageProvider(
        base_url="https://api.openai.com/v1",
        model="dall-e-3",
        api_key=os.getenv("OPENAI_API_KEY"),
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
    )
}