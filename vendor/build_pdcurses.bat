@echo off
REM Build PDCurses for Windows

REM Find Visual Studio installation
IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" (
    call "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" -arch=x64
) ELSE IF EXIST "%ProgramFiles%\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" (
    call "%ProgramFiles%\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" -arch=x64
) ELSE IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\VsDevCmd.bat" (
    call "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\VsDevCmd.bat" -arch=x64
) ELSE IF EXIST "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\VsDevCmd.bat" (
    call "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\VsDevCmd.bat" -arch=x64
) ELSE IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" (
    call "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64
) ELSE IF EXIST "%ProgramFiles%\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" (
    call "%ProgramFiles%\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64
) ELSE (
    echo Visual Studio 2022 not found. Trying Visual Studio 2019...
    
    IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat" (
        call "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat" -arch=x64
    ) ELSE IF EXIST "%ProgramFiles%\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat" (
        call "%ProgramFiles%\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat" -arch=x64
    ) ELSE IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Enterprise\Common7\Tools\VsDevCmd.bat" (
        call "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Enterprise\Common7\Tools\VsDevCmd.bat" -arch=x64
    ) ELSE IF EXIST "%ProgramFiles%\Microsoft Visual Studio\2019\Enterprise\Common7\Tools\VsDevCmd.bat" (
        call "%ProgramFiles%\Microsoft Visual Studio\2019\Enterprise\Common7\Tools\VsDevCmd.bat" -arch=x64
    ) ELSE IF EXIST "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Professional\Common7\Tools\VsDevCmd.bat" (
        call "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64
    ) ELSE IF EXIST "%ProgramFiles%\Microsoft Visual Studio\2019\Professional\Common7\Tools\VsDevCmd.bat" (
        call "%ProgramFiles%\Microsoft Visual Studio\2019\Professional\Common7\Tools\VsDevCmd.bat" -arch=x64
    ) ELSE (
        echo Visual Studio 2019 not found. Please install Visual Studio or ensure it's in the default location.
        exit /b 1
    )
)

cd PDCurses\wincon
nmake -f Makefile.vc clean
nmake -f Makefile.vc
echo PDCurses for Windows built successfully!