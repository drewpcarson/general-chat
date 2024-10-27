from agent import Agent, providers
from tool import Tool
from timetracker import TimeTracker
import asyncio
from ui.game_manager import GameManager

async def main():
    game_manager = GameManager()
    await game_manager.run()

if __name__ == "__main__":
    asyncio.run(main())
