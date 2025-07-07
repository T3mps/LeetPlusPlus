#!/usr/bin/env python3
"""
LeetCode Problem Fetcher (Simple Version) - Uses built-in urllib instead of requests
Integrates with AlfaLeetCode API to fetch problems
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
import sys

sys.path.append(str(Path(__file__).parent))
from generate_solution import generate_solution
from common import ColorPrinter, APIServerManager, MetadataManager, HTTPClient
from config import API_BASE_URL, BATCH_FETCH_DELAY
from cpp_types import CppTypeConverter
from ui_style import UIStyle

class LeetCodeAPI:
    """Interface to AlfaLeetCode API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.api_manager = APIServerManager(base_url)
        self.http_client = HTTPClient()
        
    def check_api_available(self) -> bool:
        """Check if API server is running"""
        return self.api_manager.check_available()
    
    def fetch_problem(self, title_slug: str) -> Optional[Dict]:
        """Fetch a specific problem by title slug"""
        return self.http_client.get_with_params(
            f"{self.base_url}/select",
            {"titleSlug": title_slug}
        )
    
    def fetch_daily(self) -> Optional[Dict]:
        """Fetch the daily challenge problem"""
        return self.http_client.get(f"{self.base_url}/daily")
    
    def fetch_problems(self, limit: int = 20, skip: int = 0, 
                      difficulty: Optional[str] = None, 
                      tags: Optional[List[str]] = None) -> Optional[List[Dict]]:
        """Fetch a list of problems with filters"""
        params = {"limit": str(limit), "skip": str(skip)}
        if difficulty:
            params["difficulty"] = difficulty.upper()
        if tags:
            params["tags"] = "+".join(tags)
        
        return self.http_client.get_with_params(
            f"{self.base_url}/problems",
            params
        )

# Type conversion functions moved to cpp_types.py

