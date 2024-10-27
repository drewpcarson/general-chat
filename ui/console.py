import os
import sys

# Color constants
class ConsoleColors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def print_horizontal_line(length=50, char='-'):
    """Print a horizontal line of a specified character and length."""
    print(char * length)

def print_in_box(content, width=50):
    """Print content enclosed in a box."""
    lines = content.split('\n')
    box_width = max(len(line) for line in lines) + 4
    print('+' + '-' * (box_width - 2) + '+')
    for line in lines:
        print(f"| {line:<{box_width - 4}} |")
    print('+' + '-' * (box_width - 2) + '+')

def wrap_text(text, width=50):
    """Wrap text to a specified width."""
    import textwrap
    return '\n'.join(textwrap.wrap(text, width))

def set_color(text, color_code):
    """Set the color of the text for console output."""
    return f"{color_code}{text}{ConsoleColors.RESET}"

def refresh_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_side_by_side(content1, content2):
    """Print two pieces of content side by side."""
    lines1 = content1.split('\n')
    lines2 = content2.split('\n')
    max_lines = max(len(lines1), len(lines2))
    
    for i in range(max_lines):
        line1 = lines1[i] if i < len(lines1) else ''
        line2 = lines2[i] if i < len(lines2) else ''
        print(f"{line1:<50} {line2}")