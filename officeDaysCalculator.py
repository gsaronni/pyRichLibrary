  #!/usr/bin/env python3
"""
Vacation Calculator - McGugan's Rainbow Explosion Edition! 🌈
Where vacation planning meets visual euphoria!
Now with dumbed down math: Every 3 vacation days = 1 less office day!
"""

import argparse
import calendar
import datetime
import json
import os
import sys
from typing import Dict, Tuple, List
import random

# Import required libraries
try:
    import holidays
    from rich.console import Console, Group
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.tree import Tree
    from rich.text import Text
    from rich.columns import Columns
    from rich.align import Align
    from rich import box
    from rich.progress import track
    from rich.spinner import Spinner
    from rich.live import Live
    from rich.rule import Rule
    import time
except ImportError as e:
    print(f"🌈 ERROR: Missing the rainbow magic! {e}")
    print("✨ Install with: pip install rich holidays")
    sys.exit(1)

# 🌈 RAINBOW COLOR PALETTE - McGugan Style!
RAINBOW_COLORS = [
    "bright_red", "bright_yellow", "bright_green", "bright_cyan", 
    "bright_blue", "bright_magenta", "red", "yellow", "green", 
    "cyan", "blue", "magenta", "orange1", "orange3", "gold1", 
    "green1", "cyan1", "purple", "pink1", "hot_pink"
]

GRADIENT_COLORS = ["#ff0000", "#ff4500", "#ffa500", "#ffff00", "#9aff9a", "#00ff7f", "#00ffff", "#0080ff", "#8000ff", "#ff00ff"]

# Fun emoji sets
VACATION_EMOJIS = ["🏖️", "🌴", "🏝️", "☀️", "🌺", "🍹", "🏄‍♂️", "🐚", "🌊", "🦩"]
WORK_EMOJIS = ["💼", "💻", "📊", "📈", "⚙️", "🏢", "📋", "✨", "🎯", "🚀"]
CELEBRATION_EMOJIS = ["🎉", "🎊", "✨", "🌟", "💫", "🎈", "🎁", "🥳", "🎭", "🎪"]

# Rich console with enhanced features
console = Console(color_system="truecolor", legacy_windows=False)

# Capgemini Italian offices with patron saint dates
CAPGEMINI_OFFICES = {
    "Milano": {"patron_saint": "Sant'Ambrogio", "date": "12-07", "emoji": "🏙️"},
    "Roma": {"patron_saint": "Santi Pietro e Paolo", "date": "06-29", "emoji": "🏛️"},
    "Torino": {"patron_saint": "San Giovanni Battista", "date": "06-24", "emoji": "🏔️"},
    "Napoli": {"patron_saint": "San Gennaro", "date": "09-19", "emoji": "🌋"},
    "Palermo": {"patron_saint": "Santa Rosalia", "date": "07-15", "emoji": "🏖️"},
    "Trieste": {"patron_saint": "San Giusto", "date": "11-03", "emoji": "⛵"},
    "Venezia": {"patron_saint": "San Marco Evangelista", "date": "04-25", "emoji": "🚤"},
    "Bari": {"patron_saint": "San Nicola", "date": "12-06", "emoji": "🐟"},
    "Modena": {"patron_saint": "San Geminiano", "date": "01-31", "emoji": "🏎️"},
    "Padova": {"patron_saint": "Sant'Antonio", "date": "06-13", "emoji": "🎓"},
    "Piacenza": {"patron_saint": "Sant'Antonino", "date": "07-04", "emoji": "🌾"},
    "Pisa": {"patron_saint": "San Ranieri", "date": "06-17", "emoji": "🗼"},
    "Salerno": {"patron_saint": "San Matteo", "date": "09-21", "emoji": "🌊"}
}

CONFIG_FILE = "capgemini_user_config.json"

