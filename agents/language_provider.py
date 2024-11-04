import json
import anthropic
from openai import OpenAI
from .schema_converter import SchemaConverter

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class LanguageProvider():
    def __init__(self, base_url: str, model: str, api_key: str, client: OpenAI | anthropic.Anthropic):
        self.url = base_url
        self.model = model
        self.api_key = api_key
        self.client = client
        self.chat_complete = client.chat.completions.create if isinstance(client, OpenAI) else client.messages.create

    async def chat(self, user_input: str, system_prompt: str, max_tokens: int = 1000, 
            messages: list = None, tools: list = None, expect_function_call: bool = False, temperature: float = 0.0):
                
        response = None
        if isinstance(self.client, OpenAI):
            response = self.chat_complete(
                model=self.model,
                tools=tools, # openai standard is the default
                messages=messages if messages is not None else [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=max_tokens,
                tool_choice="auto" if expect_function_call else "none",
                temperature=temperature
            )
            
            if expect_function_call and response.choices[0].message.tool_calls:
                return response.choices[0].message.content, FunctionCall(response.choices[0].message.tool_calls[0].function.name, response.choices[0].message.tool_calls[0].function.arguments)
            return response.choices[0].message.content, None
            
        else:
            # For Anthropic, you might want to use their equivalent structured output format
            # or implement a similar parsing mechanism
            response = self.chat_complete(
                model=self.model,
                tools=SchemaConverter.to_anthropic(tools),
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            if expect_function_call and len(response.content) > 1:            
                return response.content[0].text, FunctionCall(response.content[1].name, json.dumps(response.content[1].input))
            return response.content[0].text, None