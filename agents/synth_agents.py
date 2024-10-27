from agent import Agent, providers
import asyncio
"""
This file defines the agents that are used to synthesize the effects of an action with the current context. 
"""

RULES = """
Please follow these rules:
1. the response should be plain, unformatted, single-spaced text
2. the response should be as concise as possible, while still capturing all essential details
"""

synthesize_backstory = Agent(
    provider=providers['XAI'],
    system_prompt=f"""
You are an agent responsible for synthesizing the effects of an action with the player's backstory. 
The important thing is to keep track of the player's important history, background, and memories.
The final result should be the total backstory description, updated with the effects of the action.
{RULES}
"""
)

synthesize_inventory = Agent(
    provider=providers['XAI'],
    system_prompt=f"""
You are an agent responsible for synthesizing the effects of an action with the player's inventory. 
The important thing is to keep track of the items that the player has and what condition they are in.
The final result should be the total inventory description, updated with the effects of the action.
{RULES}
"""
)

synthesize_armor = Agent(
    provider=providers['XAI'],
    system_prompt=f"""
You are an agent responsible for synthesizing the effects of an action with the player's armor. 
The important thing is to keep track of the armor that the player has and what condition it is in.
The final result should be the total armor description, updated with the effects of the action.
{RULES}
"""
)

synthesize_abilities = Agent(
    provider=providers['XAI'],
    system_prompt=f"""
You are an agent responsible for synthesizing the effects of an action with the player's abilities. 
The important thing is to keep track of the abilities that the player has and to what extent those abilities are developed.
The final result should be the total abilities description, updated with the effects of the action.
{RULES}
"""
)

synthesize_location = Agent(
    provider=providers['XAI'],
    system_prompt=f"""
You are an agent responsible for synthesizing the effects of an action with the player's location. 
The important thing is to keep track of the details of the current location and the surroundings. 
The final result should be the total location description, updated with the effects of the action.
{RULES}
"""
)

synthesize_enemies = Agent(
    provider=providers['XAI'],
    system_prompt=f"""
You are an agent responsible for synthesizing the effects of an action with the player's enemies. 
The important thing is to keep track of the details of the enemies that the player is currently facing, including their abilities, equipment, strengths, weaknesses, and condition.
The final result should be the total enemies description, updated with the effects of the action.
{RULES}
"""
)

async def synthesize_effects(effects: list[tuple[str, list[str]]], context: dict) -> dict:
    """
    Synthesizes the effects of an action with the current context.
    
    Args:
        effects: List of tuples (category, list of effect descriptions)
        context: Current game context
    
    Returns:
        Updated context dictionary
    """
    try:
        # Map categories to their respective synthesis agents
        synth_agents = {
            "backstory": synthesize_backstory,
            "inventory": synthesize_inventory,
            "armor": synthesize_armor,
            "abilities": synthesize_abilities,
            "location": synthesize_location,
            "enemies": synthesize_enemies
        }
        
        # Create a copy of the current context
        new_context = context.copy()
        
        # Process each category that has effects
        async def synthesize_category(category: str, descriptions: list[str]) -> tuple[str, str]:
            if category not in synth_agents:
                return category, context[category]
                
            agent = synth_agents[category]
            agent_input = f"""
Current {category}: {context[category]}

Effects to incorporate:
{chr(10).join(f'- {desc}' for desc in descriptions)}

Synthesize these effects with the current {category} and provide an updated description.
"""
            response = await agent.chat(agent_input)
            return category, response
        
        # Create tasks for categories with effects
        tasks = [
            synthesize_category(category, descriptions)
            for category, descriptions in effects
            if descriptions  # Only process categories that have effects
        ]
        
        if tasks:
            # Run all synthesis tasks in parallel
            responses = await asyncio.gather(*tasks)
            
            # Update context with synthesized results
            for category, new_value in responses:
                new_context[category] = new_value
                
        return new_context
        
    except Exception as e:
        print(f"Error synthesizing effects: {str(e)}")
        return context  # Return original context if synthesis fails
