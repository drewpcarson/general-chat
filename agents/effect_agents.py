from agent import Agent, providers
import asyncio

"""
This file defines the agent swarm that decides the effects of an action. The flow is: 
1. decide_effect_categories agent decides which effect categories are relevant to the action (input: action, output: list of effect categories)
2. depending on the effect categories, different agents will be invoked to decide the effects of the action (input: action and context, output: list of effects)
"""

EFFECTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "select_effect_categories",
        "description": "Select which effect categories are relevant for an action",
        "parameters": {
            "type": "object",
            "properties": {
                "categories": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["backstory", "inventory", "armor", "abilities", "location", "enemies"]
                    },
                    "description": "List of categories that might be affected by the action"
                }
            },
            "required": ["categories"]
        }   
    }
}

EFFECT_EVALUATION_SCHEMA = {
    "type": "function",
    "function": {
        "name": "evaluate_effects",
        "description": "Evaluate the effects of an action with respect to the current category",
        "parameters": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "An effect that occurred as a result of the action"
            },
        }
    }
}

RULES = """
Please follow these rules:
1. If a specific detail is not provided, make something up, and be decisive. This is D&D, after all!
2. Don't say "might" or "could" or "maybe" - this is D&D, and you are the DM. The game is more fun when you are decisive.
3. Be very specific and concrete about the effects of the action. Don't leave any vague details.
4. Fast-forward to the next interesting action.

Examples of specificity and "fast-forwarding" to the next interesting action:
- "I punch the goblin in the face" -> "Goblin A is knocked unconscious.", "Goblin B rushes you with his club raised above his head, shouting maniacally."
- "I open the trapdoor" -> "The trapdoor creaks open, revealing a narrow staircase.", "The staircase disappears down into darkness", "There are thick cobwebs down its entirety."
- "I jump from the ledge into the stream far below" -> "You fall through the air, the wind rushing past your ears, before splashing into the water", "your right leg scrapes violently against a rock beneath the surface", "5 damage"
"""

decide_effects = Agent(
    provider=providers['XAI'],
    system_prompt="""You are an agent responsible for deciding which categories will be affected by a given action.""",
    tools=[EFFECTS_SCHEMA]
)

backstory_effects = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for deciding how an action will affect the player's backstory, if at all.
    Focus exclusively on changes to the player's history, background, or memories, if any (there will be other agents for handling other types of effects).
    {RULES}
    """,
    tools=[EFFECT_EVALUATION_SCHEMA]
)

inventory_effects = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for deciding how an action will affect the player's inventory, if at all.
    Focus exclusively on changes to the items in the player's inventory, if any (there will be other agents for handling other types of effects).
    {RULES}
    """,
    tools=[EFFECT_EVALUATION_SCHEMA]
)

armor_effects = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for deciding how an action will affect the player's armor, if at all.
    Focus exclusively on changes to the player's armor, if any (there will be other agents for handling other types of effects).
    {RULES}
    """,
    tools=[EFFECT_EVALUATION_SCHEMA]
)

abilities_effects = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for deciding how an action will affect the player's abilities, if at all.
    Focus exclusively on long-term changes to the player's abilities, if any (there will be other agents for handling other types of effects).
    {RULES}
    """,
    tools=[EFFECT_EVALUATION_SCHEMA]
)

location_effects = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for deciding how an action will affect the player's location or position, if at all.
    Focus exclusively on changes to the current location, objects in the environment, or terrain, if any (there will be other agents for handling other types of effects).
    {RULES}
    """,
    tools=[EFFECT_EVALUATION_SCHEMA]
)

enemies_effects = Agent(
    provider=providers['XAI'],
    system_prompt="""You are an agent responsible for deciding how an action will affect the player's enemies, if at all.
    Focus exclusively on changes to the player's enemies, if any (there will be other agents for handling other types of effects).
    If there are multiple enemies, ensure they are named (e.g. "goblin A", "troll B", "ogre A", etc.), so you can keep track of them over the course of several actions.
    If an enemy responds or counterattacks, describe the response or counterattack specifically.""",
    tools=[EFFECT_EVALUATION_SCHEMA]
)

async def determine_effects(action: str, context: dict) -> tuple[list[dict], list[str]]:
    """
    Determines the effects of an action based on the game context.
    
    Args:
        action: The action the player took
        context: Dictionary containing game state
    
    Returns:
        Tuple of (effects: list[dict], descriptions: list[str])
    """
    try:
        # Get relevant effect categories
        categories_response = await decide_effects.chat(
            f"Action to evaluate: {action}",
            expect_function_call=True,
            temperature=0.0
        )
        
        if not isinstance(categories_response, dict) or "categories" not in categories_response:
            raise ValueError("Invalid categories response format")
        
        categories = categories_response.get("categories", [])
        
        # Map categories to their respective agents
        category_agents = {
            "backstory": backstory_effects,
            "inventory": inventory_effects,
            "armor": armor_effects,
            "abilities": abilities_effects,
            "location": location_effects,
            "enemies": enemies_effects
        }
        
        # Create tasks for all relevant agents
        async def evaluate_category(category: str, agent: Agent) -> tuple[str, dict]:
            agent_input = f"Action: {action}\nContext: {context}"
            response = await agent.chat(
                agent_input,
                expect_function_call=True,
                temperature=0.0
            )
            return category, response
            
        tasks = [
            evaluate_category(category, category_agents[category])
            for category in categories
            if category in category_agents
        ]
        
        # Run all tasks in parallel
        responses = await asyncio.gather(*tasks)
        return responses
        
    except Exception as e:
        return [], [f"Error determining effects: {str(e)}"]
