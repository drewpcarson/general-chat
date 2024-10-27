from ui.console import ConsoleColors, print_in_box, set_color
from ui.cli import CLI

class GameManager:
    def __init__(self):
        self.context = {
            # TODO: Add context fields
        }
        
        self.commands = {
            "context": (self.show_context, "Show current game context"),
            "clear": (self.clear_screen, "Clear the console screen"),
            "help": (self.show_help, "Show available commands")
            # TODO: Add more commands
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
        # TODO: define how queries should be processed
        pass

    async def run(self):
        print_in_box("Agent Manager")
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
