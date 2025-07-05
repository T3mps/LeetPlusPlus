@echo off
REM LeetCode Practice Framework Launcher for Windows
REM This script runs the LeetCode practice application

setlocal

REM Check if the executable exists in different possible locations
set "EXE_PATH="

REM Check Debug build first (most common for development)
if exist "bin\Debug-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe" (
    set "EXE_PATH=bin\Debug-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe"
    goto :found
)

REM Check Release build
if exist "bin\Release-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe" (
    set "EXE_PATH=bin\Release-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe"
    goto :found
)

REM Check Distribution build
if exist "bin\Distribution-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe" (
    set "EXE_PATH=bin\Distribution-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe"
    goto :found
)

REM Check if running from Visual Studio output directory
if exist "x64\Debug\LeetPlusPlus.exe" (
    set "EXE_PATH=x64\Debug\LeetPlusPlus.exe"
    goto :found
)

if exist "x64\Release\LeetPlusPlus.exe" (
    set "EXE_PATH=x64\Release\LeetPlusPlus.exe"
    goto :found
)

REM If no executable found
echo Error: LeetCode Practice Framework executable not found!
echo.
echo Please build the project first using one of these methods:
echo   - Open LeetPlusPlus.sln in Visual Studio and build
echo   - Run: premake5 vs2022 && msbuild LeetPlusPlus.sln
echo.
echo Expected locations:
echo   - bin\Debug-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe
echo   - bin\Release-windows-x86_64\LeetPlusPlus\LeetPlusPlus.exe
echo   - x64\Debug\LeetPlusPlus.exe
echo   - x64\Release\LeetPlusPlus.exe
echo.
pause
exit /b 1

:found
echo Starting LeetCode Practice Framework...
echo ========================================
echo.

REM Run the application with any passed arguments
"%EXE_PATH%" %*

REM Check if the app crashed
if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)

endlocal