#!/usr/bin/env python3
"""
Interactive Console for LeetPlusPlus
Provides a REPL interface for all LeetPlusPlus commands
"""

import cmd
import os
import sys
import subprocess
import shlex
from pathlib import Path
from typing import List, Optional

sys.path.append(str(Path(__file__).parent))
from leetcode_fetcher_simple import LeetCodeAPI, generate_from_api_data
from metadata_updater import MetadataUpdater
from generate_solution import generate_solution
from common import ColorPrinter, APIServerManager, MetadataManager, Fore, Style
from config import (
    APP_NAME, APP_VERSION, APP_GITHUB, API_BASE_URL, 
    EXE_RELEASE_PATH, EXE_DEBUG_PATH, CONSOLE_PROMPT,
    SUPPORTS_TRUECOLOR, CONSOLE_BANNER_WIDTH
)
from ui_style import UIStyle


def create_gradient_banner():
    """Create a gradient colored banner from red to purple"""
    banner_lines = [
        "██╗     ███████╗███████╗████████╗                                 ",
        "██║     ██╔════╝██╔════╝╚══██╔══╝                                 ",
        "██║     █████╗  █████╗     ██║                                    ",
        "██║     ██╔══╝  ██╔══╝     ██║                                    ",
        "███████╗███████╗███████╗   ██║                                    ",
        "╚══════╝╚══════╝╚══════╝   ╚═╝                                    ",
        "                                                                  ",
        "██████╗ ██╗     ██╗   ██╗███████╗██████╗ ██╗     ██╗   ██╗███████╗",
        "██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██║     ██║   ██║██╔════╝",
        "██████╔╝██║     ██║   ██║███████╗██████╔╝██║     ██║   ██║███████╗",
        "██╔═══╝ ██║     ██║   ██║╚════██║██╔═══╝ ██║     ██║   ██║╚════██║",
        "██║     ███████╗╚██████╔╝███████║██║     ███████╗╚██████╔╝███████║",
        "╚═╝     ╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚══════╝"
    ]
    
    # Function to get gradient color
    def get_gradient_color(position, max_position):
        ratio = position / max_position if max_position > 0 else 0
        
        if SUPPORTS_TRUECOLOR or os.name == 'nt':
            # Three-color gradient: Orange -> Red -> Purple
            if ratio < 0.5:
                # Orange to Red
                local_ratio = ratio * 2
                red = 255
                green = int(165 * (1 - local_ratio))
                blue = 0
            else:
                # Red to Purple
                local_ratio = (ratio - 0.5) * 2
                red = int(255 * (1 - local_ratio) + 128 * local_ratio)
                green = 0
                blue = int(128 * local_ratio)
            
            return f"\033[38;2;{red};{green};{blue}m"
        else:
            # Fallback to basic colors
            if ratio < 0.33:
                return Fore.YELLOW
            elif ratio < 0.66:
                return Fore.RED
            else:
                return Fore.MAGENTA
    
    # Build gradient banner
    gradient_banner = f"{Style.BRIGHT}\n"
    max_width = max(len(line) for line in banner_lines)
    
    for line in banner_lines:
        colored_line = ""
        for i, char in enumerate(line):
            if char != ' ':
                color = get_gradient_color(i, max_width)
                colored_line += color + char
            else:
                colored_line += ' '
        # Reset after each line to prevent color bleeding
        gradient_banner += colored_line + f"{Style.RESET_ALL}\n"
    
    # Final reset to ensure clean state
    gradient_banner += f"{Style.RESET_ALL}"
    return gradient_banner


