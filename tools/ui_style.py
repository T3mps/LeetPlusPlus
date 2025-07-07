#!/usr/bin/env python3
"""
UI Style Guide for LeetPlusPlus
Provides consistent styling and formatting across all outputs
"""

from common import Fore, Style, ColorPrinter


class UIStyle:
    """Centralized UI styling constants and methods"""
    
    # Dividers
    DIVIDER_LENGTH = 70
    DIVIDER_CHAR = '━'
    DIVIDER = f"{Fore.BLUE}{DIVIDER_CHAR * DIVIDER_LENGTH}{Style.RESET_ALL}"
    DIVIDER_SHORT = f"{Fore.BLUE}{DIVIDER_CHAR * 50}{Style.RESET_ALL}"
    
    # Headers
    @staticmethod
    def header(title: str, subtitle: str = None) -> str:
        """Create a consistent header"""
        lines = []
        lines.append("")  # Empty line before header
        lines.append(f"{Fore.WHITE}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        if subtitle:
            lines.append(f"{Fore.WHITE}{Style.DIM}{subtitle}{Style.RESET_ALL}")
        lines.append(UIStyle.DIVIDER)
        return '\n'.join(lines)
    
    @staticmethod
    def section_header(title: str) -> str:
        """Create a section header"""
        return f"\n{Fore.YELLOW}{Style.BRIGHT}{title}:{Style.RESET_ALL}"
    
    # Tables
    @staticmethod
    def table_header(columns: list) -> str:
        """Create a table header with proper formatting"""
        header_parts = []
        for col, width in columns:
            header_parts.append(f"{Fore.CYAN}{col:<{width}}{Style.RESET_ALL}")
        
        lines = []
        lines.append("")  # Empty line before table
        lines.append(' '.join(header_parts))
        lines.append(f"{Fore.BLUE}{'-' * sum(w for _, w in columns)}{Style.RESET_ALL}")
        return '\n'.join(lines)
    
    # Problem formatting
    @staticmethod
    def format_problem_row(problem_id: str, title: str, difficulty: str, 
                          acceptance: str = None, width_id: int = 6,
                          width_title: int = 50, width_diff: int = 12,
                          width_acc: int = 10) -> str:
        """Format a problem row with consistent styling"""
        # Truncate title if needed
        if len(title) > width_title:
            title = title[:width_title-3] + "..."
        
        # Color code difficulty
        if difficulty == 'Easy':
            diff_color = Fore.GREEN
        elif difficulty == 'Medium':
            diff_color = Fore.YELLOW
        else:  # Hard
            diff_color = Fore.RED
        
        # Format acceptance
        if acceptance and isinstance(acceptance, (int, float)):
            acc_str = f"{acceptance:>{width_acc-1}.1f}%"
        else:
            acc_str = f"{'N/A':>{width_acc}}"
        
        return f"{problem_id:<{width_id}} {title:<{width_title}} {diff_color}{difficulty:<{width_diff}}{Style.RESET_ALL} {acc_str}"
    
    # Messages
    @staticmethod
    def success_banner(message: str) -> str:
        """Create a success banner"""
        lines = []
        lines.append(f"{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}")
        return '\n'.join(lines)
    
    @staticmethod
    def error_banner(message: str) -> str:
        """Create an error banner"""
        lines = []
        lines.append(f"{Fore.RED}{Style.BRIGHT}✗ {message}{Style.RESET_ALL}")
        return '\n'.join(lines)
    
    # Progress indicators
    @staticmethod
    def progress(current: int, total: int, prefix: str = "Progress") -> str:
        """Create a progress indicator"""
        percent = (current / total) * 100 if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        
        bar = f"{'█' * filled}{'░' * (bar_length - filled)}"
        
        return f"{prefix}: {Fore.CYAN}{bar}{Style.RESET_ALL} {percent:>5.1f}% ({current}/{total})"
    
    # Command examples
    @staticmethod
    def command_example(command: str, description: str = None) -> str:
        """Format a command example"""
        if description:
            return f"  {Fore.WHITE}{Style.DIM}lpp ▶{Style.RESET_ALL} {Fore.CYAN}{command:<30}{Style.RESET_ALL} {Fore.WHITE}{Style.DIM}# {description}{Style.RESET_ALL}"
        else:
            return f"  {Fore.WHITE}{Style.DIM}lpp ▶{Style.RESET_ALL} {Fore.CYAN}{command}{Style.RESET_ALL}"
    
    # Footer
    @staticmethod
    def footer(message: str = None) -> str:
        """Create a consistent footer"""
        lines = []
        if message:
            lines.append(f"\n{Fore.MAGENTA}{message}{Style.RESET_ALL}")
        lines.append(UIStyle.DIVIDER)
        lines.append("")  # Empty line after footer
        return '\n'.join(lines)
    
    # Input styling
    @staticmethod
    def bordered_input(prompt: str = "", width: int = 80) -> str:
        """Create a bordered input prompt"""
        # Box drawing characters
        top_left = "╭"
        top_right = "╮"
        bottom_left = "╰"
        bottom_right = "╯"
        horizontal = "─"
        vertical = "│"
        
        # Smart width calculation
        # The total visual width should be consistent
        border_width = width
        line_width = border_width - 2  # Subtract 2 for the corner characters
        
        # Top border
        top_border = f"{Style.DIM}{Fore.WHITE}{top_left}{horizontal * line_width}{top_right}{Style.RESET_ALL}"
        print(top_border)
        
        # Middle line construction
        left_border = f"{Style.DIM}{Fore.WHITE}{vertical}{Style.RESET_ALL}"
        right_border = f"{Style.DIM}{Fore.WHITE}{vertical}{Style.RESET_ALL}"
        
        # Content with prompt
        prompt_text = f"{prompt} " if prompt else ""
        content = f" {Fore.YELLOW}▶{Style.RESET_ALL} {prompt_text}"
        
        # Calculate exact padding needed
        # Visual content length (without ANSI codes)
        content_visual_length = 1 + 2 + len(prompt_text)  # space + "▶ " + prompt
        
        # Total space available inside borders
        available_space = border_width - 2  # -2 for left and right borders
        
        # Padding needed
        padding = available_space - content_visual_length
        
        # Construct middle line
        middle = left_border + content + (" " * padding) + right_border
        print(middle)
        
        # Bottom border (identical to top)
        bottom_border = f"{Style.DIM}{Fore.WHITE}{bottom_left}{horizontal * line_width}{bottom_right}{Style.RESET_ALL}"
        print(bottom_border)
        
        # Move cursor back to input position
        print(f"\033[2A", end='')  # Move up 2 lines
        cursor_x = 1 + 1 + 2 + len(prompt_text)  # border + space + "▶ " + prompt
        print(f"\033[{cursor_x}C", end='', flush=True)
        
        # Get user input
        user_input = input()
        
        # Move past bottom border
        print(f"\033[1B", end='')
        
        return user_input