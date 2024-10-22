from openai import OpenAI
import os
import dotenv
import anthropic

dotenv.load_dotenv()

class ChatAPIProvider():
    def __init__(self, url: str, model: str, api_key: str, client: OpenAI | anthropic.Anthropic):
        self.url = url
        self.model = model
        self.api_key = api_key
        self.client = client
        self.chat_complete = client.chat.completions.create if isinstance(client, OpenAI) else client.messages.create

    def chat(self, user_input: str, system_prompt: str, max_tokens: int = 1000, messages: list = None, tools: list = None):
        response = None
        if isinstance(self.client, OpenAI):        
            response = self.chat_complete(
                model=self.model,
                tools=tools,
                messages=messages if messages is not None else [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        else:
            response = self.chat_complete(
                model=self.model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=max_tokens
            )
            return response.content[0].text
        
providers = {
    "OPENAI": ChatAPIProvider(
        base_url="https://api.openai.com/v1",
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    ),
    "ANTHROPIC": ChatAPIProvider(
        base_url="https://api.anthropic.com/v1",
        model="claude-3-5-sonnet-20240620",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    ),
    "XAI": ChatAPIProvider(
        base_url="https://api.x.ai/v1",
        model="grok-beta",
        api_key=os.getenv("XAI_API_KEY"),
        client=OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1")
    )
}

class Agent:
    def __init__(self, provider: ChatAPIProvider, system_prompt: str = "", max_tokens: int = 1000, tools: list = None):
        self._provider = provider
        self._system_prompt = system_prompt
        self._max_tokens = max_tokens
        self._tools = tools if tools is not None else [
            {
                "type": "function",
                "function": {
                    "name": "do_nothing",
                    "description": "Do nothing",
                    "parameters": {}
                }
            }
        ]

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, new_provider: ChatAPIProvider):
        self._provider = new_provider

    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, prompt: str):
        self._system_prompt = prompt

    @property
    def tools(self):
        return self._tools

    @tools.setter
    def tools(self, tools: list):
        self._tools = tools

    async def chat(self, user_input: str):
        response = self._provider.chat(
            user_input,
            self._system_prompt,
            max_tokens=self._max_tokens
        )
        return response
