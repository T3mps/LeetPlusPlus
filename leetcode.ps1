# LeetCode Practice Framework Launcher for Windows PowerShell
# This script runs the LeetCode practice application with enhanced features

param(
    [switch]$Debug,
    [switch]$Release,
    [switch]$Help
)

# Script configuration
$ErrorActionPreference = "Stop"

# Display help information
if ($Help) {
    Write-Host "LeetCode Practice Framework Launcher" -ForegroundColor Cyan
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\leetcode.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Debug     Force running Debug build"
    Write-Host "  -Release   Force running Release build"
    Write-Host "  -Help      Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\leetcode.ps1              # Run default available build"
    Write-Host "  .\leetcode.ps1 -Debug       # Run Debug build specifically"
    Write-Host "  .\leetcode.ps1 -Release     # Run Release build specifically"
    Write-Host ""
    exit 0
}

# Function to test if executable exists
function Test-Executable {
    param([string]$Path)
    return (Test-Path $Path) -and (Get-Item $Path).PSIsContainer -eq $false
}

# Possible executable paths
$possiblePaths = @()

# Add paths based on command line preferences
if ($Debug) {
    $possiblePaths += @(
        "bin\Debug-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe",
        "x64\Debug\LeetPlusPlus.exe"
    )
} elseif ($Release) {
    $possiblePaths += @(
        "bin\Release-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe",
        "bin\Distribution-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe",
        "x64\Release\LeetPlusPlus.exe"
    )
} else {
    # Default: try all paths, Debug first
    $possiblePaths += @(
        "bin\Debug-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe",
        "bin\Release-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe",
        "bin\Distribution-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe",
        "x64\Debug\LeetPlusPlus.exe",
        "x64\Release\LeetPlusPlus.exe"
    )
}

# Find the first existing executable
$exePath = $null
foreach ($path in $possiblePaths) {
    if (Test-Executable $path) {
        $exePath = $path
        break
    }
}

# If no executable found
if (-not $exePath) {
    Write-Host "Error: LeetCode Practice Framework executable not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please build the project first using one of these methods:" -ForegroundColor Yellow
    Write-Host "  - Open LeetPlusPlus.sln in Visual Studio and build"
    Write-Host "  - Run: premake5 vs2022 && msbuild LeetPlusPlus.sln"
    Write-Host ""
    Write-Host "Expected locations:"
    foreach ($path in $possiblePaths) {
        Write-Host "  - $path"
    }
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Display startup information
Write-Host "Starting LeetCode Practice Framework..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Executable: $exePath" -ForegroundColor DarkGray
Write-Host ""

# Check if running in Windows Terminal or modern console
$isModernTerminal = $env:WT_SESSION -or $env:TERM_PROGRAM

if (-not $isModernTerminal) {
    Write-Host "Tip: For best experience, use Windows Terminal or PowerShell 7+" -ForegroundColor Yellow
    Write-Host ""
}

# Run the application
try {
    & $exePath $args
    $exitCode = $LASTEXITCODE
} catch {
    Write-Host ""
    Write-Host "Error: Failed to run the application" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check exit code
if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "Application exited with error code $exitCode" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}