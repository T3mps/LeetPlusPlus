import argparse
import re
import sys
import subprocess
import platform
from pathlib import Path
from datetime import datetime
from string import Template

sys.path.append(str(Path(__file__).parent))
from common import ColorPrinter, MetadataManager, ensure_directory, Fore, Style
from config import (
    STL_TYPES, TOPIC_INCLUDES, PROBLEMS_DIR, ALL_PROBLEMS_HEADER,
    TEMPLATE_FILE, METADATA_FILE, PROJECT_ROOT
)
from cpp_types import CppTypeConverter
from test_parser import TestCaseParser
from ui_style import UIStyle

def parse_signature(signature):
    sig_data = CppTypeConverter.parse_signature(signature)
    if not sig_data:
        raise ValueError(f"Invalid signature format: {signature}")
    return sig_data

def get_includes(signature, topics):
    includes = set(['<iostream>'])
    
    if 'ListNode' in signature or 'LinkedList' in str(topics):
        includes.add('"../Common/Structures.h"')
    if 'TreeNode' in signature or 'Tree' in str(topics):
        includes.add('"../Common/Structures.h"')
    
    if 'vector' in signature:
        includes.add('<vector>')
    if 'string' in signature:
        includes.add('<string>')
    if 'map' in signature:
        includes.add('<map>' if 'unordered' not in signature else '<unordered_map>')
    if 'set' in signature:
        includes.add('<set>' if 'unordered' not in signature else '<unordered_set>')
    if 'queue' in signature:
        includes.add('<queue>')
    if 'stack' in signature:
        includes.add('<stack>')
    if 'pair' in signature:
        includes.add('<utility>')
    
    for topic in topics:
        if topic in TOPIC_INCLUDES:
            includes.add(TOPIC_INCLUDES[topic])
    
    system_includes = sorted([inc for inc in includes if inc.startswith('<')])
    local_includes = sorted([inc for inc in includes if inc.startswith('"')])
    return system_includes + local_includes

# Default return function moved to cpp_types.py

# Test value parsing moved to test_parser.py
parse_test_value = TestCaseParser.parse_value

def regenerate_vs_project():
    """Regenerate Visual Studio project files if on Windows and premake5 is available"""
    if platform.system() != 'Windows':
        return
    
    try:
        # Check if premake5 is available
        result = subprocess.run(['premake5', '--version'], 
                              capture_output=True, 
                              text=True, 
                              shell=True)
        
        if result.returncode == 0:
            # Run premake5 vs2022 to regenerate project files
            result = subprocess.run(['premake5', 'vs2022'], 
                                  cwd=PROJECT_ROOT,
                                  capture_output=True,
                                  text=True,
                                  shell=True)
            
            if result.returncode == 0:
                ColorPrinter.info("✓ VS2022 project updated")
    except Exception:
        # Silently fail if premake5 is not available
        pass

def generate_solution(problem_number, title, signature, difficulty='Medium', topics=None, companies=None, test_cases_data=None, force=False):
    sig_data = parse_signature(signature)
    
    includes = get_includes(signature, topics or [])
    includes_str = '\n'.join(f'#include {inc}' for inc in includes)
    
    class_name = ''.join(word.capitalize() for word in re.findall(r'\w+', title))
    
    title_words = re.findall(r'\w+', title)
    filename = f"{problem_number}_{'_'.join(word.capitalize() for word in title_words)}.h"
    
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"Template file not found: {TEMPLATE_FILE}")
    
    template = Template(TEMPLATE_FILE.read_text(encoding='utf-8'))
    
    test_helpers_include = ""
    if ('Tree' in str(topics) or 'TreeNode' in signature or 
        'LinkedList' in str(topics) or 'ListNode' in signature):
        test_helpers_include = '\n#include "../Common/TestHelpers.h"'
    
    # Generate test cases
    test_cases_code = TestCaseParser.generate_test_code(test_cases_data, sig_data, topics)
    
    # Create a custom template for safe substitution
    template_dict = {
        'number': problem_number,
        'title': title,
        'difficulty': difficulty,
        'topics': ', '.join(topics or []),
        'companies': ', '.join(companies or []) or 'Unknown',
        'includes': includes_str,
        'test_helpers_include': test_helpers_include,
        'return_type': sig_data['return_type'],
        'method_name': sig_data['method_name'],
        'params': sig_data['params_str'],
        'default_return': CppTypeConverter.get_default_return(sig_data['return_type']),
        'test_cases': test_cases_code
    }
    
    content = template.safe_substitute(**template_dict)
    
    ensure_directory(PROBLEMS_DIR)
    
    file_path = PROBLEMS_DIR / filename
    if file_path.exists() and not force:
        raise ValueError(f"Problem {problem_number} already exists")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update AllProblems.h instead of main.cpp
    update_all_problems_header(problem_number, filename)
    
    metadata_manager = MetadataManager()
    metadata = metadata_manager.load()
    metadata[str(problem_number)] = {
        'title': title,
        'signature': signature,
        'difficulty': difficulty,
        'topics': topics or [],
        'companies': companies or [],
        'created': datetime.now().isoformat(),
        'filename': filename
    }
    metadata_manager.save(metadata)
    
    # Regenerate VS project files if on Windows
    regenerate_vs_project()
    
    return filename