# NEW SIMPLE CONSTANTS! 🎉
BASELINE_OFFICE_DAYS = 6  # Default office days per month
VACATION_TO_OFFICE_RATIO = 3  # Every 3 vacation days = 1 less office day


def get_random_color():
    """Get a random rainbow color."""
    return random.choice(RAINBOW_COLORS)


def get_random_emoji(emoji_set):
    """Get a random emoji from a set."""
    return random.choice(emoji_set)


def rainbow_text(text: str, colors: List[str] = None) -> Text:
    """Create rainbow-colored text."""
    if colors is None:
        colors = RAINBOW_COLORS[:len(text)]
    
    rainbow = Text()
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow.append(char, style=f"bold {color}")
    return rainbow


def show_spectacular_header():
    """Display the most amazing header ever created!"""
    console.print()
    
    # Rainbow title
    title = rainbow_text("🌈 CAPGEMINI VACATION CALCULATOR 🌈")
    subtitle = Text("Where Vacation Planning Meets Visual Euphoria!", style="italic bright_magenta")
    
    # NEW: Show the simple formula!
    formula = Text("✨ NEW SUPER SIMPLE FORMULA: Every 3 vacation days = 1 less office day! ✨", 
                  style="bold bright_cyan blink")
    
    # Sparkly border
    sparkles = "✨" * 50
    
    header_content = Group(
        Text(sparkles, style="bright_yellow"),
        Align.center(title),
        Align.center(subtitle),
        Align.center(formula),
        Text(sparkles, style="bright_cyan")
    )
    
    header_panel = Panel(
        header_content,
        box=box.DOUBLE,
        style="bright_magenta on black",
        padding=(1, 2)
    )
    console.print(header_panel)
    
    # Animated loading bar for fun
    console.print()
    for _ in track(range(20), description="[rainbow]Loading vacation magic..."):
        time.sleep(0.05)
    console.print()


def show_funky_error(message: str, title: str = "Oops! 🤯"):
    """Display a funky error panel."""
    error_emoji = get_random_emoji(["💥", "🚨", "⚠️", "🔥", "💔", "😱"])
    
    error_panel = Panel(
        f"{error_emoji} {message} {error_emoji}",
        title=f"[bold bright_red blink]{title}[/]",
        title_align="center",
        box=box.HEAVY,
        style="bright_red on black",
        padding=(1, 2)
    )
    console.print(error_panel)


def show_party_warning(message: str, title: str = "Hold Up! 🎪"):
    """Display a party-style warning."""
    warning_emoji = get_random_emoji(["🎭", "🎪", "🎨", "🎈", "🎊", "🎉"])
    
    warning_panel = Panel(
        f"{warning_emoji} {message} {warning_emoji}",
        title=f"[bold bright_yellow]{title}[/]",
        title_align="center",
        box=box.ROUNDED,
        style="bright_yellow on blue",
        padding=(1, 2)
    )
    console.print(warning_panel)


def show_celebration_success(message: str, title: str = "Amazing! 🎉"):
    """Display a celebration success panel."""
    success_emoji = get_random_emoji(CELEBRATION_EMOJIS)
    
    success_panel = Panel(
        f"{success_emoji} {message} {success_emoji}",
        title=f"[bold bright_green]{title}[/]",
        title_align="center",
        box=box.DOUBLE_EDGE,
        style="bright_green on black",
        padding=(1, 2)
    )
    console.print(success_panel)


def load_user_config() -> Dict:
    """Load user configuration from JSON file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_user_config(config: Dict) -> None:
    """Save user configuration to JSON file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        show_party_warning(f"Couldn't save config: {e}")


