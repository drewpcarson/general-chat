from agent import Agent, providers
from tool import Tool
from timetracker import TimeTracker
import asyncio
import re

agent = Agent(providers['XAI'], max_tokens=200)
tracker = TimeTracker()

tools = {
    'start_task': Tool(schema={
        "name": "start_task",
        "description": "Start tracking a new task when a user mentions something they're going to do next",
        "parameters": {
            "task_name": {
                "type": "string",
                "description": "The name of the task to start tracking"
            }
        }
    }, function=tracker.start_task),
    
    'stop_timer': Tool(schema={
        "name": "stop_timer",
        "description": "Stop the current timer when the user is done tracking time",
        "parameters": {}
    }, function=tracker.stop_timer)
}

agent.tools = [tool.schema for tool in tools.values()]

agent.system_prompt = """You are a time tracking assistant. You help users track time spent on different tasks.
When a user mentions something they're going to do next, extract the task name and use the start_task tool.
When a user wants to stop tracking time, use the stop_timer tool.
"""

async def main():
    print("Time Tracker started. Type 'exit' to quit.")
    print("Just describe what you're working on, or say 'stop' when done.")
    
    while True:
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            if tracker.current_entry:
                tracker.stop_timer()
            break

        response = await agent.chat(user_input)
        print(response)

        tool_calls = response.choices[0].message.tool_calls
        results = []

        for tool_call in tool_calls:
            if tool_call.function.name == 'start_task':
                task_name = tool_call.function.arguments.split('"')[3]
                results.append(tracker.start_task(task_name))
            elif tool_call.function.name == 'stop_timer':
                results.append(tracker.stop_timer())

        result = "\n".join(results) if results else "No actions performed."
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
