#!/usr/bin/env python3
"""
C++ Type utilities for LeetPlusPlus
Handles type conversions and normalization for C++ code generation
"""

import re
from typing import List, Dict, Optional
from config import LEETCODE_TO_CPP_TYPES, STL_TYPES


class CppTypeConverter:
    """Handles C++ type conversions and normalization"""
    
    @staticmethod
    def normalize_cpp_type(type_str: str) -> str:
        """
        Normalize C++ type string by fixing spacing and adding std:: prefixes
        Combines functionality of normalize_cpp_type and add_std_prefix
        """
        if not type_str:
            return type_str
        
        # Step 1: Clean up whitespace
        type_str = re.sub(r'\s+', ' ', type_str).strip()
        
        # Step 2: Fix template bracket spacing: vector < int > -> vector<int>
        type_str = re.sub(r'\s*<\s*', '<', type_str)
        type_str = re.sub(r'\s*>\s*', '>', type_str)
        
        # Step 3: Fix pointer spacing: TreeNode * -> TreeNode*, TreeNode * * -> TreeNode**
        type_str = re.sub(r'(\w|>)\s+(\*+)', r'\1\2', type_str)
        # Handle multiple spaced pointers: * * * -> ***
        while re.search(r'\*\s+\*', type_str):
            type_str = re.sub(r'\*\s+\*', '**', type_str)
        
        # Step 4: Fix reference spacing: vector<int> & -> vector<int>&
        type_str = re.sub(r'(\w|>)\s+(&)', r'\1\2', type_str)
        
        # Step 5: Ensure space after const
        type_str = re.sub(r'const(\w)', r'const \1', type_str)
        
        # Step 6: Add std:: prefix to STL types if not present
        if 'std::' not in type_str:
            for stl_type in STL_TYPES:
                # Match STL type followed by template bracket or word boundary
                pattern = rf'\b(?<!::){stl_type}(?=\s*<|\b)'
                type_str = re.sub(pattern, f'std::{stl_type}', type_str)
        
        return type_str
    
    @staticmethod
    def leetcode_to_cpp(lc_type: str) -> str:
        """Convert LeetCode type notation to C++ type"""
        # Handle arrays
        if lc_type.endswith("[][]"):
            base_type = lc_type[:-4]
            cpp_base = LEETCODE_TO_CPP_TYPES.get(base_type, base_type)
            return f"std::vector<std::vector<{cpp_base}>>"
        elif lc_type.endswith("[]"):
            base_type = lc_type[:-2]
            cpp_base = LEETCODE_TO_CPP_TYPES.get(base_type, base_type)
            return f"std::vector<{cpp_base}>"
        
        return LEETCODE_TO_CPP_TYPES.get(lc_type, lc_type)
    
    @staticmethod
    def to_pascal_case(name: str) -> str:
        """Convert method name to PascalCase"""
        if name and name[0].islower():
            return name[0].upper() + name[1:]
        return name
    
    @staticmethod
    def parse_signature(signature: str) -> Optional[Dict]:
        """Parse a C++ function signature into components"""
        match = re.match(r'^\s*(.+?)\s+(\w+)\s*\((.*)\)\s*$', signature)
        if not match:
            return None
        
        raw_return_type = match.group(1).strip()
        method_name = match.group(2).strip()
        raw_params = match.group(3).strip()
        
        # Normalize types
        return_type = CppTypeConverter.normalize_cpp_type(raw_return_type)
        method_name = CppTypeConverter.to_pascal_case(method_name)
        
        # Parse parameters
        params = []
        params_str = ""
        
        if raw_params:
            param_parts = CppTypeConverter._split_parameters(raw_params)
            
            for param in param_parts:
                param = param.strip()
                param = CppTypeConverter.normalize_cpp_type(param)
                
                # Extract parameter type and name
                param_match = re.match(r'^(.+?)\s+(\w+)\s*$', param)
                if param_match:
                    param_type = param_match.group(1).strip()
                    param_name = param_match.group(2).strip()
                    params.append({'type': param_type, 'name': param_name})
                else:
                    # No name provided, generate one
                    params.append({'type': param, 'name': 'arg' + str(len(params))})
            
            # Rebuild params string with normalized types
            params_str = ', '.join(CppTypeConverter.normalize_cpp_type(p) for p in param_parts)
        
        return {
            'return_type': return_type,
            'method_name': method_name,
            'params_str': params_str,
            'params': params
        }
    
    @staticmethod
    def _split_parameters(params_str: str) -> List[str]:
        """Split parameter string handling nested templates"""
        param_parts = []
        current_param = ""
        angle_bracket_count = 0
        
        for char in params_str:
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
        
        return param_parts
    
    @staticmethod
    def get_default_return(return_type: str) -> str:
        """Get default return statement for a type"""
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