def create_psychedelic_office_tree() -> Tree:
    """Create the most colorful office tree ever!"""
    tree = Tree(rainbow_text("🏢 CAPGEMINI ITALY RAINBOW OFFICES 🏢"))
    
    # Colorful regions
    regions = {
        "🏔️ Northern Italy": ["Milano", "Torino", "Venezia", "Padova", "Modena", "Piacenza", "Pisa"],
        "🏛️ Central Italy": ["Roma"],
        "🌊 Southern Italy": ["Napoli", "Bari", "Salerno", "Palermo"],
        "⛵ Northeast Italy": ["Trieste"]
    }
    
    region_colors = ["bright_blue", "bright_green", "bright_red", "bright_magenta"]
    
    for i, (region, cities) in enumerate(regions.items()):
        region_color = region_colors[i % len(region_colors)]
        region_branch = tree.add(f"[bold {region_color}]{region}[/]")
        
        for city in cities:
            if city in CAPGEMINI_OFFICES:
                office_info = CAPGEMINI_OFFICES[city]
                city_color = get_random_color()
                city_text = f"[{city_color}]{office_info['emoji']} {city}[/] - [dim bright_white]{office_info['patron_saint']} ({office_info['date']})[/]"
                region_branch.add(city_text)
    
    return tree


def setup_funky_office_selection() -> str:
    """The most fun office selection ever!"""
    console.print()
    
    # Exciting setup message
    setup_panel = Panel(
        Group(
            rainbow_text("🎪 FIRST TIME SETUP EXTRAVAGANZA! 🎪"),
            "",
            Text("Time to pick your Capgemini kingdom!", style="bright_cyan"),
            Text("This magical choice will be remembered forever! ✨", style="bright_magenta")
        ),
        title="[bold bright_yellow]✨ CONFIGURATION WIZARD ✨[/]",
        box=box.HEAVY,
        style="bright_blue on black",
        padding=(1, 2)
    )
    console.print(setup_panel)
    
    # Show the psychedelic tree
    console.print()
    console.print(create_psychedelic_office_tree())
    console.print()
    
    # Create the most colorful table ever
    table = Table(
        title=rainbow_text("🌈 CHOOSE YOUR DESTINY 🌈"), 
        box=box.DOUBLE_EDGE, 
        style="bright_white"
    )
    table.add_column("🎯", style="bold bright_red", width=4)
    table.add_column("🏢 City", style="bold bright_blue", width=12)
    table.add_column("⛪ Patron Saint", style="bright_green", width=25)
    table.add_column("📅 Date", style="bright_yellow", width=10)
    table.add_column("Fun Factor", style="bright_magenta", width=12)
    
    offices = list(CAPGEMINI_OFFICES.keys())
    fun_factors = ["🔥 EPIC", "⚡ WILD", "🎨 ARTSY", "🌟 STELLAR", "🚀 COSMIC", 
                   "💫 MAGICAL", "🎪 CIRCUS", "🎭 DRAMA", "🎵 MUSICAL", "🎮 GAMER",
                   "🍕 TASTY", "🌮 SPICY", "🍦 COOL"]
    
    for i, office in enumerate(offices, 1):
        office_info = CAPGEMINI_OFFICES[office]
        row_color = get_random_color()
        fun_factor = random.choice(fun_factors)
        
        table.add_row(
            f"[{row_color}]{i}[/]",
            f"[{row_color}]{office_info['emoji']} {office}[/]",
            f"[{get_random_color()}]{office_info['patron_saint']}[/]",
            f"[{get_random_color()}]{office_info['date']}[/]",
            f"[{get_random_color()}]{fun_factor}[/]"
        )
    
    console.print(table)
    console.print()
    
    # Exciting prompt
    while True:
        try:
            choice = IntPrompt.ask(
                f"[bold bright_magenta]🎯 Pick your magical number (1-{len(offices)}) 🎯[/]",
                choices=[str(i) for i in range(1, len(offices) + 1)],
                show_choices=False
            )
            
            selected_office = offices[choice - 1]
            config = {"office": selected_office}
            save_user_config(config)
            
            # Celebration animation!
            celebration_text = f"🎉 FANTASTIC CHOICE! Welcome to Capgemini {selected_office}! 🎉"
            show_celebration_success(celebration_text)
            
            # Fun loading animation
            console.print()
            for _ in range(3):
                with Live(Spinner("dots", text="Saving your awesome choice..."), refresh_per_second=10):
                    time.sleep(0.5)
            
            return selected_office
            
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[{get_random_color()}]Maybe next time! Ciao! 👋[/]")
            sys.exit(0)


