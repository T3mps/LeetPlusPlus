#!/usr/bin/env python3
"""
Configuration settings for LeetPlusPlus
Centralizes all configuration values used across the tools
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
PROBLEMS_DIR = PROJECT_ROOT / "src" / "Problems"
VENDOR_DIR = PROJECT_ROOT / "vendor"
BIN_DIR = PROJECT_ROOT / "bin"


METADATA_FILE = PROJECT_ROOT / "metadata.json"
ALL_PROBLEMS_HEADER = PROBLEMS_DIR / "AllProblems.h"
TEMPLATE_FILE = TOOLS_DIR / "template.h"


API_BASE_URL = "http://localhost:3000"
API_TIMEOUT = 10  # seconds
API_START_WAIT_TIME = 10  # seconds to wait for API to start


ALFA_LEETCODE_DIR = VENDOR_DIR / "AlfaLeetCode"


APP_NAME = "LeetPlusPlus"
APP_VERSION = "1.1.0"
APP_GITHUB = "github.com/t3mps/LeetPlusPlus"


EXE_RELEASE_PATH = BIN_DIR / "Release" / "x64" / f"{APP_NAME}.exe"
EXE_DEBUG_PATH = BIN_DIR / "Debug" / "x64" / f"{APP_NAME}.exe"


BATCH_FETCH_LIMIT = 100  # Number of problems to fetch at once
BATCH_FETCH_DELAY = 0.5  # Delay between API calls in batch mode


LEETCODE_TO_CPP_TYPES = {
    "integer": "int",
    "long": "long long",
    "double": "double",
    "string": "std::string",
    "boolean": "bool",
    "character": "char",
    "ListNode": "ListNode*",
    "TreeNode": "TreeNode*",
    "Node": "Node*"
}


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


CONSOLE_BANNER_WIDTH = 67
CONSOLE_PROMPT = "lpp"


SUPPORTS_TRUECOLOR = False
try:
    import os
    SUPPORTS_TRUECOLOR = os.environ.get('COLORTERM') in ['truecolor', '24bit']
except:
    pass