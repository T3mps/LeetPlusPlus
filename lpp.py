#!/usr/bin/env python3
"""
LeetPlusPlus Command Line Interface
Main entry point for all LeetPlusPlus operations

Supports both direct command execution and interactive console mode.
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "tools"))

from common import ColorPrinter, MetadataManager, Fore, Style
from config import APP_VERSION, EXE_RELEASE_PATH, EXE_DEBUG_PATH
from ui_style import UIStyle


class CommandHandler:
    """Handles command execution with a clean dictionary-based approach"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.tools_dir = self.root_dir / "tools"
        self.metadata_manager = MetadataManager()
        
        self.commands = {
            'console': self.console_command,
            'interactive': self.console_command,
            'i': self.console_command,
            'fetch': self.fetch_command,
            'generate': self.generate_command,
            'update': self.update_metadata_command,
            'list': self.list_command,
            'run': self.run_command,
            'help': self.help_command,
            '--help': self.help_command,
            '-h': self.help_command,
            'version': self.version_command,
            '--version': self.version_command,
            '-v': self.version_command,
        }
    
    def console_command(self, args):
        """Launch interactive console mode"""
        from console import main as console_main
        return console_main()
    
    def fetch_command(self, args):
        """Fetch a problem using the fetcher"""
        fetch_args = ['python', str(self.tools_dir / 'leetcode_fetcher_simple.py'), 'fetch'] + args
        return subprocess.call(fetch_args)
    
    def generate_command(self, args):
        """Generate solution file"""
        from generate_solution import main as generate_main
        return generate_main()
    
    def update_metadata_command(self, args):
        """Update problem metadata"""
        from metadata_updater import main as update_main
        return update_main()
    
    def list_command(self, args):
        """List available problems"""
        problems_list = self.metadata_manager.get_problems_list()
        
        if not problems_list:
            ColorPrinter.warning("No metadata found. Run 'lpp update' first.")
            return 1
        
        # Print styled header
        print(UIStyle.header("LeetCode Problems", "Showing first 20 problems"))
        
        # Print table header
        columns = [
            ('ID', 6),
            ('Title', 50),
            ('Difficulty', 12),
            ('Acceptance', 10)
        ]
        print(UIStyle.table_header(columns))
        
        # Show first 20 problems
        for problem in problems_list[:20]:
            problem_id = str(problem.get('id', ''))
            title = problem.get('title', '')
            difficulty = problem.get('difficulty', '')
            acceptance = problem.get('acRate', 'N/A')
            
            print(UIStyle.format_problem_row(
                problem_id, title, difficulty, acceptance
            ))
        
        if len(problems_list) > 20:
            footer_msg = f"Showing 20 of {len(problems_list)} problems. Use interactive mode for more options."
        else:
            footer_msg = f"Total: {len(problems_list)} problems"
        
        print(UIStyle.footer(footer_msg))
        return 0
    
    def run_command(self, args):
        """Launch TUI application"""
        exe_path = self.root_dir / EXE_RELEASE_PATH
        if not exe_path.exists():
            exe_path = self.root_dir / EXE_DEBUG_PATH
        
        if not exe_path.exists():
            ColorPrinter.error("LeetPlusPlus executable not found. Please build the project first.")
            return 1
        
        return subprocess.call([str(exe_path)], cwd=self.root_dir)
    
    def help_command(self, args):
        """Show help information"""
        print_help()
        return 0
    
    def version_command(self, args):
        """Show version information"""
        print(f"LeetPlusPlus v{APP_VERSION}")
        return 0
    
    def execute(self, command, args):
        """Execute a command with arguments"""
        handler = self.commands.get(command)
        if handler:
            return handler(args)
        else:
            ColorPrinter.error(f"Unknown command: {command}")
            print("Run 'lpp help' for usage information")
            return 1


def main():
    """Main entry point that handles both console and direct command modes."""
    handler = CommandHandler()
    
    # If no arguments provided, launch interactive console
    if len(sys.argv) == 1:
        return handler.execute('console', [])
    
    # Handle direct commands
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    return handler.execute(command, args)


def print_help():
    """Print help information for direct mode."""
    print(UIStyle.header("LeetPlusPlus", "A professional C++ development framework for LeetCode"))
    
    # Usage section
    print(UIStyle.section_header("Usage"))
    print(f"  {Fore.GREEN}lpp{Style.RESET_ALL}                        Launch interactive console mode")
    print(f"  {Fore.GREEN}lpp{Style.RESET_ALL} {Fore.CYAN}<command>{Style.RESET_ALL} {Fore.WHITE}[args...]{Style.RESET_ALL}    Execute a command directly")
    
    # Commands section
    print(UIStyle.section_header("Commands"))
    commands = [
        ("console, interactive, i", "Launch interactive console mode"),
        ("fetch <number|slug>", "Fetch a problem by number or slug"),
        ("generate <number>", "Generate solution file for existing problem"),
        ("list", "List available problems"),
        ("run", "Launch the TUI application"),
        ("update", "Update problem metadata from API"),
        ("help", "Show this help message"),
        ("version", "Show version information")
    ]
    
    for cmd, desc in commands:
        print(f"  {Fore.GREEN}{cmd:<25}{Style.RESET_ALL}  {desc}")
    
    # Examples section
    print(UIStyle.section_header("Examples"))
    examples = [
        ("lpp", "Enter interactive mode"),
        ("lpp fetch 1", "Fetch problem #1 (Two Sum)"),
        ("lpp fetch two-sum", "Fetch by problem slug"),
        ("lpp list", "List all problems"),
        ("lpp run", "Launch TUI application")
    ]
    
    for example, desc in examples:
        print(UIStyle.command_example(example, desc))
    
    print(UIStyle.footer("For more features and detailed help, use the interactive console mode."))


if __name__ == "__main__":
    sys.exit(main())