@echo off
echo Building TechOps Text Blast Formatter...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo Creating executable with PyInstaller...
pyinstaller --onefile --windowed --icon=app_icon.ico --name="TechOpsFormatter" --add-data "banner.png;." SMS.py

echo.
echo Build complete! Check the 'dist' folder for your executable.
echo The banner image is now embedded in the executable.
echo.
pause