def get_working_days_in_month(year: int, month: int, office: str) -> Tuple[int, List[datetime.date], List[datetime.date], List[datetime.date]]:
    """Calculate working days with extra fun!"""
    # Show calculation progress
    with console.status(f"[bold bright_cyan]🔮 Calculating magical working days for {office}..."):
        time.sleep(0.8)  # Add some suspense!
        
        # Get Italian holidays for the year
        italy_holidays = holidays.Italy(years=year)
        
        # Add patron saint day for the office
        patron_date = CAPGEMINI_OFFICES[office]["date"]
        patron_month, patron_day = map(int, patron_date.split('-'))
        patron_saint_date = datetime.date(year, patron_month, patron_day)
        italy_holidays[patron_saint_date] = f"{CAPGEMINI_OFFICES[office]['patron_saint']} ({office})"
        
        # Categorize days
        working_days = []
        weekend_days = []
        holiday_days = []
        days_in_month = calendar.monthrange(year, month)[1]
        
        for day in range(1, days_in_month + 1):
            date = datetime.date(year, month, day)
            
            if date.weekday() >= 5:  # Weekend
                weekend_days.append(date)
            elif date in italy_holidays:  # Holiday
                holiday_days.append(date)
            else:  # Working day
                working_days.append(date)
    
    return len(working_days), working_days, weekend_days, holiday_days


def create_rainbow_calendar(year: int, month: int, working_days: List[datetime.date], 
                           weekend_days: List[datetime.date], holiday_days: List[datetime.date]) -> Panel:
    """Create the most colorful calendar in existence!"""
    
    # Create calendar grid
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Create rainbow table for calendar
    calendar_table = Table(box=box.HEAVY, show_header=True, header_style="bold bright_magenta")
    
    # Rainbow day headers
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_colors = ["bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta", "orange1"]
    
    for i, day in enumerate(days):
        calendar_table.add_column(f"[{day_colors[i]}]{day}[/]", justify="center", width=5)
    
    # Add colorful calendar rows
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append("")
            else:
                date = datetime.date(year, month, day)
                if date in working_days:
                    # Random bright color for working days
                    work_color = random.choice(["bright_green", "green1", "spring_green1", "lime"])
                    row.append(f"[bold {work_color} on black]{day:2d}[/]")
                elif date in holiday_days:
                    # Hot colors for holidays
                    holiday_color = random.choice(["bright_red", "red1", "hot_pink", "orange_red1"])
                    row.append(f"[bold {holiday_color} on black blink]{day:2d}[/]")
                elif date in weekend_days:
                    # Cool colors for weekends
                    weekend_color = random.choice(["bright_blue", "blue1", "cyan1", "deep_sky_blue1"])
                    row.append(f"[{weekend_color}]{day:2d}[/]")
                else:
                    row.append(f"[white]{day:2d}[/]")
        calendar_table.add_row(*row)
    
    # Create psychedelic legend
    legend = Text()
    legend.append("💼 ", style="bright_green")
    legend.append("Working Days", style="bold bright_green")
    legend.append(" • ")
    legend.append("🎉 ", style="bright_red")
    legend.append("Holidays", style="bold bright_red blink")
    legend.append(" • ")
    legend.append("🏖️ ", style="bright_blue")
    legend.append("Weekends", style="bold bright_blue")
    
    # Use Group to combine elements
    calendar_content = Group(
        Align.center(calendar_table),
        "",
        Align.center(legend)
    )
    
    return Panel(
        calendar_content,
        title=rainbow_text(f"🌈 {month_name} {year} RAINBOW CALENDAR 🌈"),
        box=box.DOUBLE_EDGE,
        style="bright_cyan on black",
        padding=(1, 1)
    )


