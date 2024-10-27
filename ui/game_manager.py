from ui.console import ConsoleColors, print_in_box, set_color
from ui.cli import CLI
from agents.allowed_agents import is_action_allowed
from agents.effect_agents import determine_effects
from agents.synth_agents import synthesize_effects
import asyncio

class GameManager:
    def __init__(self):
        self.context = {
            "backstory": "A rogue knight who has been exiled from his order for his unorthodox behavior",
            "inventory": "Sword, shield, healing potion",
            "armor": "Chainmail (good condition)",
            "abilities": "Trained in swordfighting",
            "location": "In a crowded marketplace",
            "enemies": "Two armed guards blocking the path"
        }
        
        self.commands = {
            "context": (self.show_context, "Show current game context"),
            "clear": (self.clear_screen, "Clear the console screen"),
            "help": (self.show_help, "Show available commands")
        }
        self.cli = CLI(self.commands)

    def show_context(self):
        print_in_box("Current Context")
        for key, value in self.context.items():
            print(f"{set_color(key.capitalize(), ConsoleColors.CYAN)}: {value}")

    def clear_screen(self):
        from ui.console import refresh_console
        refresh_console()

    def show_help(self):
        print_in_box("Available Commands")
        print("- Type any action to check if it's allowed")
        print("- Use 'exit' to quit the game")
        for cmd, (_, desc) in self.commands.items():
            print(f"- {set_color(cmd, ConsoleColors.GREEN)}: {desc}")

    async def process_action(self, action: str):
        # First check if action is allowed
        print("\nDetermining if action is allowed...")
        is_allowed, reasons = await is_action_allowed(action, self.context)
        
        if is_allowed:
            print(f"\nIs allowed: {set_color(str(is_allowed), ConsoleColors.GREEN)}")
            for reason in reasons:
                print(f"- {reason}")
            
            # If allowed, determine and apply effects
            print("\nDetermining effects of action...")
            effects = await determine_effects(action, self.context)
            
            # Print effect descriptions
            if effects:
                print_in_box("Action Effects")
                for effect in effects:
                    effect_type, effect_descriptions = effect
                    if effect_descriptions:
                        for desc in effect_descriptions:
                            print(f"- {set_color(effect_type, ConsoleColors.GREEN)}: {desc}")

            # Synthesize effects with current context
            print("\nSynthesizing effects...")
            synth_results = await synthesize_effects(effects, self.context)
            
            # Output the updated context
            if synth_results:
                self.context = synth_results
                self.show_context()
                    
        else:
            print(f"\nIs allowed: {set_color(str(is_allowed), ConsoleColors.RED)}")
            for reason in reasons:
                print(f"- {reason}")

    async def run(self):
        print_in_box("Dungeon Master Wiz")
        print("Type 'help' to see available commands or 'exit' to quit.")
        
        while True:
            user_input = input(f"\n{set_color('>', ConsoleColors.CYAN)} ").strip()

            if user_input.lower() == 'exit':
                break

            if user_input in self.commands:
                handler, _ = self.commands[user_input]
                handler()
            else:
                await self.process_action(user_input)