def update_all_problems_header(problem_number, problem_filename):
    """Update AllProblems.h to include the new problem header"""
    all_problems_path = ALL_PROBLEMS_HEADER
    
    # Create the header if it doesn't exist
    if not all_problems_path.exists():
        print("Creating AllProblems.h...")
        all_problems_path.parent.mkdir(parents=True, exist_ok=True)
        header_content = """#pragma once

// This file is automatically generated by LeetPlusPlus
// It includes all problem solution headers

"""
        all_problems_path.write_text(header_content, encoding='utf-8')
    
    # Read current content
    content = all_problems_path.read_text(encoding='utf-8')
    
    # Check if this problem is already included
    include_line = f'#include "{problem_filename}"'
    if include_line in content:
        return
    
    # Find all existing includes and sort them
    lines = content.split('\n')
    header_lines = []
    include_lines = []
    other_lines = []
    
    for line in lines:
        if line.strip().startswith('#pragma') or line.strip().startswith('//'):
            header_lines.append(line)
        elif line.strip().startswith('#include') and '_' in line and '.h' in line:
            # This is a problem include
            include_lines.append(line)
        else:
            other_lines.append(line)
    
    # Add the new include
    include_lines.append(include_line)
    
    # Sort includes by problem number
    def get_problem_number(include_line):
        import re
        match = re.search(r'#include\s+"(\d+)_', include_line)
        return int(match.group(1)) if match else 0
    
    include_lines.sort(key=get_problem_number)
    
    # Reconstruct the file
    new_content = []
    new_content.extend(header_lines)
    if header_lines and include_lines:
        new_content.append('')  # Empty line between header and includes
    new_content.extend(include_lines)
    new_content.extend(other_lines)
    
    # Write back
    all_problems_path.write_text('\n'.join(new_content), encoding='utf-8')
    ColorPrinter.success(f"Updated AllProblems.h with {problem_filename}")

def list_problems():
    metadata_manager = MetadataManager()
    metadata = metadata_manager.load()
    if not metadata:
        ColorPrinter.info("No problems found.")
        return
    
    print(UIStyle.header("LeetCode Problems", f"Total: {len(metadata)} problems"))
    
    for num in sorted(metadata.keys(), key=int):
        prob = metadata[num]
        
        # Color code difficulty
        diff = prob.get('difficulty', 'Medium')
        if diff == 'Easy':
            diff_color = Fore.GREEN
        elif diff == 'Medium':
            diff_color = Fore.YELLOW
        else:
            diff_color = Fore.RED
        
        print(f"\n  {Fore.CYAN}#{num}:{Style.RESET_ALL} {prob['title']} {diff_color}({diff}){Style.RESET_ALL}")
        if prob.get('topics'):
            print(f"       Topics: {', '.join(prob['topics'])}")
    
    print(UIStyle.footer())