def calculate_simple_presence(vacation_days: int, baseline_office_days: int = BASELINE_OFFICE_DAYS) -> Tuple[int, int, float]:
    """
    🎉 THE NEW SUPER SIMPLE FORMULA! 🎉
    Every 3 vacation days reduces office days by 1
    Returns: (office_days, remote_days, reduction_amount_before_rounding)
    """
    
    # Calculate reduction: vacation_days / 3
    office_reduction = vacation_days / VACATION_TO_OFFICE_RATIO
    
    # Apply reduction to baseline, but don't go below 0
    office_days = max(0, baseline_office_days - round(office_reduction))
    
    # Remote days are whatever's left (assuming 20 total working days)
    # But we'll calculate this based on actual working days
    
    return office_days, office_reduction


def create_formula_explanation_panel(vacation_days: int, office_reduction: float, office_days: int) -> Panel:
    """Create a colorful panel explaining the new simple formula!"""
    
    # Create step-by-step explanation
    steps = Group(
        Text("🎯 BASELINE OFFICE DAYS:", style="bold bright_cyan"),
        Text(f"   {BASELINE_OFFICE_DAYS} days per month", style="bright_white"),
        "",
        Text("🧮 VACATION REDUCTION FORMULA:", style="bold bright_yellow"),
        Text(f"   {vacation_days} vacation days ÷ {VACATION_TO_OFFICE_RATIO} = {office_reduction:.2f} days reduction", style="bright_white"),
        "",
        Text("🔄 ROUNDING MAGIC:", style="bold bright_magenta"),
        Text(f"   {office_reduction:.2f} rounds to {round(office_reduction)} days", style="bright_white"),
        Text("   (0.5+ rounds up, <0.5 rounds down)", style="dim bright_white"),
        "",
        Text("✨ FINAL RESULT:", style="bold bright_green"),
        Text(f"   {BASELINE_OFFICE_DAYS} - {round(office_reduction)} = {office_days} office days needed!", style="bold bright_green blink")
    )
    
    return Panel(
        steps,
        title=rainbow_text("🧮 SUPER SIMPLE MATH MAGIC! 🧮"),
        box=box.DOUBLE_EDGE,
        style="bright_blue on black",
        padding=(1, 2)
    )


def create_spectacular_results_table(vacation_days: int, remote_days: int, office_days: int, 
                                   working_days: int) -> Table:
    """Create the most spectacular results table ever!"""
    table = Table(
        title=rainbow_text("🎪 YOUR FABULOUS WORK BREAKDOWN 🎪"), 
        box=box.DOUBLE_EDGE, 
        style="bright_white"
    )
    
    table.add_column("Category", style="bold bright_cyan", width=20)
    table.add_column("Days", justify="center", style="bold bright_white", width=8)
    table.add_column("Percentage", justify="center", style="bold bright_yellow", width=12)
    table.add_column("Mood", justify="center", style="bold bright_magenta", width=15)
    
    # Calculate percentages
    vacation_pct = f"{(vacation_days/working_days*100):.1f}%" if working_days > 0 else "0%"
    remote_pct = f"{(remote_days/working_days*100):.1f}%" if working_days > 0 else "0%"
    office_pct = f"{(office_days/working_days*100):.1f}%" if working_days > 0 else "0%"
    
    # Fun mood indicators
    vacation_mood = get_random_emoji(VACATION_EMOJIS) + " PARADISE!"
    remote_mood = get_random_emoji(["🏠", "☕", "🐱", "📚", "🎵"]) + " COZY!"
    office_mood = get_random_emoji(WORK_EMOJIS) + " POWER!"
    
    table.add_row(
        f"[bright_yellow]{get_random_emoji(VACATION_EMOJIS)} Vacation Days[/]", 
        f"[bold bright_red]{vacation_days}[/]", 
        f"[bright_green]{vacation_pct}[/]", 
        f"[bright_magenta]{vacation_mood}[/]"
    )
    table.add_row(
        f"[bright_green]🏠 Remote Work[/]", 
        f"[bold bright_blue]{remote_days}[/]", 
        f"[bright_cyan]{remote_pct}[/]", 
        f"[bright_yellow]{remote_mood}[/]"
    )
    table.add_row(
        f"[bright_blue]{get_random_emoji(WORK_EMOJIS)} Office Required[/]", 
        f"[bold bright_green blink]{office_days}[/]", 
        f"[bright_red]{office_pct}[/]", 
        f"[bright_green]{office_mood}[/]"
    )
    
    # Sparkly separator
    table.add_row("", "", "", "")
    table.add_row(
        f"[bright_cyan]✨ Total Magic Days[/]", 
        f"[bold bright_white]{working_days}[/]", 
        "[bold bright_white]100%[/]", 
        f"[bright_magenta]{get_random_emoji(CELEBRATION_EMOJIS)} EPIC![/]"
    )
    
    return table


