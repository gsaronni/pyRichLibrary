from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import box
import random

def calculate_tokens(num_days):
    """Calculate total tokens based on number of days worked."""
    total_tokens = (25 * num_days) / 7
    return total_tokens

def display_results(num_days, total_tokens):
    """Display results using Rich formatting with CRAZY random colors."""
    console = Console()
    
    # Generate INSANE random hex colors! 🎨🎲
    def random_hex_color():
        # Generate random RGB values (0-255) and convert to hex
        r = random.randint(0, 255)
        g = random.randint(0, 255) 
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    # Roll the dice for each color! 🎰
    title_color = random_hex_color()
    border_color = random_hex_color()
    label_color = random_hex_color()
    value_color = random_hex_color()
    
    # Create a fancy title with random color
    title = Text("🎯 TOKEN CALCULATOR 🎯", style=f"bold {title_color}")
    
    # Create the main content - more compact
    content = Text()
    content.append("Days Worked: ", style=f"bold {label_color}")
    content.append(f"{num_days} ", style=f"bold {value_color}")
    content.append("| Total Tokens: ", style=f"bold {label_color}")
    content.append(f"{total_tokens:.2f}", style=f"bold {value_color}")
    
    # Create a much smaller panel
    panel = Panel(
        content,
        title=title,
        border_style=border_color,
        box=box.ROUNDED,
        padding=(0, 1),
        width=50
    )
    
    console.print()
    console.print(panel)
    console.print()

def main():
    console = Console()
    
    # Welcome message
    console.print("\n[bold blue]Welcome to the Token Calculator![/bold blue] ✨\n")
    
    try:
        # Get input with Rich prompt
        num_days_worked = Prompt.ask(
            "[cyan]Enter the number of days worked[/cyan]",
            default="1"
        )
        
        num_days_worked = int(num_days_worked)
        
        if num_days_worked <= 0:
            console.print("[bold red]❌ Invalid number of days. Please enter a positive number.[/bold red]")
            return
        
        # Calculate tokens
        total_tokens = calculate_tokens(num_days_worked)
        
        # Display beautiful results
        display_results(num_days_worked, total_tokens)
        
    except ValueError:
        console.print("[bold red]❌ Please enter a valid number.[/bold red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")

if __name__ == "__main__":
    main()
