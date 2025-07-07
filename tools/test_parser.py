#!/usr/bin/env python3
"""
Test case parsing utilities for LeetPlusPlus
Simplifies the generation of C++ test code from LeetCode examples
"""

import re
from typing import List, Dict, Optional, Any
from cpp_types import CppTypeConverter


class TestCaseParser:
    """Handles parsing and generation of test cases"""
    
    @staticmethod
    def parse_value(value_str: str, param_type: str) -> str:
        """Convert a string representation of a value to C++ code"""
        value_str = value_str.strip()
        
        # Special handling for pointer types
        if 'ListNode' in param_type or 'TreeNode' in param_type:
            return value_str  # Return as-is, will be handled in code generation
        
        # Handle vector types
        if 'vector' in param_type:
            if value_str.startswith('[') and value_str.endswith(']'):
                # Convert [1,2,3] to {1,2,3}
                return value_str.replace('[', '{').replace(']', '}')
            return value_str
        
        # Handle string types
        if 'string' in param_type:
            if not (value_str.startswith('"') and value_str.endswith('"')):
                return f'"{value_str}"'
            return value_str
        
        # Handle boolean
        if param_type == 'bool':
            return 'true' if value_str.lower() == 'true' else 'false'
        
        # Handle char
        if param_type == 'char':
            if not (value_str.startswith("'") and value_str.endswith("'")):
                return f"'{value_str}'"
            return value_str
        
        # Default: return as-is (int, double, etc.)
        return value_str
    
    @staticmethod
    def generate_test_code(test_cases_data: Dict, sig_data: Dict, topics: List[str] = None) -> str:
        """Generate C++ test code from test case data"""
        if not test_cases_data:
            return TestCaseParser._generate_default_test_comment(sig_data)
        
        # Parse test cases
        test_cases = TestCaseParser._parse_test_cases(test_cases_data, sig_data)
        if not test_cases:
            return TestCaseParser._generate_default_test_comment(sig_data)
        
        # Generate code
        code_lines = []
        for test in test_cases:
            TestCaseParser._generate_single_test(test, sig_data, code_lines, topics)
        
        # Remove last empty line if present
        if code_lines and code_lines[-1] == '':
            code_lines.pop()
        
        return '\n'.join(code_lines)
    
    @staticmethod
    def _parse_test_cases(test_cases_data: Dict, sig_data: Dict) -> List[Dict]:
        """Parse test cases from various formats"""
        # Try complete examples first
        test_examples = test_cases_data.get('testExamples', [])
        if test_examples:
            return TestCaseParser._parse_complete_examples(test_examples, sig_data)
        
        # Fall back to parsing from example testcases
        example_testcases = test_cases_data.get('exampleTestcases', '')
        expected_outputs = test_cases_data.get('expectedOutputs', [])
        
        if example_testcases:
            return TestCaseParser._parse_from_testcases(example_testcases, sig_data, expected_outputs)
        
        return []
    
    @staticmethod
    def _parse_complete_examples(examples: List[Dict], sig_data: Dict) -> List[Dict]:
        """Parse complete input/output examples"""
        test_cases = []
        
        for i, example in enumerate(examples):
            inputs = example.get('inputs', [])
            output = example.get('output', '')
            
            if not inputs:
                continue
            
            test_case = {
                'case_num': i + 1,
                'inputs': [],
                'expected': output
            }
            
            # Match inputs with parameters
            params = sig_data['params']
            for j, param in enumerate(params):
                if j < len(inputs):
                    value = TestCaseParser.parse_value(inputs[j], param['type'])
                    test_case['inputs'].append({
                        'name': param['name'],
                        'type': param['type'],
                        'value': value,
                        'var_name': f"{param['name']}{i + 1}"
                    })
            
            test_cases.append(test_case)
        
        return test_cases
    
    @staticmethod
    def _parse_from_testcases(testcases: str, sig_data: Dict, expected_outputs: List[str]) -> List[Dict]:
        """Parse test cases from line-separated format"""
        lines = testcases.strip().split('\n')
        params = sig_data['params']
        
        if not params:
            return []
        
        test_cases = []
        case_num = 1
        i = 0
        
        while i < len(lines):
            if i + len(params) > len(lines):
                break
            
            test_case = {
                'case_num': case_num,
                'inputs': []
            }
            
            # Parse each parameter
            for j, param in enumerate(params):
                value = TestCaseParser.parse_value(lines[i + j], param['type'])
                test_case['inputs'].append({
                    'name': param['name'],
                    'type': param['type'],
                    'value': value,
                    'var_name': f"{param['name']}{case_num}"
                })
            
            # Add expected output if available
            if expected_outputs and case_num <= len(expected_outputs):
                test_case['expected'] = expected_outputs[case_num - 1]
            
            test_cases.append(test_case)
            case_num += 1
            i += len(params)
        
        return test_cases
    
    @staticmethod
    def _generate_single_test(test: Dict, sig_data: Dict, code_lines: List[str], topics: List[str]):
        """Generate code for a single test case"""
        # Add test case label
        code_lines.append(f'    TEST_CASE("Example {test["case_num"]}");')
        
        # Declare input variables
        for input_data in test['inputs']:
            TestCaseParser._generate_variable_declaration(input_data, code_lines)
        
        # Build the function call
        param_names = [inp['var_name'] for inp in test['inputs']]
        call = f"solution.{sig_data['method_name']}({', '.join(param_names)})"
        
        # Generate assertion
        if 'expected' in test and test['expected']:
            TestCaseParser._generate_assertion(test, sig_data, call, code_lines, topics)
        else:
            code_lines.append(f'    auto result{test["case_num"]} = {call};')
            code_lines.append(f'    // TODO: Add expected result for example {test["case_num"]}')
        
        # Add cleanup for pointers
        TestCaseParser._generate_cleanup(test, code_lines)
        
        code_lines.append('')  # Empty line between test cases
    
    @staticmethod
    def _generate_variable_declaration(input_data: Dict, code_lines: List[str]):
        """Generate variable declaration for an input"""
        var_type = input_data['type']
        var_name = input_data['var_name']
        var_value = input_data['value']
        
        # Handle special types
        if 'ListNode' in var_type:
            if var_value.startswith('[') and var_value.endswith(']'):
                vector_value = var_value.replace('[', '{').replace(']', '}')
                code_lines.append(f'    ListNode* {var_name} = TestHelpers::CreateLinkedList({vector_value});')
            else:
                code_lines.append(f'    ListNode* {var_name} = nullptr;')
        elif 'TreeNode' in var_type:
            if var_value.startswith('[') and var_value.endswith(']'):
                tree_value = var_value[1:-1].replace('null', 'INT_MIN')
                code_lines.append(f'    TreeNode* {var_name} = TestHelpers::CreateBinaryTree({{{tree_value}}});')
            else:
                code_lines.append(f'    TreeNode* {var_name} = nullptr;')
        else:
            # Regular types - normalize the type
            decl_type = CppTypeConverter.normalize_cpp_type(var_type.replace('&', '').strip())
            code_lines.append(f'    {decl_type} {var_name} = {var_value};')
    
    @staticmethod
    def _generate_assertion(test: Dict, sig_data: Dict, call: str, code_lines: List[str], topics: List[str]):
        """Generate assertion for test result"""
        expected_val = test['expected']
        return_type = sig_data['return_type']
        case_num = test['case_num']
        
        # Handle different return types
        if 'ListNode' in return_type:
            TestCaseParser._generate_list_assertion(expected_val, case_num, call, code_lines)
        elif 'TreeNode' in return_type:
            TestCaseParser._generate_tree_assertion(expected_val, case_num, call, code_lines)
        elif return_type in ['int', 'bool', 'double', 'float', 'char']:
            code_lines.append(f'    ASSERT_EQ({call}, {expected_val});')
        else:
            # Complex types like vectors
            norm_type = CppTypeConverter.normalize_cpp_type(return_type)
            code_lines.append(f'    {norm_type} expected{case_num} = {expected_val};')
            
            # Add comment for unordered comparisons
            if 'vector' in return_type and topics and any(t in ['Hash Table', 'Set'] for t in topics):
                code_lines.append(f'    // Note: If order doesn\'t matter, use ASSERT_UNORDERED_EQ instead')
            
            code_lines.append(f'    ASSERT_EQ({call}, expected{case_num});')
    
    @staticmethod
    def _generate_list_assertion(expected_val: str, case_num: int, call: str, code_lines: List[str]):
        """Generate assertion for linked list return type"""
        if expected_val and expected_val != 'None':
            if expected_val.startswith('[') and expected_val.endswith(']'):
                vector_value = expected_val.replace('[', '{').replace(']', '}')
                code_lines.append(f'    ListNode* expected{case_num} = TestHelpers::CreateLinkedList({vector_value});')
            else:
                code_lines.append(f'    ListNode* expected{case_num} = nullptr;')
        else:
            code_lines.append(f'    ListNode* expected{case_num} = nullptr;')
        
        code_lines.append(f'    auto result{case_num} = {call};')
        code_lines.append(f'    ASSERT_LINKED_LISTS_EQ(result{case_num}, expected{case_num});')
        code_lines.append(f'    TestHelpers::DeleteLinkedList(expected{case_num});')
        code_lines.append(f'    TestHelpers::DeleteLinkedList(result{case_num});')
    
    @staticmethod
    def _generate_tree_assertion(expected_val: str, case_num: int, call: str, code_lines: List[str]):
        """Generate assertion for tree return type"""
        if expected_val.startswith('[') and expected_val.endswith(']'):
            tree_value = expected_val[1:-1].replace('null', 'INT_MIN')
            code_lines.append(f'    TreeNode* expected{case_num} = TestHelpers::CreateBinaryTree({{{tree_value}}});')
        else:
            code_lines.append(f'    TreeNode* expected{case_num} = nullptr;')
        
        code_lines.append(f'    auto result{case_num} = {call};')
        code_lines.append(f'    ASSERT_TREES_EQ(result{case_num}, expected{case_num});')
        code_lines.append(f'    TestHelpers::DeleteTree(expected{case_num});')
        code_lines.append(f'    TestHelpers::DeleteTree(result{case_num});')
    
    @staticmethod
    def _generate_cleanup(test: Dict, code_lines: List[str]):
        """Generate cleanup code for allocated resources"""
        for input_data in test['inputs']:
            if 'ListNode' in input_data['type']:
                code_lines.append(f'    TestHelpers::DeleteLinkedList({input_data["var_name"]});')
            elif 'TreeNode' in input_data['type']:
                code_lines.append(f'    TestHelpers::DeleteTree({input_data["var_name"]});')
    
    @staticmethod
    def _generate_default_test_comment(sig_data: Dict) -> str:
        """Generate default test case comments when no data available"""
        return f"""    // TODO: Add test cases using ASSERT_EQ
    // Examples:
    // ASSERT_EQ(solution.{sig_data['method_name']}(...), expected_result);
    // 
    // For more complex tests:
    // TEST_CASE("Description of test case");
    // auto result = solution.{sig_data['method_name']}(...);
    // ASSERT_EQ(result, expected);"""