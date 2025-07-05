#!/bin/bash
# LeetCode Practice Framework Launcher for Linux/macOS
# This script runs the LeetCode practice application

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    printf "${2}${1}${NC}\n"
}

# Function to check if executable exists and is executable
check_executable() {
    if [ -f "$1" ] && [ -x "$1" ]; then
        return 0
    fi
    return 1
}

# Determine the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Look for the executable in various possible locations
EXE_PATH=""

# Check Debug build first (most common for development)
if check_executable "bin/Debug-linux-x86_64/LeetPlusPlus/LeetPlusPlus"; then
    EXE_PATH="bin/Debug-linux-x86_64/LeetPlusPlus/LeetPlusPlus"
elif check_executable "bin/Release-linux-x86_64/LeetPlusPlus/LeetPlusPlus"; then
    EXE_PATH="bin/Release-linux-x86_64/LeetPlusPlus/LeetPlusPlus"
elif check_executable "bin/Distribution-linux-x86_64/LeetPlusPlus/LeetPlusPlus"; then
    EXE_PATH="bin/Distribution-linux-x86_64/LeetPlusPlus/LeetPlusPlus"
# Check macOS paths
elif check_executable "bin/Debug-macosx-x86_64/LeetPlusPlus/LeetPlusPlus"; then
    EXE_PATH="bin/Debug-macosx-x86_64/LeetPlusPlus/LeetPlusPlus"
elif check_executable "bin/Release-macosx-x86_64/LeetPlusPlus/LeetPlusPlus"; then
    EXE_PATH="bin/Release-macosx-x86_64/LeetPlusPlus/LeetPlusPlus"
# Check if built with make
elif check_executable "LeetPlusPlus"; then
    EXE_PATH="./LeetPlusPlus"
elif check_executable "build/LeetPlusPlus"; then
    EXE_PATH="build/LeetPlusPlus"
fi

# If no executable found
if [ -z "$EXE_PATH" ]; then
    print_color "Error: LeetCode Practice Framework executable not found!" "$RED"
    echo
    echo "Please build the project first using one of these methods:"
    echo "  - Run: premake5 gmake2 && make"
    echo "  - Run: premake5 xcode4 (on macOS)"
    echo
    echo "Expected locations:"
    echo "  - bin/Debug-linux-x86_64/LeetPlusPlus/LeetPlusPlus"
    echo "  - bin/Release-linux-x86_64/LeetPlusPlus/LeetPlusPlus"
    echo "  - bin/Debug-macosx-x86_64/LeetPlusPlus/LeetPlusPlus"
    echo "  - ./LeetPlusPlus"
    echo "  - build/LeetPlusPlus"
    echo
    exit 1
fi

# Check if terminal supports the required features
if ! command -v tput &> /dev/null; then
    print_color "Warning: 'tput' command not found. Terminal features may be limited." "$YELLOW"
fi

# Set terminal type if not set
if [ -z "$TERM" ]; then
    export TERM=xterm-256color
fi

print_color "Starting LeetCode Practice Framework..." "$GREEN"
echo "========================================"
echo

# Run the application with any passed arguments
"$EXE_PATH" "$@"

EXIT_CODE=$?

# Check if the app crashed
if [ $EXIT_CODE -ne 0 ]; then
    echo
    print_color "Application exited with error code $EXIT_CODE" "$RED"
fi

exit $EXIT_CODE