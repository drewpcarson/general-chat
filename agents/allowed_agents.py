from agent import Agent, providers
import asyncio

"""
This file defines the agent swarm that decides whether an action is allowed. The flow is: 
1. decide_constraints agent decides which constraints are relevant to the action (input: action, output: list of constraints)
2. depending on the constraints, different agents will be invoked to decide whether the action is allowed (input: action and context, output: yes/no)
3. if any of the invoked agents return no, the action is not allowed.
"""

CONSTRAINTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "select_constraints",
        "description": "Select which constraints are relevant for evaluating an action",
        "parameters": {
            "type": "object",
            "properties": {
                "constraints": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["backstory", "inventory", "armor", "abilities", "location", "enemies"]
                    },
                    "description": "List of constraints that are relevant to the action"
                }
            },
            "required": ["constraints"]
        }   
    }
}

EVALUATION_SCHEMA = {
    "type": "function",
    "function": {
        "name": "evaluate_action",
        "description": "Evaluate whether an action is allowed based on the given context",
        "parameters": {
            "type": "object",
            "properties": {
                "allowed": {
                    "type": "boolean",
                    "description": "Whether the action is allowed"
                },
                "reason": {
                    "type": "string",
                    "description": "A brief explanation for the decision"
                }
            },
            "required": ["allowed", "reason"]
        }
    }
}

GAME_RULES = """
Please follow these rules:
1. Actions that break the laws of PHYSICS (except when using magic) are forbidden.
2. Actions that use magic are allowed ONLY if the player explicitly possesses that specific magical ability.
ALL OTHER ACTIONS, whether immoral, illegal, or unethical, are allowed. 
Remember: This is D&D. The world should be an open sandbox for the players to explore and experiment.
"""

decide_constraints = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for determining the constraints relevant to a given action. Your task is to analyze the action provided and return a list of constraints that other agents will need to check. Keep in mind the game rules: {GAME_RULES}""",
    tools=[CONSTRAINTS_SCHEMA]
)

backstory_agent = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for analyzing the player's backstory and deciding whether the desired action can proceed. The action should be allowed unless one of the following rules is clearly violated: {GAME_RULES}""",
    tools=[EVALUATION_SCHEMA]
)

inventory_agent = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for analyzing the player's inventory and deciding whether the desired action can proceed. The action should be allowed unless one of the following rules is clearly violated: {GAME_RULES}""",
    tools=[EVALUATION_SCHEMA]
)

armor_agent = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for assessing the player's armor and deciding whether the desired action can proceed. The action should be allowed unless one of the following rules is clearly violated: {GAME_RULES}""",
    tools=[EVALUATION_SCHEMA]
)

abilities_agent = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for evaluating the player's special abilities and deciding whether the desired action can proceed. The action should be allowed unless one of the following rules is clearly violated: {GAME_RULES}""",
    tools=[EVALUATION_SCHEMA]
)

location_agent = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for analyzing the features of the current location and deciding whether the desired action can proceed. The action should be allowed unless one of the following rules is clearly violated: {GAME_RULES}""",
    tools=[EVALUATION_SCHEMA]
)

enemies_agent = Agent(
    provider=providers['XAI'],
    system_prompt=f"""You are an agent responsible for evaluating the details of the enemies present in the current location and deciding whether the player's desired action can proceed. The action should be allowed unless one of the following rules is clearly violated: {GAME_RULES}""",
    tools=[EVALUATION_SCHEMA]
)

async def is_action_allowed(action: str, context: dict) -> tuple[bool, list[str]]:
    """
    Determines if an action is allowed based on the game context.
    
    Args:
        action: The action the player wants to take
        context: Dictionary containing game state
    
    Returns:
        Tuple of (is_allowed: bool, reasons: list[str])
    """
    try:
        # Get relevant constraints with structured output
        constraints_response = await decide_constraints.chat(
            f"Action to evaluate: {action}",
            expect_function_call=True,
            temperature=0.0
        )
        if not isinstance(constraints_response, dict) or "constraints" not in constraints_response:
            raise ValueError("Invalid constraints response format")
        
        constraints = constraints_response.get("constraints", [])
        
        # Map constraints to their respective agents
        constraint_agents = {
            "backstory": backstory_agent,
            "inventory": inventory_agent,
            "armor": armor_agent,
            "abilities": abilities_agent,
            "location": location_agent,
            "enemies": enemies_agent
        }
        
        # Create tasks for all relevant agents
        async def evaluate_constraint(constraint: str, agent: Agent) -> tuple[str, dict]:
            agent_input = f"Action: {action}\nContext: {context.get(constraint, '')}"
            response = await agent.chat(
                agent_input,
                expect_function_call=True,
                temperature=0.0
            )
            return constraint, response
        
        tasks = [
            evaluate_constraint(constraint, constraint_agents[constraint])
            for constraint in constraints
            if constraint in constraint_agents
        ]
        
        # Run all tasks in parallel
        responses = await asyncio.gather(*tasks)
        
        # Process responses
        is_allowed = True
        reasons = []
        
        for constraint, response in responses:
            if not response.get("allowed", True):
                is_allowed = False
            reasons.append(f"{constraint}: {response.get('allowed', 'allowed')}: {response.get('reason', 'No reason provided')}")
        
        return is_allowed, reasons
    
    except Exception as e:
        return False, [f"Error evaluating action: {str(e)}"]
