#!/usr/bin/env python3
"""
Common utilities for LeetPlusPlus tools
Provides shared functionality for API management, metadata handling, and more
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Optional, Any

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


class ColorPrinter:
    """Utility class for colored console output"""
    
    @staticmethod
    def success(message: str):
        """Print success message in green"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def error(message: str):
        """Print error message in red"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def info(message: str):
        """Print info message in blue"""
        print(f"{Fore.BLUE}ℹ  {message}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(message: str):
        """Print warning message in yellow"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


class APIServerManager:
    """Manages the AlfaLeetCode API server"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.root_dir = Path(__file__).parent.parent
        self.api_dir = self.root_dir / "vendor" / "AlfaLeetCode"
    
    def check_available(self) -> bool:
        """Check if API server is running"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/", timeout=2) as response:
                return response.status == 200
        except:
            return False
    
    def validate_path(self, path: Path) -> bool:
        """Validate path to prevent shell injection"""
        path_str = str(path)
        return not any(char in path_str for char in ['&', '|', ';', '$', '`', '\n', '\r'])
    
    def start_server(self, auto_mode: bool = True) -> Optional[subprocess.Popen]:
        """Start the API server"""
        if not self.api_dir.exists():
            ColorPrinter.error("AlfaLeetCode directory not found!")
            return None
        
        if not self.validate_path(self.api_dir):
            ColorPrinter.error("Invalid characters in path!")
            return None
        
        if auto_mode:
            ColorPrinter.info("Starting API server automatically...")
        
        try:
            if os.name == 'nt':  # Windows
                # Check if node_modules exists
                node_modules = self.api_dir / "node_modules"
                if not node_modules.exists():
                    ColorPrinter.warning("Node modules not installed. Running npm install first...")
                    subprocess.run(['npm', 'install'], cwd=str(self.api_dir), check=True)
                
                # Open new command window with the server
                cmd = f'start "AlfaLeetCode API" /D "{self.api_dir}" cmd /k node dist/index.js'
                subprocess.Popen(cmd, shell=True)
                
                # Wait for server to start
                ColorPrinter.info("Waiting for API server to start...")
                for i in range(10):
                    time.sleep(1)
                    if self.check_available():
                        ColorPrinter.success("API server started successfully!")
                        return None
            else:
                # For Linux/Mac, try different approaches
                npm_commands = [
                    ["npm", "start"],
                    ["npm.cmd", "start"],
                    ["node", "dist/index.js"],
                ]
                
                for cmd in npm_commands:
                    try:
                        process = subprocess.Popen(
                            cmd,
                            cwd=self.api_dir,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        time.sleep(3)
                        if self.check_available():
                            return process
                    except (FileNotFoundError, OSError):
                        continue
        
        except Exception as e:
            ColorPrinter.error(f"Failed to start server: {e}")
        
        return None
    
    def ensure_running(self) -> bool:
        """Ensure the API server is running, start if needed"""
        if self.check_available():
            return True
        
        ColorPrinter.warning("API server not running. Starting automatically...")
        self.start_server(auto_mode=True)
        
        # Final check
        return self.check_available()


class MetadataManager:
    """Handles problem metadata loading and saving"""
    
    def __init__(self, metadata_file: Optional[Path] = None):
        if metadata_file is None:
            self.metadata_file = Path(__file__).parent.parent / "metadata.json"
        else:
            self.metadata_file = metadata_file
    
    def load(self) -> Dict[str, Any]:
        """Load metadata from file"""
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            ColorPrinter.error(f"Failed to load metadata: {e}")
            return {}
    
    def save(self, metadata: Dict[str, Any]) -> bool:
        """Save metadata to file"""
        try:
            # Sort by problem number for readability
            sorted_metadata = dict(sorted(metadata.items(), key=lambda x: int(x[0])))
            
            with open(self.metadata_file, 'w') as f:
                json.dump(sorted_metadata, f, indent=2)
            
            return True
        except Exception as e:
            ColorPrinter.error(f"Failed to save metadata: {e}")
            return False
    
    def get_problem_by_id(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific problem by ID"""
        metadata = self.load()
        return metadata.get(str(problem_id))
    
    def get_problems_list(self) -> list:
        """Get list of all problems with IDs included"""
        metadata = self.load()
        problems_list = []
        
        for problem_id, problem_data in metadata.items():
            problem_with_id = problem_data.copy()
            problem_with_id['id'] = problem_id
            problems_list.append(problem_with_id)
        
        # Sort by problem ID numerically
        problems_list.sort(key=lambda p: int(p['id']))
        return problems_list


class HTTPClient:
    """Wrapper for urllib with consistent error handling"""
    
    @staticmethod
    def get(url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """Make GET request and return JSON response"""
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                data = response.read()
                return json.loads(data.decode('utf-8'))
        except urllib.error.HTTPError as e:
            ColorPrinter.error(f"HTTP Error {e.code}: {e.reason}")
            return None
        except urllib.error.URLError as e:
            ColorPrinter.error(f"URL Error: {e.reason}")
            return None
        except Exception as e:
            ColorPrinter.error(f"Request failed: {e}")
            return None
    
    @staticmethod
    def get_with_params(base_url: str, params: Dict[str, str], timeout: int = 10) -> Optional[Dict[str, Any]]:
        """Make GET request with query parameters"""
        from urllib.parse import urlencode
        query_string = urlencode(params)
        url = f"{base_url}?{query_string}"
        return HTTPClient.get(url, timeout)


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent


def ensure_directory(path: Path) -> bool:
    """Ensure directory exists, create if needed"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        ColorPrinter.error(f"Failed to create directory {path}: {e}")
        return False