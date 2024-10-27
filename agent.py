from openai import OpenAI
import os
import dotenv
import anthropic
import json

dotenv.load_dotenv()

class ChatAPIProvider():
    def __init__(self, base_url: str, model: str, api_key: str, client: OpenAI | anthropic.Anthropic):
        self.url = base_url
        self.model = model
        self.api_key = api_key
        self.client = client
        self.chat_complete = client.chat.completions.create if isinstance(client, OpenAI) else client.messages.create

    def chat(self, user_input: str, system_prompt: str, max_tokens: int = 1000, 
            messages: list = None, tools: list = None, expect_function_call: bool = False, temperature: float = 0.0):
        response = None
        if isinstance(self.client, OpenAI):
            response = self.chat_complete(
                model=self.model,
                tools=tools,
                messages=messages if messages is not None else [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=max_tokens,
                tool_choice="auto" if expect_function_call else "none",
                temperature=temperature
            )
            
            if expect_function_call and response.choices[0].message.tool_calls:
                # Parse the function call response
                tool_call = response.choices[0].message.tool_calls[0]
                return json.loads(tool_call.function.arguments)
            elif expect_function_call:
                return None
            
            return response.choices[0].message.content
            
        else:
            # For Anthropic, you might want to use their equivalent structured output format
            # or implement a similar parsing mechanism
            response = self.chat_complete(
                model=self.model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            if expect_function_call:
                # You might need to implement custom parsing for Anthropic's responses
                # or use their structured output format
                pass
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

    async def chat(self, user_input: str, expect_function_call: bool = False, temperature: float = 0.0):
        response = self._provider.chat(
            user_input,
            self._system_prompt,
            max_tokens=self._max_tokens,
            tools=self._tools,
            expect_function_call=expect_function_call,
            temperature=temperature
        )
        return response
