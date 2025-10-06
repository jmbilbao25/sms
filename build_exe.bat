@echo off
setlocal ENABLEDELAYEDEXPANSION

echo Building TechOps Text Blast Formatter...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Paths
set SCRIPT=SMS.py
set ICON=%~dp0app_icon.ico
set BANNER=%~dp0banner.png
set NAME=TechOpsFormatter

REM Verify assets
if not exist "%ICON%" (
  echo [WARN] Icon not found: %ICON%
) else (
  echo [OK] Using icon: %ICON%
)
if not exist "%BANNER%" (
  echo [WARN] Banner not found: %BANNER%
) else (
  echo [OK] Embedding banner: %BANNER%
)

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build executable with absolute icon and data paths
echo Creating executable with PyInstaller...
pyinstaller --noconfirm --clean --onefile --windowed --name "%NAME%" --icon "%ICON%" --add-data "%BANNER%;." "%SCRIPT%"
set EXITCODE=%ERRORLEVEL%

echo.
if not %EXITCODE%==0 (
  echo Build failed with exit code %EXITCODE%.
  pause
  exit /b %EXITCODE%
)

echo Build complete! Check the 'dist' folder for your executable.
echo If the icon doesn't appear, try renaming the exe to refresh Windows icon cache.
echo.
pause
endlocal