def extract_cpp_signature(problem_data: Dict) -> Optional[str]:
    """Extract C++ function signature from problem data"""
    try:
        # First try to get from code snippets
        cpp_snippet = None
        code_snippets = problem_data.get("codeSnippets", [])
        
        
        for snippet in code_snippets:
            if snippet.get("langSlug") == "cpp":
                cpp_snippet = snippet.get("code", "")
                break
        
        if not cpp_snippet:
            print("No C++ code snippet found in problem data")
            return None
        
        # Extract function signature from snippet
        # Look for class Solution and the public method
        class_match = re.search(r'class\s+Solution\s*\{[^}]*public:\s*([^}]+)\}', cpp_snippet, re.DOTALL)
        if class_match:
            methods_section = class_match.group(1)
            # Find the first complete function signature
            # Enhanced regex to handle:
            # - Multiple pointers/references: **, ***, &
            # - Type modifiers: const, unsigned, etc.
            # - Complex templates: vector<pair<int,int>>
            # - Spaces in various positions
            
            # This regex captures:
            # Group 1: Full return type (including const, templates, etc.)
            # Group 2: Pointers and references (*, **, &, etc.)
            # Group 3: Method name
            # Group 4: Parameters
            # Enhanced to handle nested templates like vector<pair<int, int>>
            pattern = r'((?:(?:const|unsigned|signed|long|short|static|virtual)\s+)*\w+(?:\s*::\s*\w+)*(?:\s*<(?:[^<>]|<[^>]*>)*>)?(?:\s+\w+)*?)\s*((?:\*\s*)*(?:&\s*)?)\s*(\w+)\s*\(([^)]*)\)'
            
            full_match = re.search(pattern, methods_section)
            if full_match:
                return_type = full_match.group(1).strip()
                pointers_refs = full_match.group(2).strip()
                method_name = full_match.group(3).strip()
                params = full_match.group(4).strip()
                
                # Normalize the return type
                return_type = CppTypeConverter.normalize_cpp_type(return_type)
                
                # Combine return type with pointers/references
                if pointers_refs:
                    # Normalize pointer/reference spacing
                    pointers_refs = re.sub(r'\s+', '', pointers_refs)
                    return_type = f"{return_type}{pointers_refs}"
                
                # Convert method name to PascalCase
                method_name = CppTypeConverter.to_pascal_case(method_name)
                
                # Normalize parameters
                if params:
                    # Split parameters and normalize each
                    param_list = []
                    # Simple parameter splitting (doesn't handle nested templates perfectly)
                    for param in re.split(r',(?![^<>]*>)', params):
                        param = param.strip()
                        if param:
                            param_list.append(CppTypeConverter.normalize_cpp_type(param))
                    params = ', '.join(param_list)
                
                return f"{return_type} {method_name}({params})"
        
        # Fallback: try to parse from metadata
        if "metaData" in problem_data and problem_data["metaData"]:
            metadata = json.loads(problem_data["metaData"])
            return_type = parse_leetcode_type_to_cpp(metadata["return"]["type"])
            method_name = to_pascal_case(metadata["name"])
            
            params = []
            for param in metadata.get("params", []):
                param_type = parse_leetcode_type_to_cpp(param["type"])
                param_name = param["name"]
                # Add reference for containers
                if "vector" in param_type and "**" not in param_type:
                    param_type += "&"
                # Normalize the parameter type
                param_str = normalize_cpp_type(f"{param_type} {param_name}")
                params.append(param_str)
            
            # Normalize return type
            return_type = normalize_cpp_type(return_type)
            
            return f"{return_type} {method_name}({', '.join(params)})"
    
    except Exception as e:
        print(f"Error extracting signature: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def parse_topics_from_api(topic_tags: List[Dict]) -> List[str]:
    """Extract topic names from API response"""
    return [tag["name"] for tag in topic_tags]

def extract_test_examples(problem_data: Dict) -> List[Dict]:
    """Extract complete input/output pairs from problem content"""
    # Try different field names where content might be stored
    content = problem_data.get('content', '') or problem_data.get('question', '') or problem_data.get('questionContent', '')
    examples = []
    
    # Find all <pre> blocks which typically contain examples
    pre_blocks = re.findall(r'<pre>(.*?)</pre>', content, re.DOTALL | re.IGNORECASE)
    
    for block in pre_blocks:
        # Clean the block
        block = block.strip()
        
        # Try to extract Input and Output from the block
        # Pattern for Input/Output in various formats
        patterns = [
            # Pattern 1: <strong>Input:</strong> ... <strong>Output:</strong> ...
            (r'<strong>Input:</strong>\s*([^<]+?)\s*(?:<br\s*/?>|\n)\s*<strong>Output:</strong>\s*([^<]+?)(?:\s*(?:<br\s*/?>|\n|$))', re.IGNORECASE),
            # Pattern 2: Input: ... Output: ... (plain text)
            (r'Input:\s*([^\n]+?)\s*\n\s*Output:\s*([^\n]+?)(?:\s*(?:\n|$))', 0),
            # Pattern 3: <b>Input:</b> ... <b>Output:</b> ...
            (r'<b>Input:</b>\s*([^<]+?)\s*(?:<br\s*/?>|\n)\s*<b>Output:</b>\s*([^<]+?)(?:\s*(?:<br\s*/?>|\n|$))', re.IGNORECASE),
        ]
        
        for pattern, flags in patterns:
            match = re.search(pattern, block, flags)
            if match:
                input_str = match.group(1).strip()
                output_str = match.group(2).strip()
                
                # Parse the input string to separate multiple inputs
                inputs = parse_input_string(input_str)
                
                # Parse output and convert to C++ format if needed
                output = parse_output_string(output_str)
                
                if inputs and output:
                    examples.append({
                        'inputs': inputs,
                        'output': output
                    })
                break
    
    return examples

def parse_input_string(input_str: str) -> List[str]:
    """Parse input string into individual parameter values"""
    # Remove any HTML tags
    input_str = re.sub(r'<[^>]+>', '', input_str)
    
    # Split by common separators
    # Handle cases like: "nums = [1,2,3], target = 9"
    parts = []
    
    # First try to split by commas that are not inside brackets
    current = ''
    bracket_depth = 0
    in_quotes = False
    
    for char in input_str:
        if char == '"' and (not current or current[-1] != '\\'):
            in_quotes = not in_quotes
        elif not in_quotes:
            if char in '[{(':
                bracket_depth += 1
            elif char in ']})':
                bracket_depth -= 1
            elif char == ',' and bracket_depth == 0:
                if current.strip():
                    parts.append(current.strip())
                current = ''
                continue
        current += char
    
    if current.strip():
        parts.append(current.strip())
    
    # Extract just the values from "name = value" format
    values = []
    for part in parts:
        if '=' in part:
            value = part.split('=', 1)[1].strip()
            values.append(value)
        else:
            values.append(part)
    
    return values

def parse_output_string(output_str: str) -> str:
    """Parse output string and convert to C++ format"""
    # Remove any HTML tags
    output_str = re.sub(r'<[^>]+>', '', output_str)
    output_str = output_str.strip()
    
    # Convert array notation [1,2,3] to {1,2,3}
    if output_str.startswith('[') and output_str.endswith(']'):
        # Handle nested arrays
        if '[[' in output_str:
            output_str = output_str.replace('[', '{').replace(']', '}')
        else:
            # Single array
            output_str = '{' + output_str[1:-1] + '}'
    
    # Handle string outputs - ensure they're quoted
    elif not (output_str.startswith('"') and output_str.endswith('"')) and \
         not output_str.replace('.', '').replace('-', '').isdigit() and \
         output_str not in ['true', 'false', 'null', 'nullptr']:
        # It's likely a string that needs quotes
        if not any(char in output_str for char in ['{', '}', '[', ']']):
            output_str = f'"{output_str}"'
    
    return output_str

def extract_expected_outputs(problem_data: Dict) -> List[str]:
    """Legacy function - now extracts from complete examples"""
    examples = extract_test_examples(problem_data)
    return [ex['output'] for ex in examples]

# API server management moved to common.py

def interactive_fetch():
    """Interactive mode for fetching problems"""
    api = LeetCodeAPI()
    
    # Check if API is available, start if not
    if not api.api_manager.ensure_running():
        ColorPrinter.warning("API server not available.")
        print("\nWould you like to:")
        print("1. Continue without API (manual entry only)")
        print("2. Exit")
        
        print()
        choice = UIStyle.bordered_input("Your choice (1-2):").strip()
        
        if choice == "1":
            ColorPrinter.info("Continuing with manual entry mode...")
            manual_entry_mode()
            return
        else:
            return
    
    try:
        while True:
            print("\n[LeetCode Problem Fetcher]")
            print("="*40)
            print("1. Fetch specific problem")
            print("2. Fetch daily challenge")
            print("3. Batch import problems")
            print("4. Exit")
            
            print()
            choice = UIStyle.bordered_input("Your choice (1-4):").strip()
            
            if choice == "1":
                fetch_specific_problem(api)
            elif choice == "2":
                fetch_daily_challenge(api)
            elif choice == "3":
                batch_import_problems(api)
            elif choice == "4":
                break
            else:
                print("Invalid choice!")
    
    finally:
        if server_process:
            stop_api_server(server_process)

def manual_entry_mode():
    """Fallback mode for manual problem entry"""
    print("\nManual Problem Entry Mode")
    print("="*40)
    
    # Import the interactive mode from generate_solution
    from generate_solution import interactive_mode
    interactive_mode()

def fetch_specific_problem(api: LeetCodeAPI):
    """Fetch and generate a specific problem"""
    print()
    title_slug = UIStyle.bordered_input("Enter problem slug (e.g., two-sum):").strip()
    
    if not title_slug:
        print("No slug provided!")
        return
    
    print(f"\nFetching problem: {title_slug}...")
    problem_data = api.fetch_problem(title_slug)
    
    if not problem_data:
        ColorPrinter.error("Failed to fetch problem!")
        return
    
    generate_from_api_data(problem_data, interactive_mode=True)

def fetch_daily_challenge(api: LeetCodeAPI):
    """Fetch and generate daily challenge"""
    print("\nFetching daily challenge...")
    daily_data = api.fetch_daily()
    
    if not daily_data:
        ColorPrinter.error("Failed to fetch daily challenge!")
        return
    
    # The daily endpoint returns limited data, we need to fetch full details
    title_slug = daily_data.get("titleSlug")
    title = daily_data.get("questionTitle", "Unknown")
    
    if title_slug:
        print(f"Found daily challenge: {title}")
        
        # Fetch the complete problem data
        problem_data = api.fetch_problem(title_slug)
        if problem_data:
            generate_from_api_data(problem_data, interactive_mode=True)
        else:
            print(f"Failed to fetch full details for problem: {title_slug}")
    else:
        print("Could not find problem slug in daily challenge data")
        print("Debug - Response:", daily_data)

def batch_import_problems(api: LeetCodeAPI):
    """Batch import multiple problems"""
    print("\nBatch Import Problems")
    print("-"*20)
    
    limit = UIStyle.bordered_input("Number of problems to import [10]:").strip() or "10"
    difficulty = UIStyle.bordered_input("Difficulty (Easy/Medium/Hard/All) [All]:").strip() or None
    tags_input = UIStyle.bordered_input("Tags (comma-separated) []:").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else None
    
    if difficulty and difficulty.lower() == "all":
        difficulty = None
    
    print(f"\nFetching {limit} problems...")
    problems = api.fetch_problems(limit=int(limit), difficulty=difficulty, tags=tags)
    
    if not problems:
        ColorPrinter.error("Failed to fetch problems!")
        return
    
    print(f"\nFound {len(problems)} problems.")
    if UIStyle.bordered_input("Generate all? (y/n):").lower() != 'y':
        return
    
    success_count = 0
    skipped_paid = 0
    for i, problem in enumerate(problems):
        # Skip paid problems in batch import
        if problem.get("isPaidOnly", False):
            skipped_paid += 1
            continue
            
        print(f"\n[{i+1}/{len(problems)}] Processing: {problem.get('title', 'Unknown')}...")
        try:
            # Fetch full problem details
            if "titleSlug" in problem:
                full_problem = api.fetch_problem(problem["titleSlug"])
                if full_problem:
                    if generate_from_api_data(full_problem, interactive_mode=True):
                        success_count += 1
                    time.sleep(BATCH_FETCH_DELAY)  # Be nice to the API
        except Exception as e:
            print(f"Error processing problem: {e}")
    
    print(f"\nSuccessfully generated {success_count}/{len(problems)} problems!")
    if skipped_paid > 0:
        print(f"Skipped {skipped_paid} paid-only problems")

def generate_from_api_data(problem_data: Dict, interactive_mode: bool = True, force: bool = False) -> bool:
    """Generate a problem file from API data"""
    try:
        # Check if problem is paid-only
        if problem_data.get("isPaidOnly", False):
            problem_id = problem_data.get("questionFrontendId", problem_data.get("questionId", "0"))
            title = problem_data.get("title", problem_data.get("questionTitle", "Unknown Problem"))
            ColorPrinter.error(f"Problem #{problem_id}: {title} is a paid-only problem!")
            ColorPrinter.info("Paid problems cannot be fetched. Please choose a free problem.")
            return False
        
        # Use the original generator
        from generate_solution import generate_solution
        
        # Extract problem details
        problem_id = problem_data.get("questionFrontendId", problem_data.get("questionId", "0"))
        title = problem_data.get("title", problem_data.get("questionTitle", "Unknown Problem"))
        difficulty = problem_data.get("difficulty", "Medium")
        topics = parse_topics_from_api(problem_data.get("topicTags", []))
        
        # Extract signature
        signature = extract_cpp_signature(problem_data)
        if not signature:
            ColorPrinter.error(f"Could not extract C++ signature for problem #{problem_id}: {title}")
            if interactive_mode:
                print("Please enter signature manually or skip (press Enter to skip):")
                signature = UIStyle.bordered_input().strip()
                if not signature:
                    return False
            else:
                print("Skipping problem due to signature extraction failure.")
                print("This is often caused by unusual formatting in LeetCode's C++ template.")
                return False
        
        # Use UIStyle for problem display
        print(UIStyle.header(f"Problem #{problem_id}: {title}", f"Difficulty: {difficulty}"))
        
        print(UIStyle.section_header("Details"))
        print(f"  Topics: {', '.join(topics) if topics else 'None'}")
        print(f"  Signature: {signature}")
        
        # Prepare test case data
        test_examples = extract_test_examples(problem_data)
        test_cases_data = {
            'exampleTestcases': problem_data.get('exampleTestcases', ''),
            'signature': signature,  # Pass signature for parameter parsing
            'expectedOutputs': [ex['output'] for ex in test_examples],
            'testExamples': test_examples  # Pass complete examples
        }
        
        # Generate the solution file
        filename = generate_solution(
            problem_number=int(problem_id),
            title=title,
            signature=signature,
            difficulty=difficulty,
            topics=topics,
            companies=[],  # API doesn't provide company info
            test_cases_data=test_cases_data,
            force=force
        )
        
        print(UIStyle.success_banner(f"Successfully generated: {filename}"))
        
        return True
        
    except ValueError as e:
        if "already exists" in str(e):
            ColorPrinter.warning(str(e))
            ColorPrinter.info("Use --force flag to overwrite existing solution")
            ColorPrinter.info("Example: lpp fetch 1 --force")
            return False
        else:
            print(f"Error generating problem: {e}")
            import traceback
            traceback.print_exc()
            return False
    except Exception as e:
        print(f"Error generating problem: {e}")
        import traceback
        traceback.print_exc()
        return False

def fetch_by_number(api: LeetCodeAPI, problem_number: str):
    """Fetch a problem by number using metadata"""
    metadata_manager = MetadataManager()
    problem_info = metadata_manager.get_problem_by_id(problem_number)
    
    if not problem_info:
        ColorPrinter.error(f"Problem #{problem_number} not found in metadata")
        print("This could be because:")
        print("  1. The problem number is invalid")
        print("  2. It's a paid-only problem (excluded from metadata)")
        print("  3. Metadata needs updating: run 'lpp update'")
        return
    
    slug = problem_info.get('titleSlug')
    
    if not slug:
        ColorPrinter.error(f"No slug found for problem #{problem_number}")
        return
    
    ColorPrinter.info(f"Fetching problem #{problem_number}: {problem_info.get('title', 'Unknown')}")
    problem_data = api.fetch_problem(slug)
    
    if problem_data:
        generate_from_api_data(problem_data, interactive_mode=False)

# Server auto-start functionality moved to common.py

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1]
        api = LeetCodeAPI()
        
        # Auto-start server if needed for commands that require it
        if command in ["fetch", "daily"]:
            api.api_manager.ensure_running()
        
        if command == "fetch":
            if len(sys.argv) < 3:
                print("Usage: leetcode_fetcher_simple.py fetch <title-slug>")
                sys.exit(1)
            
            slug = sys.argv[2]
            # Check if it's a number
            if slug.isdigit():
                fetch_by_number(api, slug)
            else:
                problem_data = api.fetch_problem(slug)
                if problem_data:
                    generate_from_api_data(problem_data)
        
        elif command == "daily":
            problem_data = api.fetch_daily()
            if problem_data:
                generate_from_api_data(problem_data)
        
        else:
            print(f"Unknown command: {command}")
            print("Available commands: fetch, daily")
            sys.exit(1)
    
    else:
        # Interactive mode
        interactive_fetch()

if __name__ == "__main__":
    main()