def interactive_mode():
    """Interactive mode for creating problems"""
    print(UIStyle.header("LeetCode Problem Generator", "Interactive Mode"))
    
    # Load metadata to suggest next problem number
    metadata_manager = MetadataManager()
    metadata = metadata_manager.load()
    existing_numbers = [int(num) for num in metadata.keys()] if metadata else []
    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    
    # Problem number
    print()
    number_input = UIStyle.bordered_input(f"Problem number [{next_number}]:").strip()
    problem_number = int(number_input) if number_input else next_number
    
    # Check if problem exists
    if str(problem_number) in metadata:
        print(f"⚠️  Problem #{problem_number} already exists: {metadata[str(problem_number)]['title']}")
        if UIStyle.bordered_input("Overwrite? (y/N):").lower() != 'y':
            return
    
    # Title
    title = UIStyle.bordered_input("Problem title:").strip()
    if not title:
        ColorPrinter.error("Title is required!")
        return
    
    # Show signature examples
    print(UIStyle.section_header("Example Signatures"))
    print("  • vector<int> twoSum(vector<int>& nums, int target)")
    print("  • ListNode* reverseList(ListNode* head)")
    print("  • bool isValid(string s)")
    print("  • int maxDepth(TreeNode* root)")
    
    print()
    signature = UIStyle.bordered_input("Method signature:").strip()
    if not signature:
        ColorPrinter.error("Signature is required!")
        return
    
    # Difficulty
    print("\n🎚️  Difficulty levels: Easy, Medium, Hard")
    diff_input = UIStyle.bordered_input("Difficulty [Medium]:").strip()
    difficulty = diff_input if diff_input in ['Easy', 'Medium', 'Hard'] else 'Medium'
    
    # Topics
    print(UIStyle.section_header("Common Topics"))
    print("  • Array, Hash Table, Two Pointers, String, Binary Search")
    print("  • Stack, Queue, Linked List, Tree, Graph, DP, Greedy")
    print("  • Math, Bit Manipulation, Recursion, Backtracking")
    
    print()
    topics_input = UIStyle.bordered_input("Topics (comma-separated):").strip()
    topics = [t.strip() for t in topics_input.split(',')] if topics_input else []
    
    # Companies (optional)
    companies_input = UIStyle.bordered_input("Companies (comma-separated) [optional]:").strip()
    companies = [c.strip() for c in companies_input.split(',')] if companies_input else []
    
    # Confirm
    print(UIStyle.section_header("Summary"))
    print(f"  Number: #{problem_number}")
    print(f"  Title: {title}")
    print(f"  Signature: {signature}")
    print(f"  Difficulty: {difficulty}")
    print(f"  Topics: {', '.join(topics) if topics else 'None'}")
    print(f"  Companies: {', '.join(companies) if companies else 'None'}")
    
    print()
    if UIStyle.bordered_input("Generate problem? (Y/n):").lower() in ['', 'y']:
        try:
            filename = generate_solution(
                problem_number, title, signature,
                difficulty, topics, companies
            )
            ColorPrinter.success(f"Successfully created: {filename}")
            ColorPrinter.info(f"Location: src/Problems/{filename}")
        except Exception as e:
            ColorPrinter.error(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='LeetCode C++ Solution Generator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    new_parser = subparsers.add_parser('new', help='Create new problem')
    new_parser.add_argument('number', type=int, nargs='?', help='Problem number')
    new_parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    new_parser.add_argument('-t', '--title', help='Problem title')
    new_parser.add_argument('-s', '--signature', help='Method signature')
    new_parser.add_argument('-d', '--difficulty', choices=['Easy', 'Medium', 'Hard'], 
                          default='Medium', help='Difficulty')
    new_parser.add_argument('-T', '--topics', nargs='+', help='Topics')
    new_parser.add_argument('-c', '--companies', nargs='+', help='Companies')
    
    subparsers.add_parser('list', help='List all problems')
    
    args = parser.parse_args()
    
    if args.command == 'new':
        # Use interactive mode if -i flag or if required args are missing
        if args.interactive or not (args.number and args.title and args.signature):
            interactive_mode()
        else:
            try:
                filename = generate_solution(
                    args.number, args.title, args.signature,
                    args.difficulty, args.topics, args.companies
                )
                ColorPrinter.success(f"Created: {filename}")
            except Exception as e:
                ColorPrinter.error(f"Error: {e}")
                sys.exit(1)
    
    elif args.command == 'list':
        list_problems()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()