class LeetPlusPlusConsole(cmd.Cmd):
    """Interactive console for LeetPlusPlus"""
    
    intro = None  # Will be set dynamically in __init__
    
    prompt = f"{Fore.GREEN}{CONSOLE_PROMPT}{Style.RESET_ALL} {Fore.YELLOW}▶{Style.RESET_ALL} "
    use_bordered_prompt = True  # Flag to enable/disable bordered prompt
    
    def __init__(self):
        super().__init__()
        self.root_dir = Path(__file__).parent.parent
        self.api = LeetCodeAPI()
        self.metadata_updater = MetadataUpdater()
        self.metadata_manager = MetadataManager()
        self.api_manager = APIServerManager(API_BASE_URL)
        self._load_metadata()
        self._check_api_status()
        
        # Create intro dynamically based on metadata
        if not self.metadata or len(self.metadata) == 0:
            footer_message = f"{Fore.MAGENTA}First time?{Style.RESET_ALL} Run {Fore.YELLOW}'update'{Style.RESET_ALL} to fetch the problem list from LeetCode."
        else:
            total = len(self.metadata)
            footer_message = f"{Fore.CYAN}ℹ{Style.RESET_ALL}  Loaded {Fore.GREEN}{total}{Style.RESET_ALL} problems from metadata"
        
        self.intro = f"""{create_gradient_banner()}{Style.RESET_ALL}

{Fore.WHITE}{Style.DIM}A professional C++ development framework for LeetCode{Style.RESET_ALL}
{Fore.BLUE}{'━' * CONSOLE_BANNER_WIDTH}{Style.RESET_ALL}
{Fore.YELLOW}v{APP_VERSION}{Style.RESET_ALL} {Fore.WHITE}|{Style.RESET_ALL} {Fore.CYAN}{APP_GITHUB}{Style.RESET_ALL}

{Fore.YELLOW}Quick Start:{Style.RESET_ALL}
  {Fore.GREEN}fetch <number|slug>{Style.RESET_ALL}  - Fetch a problem (e.g., 'fetch 1' or 'fetch two-sum')
  {Fore.GREEN}list{Style.RESET_ALL}                 - List all problems
  {Fore.GREEN}status{Style.RESET_ALL}               - Show system status
  {Fore.GREEN}help{Style.RESET_ALL}                 - Show all commands
  {Fore.GREEN}exit{Style.RESET_ALL}                 - Leave the console

{footer_message}
"""
        
    def _load_metadata(self):
        """Load problem metadata"""
        self.metadata = self.metadata_manager.load()
        self.problems_list = self.metadata_manager.get_problems_list()
    
    # Wrapper methods for ColorPrinter with UIStyle support
    def _print_success(self, message: str, banner: bool = False):
        if banner:
            print(UIStyle.success_banner(message))
        else:
            ColorPrinter.success(message)
    
    def _print_error(self, message: str, banner: bool = False):
        if banner:
            print(UIStyle.error_banner(message))
        else:
            ColorPrinter.error(message)
    
    def _print_info(self, message: str):
        ColorPrinter.info(message)
    
    def _print_warning(self, message: str):
        ColorPrinter.warning(message)
    
    def _check_api_status(self):
        """Check if AlfaLeetCode API is running and start it if not"""
        if not self.api_manager.check_available():
            ColorPrinter.warning("AlfaLeetCode API server is not running!")
            self._start_api_server()
    
    def _start_api_server(self):
        """Attempt to start the API server"""
        # Use the centralized API manager
        self.api_manager.start_server(auto_mode=True)
    
    # Command implementations
    
    def do_fetch(self, arg):
        """Fetch a LeetCode problem by number or slug
        
        Usage: fetch <number|slug> [--force] [--interactive]
        
        Examples:
            fetch 1                 # Fetch problem #1 (Two Sum)
            fetch two-sum          # Fetch by slug
            fetch 1 --force        # Overwrite existing solution
            fetch daily            # Fetch today's daily problem
        """
        args = shlex.split(arg)
        if not args:
            self._print_error("Please provide a problem number or slug")
            return
        
        identifier = args[0]
        force = '--force' in args
        interactive = '--interactive' in args
        
        # Check API availability and try to start if needed
        if not self.api_manager.ensure_running():
            ColorPrinter.error("Cannot fetch problems - API server could not be started")
            return
        
        try:
            # Check if fetching daily problem
            if identifier.lower() == 'daily':
                self._print_info("Fetching daily problem...")
                problem_data = self.api.fetch_daily()
                if problem_data:
                    generate_from_api_data(problem_data, interactive_mode=interactive)
                    self._print_success("Daily problem fetched successfully!", banner=True)
                else:
                    self._print_error("Failed to fetch daily problem")
            else:
                self._print_info(f"Fetching problem: {identifier}")
                
                # Check if it's a number (fetch by ID) or slug
                if identifier.isdigit():
                    # Fetch by number using metadata
                    if identifier not in self.metadata:
                        self._print_error(f"Problem #{identifier} not found in metadata")
                        self._print_info("Run 'update' to refresh problem list")
                        return
                    
                    problem_info = self.metadata[identifier]
                    slug = problem_info.get('titleSlug')
                    
                    # If no slug, try to derive it from the title
                    if not slug and 'title' in problem_info:
                        # Convert title to slug format (e.g., "Two Sum" -> "two-sum")
                        slug = problem_info['title'].lower().replace(' ', '-')
                        self._print_info(f"Using derived slug: {slug}")
                    
                    if not slug:
                        self._print_error(f"No slug found for problem #{identifier}")
                        self._print_info("Please update metadata: 'update'")
                        return
                    
                    self._print_info(f"Found problem #{identifier}: {problem_info.get('title', 'Unknown')}")
                    problem_data = self.api.fetch_problem(slug)
                else:
                    # Fetch by slug
                    problem_data = self.api.fetch_problem(identifier)
                
                if problem_data:
                    try:
                        # Check if problem already exists
                        problem_id = problem_data.get('questionFrontendId', problem_data.get('questionId'))
                        problems_dir = self.root_dir / "src" / "Problems"
                        existing_files = list(problems_dir.glob(f"{problem_id}_*.h")) if problems_dir.exists() else []
                        
                        if existing_files and not force:
                            # Problem exists, ask user what to do
                            self._print_warning(f"Problem #{problem_id} already exists: {existing_files[0].name}")
                            print(f"\n{Fore.YELLOW}Do you want to overwrite it?{Style.RESET_ALL}")
                            print(f"  {Fore.GREEN}y{Style.RESET_ALL} - Yes, overwrite the existing solution")
                            print(f"  {Fore.RED}n{Style.RESET_ALL} - No, keep the existing solution")
                            print()
                            
                            choice = UIStyle.bordered_input("Your choice (y/n):").strip().lower()
                            
                            if choice == 'y':
                                # Delete existing files
                                for file in existing_files:
                                    file.unlink()
                                    self._print_info(f"Removed existing file: {file.name}")
                                generate_from_api_data(problem_data, interactive_mode=interactive, force=True)
                                self._print_success("Problem fetched and overwritten successfully!", banner=True)
                            else:
                                self._print_info("Keeping existing solution. No changes made.")
                        else:
                            # No existing file or force flag is set
                            if force and existing_files:
                                for file in existing_files:
                                    file.unlink()
                                    self._print_info(f"Removed existing file: {file.name}")
                            
                            generate_from_api_data(problem_data, interactive_mode=interactive, force=force)
                            self._print_success("Problem fetched successfully!", banner=True)
                            
                    except ValueError as e:
                        # Handle other ValueError exceptions that aren't about existing files
                        if "already exists" not in str(e):
                            self._print_error(f"Failed to generate problem: {e}")
                    except Exception as e:
                        self._print_error(f"Unexpected error: {e}")
                else:
                    self._print_error("Failed to fetch problem")
                    
        except Exception as e:
            self._print_error(f"Failed to fetch problem: {e}")
    
    def do_list(self, arg):
        """List available problems
        
        Usage: list [--difficulty <easy|medium|hard>] [--topic <topic>] [--limit <n>]
        
        Examples:
            list                           # List all problems
            list --difficulty easy         # List only easy problems
            list --topic "dynamic programming"  # List DP problems
            list --limit 10               # Show only first 10 problems
        """
        args = shlex.split(arg)
        difficulty = None
        topic = None
        limit = None
        
        # Parse arguments
        i = 0
        while i < len(args):
            if args[i] == '--difficulty' and i + 1 < len(args):
                difficulty = args[i + 1].lower()
                i += 2
            elif args[i] == '--topic' and i + 1 < len(args):
                topic = args[i + 1].lower()
                i += 2
            elif args[i] == '--limit' and i + 1 < len(args):
                try:
                    limit = int(args[i + 1])
                    i += 2
                except ValueError:
                    self._print_error("Limit must be a number")
                    return
            else:
                i += 1
        
        # Load and filter problems
        if not self.problems_list:
            self._print_warning("No metadata found. Run 'update' first.")
            return
        
        problems = self.problems_list
        
        # Apply filters
        if difficulty:
            problems = [p for p in problems if p.get('difficulty', '').lower() == difficulty]
        
        if topic:
            problems = [p for p in problems if any(topic in t.lower() for t in p.get('topicTags', []))]
        
        if limit:
            problems = problems[:limit]
        
        # Display problems
        if not problems:
            self._print_info("No problems found matching criteria")
            return
        
        # Create header with filters info
        header_title = "LeetCode Problems"
        filter_info = []
        if difficulty:
            filter_info.append(f"Difficulty: {difficulty.capitalize()}")
        if topic:
            filter_info.append(f"Topic: {topic}")
        if limit:
            filter_info.append(f"Limit: {limit}")
        
        subtitle = f"Filters: {', '.join(filter_info)}" if filter_info else "All problems"
        
        # Print styled header
        print(UIStyle.header(header_title, subtitle))
        
        # Print table header
        columns = [
            ('ID', 6),
            ('Title', 50),
            ('Difficulty', 12),
            ('Acceptance', 10)
        ]
        print(UIStyle.table_header(columns))
        
        # Print problems
        for problem in problems:
            problem_id = str(problem.get('id', ''))
            title = problem.get('title', '')
            difficulty = problem.get('difficulty', '')
            acceptance = problem.get('acRate', 'N/A')
            
            print(UIStyle.format_problem_row(
                problem_id, title, difficulty, acceptance
            ))
        
        # Print footer
        print(UIStyle.footer(f"Total: {len(problems)} problems"))
    
    def do_run(self, arg):
        """Launch the TUI application
        
        Usage: run
        """
        try:
            exe_path = self.root_dir / EXE_RELEASE_PATH
            if not exe_path.exists():
                # Try debug build
                exe_path = self.root_dir / EXE_DEBUG_PATH
            
            if not exe_path.exists():
                self._print_error("LeetPlusPlus executable not found. Please build the project first.")
                return
            
            self._print_info("Launching TUI application...")
            subprocess.run([str(exe_path)], cwd=self.root_dir)
        except Exception as e:
            self._print_error(f"Failed to launch application: {e}")
    
    def do_generate(self, arg):
        """Generate solution file for an existing problem
        
        Usage: generate <number> [--force]
        
        Examples:
            generate 1              # Generate solution for problem #1
            generate 1 --force      # Overwrite existing solution
        """
        args = shlex.split(arg)
        if not args:
            self._print_error("Please provide a problem number")
            return
        
        try:
            problem_id = args[0]
            force = '--force' in args
            
            # Find problem in metadata
            if not self.metadata:
                self._print_error("No metadata found. Run 'update' first.")
                return
            
            problem = self.metadata.get(problem_id)
            
            if not problem:
                self._print_error(f"Problem #{problem_id} not found in metadata")
                return
            
            self._print_info(f"Generating solution for problem #{problem_id}: {problem.get('title')}")
            
            # Call generate_solution directly
            sys.argv = ['generate_solution.py', problem_id]
            if force:
                sys.argv.append('--force')
            
            generate_solution()
            self._print_success("Solution file generated successfully!", banner=True)
            
        except Exception as e:
            self._print_error(f"Failed to generate solution: {e}")
    
    def do_update(self, arg):
        """Update problem metadata from LeetCode API
        
        Usage: update
        """
        # Check API availability and try to start if needed
        if not self.api_manager.ensure_running():
            ColorPrinter.error("Cannot update metadata - API server could not be started")
            return
            
        try:
            self._print_info("Updating metadata from LeetCode API...")
            self.metadata_updater.run()
            self._load_metadata()  # Reload metadata
            ColorPrinter.success("Metadata update process completed")
        except Exception as e:
            self._print_error(f"Failed to update metadata: {e}")
    
    def do_api_start(self, arg):
        """Show instructions to start the AlfaLeetCode API server
        
        Usage: api-start
        """
        # Check if AlfaLeetCode directory exists
        alfa_dir = self.root_dir / "vendor" / "AlfaLeetCode"
        if not alfa_dir.exists():
            self._print_error("AlfaLeetCode API not found in vendor directory!")
            print("Please ensure you have cloned the repository with submodules:")
            print(f"  {Fore.GREEN}git submodule update --init --recursive{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Starting AlfaLeetCode API Server:{Style.RESET_ALL}")
        print("\nOption 1: Manual start (recommended)")
        print("  1. Open a new terminal window")
        print("  2. Navigate to the project root")
        print("  3. Run these commands:")
        print(f"     {Fore.GREEN}cd vendor/AlfaLeetCode{Style.RESET_ALL}")
        print(f"     {Fore.GREEN}npm install{Style.RESET_ALL} (first time only)")
        print(f"     {Fore.GREEN}npm start{Style.RESET_ALL}")
        print("\nThe server will run on http://localhost:3000")
        print("Keep the terminal open while using LeetPlusPlus")
        
        # Check if npm is available
        try:
            subprocess.run(['npm', '--version'], capture_output=True, check=True)
        except:
            self._print_warning("\nNode.js/npm not found! Please install Node.js first.")
            print("Download from: https://nodejs.org/")
    
    def do_status(self, arg):
        """Show API server status and statistics
        
        Usage: status
        """
        print(UIStyle.header("System Status", "API server and problem statistics"))
        
        # Check API server
        api_status = "🟢 Running" if self.api.check_api_available() else "🔴 Not running"
        
        print(UIStyle.section_header("API Server"))
        print(f"  Status: {api_status}")
        
        if not self.api.check_api_available():
            print(f"  {Fore.YELLOW}Tip:{Style.RESET_ALL} Run 'api-start' for instructions to start the server")
        
        # Show statistics
        if self.problems_list:
            total_problems = len(self.problems_list)
            by_difficulty = {}
            for p in self.problems_list:
                diff = p.get('difficulty', 'Unknown')
                by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
            
            print(UIStyle.section_header("Problem Statistics"))
            print(f"  Total problems: {total_problems}")
            
            # Sort difficulties for consistent display
            diff_order = ['Easy', 'Medium', 'Hard']
            for diff in diff_order:
                if diff in by_difficulty:
                    # Color code difficulties
                    if diff == 'Easy':
                        color = Fore.GREEN
                    elif diff == 'Medium':
                        color = Fore.YELLOW
                    else:
                        color = Fore.RED
                    print(f"  {color}{diff:<10}{Style.RESET_ALL}: {by_difficulty[diff]:>4}")
            
            # Show any other difficulties
            for diff, count in by_difficulty.items():
                if diff not in diff_order:
                    print(f"  {diff:<10}: {count:>4}")
        
        # Show local solutions
        print(UIStyle.section_header("Local Solutions"))
        problems_dir = self.root_dir / "src" / "Problems"
        if problems_dir.exists():
            solution_files = list(problems_dir.glob("*.h"))
            print(f"  Solution files: {len(solution_files)}")
            
            # Show progress bar
            if self.problems_list:
                progress = UIStyle.progress(len(solution_files), total_problems, "Progress")
                print(f"  {progress}")
        
        print(UIStyle.footer())
    
    def do_random(self, arg):
        """Fetch a random problem
        
        Usage: random [difficulty]
        
        Examples:
            random              # Fetch any random problem
            random easy         # Fetch random easy problem
            random medium       # Fetch random medium problem
        """
        import random
        
        if not self.problems_list:
            self._print_error("No metadata found. Run 'update' first.")
            return
        
        problems = self.problems_list
        
        # Filter by difficulty if specified
        if arg:
            difficulty = arg.strip().lower()
            problems = [p for p in problems if p.get('difficulty', '').lower() == difficulty]
            
            if not problems:
                self._print_error(f"No {difficulty} problems found")
                return
        
        if not problems:
            self._print_error("No problems available")
            return
        
        # Pick random problem
        problem = random.choice(problems)
        problem_id = problem.get('frontendQuestionId')
        
        self._print_info(f"Selected problem #{problem_id}: {problem.get('title')} ({problem.get('difficulty')})")
        
        # Fetch the problem
        self.do_fetch(str(problem_id))
    
    def do_regenerate(self, arg):
        """Regenerate AllProblems.h from existing problem files
        
        Usage: regenerate
        
        This is useful if AllProblems.h gets out of sync or is deleted.
        """
        try:
            from regenerate_all_problems import regenerate_all_problems_header
            self._print_info("Regenerating AllProblems.h...")
            regenerate_all_problems_header()
            self._print_success("AllProblems.h regenerated successfully!", banner=True)
        except Exception as e:
            self._print_error(f"Failed to regenerate AllProblems.h: {e}")
    
    def do_clear(self, arg):
        """Clear the console screen
        
        Usage: clear
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Reload metadata to check current state
        self._load_metadata()
        
        # Create intro dynamically based on current metadata state
        if not self.metadata or len(self.metadata) == 0:
            footer_message = f"{Fore.MAGENTA}First time?{Style.RESET_ALL} Run {Fore.YELLOW}'update'{Style.RESET_ALL} to fetch the problem list from LeetCode."
        else:
            total = len(self.metadata)
            footer_message = f"{Fore.CYAN}ℹ{Style.RESET_ALL}  Loaded {Fore.GREEN}{total}{Style.RESET_ALL} problems from metadata"
        
        intro = f"""{create_gradient_banner()}