def main():
    parser = argparse.ArgumentParser(
        description="🌈 The most colorful vacation calculator in the universe! 🌈",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument('vacation_days', type=int, 
                       help='Number of vacation days planned (MANDATORY)')
    parser.add_argument('--working-days', type=int, default=None,
                       help='Override working days (default: auto-calculate for current month)')
    parser.add_argument('--month', type=int, default=None, choices=range(1, 13),
                       help='Month (1-12, default: current month)')
    
    args = parser.parse_args()
    
    # Show spectacular header
    show_spectacular_header()
    
    # Load or setup user configuration
    config = load_user_config()
    if not config.get('office'):
        office = setup_funky_office_selection()
    else:
        office = config['office']
        office_info = CAPGEMINI_OFFICES[office]
        welcome_back = f"Welcome back to {office_info['emoji']} {office}!"
        show_celebration_success(welcome_back, "Hey There, Superstar! 🌟")
    
    # Determine month and year
    now = datetime.datetime.now()
    month = args.month if args.month else now.month
    year = now.year
    
    # Handle December edge case
    if month == 12 and now.month == 12 and now.day > 15:
        year_end_msg = "🎄 Ho ho ho! Looking at next year's holidays! 🎅"
        show_party_warning(year_end_msg, "Christmas Magic! 🎄")
        year += 1
    
    # Validate input
    vacation_days = args.vacation_days
    if vacation_days < 0:
        show_funky_error("Negative vacation days? That's like anti-fun! 😱")
        sys.exit(1)
    
    # Calculate working days
    if args.working_days:
        working_days_count = args.working_days
        working_days_list = []
        weekend_days_list = []
        holiday_days_list = []
        console.print(f"\n[bright_cyan]🎯 Using custom working days: {working_days_count}[/]")
    else:
        working_days_count, working_days_list, weekend_days_list, holiday_days_list = get_working_days_in_month(year, month, office)
    
    if vacation_days > working_days_count:
        over_vacation_msg = f"Whoa! {vacation_days} vacation days vs {working_days_count} working days? You're living the dream! 🌈"
        show_party_warning(over_vacation_msg, "Dream Mode Activated! 💫")
    
    # 🎉 THE NEW SIMPLE CALCULATION! 🎉
    console.print(f"\n[bold bright_magenta]🔮 Using the new SUPER SIMPLE formula...[/]")
    
    # Calculate office days needed using simple formula
    office_days, office_reduction = calculate_simple_presence(vacation_days)
    
    # Calculate remote days (remaining working days after vacation and office)
    remaining_working_days = max(0, working_days_count - vacation_days)
    remote_days = max(0, remaining_working_days - office_days)
    
    console.print()
    
    # Show the simple formula explanation
    formula_panel = create_formula_explanation_panel(vacation_days, office_reduction, office_days)
    console.print(formula_panel)
    console.print()
    
    # Create colorful office info panel
    office_info = CAPGEMINI_OFFICES[office]
    office_panel = Panel(
        Group(
            Text(f"{office_info['emoji']} Location: {office}", style="bold bright_blue"),
            Text(f"⛪ Patron Saint: {office_info['patron_saint']}", style="bold bright_green"),
            Text(f"📅 Holiday Date: {office_info['date']}", style="bold bright_red"),
            Text(f"🗓️ Month/Year: {calendar.month_name[month]} {year}", style="bold bright_magenta")
        ),
        title=rainbow_text("🏢 YOUR FANTASTIC OFFICE 🏢"),
        box=box.DOUBLE_EDGE,
        style="bright_blue on black",
        padding=(1, 1)
    )
    
    # Create method panel - now much simpler!
    method_panel = Panel(
        Group(
            Text("✨ SIMPLE FORMULA ✨", style="bold bright_green", justify="center"),
            Text("Every 3 vacation days = 1 less office day", style="bright_cyan", justify="center"),
            Text(f"Baseline: {BASELINE_OFFICE_DAYS} office days per month", style="bright_yellow", justify="center")
        ),
        title=rainbow_text("🔮 CALCULATION MAGIC 🔮"),
        box=box.DOUBLE_EDGE,
        style="bright_magenta on black",
        padding=(1, 1)
    )
    
    # Show office info and method
    console.print(Columns([office_panel, method_panel]))
    console.print()
    
    # Show rainbow calendar if we have the data
    if working_days_list and not args.working_days:
        console.print(create_rainbow_calendar(year, month, working_days_list, weekend_days_list, holiday_days_list))
        console.print()
    
    # Show spectacular results table
    results_table = create_spectacular_results_table(vacation_days, remote_days, office_days, working_days_count)
    console.print(Align.center(results_table))
    console.print()
    
    # GRAND FINALE - The most epic final result ever!
    finale_emojis = get_random_emoji(CELEBRATION_EMOJIS)
    office_emoji = get_random_emoji(WORK_EMOJIS)
    
    # Create pulsating final result
    final_message = Group(
        rainbow_text("🎊 THE MOMENT YOU'VE BEEN WAITING FOR! 🎊"),
        "",
        Text(f"You need to be in the office", style="bold bright_white"),
        Text(f"{office_emoji} {office_days} DAYS {office_emoji}", style="bold bright_green blink", justify="center"),
        Text("this month!", style="bold bright_white"),
        "",
        Text(f"{finale_emojis} Now go forth and conquer! {finale_emojis}", style="bold bright_magenta")
    )
    
    final_panel = Panel(
        Align.center(final_message),
        title=rainbow_text("🌟 FINAL VERDICT 🌟"),
        box=box.DOUBLE,
        style="bright_green on black",
        padding=(2, 3)
    )
    
    console.print(final_panel)
    
    # Celebration fireworks!
    console.print()
    fireworks = "🎆 " * 20
    console.print(Text(fireworks, style="bright_yellow blink"))
    console.print(Text("Thanks for using the most AWESOME vacation calculator ever! ✨", 
                      style="bold bright_cyan", justify="center"))
    console.print(Text(fireworks, style="bright_red blink"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        goodbye_messages = [
            "🌈 Farewell, rainbow warrior! 🌈",
            "✨ Until we meet again in color! ✨", 
            "🎪 The circus must go on... elsewhere! 🎪",
            "🎨 Keep painting the world colorful! 🎨",
            "🦄 Unicorns never say goodbye! 🦄"
        ]
        console.print(f"\n[bold {get_random_color()}]{random.choice(goodbye_messages)}[/]")
        sys.exit(0)
