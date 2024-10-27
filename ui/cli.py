class CLI:
    """
    A simple Command Line Interface (CLI) class for handling user input.

    Usage:
    1. Create an instance of the CLI class by passing a dictionary of commands.
       Each command should be a key with a tuple as its value, where the first
       element is the handler function and the second element is a description.
    2. Call the `run()` method to start the input loop.
    3. Type 'help' to see available commands or 'quit' to exit the loop.
    """

    def __init__(self, commands):
        """
        Initialize the CLI with a dictionary of commands.
        Each command should be a tuple of (handler_function, description).
        """
        self.commands = commands

    def help(self):
        """Print the list of available commands and their descriptions."""
        print("Available commands:")
        for command, (handler, description) in self.commands.items():
            print(f"  {command}: {description}")

    def run(self):
        """Start the CLI input loop."""
        while True:
            user_input = input("> ").strip()
            if user_input == 'quit':
                print("Exiting the CLI.")
                break
            elif user_input == 'help':
                self.help()
            elif user_input in self.commands:
                handler, _ = self.commands[user_input]
                handler()
            else:
                print(f"Unknown command: {user_input}. Type 'help' for a list of commands.")