{Fore.WHITE}{Style.DIM}A professional C++ development framework for LeetCode{Style.RESET_ALL}
{Fore.BLUE}{'━' * CONSOLE_BANNER_WIDTH}{Style.RESET_ALL}
{Fore.YELLOW}v{APP_VERSION}{Style.RESET_ALL} {Fore.WHITE}|{Style.RESET_ALL} {Fore.CYAN}{APP_GITHUB}{Style.RESET_ALL}

{Fore.YELLOW}Quick Start:{Style.RESET_ALL}
  {Fore.GREEN}fetch <number|slug>{Style.RESET_ALL}  - Fetch a problem (e.g., 'fetch 1' or 'fetch two-sum')
  {Fore.GREEN}list{Style.RESET_ALL}                 - List all problems
  {Fore.GREEN}status{Style.RESET_ALL}               - Show system status
  {Fore.GREEN}help{Style.RESET_ALL}                 - Show all commands
  {Fore.GREEN}exit{Style.RESET_ALL}                 - Leave the console

{footer_message}
"""
        print(intro)
    
    def do_help(self, arg):
        """Show help information
        
        Usage: help [command]
        """
        if arg:
            # Show help for specific command
            try:
                func = getattr(self, 'do_' + arg)
                print(f"\n{Fore.YELLOW}{Style.BRIGHT}{arg.upper()}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}{'━' * 50}{Style.RESET_ALL}")
                if func.__doc__:
                    print(func.__doc__.strip())
                else:
                    print(f"No help available for '{arg}'")
                print()
            except AttributeError:
                self._print_error(f"Unknown command: '{arg}'")
        else:
            # Show general help
            print(UIStyle.header("LeetPlusPlus Console", "Interactive mode for managing LeetCode problems"))
            
            # Commands organized by category
            print(UIStyle.section_header("Problem Management"))
            problem_cmds = [
                ("fetch <number|slug>", "Fetch a problem from LeetCode"),
                ("generate <number>", "Generate solution file for existing problem"),
                ("list", "List all available problems"),
                ("random [difficulty]", "Fetch a random problem"),
                ("regenerate", "Regenerate AllProblems.h")
            ]
            for cmd, desc in problem_cmds:
                print(f"  {Fore.GREEN}{cmd:<20}{Style.RESET_ALL}  {desc}")
            
            print(UIStyle.section_header("System Commands"))
            system_cmds = [
                ("run", "Launch the TUI application"),
                ("update", "Update problem metadata from API"),
                ("status", "Show API server status and statistics"),
                ("api-start", "Instructions to start API server"),
                ("clear", "Clear the console screen")
            ]
            for cmd, desc in system_cmds:
                print(f"  {Fore.GREEN}{cmd:<20}{Style.RESET_ALL}  {desc}")
            
            print(UIStyle.section_header("Console Commands"))
            console_cmds = [
                ("help [command]", "Show help (optionally for specific command)"),
                ("exit / quit", "Exit the console"),
                ("Ctrl+D", "Exit the console")
            ]
            for cmd, desc in console_cmds:
                print(f"  {Fore.GREEN}{cmd:<20}{Style.RESET_ALL}  {desc}")
            
            print(UIStyle.section_header("Examples"))
            examples = [
                ("fetch 1", "Fetch problem #1"),
                ("fetch two-sum", "Fetch by slug"), 
                ("list --difficulty easy", "List easy problems"),
                ("random medium", "Random medium problem"),
                ("help fetch", "Help for fetch command")
            ]
            for example, desc in examples:
                print(UIStyle.command_example(example, desc))
            
            print(UIStyle.footer("Type 'help <command>' for detailed information about a command."))
    
    def do_exit(self, arg):
        """Exit the console
        
        Usage: exit
        """
        print(f"\n{Fore.CYAN}Thanks for using LeetPlusPlus!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Happy coding!{Style.RESET_ALL}\n")
        return True
    
    def do_quit(self, arg):
        """Exit the console
        
        Usage: quit
        """
        return self.do_exit(arg)
    
    def do_EOF(self, arg):
        """Handle Ctrl+D"""
        print()  # New line after ^D
        return self.do_exit(arg)
    
    def emptyline(self):
        """Do nothing on empty line"""
        pass
    
    def default(self, line):
        """Handle unknown commands"""
        self._print_error(f"Unknown command: {line.split()[0]}")
        self._print_info("Type 'help' for available commands")
    
    # Tab completion support
    def complete_fetch(self, text, line, begidx, endidx):
        """Tab completion for fetch command"""
        options = ['daily', '--force', '--interactive']
        return [opt for opt in options if opt.startswith(text)]
    
    def complete_list(self, text, line, begidx, endidx):
        """Tab completion for list command"""
        options = ['--difficulty', '--topic', '--limit', 'easy', 'medium', 'hard']
        return [opt for opt in options if opt.startswith(text)]
    
    def complete_random(self, text, line, begidx, endidx):
        """Tab completion for random command"""
        options = ['easy', 'medium', 'hard']
        return [opt for opt in options if opt.startswith(text)]
    
    def cmdloop(self, intro=None):
        """Override cmdloop to use bordered input"""
        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey+": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            if self.use_bordered_prompt:
                                # Use bordered input for the main prompt
                                line = UIStyle.bordered_input()
                            else:
                                line = input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass


def main():
    """Main entry point for console mode"""
    try:
        # Clear the screen before starting
        os.system('cls' if os.name == 'nt' else 'clear')
        console = LeetPlusPlusConsole()
        console.cmdloop()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main()