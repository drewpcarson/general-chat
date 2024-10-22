from agent import Agent, providers
import asyncio

agent = Agent(providers['XAI'], max_tokens=200)

async def main():
    while True:
        user_input = input("> ")
    
        if user_input.lower() == 'exit':
            break

        response = await agent.chat(user_input)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())