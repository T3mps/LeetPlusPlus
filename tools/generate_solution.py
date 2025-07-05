import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from string import Template

STL_TYPES = {
    'vector', 'string', 'map', 'unordered_map', 'set', 'unordered_set',
    'pair', 'queue', 'stack', 'priority_queue', 'deque', 'list'
}

TOPIC_INCLUDES = {
    'Hash Table': '<unordered_map>',
    'Binary Tree': '<queue>',
    'Binary Search': '<algorithm>',
    'Sorting': '<algorithm>',
    'Stack': '<stack>',
    'Queue': '<queue>',
    'Heap': '<queue>',
    'Graph': '<vector>',
    'Dynamic Programming': '<vector>',
    'Linked List': '<iostream>',
}

def add_std_prefix(text):
    if 'std::' in text:
        return text
    
    for stl_type in STL_TYPES:
        pattern = rf'\b(?<!::){stl_type}(?=\s*<|\b)'
        text = re.sub(pattern, f'std::{stl_type}', text)
    
    return text

def to_pascal_case(name):
    if name and name[0].islower():
        return name[0].upper() + name[1:]
    return name

def parse_signature(signature):
    match = re.match(r'^\s*(.+?)\s+(\w+)\s*\((.*)\)\s*$', signature)
    if not match:
        raise ValueError(f"Invalid signature format: {signature}")
    
    raw_return_type = match.group(1).strip()
    method_name = match.group(2).strip()
    raw_params = match.group(3).strip()
    
    return_type = add_std_prefix(raw_return_type)
    method_name = to_pascal_case(method_name)
    
    params = []
    params_str = ""
    
    if raw_params:
        param_parts = []
        current_param = ""
        angle_bracket_count = 0
        
        for char in raw_params:
            if char == '<':
                angle_bracket_count += 1
            elif char == '>':
                angle_bracket_count -= 1
            elif char == ',' and angle_bracket_count == 0:
                param_parts.append(current_param.strip())
                current_param = ""
                continue
            current_param += char
        
        if current_param.strip():
            param_parts.append(current_param.strip())
        
        for param in param_parts:
            param = param.strip()
            param = add_std_prefix(param)
            
            param_match = re.match(r'^(.+?)\s+(\w+)\s*$', param)
            if param_match:
                param_type = param_match.group(1).strip()
                param_name = param_match.group(2).strip()
                params.append({'type': param_type, 'name': param_name})
            else:
                params.append({'type': param, 'name': 'arg' + str(len(params))})
        
        params_str = ', '.join(param_parts)
        params_str = add_std_prefix(params_str)
    
    return {
        'return_type': return_type,
        'method_name': method_name,
        'params_str': params_str,
        'params': params
    }

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

def get_default_return(return_type):
    if 'vector' in return_type:
        return 'return {};'
    elif 'string' in return_type:
        return 'return "";'
    elif return_type == 'int':
        return 'return 0;'
    elif return_type == 'bool':
        return 'return false;'
    elif return_type in ['double', 'float']:
        return 'return 0.0;'
    elif '*' in return_type:
        return 'return nullptr;'
    elif return_type == 'void':
        return '// void return'
    else:
        return 'return {}; // TODO: check return type'

def load_metadata(file_path='../metadata.json'):
    script_dir = Path(__file__).parent
    metadata_path = script_dir / file_path
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(metadata, file_path='../metadata.json'):
    script_dir = Path(__file__).parent
    metadata_path = script_dir / file_path
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

def generate_solution(problem_number, title, signature, difficulty='Medium', topics=None, companies=None):
    sig_data = parse_signature(signature)
    
    includes = get_includes(signature, topics or [])
    includes_str = '\n'.join(f'#include {inc}' for inc in includes)
    
    class_name = ''.join(word.capitalize() for word in re.findall(r'\w+', title))
    
    filename = f"{problem_number}_{'_'.join(word.capitalize() for word in re.findall(r'\w+', title))}.h"
    
    template_path = Path(__file__).parent / 'template.h'
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    template = Template(template_path.read_text())
    
    test_helpers_include = ""
    if ('Tree' in str(topics) or 'TreeNode' in signature or 
        'LinkedList' in str(topics) or 'ListNode' in signature):
        test_helpers_include = '\n#include "../Common/TestHelpers.h"'
    
    content = template.substitute(
        number=problem_number,
        title=title,
        difficulty=difficulty,
        topics=', '.join(topics or []),
        companies=', '.join(companies or []) or 'Unknown',
        includes=includes_str,
        test_helpers_include=test_helpers_include,
        return_type=sig_data['return_type'],
        method_name=sig_data['method_name'],
        params=sig_data['params_str'],
        default_return=get_default_return(sig_data['return_type'])
    )
    
    problems_dir = Path('src/Problems')
    problems_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = problems_dir / filename
    if file_path.exists():
        raise ValueError(f"Problem {problem_number} already exists")
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    update_main_cpp(problem_number, f"Problems/{filename}")
    
    metadata = load_metadata()
    metadata[str(problem_number)] = {
        'title': title,
        'signature': signature,
        'difficulty': difficulty,
        'topics': topics or [],
        'companies': companies or [],
        'created': datetime.now().isoformat(),
        'filename': filename
    }
    save_metadata(metadata)
    
    return filename

def update_main_cpp(problem_number, include_path):
    main_path = Path('src/main.cpp')
    if not main_path.exists():
        print("Warning: main.cpp not found")
        return
    
    content = main_path.read_text()
    include_line = f'#include "{include_path}"'
    
    if include_line in content:
        return
    
    lines = content.split('\n')
    insert_idx = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('#include'):
            insert_idx = i + 1
    
    lines.insert(insert_idx, include_line)
    main_path.write_text('\n'.join(lines))

def list_problems():
    metadata = load_metadata()
    if not metadata:
        print("No problems found.")
        return
    
    print("\nLeetCode Problems:")
    print("=" * 60)
    for num in sorted(metadata.keys(), key=int):
        prob = metadata[num]
        print(f"#{num}: {prob['title']} ({prob.get('difficulty', 'Medium')})")
        if prob.get('topics'):
            print(f"      Topics: {', '.join(prob['topics'])}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='LeetCode C++ Solution Generator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    new_parser = subparsers.add_parser('new', help='Create new problem')
    new_parser.add_argument('number', type=int, help='Problem number')
    new_parser.add_argument('-t', '--title', required=True, help='Problem title')
    new_parser.add_argument('-s', '--signature', required=True, help='Method signature')
    new_parser.add_argument('-d', '--difficulty', choices=['Easy', 'Medium', 'Hard'], 
                          default='Medium', help='Difficulty')
    new_parser.add_argument('-T', '--topics', nargs='+', help='Topics')
    new_parser.add_argument('-c', '--companies', nargs='+', help='Companies')
    
    subparsers.add_parser('list', help='List all problems')
    
    args = parser.parse_args()
    
    if args.command == 'new':
        try:
            filename = generate_solution(
                args.number, args.title, args.signature,
                args.difficulty, args.topics, args.companies
            )
            print(f"✓ Created: {filename}")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'list':
        list_problems()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()